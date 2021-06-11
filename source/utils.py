import uuid

def print_attributes(s):
    attrs = vars(s)
    for item in attrs.items():
        if not item[0].startswith('__'):
            print("%s: %s" % item )

def get_a_uuid():
    temp = uuid.uuid4().hex
    return temp