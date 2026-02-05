"""
SocketUtility: Factory for creating IPv4 TCP and UDP sockets.
Used by NetCat and other utilities that need a consistent socket API.
"""

import socket


class SocketUtility:
  """Provides static helpers to create IPv4 TCP or UDP sockets."""

  # IPv4 address family
  internet_protocol = socket.AF_INET
  # Stream socket = TCP (reliable, ordered)
  TCP_Protocol = socket.SOCK_STREAM
  # Datagram socket = UDP (unreliable, no guarantee of order)
  UDP_Protocol = socket.SOCK_DGRAM

  @staticmethod
  def create_tcp_socket():
    """Create and return a new TCP (stream) socket."""
    return SocketUtility.create_internet_socket(SocketUtility.TCP_Protocol)

  @staticmethod
  def create_udp_socket():
    """Create and return a new UDP (datagram) socket."""
    return SocketUtility.create_internet_socket(SocketUtility.UDP_Protocol)

  @staticmethod
  def create_internet_socket(msg_protocol):
    """Create an IPv4 socket with the given protocol (SOCK_STREAM or SOCK_DGRAM)."""
    return socket.socket(SocketUtility.internet_protocol, msg_protocol) 