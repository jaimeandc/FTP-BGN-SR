# udt.py - Unreliable data transfer using UDP
import random
DROP_PROB = 0

# Send a packet across the unreliable channel
# Packet may be lost
def send(packet, sock, addr):
    if random.randint(0, 10) > DROP_PROB:
        sock.sendto(packet, addr)
    return

# Receive a packet from the unreliable channel
def recv(sock):
    ##ADJUST BYTE SIZE
    packet, addr = sock.recvfrom(1024)
    return packet, addr