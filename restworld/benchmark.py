#!/usr/bin/env python3
import random
import sys

a_cnts = []
m = 0
for a in range(10):
    cnts = {}
    for i in range(0, 100000):
        cnt = int(random.betavariate(a / 10.0 + 0.1, 5.0) * 4)
        cnts.setdefault(cnt, 0)
        cnts[cnt] += 1
        m = max(m, cnt)
    a_cnts.append(cnts)

for a in range(10):
    print(f'\t{(a / 10 + 0.1):5.2}', end='')
print('')
preferred = []
prev = 0
for v in range(m):
    print(f'{v}', end='')
    for a in range(10):
        print(f'\t{a_cnts[a][v]:5}', end='')
        if a == 9:
            c = a_cnts[a][v]
            preferred.append(c + prev)
            prev += c
    print('')

print(preferred)

sys.exit(0)

func = sys.argv[1]
cmd = ' '.join(sys.argv[2:])

loc = Path.home() / Path('clarity/home/saves/Benchmarks')
try:
    pack = DataPack.load(loc, 'minecraft')
except FileNotFoundError:
    pack = DataPack('minecraft')

funcs = pack.functions
f = funcs[func] = Function(func)
#     echo execute store result storage times start long 1 run time query gametime
# f.add(execute().store(RESULT).storage('times', 'start', LONG).run(time().query(GAMETIME)))
for i in range(0, 10000):
    f.add(cmd)
# elapsed = Score('elapsed', 'main')
# start = Score('start', 'main')
f.add(
    # execute().store(RESULT).storage('times', 'end', LONG).run(time().query(GAMETIME)),
    # scoreboard().objectives().add(elapsed.objective, DUMMY),
    # execute().store(RESULT).score(elapsed).run(data().get('times', 'end')),
    # execute().store(RESULT).score(start).run(data().get('times', 'start')),
    # elapsed.operation(MINUS, start),
    # tellraw(a(), 'Elapsed: ', JsonText.score(elapsed))
)

pack.save(loc)
