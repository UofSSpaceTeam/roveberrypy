# basic example of throwing a packet at someone

import socket

# IP address and port of our destination machine
target = ("127.0.0.1", 8001)
myAddress = ("0.0.0.0", 8000) # 0.0.0.0 means "use any available addresses"

# make a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# choose an address for the socket
sock.bind(myAddress)

# send a message to our destination
message = "Hi! This is a UDP packet!"
sock.sendto(message, target)

print("sent a packet to " + str(target))

