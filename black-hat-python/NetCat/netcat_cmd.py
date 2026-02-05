"""
NetCat CLI: Command-line entry point for the BHP NetCat tool.
Parses arguments, defines execute() for remote command runs, and starts NetCat.
"""

import argparse
import shlex
import subprocess
import sys
import os
import textwrap

# Add parent directory to path so we can import Utilities and NetCat
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from NetCat import netcat
from NetCat.netcat import NetCat

def _execute(cmd):
  """Run a shell command and return its stdout (and stderr) as a string."""
  cmd = cmd.strip()
  if not cmd:
    return
  output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
  return output.decode()


# Provide execute to the netcat module so handle() can run remote commands
netcat.execute = _execute


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='BHP NET TOOL',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent(''' Examples:
      netcat.py -t 192.168.1.108 -p 5555 -l  -c #command shell
      netcat.py -t 192.168.1.108 -p 5555 -l  -u mytest.text #upload to file
      netcat.py -t 192.168.1.108 -p 5555 -l  -e="cat /etc/pwd" #execute cmd
      echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 #echo text to server port 135
      netcat.py -t 192.168.1.108 -p 5555 #connect to server
    ''')
  )

  parser.add_argument('-c', '--command', action='store_true', help='command shell')
  parser.add_argument('-e', '--execute', help='execute specific cmd')
  parser.add_argument('-l', '--listen', action='store_true', help='listen')
  parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
  parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
  parser.add_argument('-u', '--upload', help='upload file')

  args = parser.parse_args()

  # In listen mode we don't send initial data; in client mode we can pipe stdin
  if args.listen:
    buffer = ''
  else:
    buffer = sys.stdin.read()

  nc = NetCat(args, buffer.encode())
  nc.run()