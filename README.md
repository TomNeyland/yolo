# yolo
Yolo, sorry.


Command line usage
--------
```shell
# install after cloning the repo (since this is no on pypy yet)
pip install -e . -U

# run yolo on some files
yolo myfile.py yolo/yolo.py

# ask yolo for help
yolo --help

# usage: yolo [-h] [-c CONFIG] [--repo REPO] sourcefiles [sourcefiles ...]

# Args that start with '--' (eg. --repo) can also be set in a config file
# (./.yolorc or specified via -c). The recognized syntax for setting (key,
# value) pairs is based on the INI and YAML formats (e.g. key=value or
# foo=TRUE). For full documentation of the differences from the standards please
# refer to the ConfigArgParse documentation. If an arg is specified in more than
# one place, then commandline values override environment variables which
# override config file values which override defaults.

# positional arguments:
#   sourcefiles           the sourcefile(s) to run yolo on

# optional arguments:
#   -h, --help            show this help message and exit
#   -c CONFIG, --config CONFIG
#                         config file path [env var: YOLO_CONFIG]
#   --repo REPO           the git repo running yolo on
```

Python usage
--------
```python
from yolo import yolo, yolo_file

# run yolo on a string
my_source_code = 'pretend this is some python code'
yolo_result = yolo(my_source_code)

# run yolo on a file
yolo_result = yolo_file('something.py')
```