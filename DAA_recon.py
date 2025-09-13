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

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-D", "--DNS-server", help="Assign specific DNS server", dest="D", default = '8.8.8.8')
    parser.add_argument("-q", "--query", help="domainname to query", dest="q", default = 'google.com')
    parser.add_argument("-qt", "--querytype", help="type of record to query", dest="qt", type=int, default = 255)
    args = parser.parse_args()
    print('DNS server: %s' %args.D)
    print('Query: %s' %args.q)
    print('Query Type: %s' %args.qt)

    ip = construct_IP(DNSaddr = args.D)
    udp = construct_UDP()
    q = construct_DNSQR(qtype = args.qt, qname = args.q)
    dns = construct_DNS(q)

    p = (ip/udp/dns) # create test packet
    print('Size of initial packet: %s' %len(p))
    r = sr(p, timeout=0.5)
    print('Size of returned packet: %s' %len(r))
    r.display()
    amp = len(r)/len(p)
    print('Amplification: %f' %amp)
    exit()