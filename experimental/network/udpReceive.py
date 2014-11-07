# basic example of catching a packet

import socket

# IP address and port of our machine
myAddress = ("0.0.0.0", 8001) # 0.0.0.0 means "use any available addresses"

# make a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# choose an address for the socket
sock.bind(myAddress)

# wait for a message
message, addr = sock.recvfrom(1024) # buffer size

print("got: " + message + " from: " + str(addr))

