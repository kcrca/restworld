import re
import csv

with open("blocks.txt") as fp:
    blocks = tuple(x.replace('_', ' ').rstrip() for x in fp.readlines())

categories = (
    r'\bblock( of)?\b', r'\bstairs\b', r'\bwall\b|\bfence$', r'\b(fence )?gate\b', r'\bslab\b', r'\bpillar\b')
category_names = tuple(re.sub(r'\\.|[$?]|\(.*\)|\|.*', '', c) for c in categories)

found = {}
for i in range(0, len(categories)):
    c = categories[i]
    cpat = re.compile(r'\s*%s\s*' % c)
    for b in blocks:
        if cpat.search(b):
            base = cpat.sub(' ', b).strip()
            if base not in found:
                found[base] = []
            found[base].append(category_names[i])

with open('blocks.csv', 'w', newline='') as out:
    w = csv.writer(out)
    w.writerow(category_names[1:] + ('block',))
    for b in sorted(found):
        cats = found[b]
        if cats == ['block'] or b == '':
            continue
        w.writerow(tuple('x' if c in cats else '' for c in category_names[1:]) + (b,))
