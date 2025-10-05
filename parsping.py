#!/usr/bin/env python3

## ParsPing is a simple network scanner that checks if each host in a
## given IP address range is online or offline.

## There are also optional commands '-u' and '-d' that can be used to find either
## online ('up') or offline ('down') hosts respectively. If neither of these are provided,
## the script simply displays the number of hosts that are online.

from scapy.all import *
import logging
import argparse
import re
import time

print("""\t   ____                ____  _             
\t  |  _ \ __ _ _ __ ___|  _ \(_)_ __   __ _ 
\t  | |_) / _` | '__/ __| |_) | | '_ \ / _` |
\t  |  __/ (_| | |  \__ \  __/| | | | | (_| |
\t  |_|   \__,_|_|  |___/_|   |_|_| |_|\__, |
\t                                      |___/ """)
print("\t  *****************************************")
print("\t  ****         By Corbin Parsley       ****")
print("\t  ****    (https://github.com/cr0bb)   ****")
print("\t  *****************************************")


## Shut up warning messages
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

parser = argparse.ArgumentParser(description="Ping an IP address range")
parser.add_argument("ip", type=str, help="IP address (e.g 102.168.1.1)")
parser.add_argument("-u", action='store_true', help="Search for open addresses in range")
parser.add_argument("-d", action='store_true', help="Search for closed addresses in range")

args = parser.parse_args()

ip_addr = args.ip

def get_ip(ip):
    result = ip
    ip_regex = r"^(\d{1,3}\.\d{1,3}\.\d{1,3})"
    match = re.search(ip_regex, result)
    if match:
        return match.group(1)
    else:
        return None

first_octets = get_ip(ip_addr)

def progress_bar(progress, total):
    perc = 100 * (progress / float(total))
    bar = '█' * int(perc / 2) + '-' * (50 - int(perc / 2))
    print(f'\r   [{bar}] {perc:.2f}%', end="\r")
    if progress == total:
        print("\n")

def scan(octets):
    num_open = 0
    num_down = 0
    up = []
    down = []
    print(f"\n\t\t\033[1mScanning network range {octets}\033[0m")
    for last_octet in range(0,255):
        progress_bar(last_octet, 254)
        ip_add = f'{first_octets}.{last_octet}'
        # Construct the packet with IP and ICMP headers (checking host availability)
        packet = IP(dst=ip_add)/ICMP()
        response = sr1(packet, timeout=0.1, verbose=False)
        if response:
            num_open += 1
            if args.d:
                continue
            else:
                up.append(ip_add)
        else:
            num_down += 1
            if args.u:
                continue
            else:
                down.append(ip_add)

    print(f"Scan complete.\n")
    time.sleep(1)
    if args.u:
        print(f'\033[1m{num_open}/255\033[0m hosts are up in address range {first_octets}.\n')
        time.sleep(1)
        print(f'Online hosts are: {up}\n')
    elif args.d:
        print(f'\033[1m{num_down}/255\033[0m hosts are down in address range {first_octets}.\n')
        time.sleep(1)
        print(f'Offline hosts are: {down}\n')
    else:
        print(f'\033[1m{num_open}/255\033[0m hosts are up in address range {first_octets}.\n')

if __name__ == "__main__":
    scan(first_octets)
