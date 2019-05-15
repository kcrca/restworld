thing = 'foo[bar=yes]'
import re

def cleanup(value):
    if value is None:
        value = ''
    s = value.replace('_', ' ').replace('=', ' ').replace(' true', '')
    if ' false' in s:
        s = 'No ' + s.replace(' false', '')
    return s.title()

m = re.search(r'([^[]*)(?:\[([^],]*)(?:,([^]]*)\])?)?', thing)
name, attr1, attr2 = m.groups()
if m:
    attr1 = cleanup(m.groups()[1])
    attr2 = cleanup(m.groups()[1])