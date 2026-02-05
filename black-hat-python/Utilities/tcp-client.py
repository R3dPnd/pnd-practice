"""
Simple TCP client: connects to a host:port, sends one message, receives a response, then exits.
TCP guarantees in-order delivery and reliability (retransmits lost packets).
"""
import socket

target_host = "127.0.0.1"
target_port = 9998

# Create a TCP socket: AF_INET = IPv4, SOCK_STREAM = TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (blocks until connection is established or fails)
client.connect((target_host, target_port))

# Send a single message
client.send(b"Hello, TCP Server!")

# Receive up to 4096 bytes (blocks until data arrives or connection closes)
response = client.recv(4096)

print(response.decode())

# Release the connection
client.close()