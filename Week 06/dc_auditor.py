import os

# Configuration
dc_ip = "8.8.8.8"  # <--- REPLACE THIS WITH THE ACTUAL IP
log_path = "/var/log/dc_audit.log"

# Step 2: Logic - Ping the DC 4 times
# -c 4 means 4 packets
response = os.system(f"ping -c 4 {dc_ip}")

# Step 3: Output - Determine status and write to log
if response == 0:
    status = "DC is UP"
else:
    status = "DC is DOWN"

with open(log_path, "w") as f:
    f.write(status + "\n")

print(f"Audit complete: {status}")
