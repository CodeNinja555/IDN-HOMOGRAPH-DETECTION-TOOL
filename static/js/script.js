document.addEventListener('DOMContentLoaded', function() {
    const analysisForm = document.getElementById('analysisForm');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsBody = document.getElementById('resultsBody');
    const totalCount = document.getElementById('totalCount');
    const liveCount = document.getElementById('liveCount');
    const registeredCount = document.getElementById('registeredCount');
    const detailsModal = new bootstrap.Modal(document.getElementById('detailsModal'));
    
    analysisForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const domainInput = document.getElementById('domainInput');
        const domain = domainInput.value.trim();
        
        if (!domain) {
            alert('Please enter a domain to analyze');
            return;
        }
        
        // Get selected TLDs
        const tlds = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                          .map(checkbox => checkbox.value);
        
        // Show loading state
        resultsBody.innerHTML = '<tr><td colspan="4" class="text-center py-4"><div class="spinner-border text-primary" role="status"></div></td></tr>';
        resultsContainer.classList.remove('d-none');
        
        // Send request to backend
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `domain=${encodeURIComponent(domain)}&tlds=${tlds.join(',')}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultsBody.innerHTML = `<tr><td colspan="4" class="text-center text-danger py-4">${data.error}</td></tr>`;
                return;
            }
            
            // Update counts
            totalCount.textContent = data.count;
            
            let liveDomains = 0;
            let registeredDomains = 0;
            
            // Clear previous results
            resultsBody.innerHTML = '';
            
            // Add each homograph to the table
            data.homographs.forEach(homograph => {
                if (homograph.is_live) liveDomains++;
                if (homograph.is_registered) registeredDomains++;
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>
                        <span class="original-domain">${homograph.original_domain}</span><br>
                        <span class="homograph-domain ${homograph.is_live ? 'text-danger fw-bold' : ''}">${homograph.homograph}</span>
                    </td>
                    <td><code>${homograph.punycode}</code></td>
                    <td>
                        ${homograph.is_live ? '<span class="badge bg-danger">Live</span>' : ''}
                        ${homograph.is_registered ? '<span class="badge bg-warning">Registered</span>' : ''}
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary view-details" 
                                data-homograph='${JSON.stringify(homograph)}'>
                            <i class="bi bi-zoom-in"></i> Details
                        </button>
                    </td>
                `;
                resultsBody.appendChild(row);
            });
            
            // Update counts
            liveCount.textContent = liveDomains;
            registeredCount.textContent = registeredDomains;
            
            // Add event listeners to details buttons
            document.querySelectorAll('.view-details').forEach(button => {
                button.addEventListener('click', function() {
                    const homograph = JSON.parse(this.dataset.homograph);
                    showDetails(homograph);
                });
            });
        })
        .catch(error => {
            resultsBody.innerHTML = `<tr><td colspan="4" class="text-center text-danger py-4">Error: ${error.message}</td></tr>`;
        });
    });
    
    function showDetails(homograph) {
        const modalBody = document.getElementById('modalBody');
        
        // Create visual comparison
        let originalChars = homograph.original_domain.split('');
        let homographChars = homograph.homograph.split('');
        
        let visualComparison = '';
        for (let i = 0; i < originalChars.length; i++) {
            if (i === homograph.position) {
                visualComparison += `<span class="text-danger fw-bold">${homographChars[i]}</span>`;
            } else {
                visualComparison += originalChars[i];
            }
        }
        
        // Populate modal
        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <div class="card mb-4">
                        <div class="card-header bg-info text-white">
                            <h6 class="mb-0">Original Character</h6>
                        </div>
                        <div class="card-body">
                            <div class="text-center mb-3">
                                <div class="display-4">${homograph.original_char.char}</div>
                            </div>
                            <table class="table table-sm">
                                <tr>
                                    <th>Unicode:</th>
                                    <td><code>${homograph.original_char.code}</code></td>
                                </tr>
                                <tr>
                                    <th>Name:</th>
                                    <td>${homograph.original_char.name}</td>
                                </tr>
                                <tr>
                                    <th>Category:</th>
                                    <td>${homograph.original_char.category}</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card mb-4">
                        <div class="card-header bg-danger text-white">
                            <h6 class="mb-0">Replacement Character</h6>
                        </div>
                        <div class="card-body">
                            <div class="text-center mb-3">
                                <div class="display-4">${homograph.replacement_char.char}</div>
                            </div>
                            <table class="table table-sm">
                                <tr>
                                    <th>Unicode:</th>
                                    <td><code>${homograph.replacement_char.code}</code></td>
                                </tr>
                                <tr>
                                    <th>Name:</th>
                                    <td>${homograph.replacement_char.name}</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0">Visual Comparison</h6>
                </div>
                <div class="card-body">
                    <div class="text-center">
                        <div class="mb-2">
                            <small class="text-muted">Original</small><br>
                            <span class="h4">${homograph.original_domain}</span>
                        </div>
                        <div class="mb-2">
                            <i class="bi bi-arrow-down"></i>
                        </div>
                        <div>
                            <small class="text-muted">Homograph</small><br>
                            <span class="h4">${visualComparison}</span>
                        </div>
                        <div class="mt-3">
                            <small class="text-muted">Punycode</small><br>
                            <code class="h5">${homograph.punycode}</code>
                        </div>
                    </div>
                    <div class="alert alert-warning mt-3">
                        <i class="bi bi-exclamation-triangle"></i> 
                        This homograph replaces character at position ${homograph.position} (${homograph.original_char.char} → ${homograph.replacement_char.char})
                    </div>
                </div>
            </div>
        `;
        
        detailsModal.show();
    }
});