"""
Simple TCP server: binds to 0.0.0.0:9998, accepts connections, and handles each
client in a separate thread. Echoes received data and sends back "ACK".
"""
import socket
import threading

# Listen on all interfaces (0.0.0.0) so remote clients can connect
IP = '0.0.0.0'
PORT = 9998


def main():
    # Same socket type as the client (AF_INET, SOCK_STREAM); usage differs: we bind and listen
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)  # Backlog for pending connections
    print(f"Listening on {IP}:{PORT}")

    while True:
        # Block until a client connects
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        # Handle each client in its own thread so we can serve multiple at once
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


def handle_client(client_socket):
    """Read one message from the client, print it, and reply with ACK."""
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"Received: {request.decode('utf-8')}")
        sock.send(b"ACK")


if __name__ == "__main__":
    main()