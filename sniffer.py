from scapy.all import *
def pkt_callback(pkt):
    if DNS in pkt:
        pkt.show()

if __name__ == '__main__':
    sniff(prn = pkt_callback)
