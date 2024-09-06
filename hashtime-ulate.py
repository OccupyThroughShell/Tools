#!/usr/bin/python
# I know you've probably seen better documentation by malware gangs. 

# IMPORTant hahaha

import sys
from colorama import Fore

# Raises max str digits

sys.set_int_max_str_digits(2147483647)

# Looks cool. Couldn't be bothered to do ascii art

print(Fore.RED + "# Simple Tool Written By OccupyThroughShell!!!\n# Calculate how long it'll take to finish cracking a hash!\n# If you don't know exact values just take a guess :/\n# Just follow the prompts to use the tool!\n<==========================================================>\n\n\n")

# This input design is very humane

x = int(input(Fore.BLUE + "\n[*] How many characters are in the passwords alphabet: "))
y = int(input(Fore.BLUE + "\n[*] How many uppercase characters are there: "))
z = int(input(Fore.BLUE + "\n[*] How many special characters are there: "))
a = int(input(Fore.BLUE + "\n[*] How long is the password: "))
h = float(input(Fore.RED + "\n[*] Check Hashrate by using 'hashcat -b'\n[*] Hash rate: "))
b = int(1000000)

# Calculates stuff

def calculate():

 alphabet = int(x + y + z)
 print(Fore.GREEN + f"\n[*] Number of Potential Characters: {alphabet}")
 keyspace = int(alphabet**a)
 print(Fore.GREEN + f"\n[*] Keyspace Calculated to the value of: {keyspace}")
 hashrate = float(h*b)
 print(Fore.GREEN + f"\n[*] Calculated Hash Rate: {hashrate}")
 speed = float(keyspace / hashrate)
 print(Fore.GREEN + f"\n[*] It'll take {speed} seconds to crack the passcode")
 minutes = int(speed / 60)
 hours = int(minutes / 60)
 days = int(hours / 24)
 years = int(days / 365)
 
# Gotta make it pretty though

 if minutes == 1:
  print(Fore.GREEN + f"\n[*] You'll have to wait roughly a minute!")
 elif minutes < 60 and minutes > 1:
  print(Fore.GREEN + f"\n[*] You'll have to wait roughly {minutes} minutes!")
 else:
  print(Fore.GREEN + "\n[*] Skipping")

 if hours == 1:
  print(Fore.GREEN + f"\n[*] You'll have to wait roughly an hour!")
 elif hours < 24 and hours > 1:
  print(Fore.GREEN + f"\n[*] You'll have to wait roughly {hours} hours!")
 else:
  print(Fore.GREEN + "\n[*] Skipping")
 
 if days == 1:
  print(Fore.GREEN + f"\n[*] It'll take roughly a day!")
 elif days < 365 and days > 1:
  print(Fore.GREEN + f"\n[*] It'll take roughly {days} days!")
 else:
  print(Fore.GREEN + "\n[*] Skipping")
 
 if years == 1:
  print(Fore.GREEN + f"\n[*] It'll take about an entire year ^-^\n[*] Give up on this one...")
 elif years < 1000000000 and years > 1:
  print(Fore.GREEN + f"\n[*] It'll take roughly {years} years ^-^\n[*] REALLY Give this one up...")
 else: 
  print(Fore.GREEN + "\n[*] Skipping")

# Just a little sass

 if years > 1000000000:
  print(Fore.GREEN + "\n[*] Congrats, it'll be cracked in + - a billion years...")
 else:
   print(Fore.GREEN + "\n[*] Skipping") 

# GO PROGRAM GO

calculate()
print(Fore.GREEN + f"\n[*] Exiting")

