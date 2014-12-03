"""Osxbox network module:
Collects information about network traffic generated
during the process execution.

Copyright 2014, Jose Toro.
Licensed under MIT.
"""

import subprocess
import os
import socket

class NetworkReport(object):
  """ Network Report Generator.
  Attributes:
    outputFile: Location where the Network report is gonna to be written.
    tcp_out: Temporal file where tcpdump output will be located.
    monitor: The tcpdump process.
  """
  def __init__(self, output):
    """ Inits the report.
    Args:
      outputFile: Location where the Network report is gonna to be written.
    """
    self.output = output
    self.tcp_out = open('tcpdump.out', 'w')

    local_ip = socket.gethostbyname(socket.gethostname())
    self.monitor = subprocess.Popen(('tcpdump', '-nl', 'ip and src host ' + local_ip), stdout=self.tcp_out, stderr=subprocess.PIPE)

  def finish(self):
    """ Stops the network monitoring and closes the temporal file. """
    self.monitor.kill()
    self.tcp_out.close()

  def generate(self):
    """ Parses the tcpdump output to the report file (outputFile) """
    report = open('tcpdump.out', 'r')

    self.output.write("###########################\n")
    self.output.write("# Connections Established #\n")
    self.output.write("###########################\n")
    self.output.flush()

    p1 = subprocess.Popen(('cut', '-d', ' ', '-f5'), stdin=report, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('sed', 's/.$//'), stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen('sort', stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(('sed', 's/\./:/4'), stdin=p3.stdout, stdout=subprocess.PIPE)
    p5 = subprocess.Popen('uniq', stdin=p4.stdout, stdout=self.output)
    p5.wait()

    self.output.write('\n')
    report.close()

    # Delete temporal file
    os.remove('tcpdump.out')