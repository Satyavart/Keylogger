#!usr/bin/env python
import tempfile


def Path():
    temp_dir = tempfile.gettempdir()
    temp_dir = temp_dir + "/log/"
    return temp_dir