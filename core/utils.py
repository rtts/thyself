import re
from settings import uris

id_re = re.compile('<id>')

def reverse(name, *args):
    if name in uris:
        if '<id>' in uris[name]['path']:
            return id_re.sub(args[0], uris[name]['path'])
        return uris[name]['path']
    raise ValueError