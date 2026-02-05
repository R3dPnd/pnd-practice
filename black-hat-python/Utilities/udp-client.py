"""
Simple UDP client: sends one datagram to host:port and optionally waits for a reply.
UDP is connectionless (no handshake); use SOCK_DGRAM. No guarantee of delivery or order.
"""
import socket

target_host = '127.0.0.1'
target_port = 9997

# UDP socket: AF_INET = IPv4, SOCK_DGRAM = UDP (datagram, no connection)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Avoid blocking forever if no one is listening or no reply is sent
client.settimeout(5.0)

try:
    # sendto() includes destination; no connect() required for UDP
    client.sendto(b"AAABBBCCC", (target_host, target_port))
    print(f"Data sent to {target_host}:{target_port}")
except OSError as e:
    if e.winerror == 10054:  # Windows: connection forcibly closed
        print(f"Error: Connection refused - no server listening on {target_host}:{target_port}")
    else:
        print(f"Error sending data: {e}")
    client.close()
    exit(1)
except Exception as e:
    print(f"Error sending data: {e}")
    client.close()
    exit(1)

try:
    # recvfrom() returns (data, sender_address) since UDP is connectionless
    data, addr = client.recvfrom(4096)
    print(f"Received from {addr}: {data.decode()}")
except socket.timeout:
    print("Warning: No response from server (timeout) - data may have been sent but not acknowledged")
except OSError as e:
    if e.winerror == 10054:  # Windows: connection forcibly closed
        print("Warning: Server closed connection - data may have been sent")
    else:
        print(f"Error receiving data: {e}")
except Exception as e:
    print(f"Error receiving data: {e}")
finally:
    client.close()