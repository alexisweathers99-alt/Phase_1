# TITAN SMALL BUSINESS SERVICES: SECURITY ARCHITECTURE DOCUMENT (SAD)
**Operator:** [Alexis Weathers]
**Date:** [4/21/2026]

## 1. Perimeter Hardening (UFW & SSH)
* **SSH Status:** [Disabled Root Login and disabled Password Authentication to enforce key-based security.]
* **Firewall Logic:** [Implemented a "Default Deny" policy for all incoming traffic. Explicitly allowed port 22/tcp for secure management and 8080/tcp for application traffic.]

## 2. The Automated Auditor (Python)
* **Script Logic:** [ import os
output = os.popen("df -h").read()
with open("/var/log/sys_audit.log", "w") as f:
    f.write(output)]
* **Telemetry Path:** `/var/log/sys_audit.log`

## 3. Containerized App (Docker)
* **Network Isolation:** [The Redis database was placed on a private internal bridge network without any host port mapping. This means it is only reachable by the Nginx frontend container and is invisible to the outside world.]
* **Stack Health:** [ root_frontend_1 | Up | 0.0.0.0:8080->80/tcp
root_backend_1  | Up | 6379/tcp ]

## 4. Executive Summary
[The outpost is a lot more secure now after tightening things up at the operating system level mainly by locking down SSH access and setting up UFW rules. There's also a simple automated script running to keep an eye on system's health. The app is set up in different layers so the parts that handle sensitive data are kept separate from anything exposed to the public. Overall, this layered setup helps protect the system better and makes it harder for unauthorized users to get in.]
