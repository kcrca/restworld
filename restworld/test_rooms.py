from __future__ import annotations

from pynecraft.__init__ import NORTH, d
from pynecraft.commands import item, lines
from restworld.rooms import *


def test_unclocked_room():
    room = Room('foo', RoomPack('dp'), NORTH, 'foo', )
    room.loop('bar').loop(lambda step: say(f'var {step.loop.score}, i {step.i}, item {item}'), range(0, 5))
    room.add_room_funcs()
    func_names = sorted(list(x.name for x in room.functions))
    assert func_names == ['_cur', '_decr', '_enter', '_exit', '_finish', '_incr', '_init', 'bar', 'bar_cur', 'bar_home',
                          'foo_room_home', 'foo_room_init']

    room.add(Function('bar_finish_main'))
    room.add(Function('xyzzy'))
    room.add_room_funcs()
    func_names = sorted(list(x.name for x in room.functions))
    assert func_names == ['_cur', '_decr', '_enter', '_exit', '_finish', '_incr', '_init', 'bar', 'bar_cur',
                          'bar_finish_main', 'bar_home', 'foo_room_home', 'foo_room_init', 'xyzzy']


def test_clocked_room():
    room = Room('foo', RoomPack('dp'), NORTH, 'foo', )
    clock = Clock('main')
    room.loop('bar', clock).loop(lambda step: say(f'var {step.loop.score}, i {step.i}, item {item}'),
                                 range(0, 5))
    room.add_room_funcs()
    func_names = sorted(list(x.name for x in room.functions))
    assert func_names == ['_cur', '_decr', '_enter', '_exit', '_finish', '_incr', '_init', '_main', '_tick', 'bar',
                          'bar_cur', 'bar_home', 'foo_room_home', 'foo_room_init']

    room.add(Function('bar_finish_main'))
    room.add(Function('xyzzy'))
    room.add_room_funcs()
    func_names = sorted(list(x.name for x in room.functions))
    assert func_names == ['_cur', '_decr', '_enter', '_exit', '_finish', '_finish_main', '_incr', '_init', '_main',
                          '_tick', 'bar', 'bar_cur', 'bar_finish_main', 'bar_home', 'foo_room_home', 'foo_room_init',
                          'xyzzy']


def test_room_sign():
    room = Room('foo', RoomPack('dp'), NORTH, 'foo', )
    room.add_room_funcs()
    func_names = sorted(list(x.name for x in room.functions))
    assert func_names == ['_enter', '_exit', '_finish', '_init', 'foo_room_home', 'foo_room_init']


def test_mob_placer():
    mp = MobPlacer((1.1, 12, 2.2), 'North', 3.3, 4.4)
    cmds = lines(mp.summon(((Entity('m_1')), (Entity('m_2')))))
    assert cmds[0].startswith('summon m_1 1.1 12 2.2 {')
    assert cmds[1].startswith('summon m_1 1.1 12 -2.2 {')
    assert cmds[2].startswith('summon m_2 4.4 12 2.2 {')
    assert cmds[3].startswith('summon m_2 4.4 12 -2.2 {')
    assert 'adult' in cmds[0]
    assert 'adult' in cmds[2]
    assert 'kid' in cmds[1]
    assert 'kid' in cmds[3]
    assert 'NoAI' in cmds[0]
    assert 'NoAI' in cmds[1]
    assert 'NoAI' in cmds[2]
    assert 'NoAI' in cmds[3]
    assert re.search(r'Tags:.*m_1', cmds[0])
    assert re.search(r'Tags:.*m_1', cmds[1])

    mp = MobPlacer(r(1.1, 12, 2.2), 'North', 3.3, 4.4, tags=('gtag',), nbt={'GProp': True})
    cmds = lines(mp.summon(((Entity('m_1')), (Entity('m_2')))))
    for c in cmds:
        assert c.count('~') == 3, c
    assert 'gtag' in cmds[0]
    assert 'GProp: true' in cmds[0]

    mp = MobPlacer(d(1.1, 12, 2.2), 'North', 3.3, 4.4, auto_tag=False)
    cmds = lines(mp.summon(((Entity('m_1')), (Entity('m_2')))))
    assert cmds[0].count('^') == 3
    assert cmds[1].count('^') == 3
    assert cmds[2].count('^') == 3
    assert cmds[3].count('^') == 3
    assert not re.search(r'Tags:.*m_1', cmds[0])
    assert not re.search(r'Tags:.*m_1', cmds[1])
    assert not re.search(r'Tags:.*m_2', cmds[2])
    assert not re.search(r'Tags:.*m_2', cmds[3])

    mp = MobPlacer((1.1, 12, 2.2), 'North', 3.3, 4.4)
    cmds = lines(mp.summon(((Entity('m_1')), (Entity('m_2'))), on_stand=True))
    assert cmds[0].startswith('summon armor_stand 1.1 12 2.2 {')
    assert cmds[1].startswith('summon armor_stand 1.1 12 -2.2 {')
    assert cmds[2].startswith('summon armor_stand 4.4 12 2.2 {')
    assert cmds[3].startswith('summon armor_stand 4.4 12 -2.2 {')
    assert cmds[0].count('adult') == 2
    assert cmds[1].count('kid') == 2
    assert cmds[2].count('adult') == 2
    assert cmds[3].count('kid') == 2


def test_say_score():
    say = say_score(Score('a', 'b'), ('c', 'd'))
    assert say == (('tellraw @a [{"text": "scores:"}, {"text": "a="}, {"score": {"name": "a", '
                    '"objective": "b"}}, {"text": "c="}, {"score": {"name": "c", "objective": '
                    '"d"}}]'))
