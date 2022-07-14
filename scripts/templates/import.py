#!/usr/bin/python3
import re
import sys
from pathlib import Path

from pynecraft.commands import Command


def entity(m):
    base = {'e': 'entity', 's': 'self', 'p': 'player', 'r': 'random', 'a': 'all'}[m.group(1)]
    out = '%s()' % base
    spec = m.group(2)
    if spec:
        specs = spec.split(',')
        for s in specs:
            func, param = s.split('=')
            if '..' in param:
                start, end = param.split('..')
                if not start:
                    start = None
                if not end:
                    end = None
                param = '(%s, %s)' % (start, end)
            if param[0].isalpha():
                param = "'%s'" % param
            out += ".%s(%s)" % (func, param)
    return out


def coord(p, *n):
    params = ', '.join(n)
    if p == '~':
        return 'r(%s)' % params
    elif p == '^':
        return 'd(%s)' % params
    elif p == '':
        return params
    else:
        raise ValueError('"%s": Illegal prefix' % p)


def coords(m):
    g = tuple(x.strip() for x in m.groups())
    if g[0] != g[2] or g[0] != g[4] or g[2] != g[4]:
        return '(' + coord(g[0], g[1]) + ', ' + coord(g[2], g[3]) + ',' + coord(g[4], g[5]) + '), '
    return coord(g[0], g[1], g[3], g[5]) + ', '


def particle(m):
    return 'particle(Particle.' + m.group(1).upper()


def convert_path(f, py):
    fname = f.stem
    is_loop = has_loop(f)
    m = re.match(r'^(\w+)_(fast|main|slow)$', fname)
    if m:
        print("    room.loop('%s', %s_clock).loop(" % (m.group(1), m.group(2)), file=py)
    elif is_loop:
        print("    room.loop('%s').loop(" % fname, file=py)
    else:
        print("    room.function('%s').add(" % fname, file=py)
    with open(f) as inf:
        convert(inf, py)
    print(")", file=py)


def has_loop(f):
    with open(f) as fp:
        return '<%base:loop' in fp.read()


def mapping(m):
    return ("'%s': " % m.group(1)) + str(value(m.group(2)))


def value(v):
    m = re.match(r'(\d*)\.\.(\d*)', v)
    if m:
        return (int(m.group(1)) if m.group(1) else None, int(m.group(2)) if m.group(2) else None)
    try:
        return int(v)
    except:
        pass
    try:
        return float(v)
    except:
        pass
    if v in ('north', 'east', 'west', 'south'):
        return v.upper()
    if v[0] in '\'"':
        return v
    return "'%s'" % v


def quote_key(m):
    if m.group(1) in ('restworld', 'minecraft'):
        return m.group(0)
    return "'%s': " % m.group(1)


def invoke(m):
    if m.group(1) in dir(Command):
        return 'mc.%s' % m.group(0)
    return m.group(0)


def clock_invoke(m):
    return '%s.%s' % (m.group(1).replace('_clock',''), '%s' % m.group(2) if m.group(2) in dir(Command) else m.group(2))


def convert(inf, outf):
    for line in inf:
        if '%namespace' in line:
            continue
        out = line
        out = out.replace(' ~ ', ' ~0 ')
        out = re.sub(r'@(.)(?:\[([^]]*)])?', entity, out)
        out = re.sub(r'^..when.i.. ', 'yield ', out)
        out = re.sub(r'([~^])([^~^]*) ([~^])?([^~^]*) ([~^])?([^~^a-z]*)', coords, out)
        out = re.sub(r'\btrue\b', 'True', out)
        out = re.sub(r'\bfalse\b', 'False', out)
        out = re.sub(r'\${([^}]*)}', r'\1', out)
        out = re.sub(r'^([a-z]+) ', invoke, out)
        out = re.sub(r'\bparticle ([^ ]*)', particle, out)
        out = re.sub(r'\b"?(restworld:)"?([\w/]+)"?', r"'\1\2'", out)
        if out[0] != '<':
            out = re.sub('(\w+)=([^],]+)', mapping, out)
            out = re.sub('(\w+):', quote_key, out)
        out = re.sub(r'<%base:loop collection="(.*?)}?".*', r'collection=\1', out)
        out = re.sub(r'</%base:loop.*', '', out)
        out = re.sub(r'\\$', '', out)
        out = out.replace('##', '#')
        out = re.sub(r'\[', ' {', out)
        out = re.sub(r']', ' }', out)
        out = re.sub(r'((?:fast|main|slow)_clock\(\)) ([a-z]+)', clock_invoke, out)
        out = re.sub(r'<%\s*', '', out)
        out = re.sub(r'\s*%>', '', out)
        out = re.sub(r'\bThing\b', 'Block', out)
        out = out.replace('"', "'")
        out  = out.replace('base.remove', 'kill_em')
        out = out.replace(r'base\.', '')
        print(out, file=outf, end='')


if len(sys.argv) > 1:
    for p in sys.argv[1:]:
        p = Path(p)
        if p.is_dir:
            with open(p.stem + '.py', 'w') as py:
                for f in sorted(p.glob('*.mcftmpl')):
                    if not  f.stem.endswith('_base'):
                        convert_path(f, py)
        else:
            convert_path(p, sys.stdout)
else:
    convert(sys.stdin, sys.stdout)
##!/bin/zsh
# perl -pe 's/[@]e/entity()/g' | \
# perl -pe 's/[@]p/player()/g' | \
# perl -pe 's/[@]s/self()/g' | \
# perl -pe 's/\\(\\)\[/()/g' | \
# perl -pe 's/[[,]*(\w+)=(!?\w+)]*/.$1($2)/g' | \
# perl -pe 's/(\w+):/"$1":/g' | \
# perl -pe 's/\btrue\b/True/g' | \
# perl -pe 's/\bfalse\b/False/g' | \
# perl -pe 's/^..when.i.. /yield /' | \
# perl -pe 's/^%([a-z])/$1/' | \
# perl -pe 's/\${([^}]*)}/$1./' | \
# perl -pe 's/particle ([^ ]*)/particle(Particle.$1)/'
