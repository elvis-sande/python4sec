"""
EXPLORE DNS SERVER FOR VARIOUS COMMON
SUBDOMAINS ASSOCIATED TO AN IP OR DOMAIN NAME
"""
import dns
import dns.resolver
import socket


def reversedns(ip):
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]]+result[1]
    except socket.herror:
        return None


def dnsrequest(domain):
    ips = []
    try:
        result = dns.resolver.resolve(domain)
        if result:
            print(domain)
            for answer in result:
                print(answer)
                print("Domain Names: %s" % reversedns(answer.to_text()))
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []
    return ips


def subdomainsearch(domain, dictionary, nums):
    successes = []
    for word in dictionary:
        subdomain = word+"."+domain  # Create subdomain e.g: mail.google.com
        dnsrequest(subdomain)  # Perform dns request for that subdomain
        if nums:  # Check if the subdomain has a number appended, e.g vpn1.x.com
            for i in range(0, 10):
                s = word+str(i)+"."+domain
                dnsrequest(s)


domain = "google.com"  # OUR TARGET DOMAIN/NETWORK
d = "subdomains.txt"
dictionary = []
with open(d, "r") as f:
    dictionary = f.read().splitlines()
subdomainsearch(domain, dictionary, True)  # The bool will de/activate checking for numbered subdomains
