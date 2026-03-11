#!/bin/bash
# T1-M1-S02: SECURITY HARDENING AUTOMATION
# Task: Restore Gold Standard permissions to restricted artifacts.

# TODO: Add commands to secure ~/Vault/secrets.txt to 600
# TODO: Add commands to secure /etc/shadow to 640
chmod 700 /home/aweathers/Vault
chmod 600 /home/aweathers/Vault/secrets.txt

sudo chmod 640 /etc/shadow
sudo chown root:shadow /etc/shadow
