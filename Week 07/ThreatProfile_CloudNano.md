# TARGET THREAT PROFILE: CloudNano 
**Classification:** Passive Security Audit
**Operator:** ## 1. Subdomain Discovery 
* **Tool Used:** Sublist3r
* **Subdomains Found:** * [accounts.tesla.com] 
  * [developer.tesla.com] 

## 2. Tech Stack Mapping 
* **Tool Used:** BuiltWith / Wappalyzer
* **Identified Technologies (CMS/CDN/Backend):** * [Akamai mPulse] 
  * [Salesforce] 

## 3. Major Exposure Points & Dangers 
*(List three major exposure points discovered during your OSINT audit and explain why they are dangerous)*
1. **[Unsecured RDP (Port 3389)]:** [Open Remote Desktop ports allow attackers to attempt brute force attacks to gain direct administrative control over internal systems] 
2. **[vsFTPd 2,3.4(Port 21)]:** [This software version contains a well known backdoor that allows unauthorized users to gain immediate shell access to the server] 
3. **[Leaked server banners(Microsoft IIS 10.0)]:** [Publicly broadcasting specific software versions allows an adversary to quickly identify and deploy targeted exploits (CVEs) against the enviornment] 
