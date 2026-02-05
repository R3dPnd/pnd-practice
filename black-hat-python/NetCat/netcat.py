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
    self.socket.connect((self.args.target, self.args.port))
    if self.buffer:
      self.socket.send(self.buffer)

    try:
      while True:
        recv_len = 1
        resp = ""

        # Keep reading until we get a full response (or less than 4096 bytes)
        while recv_len:
          data = self.socket.recv(4096)
          recv_len = len(data)
          resp += data.decode()
          if recv_len < 4096:
            break
          if resp:
            print(resp)
            buffer = "> "
            buffer += "\n"
            self.socket.send(buffer.encode())
    except KeyboardInterrupt:
      print("User Terminated.")
      self.socket.close()
      sys.exit()

  def listen(self):
    """Server mode: bind to target:port, accept connections, and handle each in a thread."""
    self.socket.bind((self.args.target, self.args.port))
    self.socket.listen(5)

    while True:
      client_socket, _ = self.socket.accept()
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
    if self.args.execute:
      # Run a single command and send its output back to the client
      output = execute(self.args.execute)
      client_socket.send(output.encode())
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
    elif self.args.command:
      # Interactive shell: prompt BHP: #> and run each line the client sends
      cmd_buff = b''
      while True:
        try:
          client_socket.send(b'BHP: #> ')
          while '\n' not in cmd_buff.decode():
            # Read more input (implementation would need to recv into cmd_buff here)
            response = execute(cmd_buff.decode())
            if response:
              client_socket.send(response.encode())
            cmd_buff = b''
        except Exception as e:
          print(f'server killed {e}')
          self.socket.close()
          sys.exit()