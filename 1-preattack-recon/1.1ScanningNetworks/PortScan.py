"""
PORT SCANNER TEMPLATE USING SCAPY
"""
from scapy.all import *

ports = [25, 80, 53, 443, 445, 8080, 8443]  # ports to scan


def synscan(host):
    ans, unans = sr(IP(dst=host) / TCP(sport=5555, dport=ports, flags="S"), timeout=2, verbose=0)
    print("Open ports at %s:" % host)
    for (s, r,) in ans:  # Loop through sent and received packets in ans
        if s[TCP].dport == r[TCP].sport:  # does destination port respond?
            print(s[TCP].dport)  # Print which port responds(is open)


"""
Half-connect scan, will Determine if a port is open
send SYN, receive SYN/ACK and does not send ACK
create vars to hold answered and unanswered packets
unans does nothing for now, but one can decide to do something with unans packets
use scapy sr function to send packets and listen for responses
We build our packet layers in sr with desired fields
dport specifies the destination ports to scan/ send packets to
the flag specifies the type of packets to send (S = syn, A = ack, etc)
Time out after 2 seconds of waiting, and no verbose logs, just the result
"""


def dnsscan(host):
    ans, unans = sr(IP(dst=host) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com")), timeout=2, verbose=0)
    if ans:
        print("DNS Server at %s" % host)


"""
Simple DNS Scan Will check for a proper response to a DNS scan
Send only 1 packet to specified port
No flags in UDP packet commonly used by DNS
Specify 1 request(rd) and query the name provided in qname
"""

# This code will scan just one host at a time, but a loop can be designed to loop through a subnet
host = "8.8.8.8"

synscan(host)
dnsscan(host)

"""
Got modulenotfounderror: no module named scapy even though i had scapy in my system
FIX: install scapy as root, run python3 as root still
"""
