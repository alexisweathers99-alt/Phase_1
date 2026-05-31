# Phase 1 Final Reckoning — TEPP Post-Mortem
**Operator:** [Alexis Weathers]
**Date:** May 28, 2026
**Repository:** [https://github.com/alexisweathers99-alt/Phase_1]
**TKH Innovation Fellowship 2026 | Phase 1 | Cybersecurity**

---

## Phase 0: Reconnaissance

### Triage Network — 172.100.0.0/24
[Four active hosts were identified on the 172.100.0.0/24 subnet at IP addresses 172.100.0.1, 172.100.0.11, 172.100.0.12, and 172.100.0.13. After analyzing these systems, open services were found, including Secure Shell (SSH) on port 22 and Hypertext Transfer Protocol (HTTP) on port 80, showing that remote management and web services were active. A possible security issue was identified because there did not appear to be proper firewall separation between the management system and internal containers, which could make it easier for attackers to move through the network and access internal systems.]


### Breach Network — 172.80.0.0/24
[3–5 sentences in APA style. What hosts did you find? What ports and
services were exposed? What did you observe that informed your Phase 2
approach?]

[The host identifed in this a virtual container with networks bridged between 172.80.0.0/24 and 172.100.0.0/24. Due to the lasck of the firewall, there is a major risk of anyone gaining acesses to this allowing them to map out, scan, and attack the backend services.]

### Exploitation Network — 172.60.0.0/24

[One active host was found at IP address 172.60.0.1 which is connected to the main VirtualBox environment. Based on the network analysis, SSH access on port 22 was available, which could allow remote administrative access to the system. Before exploitation, a possible security issue was identified because the network did not seem to have strong separation between systems, which may allow an attacker to gain access to the host operating system from another compromised part of the network.]

---

## Phase 1: Rapid Triage

### Server 1 — 172.100.0.11
**Vulnerability Identified:**
[An active network deployment audit confirmed that target host 172.100.0.11 leaves an unauthenticated Redis key-value store database exposed to the network on TCP port 6379? This was verified via a targeted Nmap service-version identification scan, which successfully pulled a banner identifying the service instance as Redis key-value store 8.6.3. The application configuration lacks any prompt for administrative authentication which allows for external users to access it.]

**Remediation Commands:**
[docker exec -it broken_server_2 vi /etc/vsftpd/vsftpd.conf |docker exec -it broken_server_2 sed -i 's/anonymous_enable=YES/anonymous_enable=NO/' /etc/vsftpd/vsftpd.conf |exit | docker restart broken_server_2]

**Before State:**
[The configuration file contained the active parameter anonymous_enbale=YES. This lets remote unauthorized persons to establish access using genaric username (anonymous or ftp) and week passwords that will allow full access and download public files. ]

**After State:**
[The parameter was updated to anonymous_enable=NO. Now users with inncorrect cerdentials will be rejected and met with a 530 Permisssion denied]

**Analysis:**
[Anonymous authentication in the real world poses a dangerous risk due to the fact that it allows unauthorized users with malicious intent to gain access to PPI while not triggering any failure alarms.]

### Server 2 — 172.100.0.12
**Vulnerability Identified:**
[looking at the target machine, the docker ps command was run to see what containers were currently active on the system. Inside the list of containers, one stood out called broken_server_2, which had the container ID of dc1e9f0a9757. After checking inside this specific container, it was found to be running an FTP server using the fauria/vsftpd image. To make sure the service was actually running, the ps aux command was typed into the container's terminal. This showed that the active program, located at /usr/sbin/vsftpd, was currently running under process ID (PID) 21.]

**Remediation Commands:**
[docker ps | docker exec -it broken_server_2 /bin/bash| ps aux| kill -9 21]

**Before State:**
[Before fixing the issues, the container application was running an unencrypted FTP server (vsftpd) on process ID 21. Because this container left network ports 20 and 21 completely open to the network, it created a major security risk. Anyone listening on the network could easily see and steal usernames and passwords because the data is sent in plain text, which is called cleartext sniffing. Also, since these ports were open, an unauthorized user might be able to get into the system and read or modify files on the server without permission]

**After State:**
[After sending the command to stop process PID 21, the program running inside the container stopped right away. Because this program was the main thing keeping the container alive, stopping it caused the whole container to shut down. This also ended the terminal session I was using inside the container, which automatically took me back to the main command prompt of the host computer.]

**Analysis:**
[Leaving old or unprotected file transfer protocols like FTP running on a company network can cause huge problems for data security and server stability. Because standard FTP does not use encryption, hackers can easily intercept and steal sensitive user login information while it travels across the network. Furthermore, if the FTP software is old and unpatched, attackers could exploit weaknesses to gain higher administrator privileges or even break out of the container completely (Siddique et al., 2024). Getting rid of these outdated services or setting up containers to automatically shut down when finished is a great way to stop hackers from staying hidden in the network for a long time.]

### Server 3 — 172.100.0.13
**Vulnerability Identified:**
[After looking through the files inside the broken_server_3 container, it was discovered that the main website folder located at /var/www/html had its permissions set to world-writable, which is also known as 777 permissions. To double-check this mistake, the ls -la /var/www command was run in the terminal. The output showed the full list of flags as drwxrwxrwx, which proved that absolutely anyone on the system has total permission to read, write, and execute files in that folder.]

**Remediation Commands:**
[docker exec -it broken_server_3 /bin/sh| ls -la /var/www | chmod 755 /var/www/html]

**Before State:**
[Before the issue was fixed, the /var/www/html folder had global permissions set to drwxrwxrwx, which is the same as 777 permissions. This setup was a big security risk because it meant that anyone or anything on the computer could change things. For example, any standard user, an automated background program, or a hacked low-privilege account could easily make new files, change existing ones, or completely delete important website files right out of the main web folder.]

**After State:**
[After executing the corrected chmod command, a secondary directory check using ls -la /var/www verifies that the permission string changed to drwxr-xr-x (755). This confirms that only the root owner retains write privileges, while all other users are limited strictly to reading and executing.]

**Analysis:**
[Giving everyone full read, write, and execute access (777 permissions) to folders on a web server goes completely against the security principle of least privilege. It also makes it much easier for an attacker to gain higher administrator privileges on the system. If a hacker manages to find a glitch in the website that lets them upload random files or run commands from a distance, these weak permissions mean they can easily drop malicious tools like web shells or backdoors right into the website's folders (Sutton, 2024). Leaving the system exposed like this makes it way more likely that a hacker could ruin the website's appearance, keep a permanent back door open to spy on the system, or completely take over the container.]


---

## Phase 2: The Breach

**Cracked Credentials:**
# My Credendtels were stollen so that i hid the password for privacy reasons
- Username: [aweathers]
- Password: [********]

**Forensic Evidence:**
- Exact Timestamp of Successful Login: [2026-05-30T21:16:53.30114410-04:00]
- Attacker IP Address: [10.0.2.2]

**Engineered iptables Rule:**
[sudo iptables -A INPUT -s 10.0.2.2 -j DROP]

**SOC Analysis:**
[using a single iptables rule to block one IP address on the host computer is not enough to keep a system safe by itself. This is because it is a reactive fix, meaning it only helps after a hacker has already broken into the system or started an attack. Smart attackers often change their IP addresses constantly, use proxy networks, or use other hacked computers to easily get around static IP blocks (Torres, 2023). Instead of just blocking one IP, a real Security Operations Center (SOC) would use multiple layers of defense. This includes tools like fail2ban to automatically block people trying to guess passwords, multi-factor authentication (MFA) so stolen passwords will not work, and a centralized logging system (like a SIEM) to catch strange login patterns before an attacker can even get in.]

---

## Phase 3: Full Spectrum

**Listener Configuration:**
[Tool Netcat (nc), Port: 444, command: nc -lvnp 4444]

**Reverse Shell Payload:**
[nc 172.80.0.10 22]

**Command Injection Explanation:**
[Injection risks happen when a system takes untrusted inputs or connection strings from a user and passes them directly to an unprotected system manager or protocol handler without checking them first. Even though secure shells (SSH) are usually pretty good at stopping regular hackers from typing direct malicious commands through a website, leaving SSH login banners and open network ports unmonitored on an internal network is still dangerous. It gives attackers a chance to scan the network, find out what specific version of the operating system kernel is running, and see what active programs are running in the background.]

**Forensic Evidence:**
- Process ID (PID): [1 auth.log]
- User-Agent: [SSH-2.0-OpenSSH_10.2]

**Lockdown Command:**
[sudo iptables -A INPUT -p tcp --dport 22 -j DROP]

**Final Analytical Paragraph:**
[this attack proves that you cannot just rely on a strong outer firewall to keep a network safe. Once a hacker actually gets inside the local network, they can easily exploit unprotected internal services (Smith, 2026). Seeing how the network login banner openly gave away the exact version numbers of the software shows how easily a hacker can gather information about the inside of a network. The main security control that would have stopped this whole attack from happening is a strict network access control list (ACL) or an internal firewall rule made to block unauthorized traffic moving sideways between systems. Setting up this kind of network segmentation ahead of time keeps internal systems isolated from each other, which completely stops an attacker from being able to find, connect to, or mess with open ports from a nearby container or network section.]

---

## References
[[Google. (2026). Gemini [Large language model]. https://gemini.google.com/]
