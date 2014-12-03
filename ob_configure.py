#!/usr/bin/env python

"""Osxbox configuration module:
Setups the environment for Osxbox to work properly.

Copyright 2014, Jose Toro.
Licensed under MIT.
"""

import sys
import os
import getpass

def main():
  # Check if normal user
  if os.geteuid() == 0:
    sys.exit('Script must be run as your current user')

  f = open('osxbox.conf', 'w')
  f.write(getpass.getuser())
  f.close()

  print 'Done!'

if __name__ == '__main__':
    main()