"""Osxbox report module:
Classes:
  Report: Includes the necesary information to build the Osxbox report.

Copyright 2014, Jose Toro.
Licensed under MIT.
"""

class Report:
  """Osxbox report class.

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

  def __init__(self, initial_pid):
    self.pids = set()
    self.processes = set()
    self.files_opened = set()
    self.f_whitelist = set()

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

    print '===============\n' \
          ' Osxbox report\n'  \
          '===============\n'

    if self.processes:
      print '####################'
      print '# Processes opened #'
      print '####################'
      for (pid, name) in self.processes:
        print str(pid) + ': ' + name
      print ''

    if self.file_opened:
      print '################'
      print '# Files opened #'
      print '################'
      for (pid, file) in self.files_opened:
        if pid in self.pids: print file
      print ''
