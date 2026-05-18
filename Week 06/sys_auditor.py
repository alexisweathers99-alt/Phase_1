import os

# Define the command and log file path
command = "df -h"
log_file = "/var/log/sys_audit.log"

# Execute the command and capture output
output = os.popen(command).read()

# Write the output to the log file
with open(log_file, "w") as f:
    f.write("--- System Disk Audit ---\n")
    f.write(output)

print(f"Audit complete. Results saved to {log_file}")
