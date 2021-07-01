import uuid
import os

def print_attributes(s):
    attrs = vars(s)
    for item in attrs.items():
        if not item[0].startswith('__'):
            print("%s: %s" % item )

def get_a_uuid():
    temp = uuid.uuid4().hex
    return temp

def make_dirs(ls_paths):
    for path in ls_paths:
        if not os.path.exists(path):
            os.makedirs(path)