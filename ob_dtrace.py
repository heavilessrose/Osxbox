"""Osxbox dtrace module:
Collects and parses the traces from dtrace
while the process is running and finalizes with
a report when the process end.

Classes:
  Report: Includes the necesary information to build the Osxbox report.

Copyright 2014, Jose Toro.
Licensed under MIT.
"""

import sys
import signal

class Report(object):
  """Dtrace report class.

  Attributes:
    pids: Set of target pids, for avoid other pid's actions in the report.
    processes: Set of tuples with the pid and name of process created.
    files_opened: Set of filenames opened.
    f_whitelist: Set of filenames that are omitted in the report.

  Methods:
    new_process: Adds a new process created to the report.
    file_opened: Adds a new file opened to the report.
    report: Generate and prints the report.
  """

  def __init__(self, initial_pid, output=sys.stdout):
    self.pids = set()
    self.processes = set()
    self.files_opened = set()
    self.f_whitelist = set()
    self.output = output

    # Load file whitelist
    whitelist = open('f_whitelist', 'r')
    for line in whitelist:
      self.f_whitelist.add(line.strip())
    whitelist.close()

    self.pids.add(initial_pid)

  def new_process(self, pid, child, name):
    """Adds a new process created to the report.

    Checks if the parent process is in the pids set,
    if it is, adds the pid of the child process to the pids set
    and the pid with its name to the processes set.

    Args:
      pid: PID of the parent process.
      child: PID of the child process.
      name: name of the child process.
    """
    if pid in self.pids:
      self.processes.add((child, name))
      self.pids.add(child)

  def file_opened(self, pid, file):
    """Adds a new file opened to the report.

    All files are saved, check is performed at the generation
    of the report, the reason of this is that files can arrive
    with a pid that isn't beed notified yet as a new process in dtrace,
    this can lead to lost files that should appear in the report.

    Args:
      pid: PID of the parent process.
      file: filename to add.
    """
    if file not in self.f_whitelist:
      self.files_opened.add((pid, file))

  def report(self):
    """Prints the report."""

    # Filter target pids
    self.files_opened = filter(lambda (x,y): x in self.pids, self.files_opened)

    if len(self.processes) != 0:
      self.output.write('####################' + '\n')
      self.output.write('# Processes opened #' + '\n')
      self.output.write('####################' + '\n')
      for (pid, name) in self.processes:
        self.output.write(str(pid) + ': ' + name + '\n')
      self.output.write('\n')

    if len(self.files_opened) != 0:
      self.output.write('################' + '\n')
      self.output.write('# Files opened #' + '\n')
      self.output.write('################' + '\n')
      for (pid, file) in self.files_opened:
        if pid in self.pids: self.output.write(file + '\n')
      self.output.write('\n')

def main():
  def handler(signum, frame):
    """Signal handler

    Used by the process to stop parsing the input,
    print the report and exit.

    Args are not relevant.
    """
    dtrace_report.report()
    sys.exit(0)

  # Add the process PID to the report.
  dtrace_report = Report(int(sys.argv[1]))

  # Register SIGUSR1 handler with the function.
  signal.signal(signal.SIGUSR1, handler)

  # Collect info from dtrace.
  while True:
    pid = sys.stdin.readline().strip()
    type = sys.stdin.readline().strip()
    op = sys.stdin.readline().strip() # Not used yet.

    if type == 'FILE':
      file = sys.stdin.readline().strip()
      dtrace_report.file_opened(int(pid), file)
    elif type == 'PROCESS':
      name = sys.stdin.readline().strip()
      child = sys.stdin.readline().strip()
      dtrace_report.new_process(int(pid), int(child), name)

if __name__ == '__main__':
  main()
