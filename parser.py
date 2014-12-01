"""Osxbox parser module:
Collects and parses the traces from dtrace
while the process is running and finalizes with
a Osxbox report when the process end.

Copyright 2014, Jose Toro.
Licensed under MIT.
"""

import sys
import signal
from report import Report

REPORT = Report()

def handler(signum, frame):
  """Signal handler

  Used by the process to stop parsing the input,
  print the report and exit.

  Args are not relevant.
  """
  REPORT.report()
  sys.exit(0)

def main():
  # Add the process PID to the report.
  REPORT.add_pid(int(sys.argv[1]))

  # Register SIGUSR1 handler with the function.
  signal.signal(signal.SIGUSR1, handler)

  # Collect info from dtrace.
  while True:
    pid = sys.stdin.readline().strip()
    type = sys.stdin.readline().strip()
    op = sys.stdin.readline().strip() # Not used yet.

    if type == 'FILE':
      file = sys.stdin.readline().strip()
      REPORT.file_opened(int(pid), file)
    elif type == 'PROCESS':
      name = sys.stdin.readline().strip()
      child = sys.stdin.readline().strip()
      REPORT.new_process(int(pid), int(child), name)

if __name__ == '__main__':
  main()
