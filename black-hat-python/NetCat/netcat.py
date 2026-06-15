"""
NetCat: A simple TCP netcat-like tool for listening, sending, and remote execution.
Supports client/server modes, file upload, command execution, and interactive shell.
"""

import socket
import sys
import threading


from Utilities.socket_utility import SocketUtility


def execute(cmd):
  """
  Run a shell command and return stdout. Overridden by netcat_cmd when used as CLI
  so that handle() can call it; otherwise would raise.
  """
  raise NotImplementedError("execute must be set by the entry point (e.g. netcat_cmd)")


class NetCat:
  """Netcat-like TCP client/server. Use -l to listen or connect to a target host:port."""

  def __init__(self, args, buffer=None):
    self.args = args
    self.buffer = buffer
    # Create a TCP socket and allow reusing the address (useful when restarting a listener)
    self.socket = SocketUtility.create_tcp_socket()
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.run()

  def run(self):
    """Dispatch to either listen (server) or send (client) based on args."""
    if self.args.listen:
      self.listen()
    else:
      self.send()

  def send(self):
    """Client mode: connect to target, optionally send initial buffer, then receive/send in a loop."""
    print(f'[*] Connecting to {self.args.target}:{self.args.port}...')
    try:
      self.socket.connect((self.args.target, self.args.port))
      print(f'[*] Connected to {self.args.target}:{self.args.port}')
    except Exception as e:
      print(f'[!] Connection failed: {e}')
      sys.exit(1)
    
    if self.buffer:
      self.socket.send(self.buffer)
      print(f'[*] Sent {len(self.buffer)} bytes')

    try:
      while True:
        # Receive data from server
        data = self.socket.recv(4096)
        if not data:
          print('\n[*] Connection closed by server')
          break
        print(data.decode(), end='', flush=True)
    except KeyboardInterrupt:
      print("\nUser Terminated.")
      self.socket.close()
      sys.exit()
    except Exception as e:
      print(f"\nConnection error: {e}")
      self.socket.close()
      sys.exit()

  def listen(self):
    """Server mode: bind to 0.0.0.0:port (all interfaces), accept connections, and handle each in a thread."""
    self.socket.bind(('0.0.0.0', self.args.port))
    self.socket.listen(5)
    print(f'[*] Listening on 0.0.0.0:{self.args.port}')

    while True:
      client_socket, addr = self.socket.accept()
      print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
      # Handle each client in a separate thread so we can serve multiple connections
      client_thread = threading.Thread(
        target=self.handle,
        args=(client_socket,),
      )
      client_thread.start()

  def handle(self, client_socket):
    """
    Handle one client connection: either execute a command, receive an upload,
    or run an interactive command shell. Expects execute() to be in scope (e.g. from netcat_cmd).
    """
    try:
      if self.args.execute:
        # Run a single command and send its output back to the client
        print(f'[*] Executing command: {self.args.execute}')
        output = execute(self.args.execute)
        if output:
          client_socket.send(output.encode())
          print(f'[*] Sent {len(output)} bytes to client')
        else:
          print('[*] Command produced no output')
        client_socket.close()
        print('[*] Connection closed')
      elif self.args.upload:
        # Receive raw bytes until connection closes, then save to the specified file
        file_buffer = b''
        while True:
          data = client_socket.recv(4096)
          if data:
            file_buffer += data
          else:
            break
        with open(self.args.upload, 'wb') as f:
          f.write(file_buffer)
        message = f'Saved file {self.args.upload}'
        client_socket.send(message.encode())
        client_socket.close()
      elif self.args.command:
        # Interactive shell: prompt BHP: #> and run each line the client sends
        while True:
          try:
            client_socket.send(b'BHP: #> ')
            cmd_buff = b''
            while True:
              data = client_socket.recv(1)
              if not data:
                raise Exception("Connection closed")
              cmd_buff += data
              if data == b'\n':
                break
            cmd = cmd_buff.decode().strip()
            if cmd:
              response = execute(cmd)
              if response:
                client_socket.send(response.encode())
          except Exception as e:
            print(f'server killed {e}')
            client_socket.close()
            break
      else:
        # No specific mode, just echo back what we receive
        while True:
          data = client_socket.recv(4096)
          if not data:
            break
          client_socket.send(data)
        client_socket.close()
    except Exception as e:
      print(f'Error handling client: {e}')
      client_socket.close()