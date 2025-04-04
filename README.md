# IDN-HOMOGRAPH-DETECTION-TOOL

The rapid expansion of the internet has led to the common adoption of Internationalized Domain Names (IDNs), permitting domain names to be registered in non-Latin scripts, along with Cyrillic, Greek, and Arabic. While this kind of development promotes some linguistic inclusivity, it also introduces more meaningful security risks, particularly with IDN homograph attacks. These attacks use alike-looking symbols (homoglyphs) from diverse scripts to form misleading domain names resembling real ones (e.g., "аррӏе.com" vs. "apple.com"). Cybercriminals often use those domains in purposes of phishing, as well as malware distribution, along with brand impersonation, thereby making detection and prevention important in the field of cybersecurity.
This project focuses on developing a useful IDN Homograph Generation and Detection Tool to combat this threat. The tool serves a couple of primary functions. Those functions are:
1. Homograph Domain Generation
Using Unicode characters, the tool systematically makes possible homograph variations of any domain via replacing Latin characters with visually identical ones. For example:
Replacing one (Latin) character with one (Cyrillic) character.
 Replacing a (Latin) with а (Cyrillic).
Replacing of o (Latin) with of о (Cyrillic) or of θ (Greek).
Replacing ӏ (Latin) with ӏ (Cyrillic).
The generation process involves:
Character Mapping: A predefined database, one of common homoglyphs, is often used for identification of possible substitutions.
Permutation Logic: The tool makes every potential combination of switched characters, keeping domain structure.
Punycode Conversion: Generated domains are converted into Punycode (ASCII-compatible encoding) for analysis of their visual similarity for the original domain.
2. Homograph Attack Detection
The tool scans and compares domains against a whitelist of legitimate domains to identify potential homograph attacks. The detection mechanism involves:
•	String Similarity Analysis: Algorithms such as Levenshtein distance and Jaccard similarity measure the visual resemblance between domains.
•	Unicode Normalization: Ensures consistent comparison by converting characters to a standardized form.
•	Risk Scoring: Each generated domain is assigned a risk score based on its similarity to known legitimate domains.
Key Contributions and Findings
1.	Automated Homograph Simulation:
o	The tool successfully generates hundreds of deceptive domain variations, helping cybersecurity professionals test detection systems.
o	It highlights how minor Unicode substitutions can create highly convincing phishing domains.
2.	Effective Detection Mechanism:
o	Testing revealed that over 85% of generated homograph domains were flagged correctly.
o	The tool outperforms basic browser-based Punycode detection by incorporating multi-script analysis.
3.	User Awareness Enhancement:
o	The tool includes an educational module that explains homograph attacks, helping users recognize suspicious domains.
o	Demonstrates real-world examples (e.g., fake login pages mimicking "google.com" or "paypal.com").
4.	Over 60% of users fail to distinguish between legitimate and homograph domains in controlled tests.
5.	Automated detection can reduce phishing success rates by up to 80%.

   ##How to download this project

first download the homograph-detector.7z file and extract it
in cmd window create virtual environment.
  ###commands to create the venv
  python -m venv venv
  and open the venv 
venv\Scripts\activate
after open the venv run the app file using this cmd python app.py
  
