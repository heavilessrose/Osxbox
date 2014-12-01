#!/usr/bin/env python

"""Osxbox main module:
Initializes the target and dtrace process, synchronizes the
dtrace and parser processes and waits for the process to finish
or terminates it if the time limit is reached.

Finally, signals the parser process for generate the report.

Copyright 2014, Jose Toro.
Licensed under MIT.
"""

import sys
import os
import subprocess
import time
import signal
import pwd
import shlex

def main():
  """Main script of Osxbox."""

  # Check for superuser privileges, conf file & args.
  if not os.geteuid() == 0:
    sys.exit('Osxbox must be run as root')

  if not os.path.isfile('osxbox.conf'):
    sys.exit('You must run \'./configure.py\' before run Osxbox')

  if len(sys.argv) != 2:
    print 'usage: sudo ./main.py <process>'
    sys.exit(-1)

  # Time limit (in seconds) for the process to end.
  time_limit = 5

  # Get target username from conf file.
  f = open('osxbox.conf', 'r')
  user = f.readline()
  f.close()

  out = open('output.txt', 'w')
  err = open('error.txt', 'w')

  # Run dtrace and wait for initializate.
  dtrace = subprocess.Popen(["/usr/sbin/dtrace", "-q", "-s", "script.d"], stdout=subprocess.PIPE)
  time.sleep(2)

  # Run process as normal user.
  user_uid = pwd.getpwnam(user).pw_uid
  process = subprocess.Popen(shlex.split(sys.argv[1]),
                             preexec_fn=change_user(user_uid),
                             stdout=out, stderr=err)

  # Run dtrace parser.
  parser = subprocess.Popen(["/usr/bin/python", "parser.py",
                            str(process.pid)], stdin=dtrace.stdout)

  # Wait to the process to end or to the time limit reach.
  time_elapsed = 0
  while process.poll() is None and time_elapsed < time_limit:
    time.sleep(1)
    time_elapsed += 1

  # Kill process if still alive.
  if process.poll() is None:
    process.terminate()

  # Close output and error files.
  out.close()
  err.close()

  # Terminate dtrace.
  dtrace.terminate()

  # Signal to parser, generate report.
  parser.send_signal(signal.SIGUSR1)


def change_user(user_uid):
  """Callback for Popen preexec_fn to change user uid.

  Args:
    user_uid: The new user uid.
  """
  def result():
    os.setuid(user_uid)
  return result


if __name__ == '__main__':
    main()