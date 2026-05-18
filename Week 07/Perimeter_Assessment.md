# TITANCORP: PERIMETER ASSESSMENT REPORT
**Operator:** **Target Subnet:** 172.88.0.0/24

## PHASE 1: ACTIVE ENUMERATION (NMAP)
*(List the live IPs discovered and their running services/versions)*
* **Host 1 ([172.88.0.10]):** [80/tcp http nginx 1.14.2]
* **Host 2 ([172.88.0.15]):** [All 1,000 posrts are closed]
* **Host 3 ([172.88.0.20]):** [80/tcp http Apache http 2.4.67 ((Unix))]

## PHASE 2: VULNERABILITY AUDIT (NIKTO)
*(Run Nikto against the TWO web servers discovered above. List one major finding for each.)*
* **Web Server 1 Finding:** [The anti-clickjacking X-Frame-Options header is not present]
* **Web Server 2 Finding:** [HTTP TRACE method is active (vulnerable to XST)]

## PHASE 3: RISK TRIAGE
*(Review your findings. Identify the SINGLE highest-risk vulnerability across the entire DMZ. Justify why it is the top priority using the Likelihood x Impact formula.)*

* **Top Priority Remediation:** [X-Frame-Options]
* **Justification:** [Without this header a hacker can load your site on a layer over their own malicious site. This can lead you clicking on something with a different intent. ]
