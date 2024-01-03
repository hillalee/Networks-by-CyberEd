from scapy.all import *
myMAC = "70:b3:d5:5c:0c:a7"

def filter_mac(frame):
	return (Ether in frame) and (frame[Ether].dst == myMAC)

def print_src_address(frame):
	print(frame[Ether].src)

frames = sniff(count=10, lfilter = filter_mac, prn=print_src_address)

frames.show()
