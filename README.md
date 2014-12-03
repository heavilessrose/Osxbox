# Osxbox: Apple OS X Sandbox

> Osxbox is an open-source sandbox for OS X, providing a tool for see what a program "is doing" in a friendly way.
> 

## Features
Osxbox currently reports (more features incoming):
  - Files opened
  - Processes created
  - Network connections

## Setup
```sh
git clone https://github.com/wynkth/Osxbox.git
cd Osxbox
./ob_configure.py
```
## Usage
```sh
sudo ./osxbox.py <command>
```

## Example
```sh
sudo ./osxbox.py 'python examples/t.py'
```
Stdout and stderr of the process will be saved in the output.txt and error.txt, respectively.
### Example output
```
===============
 Osxbox report
===============

###########################
# Connections Established #
###########################
173.194.41.56:443
173.194.41.56:80

####################
# Processes opened #
####################
2244: test

################
# Files opened #
################
/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/Python
/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/time.so
/Users/<User>/.CFUserTextEncoding
/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/fcntl.so
/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/_struct.so
test.txt
/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/cStringIO.so
/dev/autofs_nowait
/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/select.so
/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/binascii.so
```

## License
Copyright (c) 2014, Jose Toro. MIT License.
