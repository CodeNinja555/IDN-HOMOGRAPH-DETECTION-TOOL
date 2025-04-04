from flask import Flask, render_template, request, jsonify
from werkzeug.urls import url_quote_plus as url_quote  # Updated import
import tldextract
import idna
import unicodedata
from whois import whois
import requests
import dns.resolver

app = Flask(__name__)

# Extended homograph character mapping with Unicode details
HOMOGRAPH_MAP = {
        'a': [
            {'char': 'а', 'name': 'CYRILLIC SMALL LETTER A', 'code': 'U+0430'},
            {'char': 'ɑ', 'name': 'LATIN SMALL LETTER ALPHA', 'code': 'U+0251'},
            {'char': 'α', 'name': 'GREEK SMALL LETTER ALPHA', 'code': 'U+03B1'}
        ],
        'b': [
            {'char': 'Ь', 'name': 'CYRILLIC CAPITAL LETTER SOFT SIGN', 'code': 'U+042C'},
            {'char': 'ḅ', 'name': 'LATIN SMALL LETTER B WITH DOT BELOW', 'code': 'U+1E05'}
        ],
        'c': [
            {'char': 'с', 'name': 'CYRILLIC SMALL LETTER ES', 'code': 'U+0441'},
            {'char': 'ϲ', 'name': 'GREEK SMALL LETTER ARCHAIC SAMPI', 'code': 'U+03F2'},
            {'char': 'ċ', 'name': 'LATIN SMALL LETTER C WITH DOT ABOVE', 'code': 'U+010B'}
        ],
        'e': [
            {'char': 'е', 'name': 'CYRILLIC SMALL LETTER IE', 'code': 'U+0435'},
            {'char': 'ė', 'name': 'LATIN SMALL LETTER E WITH DOT ABOVE', 'code': 'U+0117'},
            {'char': 'ë', 'name': 'LATIN SMALL LETTER E WITH DIAERESIS', 'code': 'U+00EB'}
        ],
        'g': [
            {'char': 'ɡ', 'name': 'LATIN SMALL LETTER SCRIPT G', 'code': 'U+0261'},
            {'char': 'ġ', 'name': 'LATIN SMALL LETTER G WITH DOT ABOVE', 'code': 'U+0121'}
        ],
        'i': [
            {'char': 'і', 'name': 'CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I', 'code': 'U+0456'},
            {'char': 'ï', 'name': 'LATIN SMALL LETTER I WITH DIAERESIS', 'code': 'U+00EF'},
            {'char': 'ǐ', 'name': 'LATIN SMALL LETTER I WITH CARON', 'code': 'U+01D0'}
        ],
        'o': [
            {'char': 'о', 'name': 'CYRILLIC SMALL LETTER O', 'code': 'U+043E'},
            {'char': 'ο', 'name': 'GREEK SMALL LETTER OMICRON', 'code': 'U+03BF'},
            {'char': 'ọ', 'name': 'LATIN SMALL LETTER O WITH DOT BELOW', 'code': 'U+1ECD'}
        ],
        'p': [
            {'char': 'р', 'name': 'CYRILLIC SMALL LETTER ER', 'code': 'U+0440'},
            {'char': 'ρ', 'name': 'GREEK SMALL LETTER RHO', 'code': 'U+03C1'}
        ],
        's': [
            {'char': 'ѕ', 'name': 'CYRILLIC SMALL LETTER DZE', 'code': 'U+0455'},
            {'char': 'ŝ', 'name': 'LATIN SMALL LETTER S WITH CIRCUMFLEX', 'code': 'U+015D'}
        ],
        'w': [
            {'char': 'ѡ', 'name': 'CYRILLIC SMALL LETTER OMEGA', 'code': 'U+0461'},
            {'char': 'ώ', 'name': 'GREEK SMALL LETTER OMEGA WITH TONOS', 'code': 'U+03CE'}
        ],
        'x': [
            {'char': 'х', 'name': 'CYRILLIC SMALL LETTER HA', 'code': 'U+0445'},
            {'char': 'ẋ', 'name': 'LATIN SMALL LETTER X WITH DOT ABOVE', 'code': 'U+1E8B'}
        ],
        'y': [
            {'char': 'у', 'name': 'CYRILLIC SMALL LETTER U', 'code': 'U+0443'},
            {'char': 'ý', 'name': 'LATIN SMALL LETTER Y WITH ACUTE', 'code': 'U+00FD'}
        ]
}

def get_char_details(char):
    try:
        name = unicodedata.name(char)
    except ValueError:
        name = "UNKNOWN CHARACTER"
    return {
        'char': char,
        'name': name,
        'code': f"U+{ord(char):04X}",
        'category': unicodedata.category(char)
    }

def generate_homographs(domain, tlds=['.com']):
    extracted = tldextract.extract(domain)
    base_domain = extracted.domain
    original_tld = '.' + extracted.suffix

    homographs = []
    
    for i, char in enumerate(base_domain.lower()):
        if char in HOMOGRAPH_MAP:
            for replacement in HOMOGRAPH_MAP[char]:
                new_domain = base_domain[:i] + replacement['char'] + base_domain[i+1:] + original_tld
                punycode = idna.encode(new_domain).decode('ascii')
                
                homographs.append({
                    'original_domain': domain,
                    'homograph': new_domain,
                    'position': i,
                    'original_char': get_char_details(base_domain[i]),
                    'replacement_char': replacement,
                    'punycode': punycode,
                    'is_live': False,
                    'is_registered': False
                })

    return homographs

def check_domain_status(domain):
    try:
        # Check if domain is registered
        domain_info = whois(domain)
        is_registered = domain_info.domain_name is not None
        
        # Check if domain is live
        try:
            response = requests.get(f"http://{domain}", timeout=5)
            is_live = response.status_code in range(200, 400)
        except:
            is_live = False
            
        return is_registered, is_live
    except:
        return False, False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    domain = request.form.get('domain')
    tlds = request.form.get('tlds', '.com').split(',')
    
    if not domain:
        return jsonify({'error': 'Domain is required'}), 400
    
    homographs = generate_homographs(domain, tlds)
    
    # Check status for each homograph (can be slow, might want to do this async)
    for h in homographs:
        h['is_registered'], h['is_live'] = check_domain_status(h['homograph'])
    
    return jsonify({
        'original': domain,
        'homographs': homographs,
        'count': len(homographs)
    })

if __name__ == '__main__':
    app.run(debug=True)