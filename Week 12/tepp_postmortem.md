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

[The host identifed in this a virtual container with networks bridged between 172.80.0.0/24 and 172.100.0.0/24. Due to the lasck of the firewall, there is a major risk of anyone gaining acesses to this allowing them to map out, scan, and attack the backend services.]

### Exploitation Network — 172.60.0.0/24

[One active host was found at IP address 172.60.0.1 which is connected to the main VirtualBox environment. Based on the network analysis, SSH access on port 22 was available, which could allow remote administrative access to the system. Before exploitation, a possible security issue was identified because the network did not seem to have strong separation between systems, which may allow an attacker to gain access to the host operating system from another compromised part of the network.]

---

## Phase 1: Rapid Triage

### Server 1 — 172.100.0.11
**Vulnerability Identified:**
[An active network deployment audit confirmed that target host 172.100.0.11 leaves an unauthenticated Redis key-value store database exposed to the network on TCP port 6379? This was verified via a targeted Nmap service-version identification scan, which successfully pulled a banner identifying the service instance as Redis key-value store 8.6.3. The application configuration lacks any prompt for administrative authentication which allows for external users to access it.]

**Remediation Commands:**
docker exec -it broken_server_1 /bin/sh
redis-cli CONFIG SET requirepass "SecurePass123"

**Before State:**
The Redis instance was running with no password (requirepass was set to empty ""), meaning any user on the network could connect to the database on port 6379 without authentication and freely access or modify all stored data.

**After State:**
The requirepass parameter was set to a secure password. Any connection attempt without the correct credentials now returns "NOAUTH Authentication required", confirming that unauthorized users can no longer access the Redis database.

**Analysis:**
The exposure was that Redis had no password, allowing unauthorized personnel to gain access. This is a major issue because if an attacker gains access, they will be able to read, write, and modify the data that is stored. This data can contain PII that can be catastrophic to the owner. Requiring authentication through a strong password ensures that only authorized users can connect to the database, preventing unauthorized access to sensitive information.

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
The vulnerability here was the FTP server sending data in plain text, allowing things like passwords to be intercepted easily. This is a problem because anyone can log in anonymously without credentials and steal files. Furthermore, an attacker could also upload malicious files to the server, potentially compromising the entire system. FTP is outdated and should be replaced with SFTP or FTPS to ensure data is encrypted during transfer.

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
777 permissions are dangerous because they allow everyone to read, write, and execute files in the folder, which means an attacker could easily upload malicious files like web shells. This violates the principle of least privilege, which states that users should only have the minimum access they need to do their job. A web shell could give an attacker remote control over the server, allowing them to steal data or cause further damage. Setting permissions to 755 ensures that only the owner can make changes, while everyone else can only read and execute.


---

## Phase 2: The Breach

**Cracked Credentials:**
My Credentials were stolen so that I hid the password for privacy reasons 
- Username: [aweathers]
- Password: [********]

**Forensic Evidence:**
- Exact Timestamp of Successful Login: [2026-05-30T21:16:53.30114410-04:00]
- Attacker IP Address: [10.0.2.2]

**Engineered iptables Rule:**
[sudo iptables -A INPUT -s 10.0.2.2 -j DROP]

**SOC Analysis:**
Blocking a single IP address will only temporarily fix the problem because attackers can easily change their IP or use proxies to get around it. A real Security Operations Center (SOC) needs tools that can respond to threats no matter where they come from. Tools like fail2ban can automatically block repeated login attempts, and Multi-Factor Authentication (MFA) ensures that stolen passwords alone are not enough to gain access. A SIEM system tracks suspicious login patterns early, allowing security teams to catch and stop attackers before they can do serious damage.

---

## Phase 3: Full Spectrum

**Listener Configuration:**
[Tool Netcat (nc), Port: 444, command: nc -lvnp 4444]

**Reverse Shell Payload:**
[nc 172.80.0.10 22]

**Command Injection Explanation:**
[Injection risks happen when a system takes untrusted inputs or connection strings from a user and passes them directly to an unprotected system manager or protocol handler without checking them first. Even though secure shells (SSH) are usually pretty good at stopping regular hackers from typing direct malicious commands through a website, leaving SSH login banners and open network ports unmonitored on an internal network is still dangerous. It gives attackers a chance to scan the network, find out what specific version of the operating system kernel is running, and see what active programs are running in the background.]

**Forensic Evidence:**
- Process ID (PID): [1]
- User-Agent: [SSH-2.0-OpenSSH_10.2]

**Lockdown Command:**
[sudo iptables -A INPUT -p tcp --dport 22 -j DROP]

**Final Analytical Paragraph:**
Relying solely on a perimeter firewall is not enough to keep a network safe because once an attacker gets inside, they can move freely between systems. Leaving ports open on an internal network is just as dangerous as leaving them open to the outside, because attackers can use them to find and exploit vulnerable services. Additionally, version banners on open ports give attackers valuable information about what software is running, making it easier for them to plan their attack. Implementing Network Access Control Lists (ACLs) and proper network segmentation would prevent unauthorized traffic from moving between systems, stopping attackers from being able to reach sensitive internal services.

---

## References
[[Google. (2026). Gemini [Large language model]. https://gemini.google.com/]
