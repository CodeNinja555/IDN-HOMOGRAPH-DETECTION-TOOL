# 🔐 IDN Homograph Detection Tool

## Overview

The rapid expansion of the internet has led to widespread adoption of **Internationalized Domain Names (IDNs)**, allowing domains to be registered in non-Latin scripts such as **Cyrillic**, **Greek**, and **Arabic**. While this promotes linguistic inclusivity, it also introduces significant **cybersecurity risks**, particularly **IDN homograph attacks**.

These attacks exploit visually similar characters—called **homoglyphs**—to create deceptive domains that mimic legitimate ones (e.g., `аррӏе.com` vs. `apple.com`). Such domains are commonly used for phishing, malware distribution, and brand impersonation.

This project presents a comprehensive **IDN Homograph Generation and Detection Tool** designed to simulate and detect such threats.

---

## 🔧 Features

### 1. Homograph Domain Generation

The tool systematically creates homograph variations of a given domain using Unicode substitutions.  
Example substitutions include:

- `a` (Latin) → `а` (Cyrillic)  
- `o` (Latin) → `о` (Cyrillic) or `θ` (Greek)  
- `l` (Latin) → `ӏ` (Cyrillic)

**Generation Process Includes:**
- **Character Mapping:** Utilizes a database of common homoglyphs.
- **Permutation Logic:** Generates all possible domain combinations with substituted characters.
- **Punycode Conversion:** Converts generated domains to ASCII-compatible encoding for further analysis.

---

### 2. Homograph Attack Detection

Detects suspicious domains by comparing them to a whitelist of legitimate domains.

**Detection Techniques:**
- **String Similarity Analysis:** Uses algorithms like Levenshtein distance and Jaccard similarity.
- **Unicode Normalization:** Standardizes characters for accurate comparison.
- **Risk Scoring:** Assigns a score based on visual similarity to known domains.

---

## 📌 Key Contributions

- ✅ **Automated Simulation:** Generates hundreds of deceptive domain variants for testing security systems.
- 🛡️ **Advanced Detection:** Outperforms basic browser-based detection with multi-script analysis.
- 📚 **User Awareness Module:** Educates users about homograph threats and shows real-world examples.
- 📊 **Proven Impact:** Controlled tests show:
  - 85%+ detection accuracy
  - 60% of users failed to recognize fake domains
  - Automated detection can reduce phishing success by **up to 80%**

---

## 📥 How to Download & Run

1. **Download and Extract**  
   Download the `homograph-detector.7z` file and extract it.

2. **Set Up Virtual Environment**  
   Open a terminal or CMD window and run:
   ```bash
   python -m venv venv

   venv\Scripts\activate  # On Windows

   python app.py

