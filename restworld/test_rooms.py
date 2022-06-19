from __future__ import annotations

from restworld.rooms import *
from restworld.world import Restworld


def test_unclocked_room():
    room = Room('foo', DataPack('dp', 'none'), NORTH, ('foo'), )
    room.loop('bar').loop(lambda step: mc.say('var %s, i %s, item %s' % (step.loop.score, step.i, item)), range(0, 5))
    func_names = sorted(list(x.name for x in (room.room_funcs())))
    assert func_names == ['_cur', '_decr', '_enter', '_exit', '_finish', '_incr', '_init', 'bar', 'bar_cur', 'bar_home',
                          'foo_room_home', 'foo_room_init']

    room.add(Function('bar_finish_main'))
    room.add(Function('xyzzy'))
    func_names = sorted(list(x.name for x in (room.room_funcs())))
    assert func_names == ['_cur', '_decr', '_enter', '_exit', '_finish', '_incr', '_init', 'bar', 'bar_cur',
                          'bar_finish_main', 'bar_home', 'foo_room_home', 'foo_room_init', 'xyzzy']


def test_clocked_room():
    room = Room('foo', DataPack('dp', 'none'), NORTH, ('foo'), )
    clock = Clock('main')
    room.loop('bar', clock).loop(lambda step: mc.say('var %s, i %s, item %s' % (step.loop.score, step.i, item)),
                                 range(0, 5))
    func_names = sorted(list(x.name for x in (room.room_funcs())))
    assert func_names == ['_cur', '_decr', '_enter', '_exit', '_finish', '_incr', '_init', '_main', '_tick', 'bar',
                          'bar_cur', 'bar_home', 'foo_room_home', 'foo_room_init']

    room.add(Function('bar_finish_main'))
    room.add(Function('xyzzy'))
    func_names = sorted(list(x.name for x in (room.room_funcs())))
    assert func_names == ['_cur', '_decr', '_enter', '_exit', '_finish', '_finish_main', '_incr', '_init', '_main',
                          '_tick', 'bar', 'bar_cur', 'bar_finish_main', 'bar_home', 'foo_room_home', 'foo_room_init',
                          'xyzzy']


def test_room_sign():
    room = Room('foo', DataPack('dp', 'none'), NORTH, ('foo'), )
    func_names = sorted(list(x.name for x in (room.room_funcs())))
    assert func_names == ['_enter', '_exit', '_finish', '_init', 'foo_room_home', 'foo_room_init']


def test_mob_placer():
    mp = MobPlacer(1.1, 12, 2.2, 'North', 3.3, 4.4)
    cmds = lines(mp.summon(((Entity('m_1')), (Entity('m_2')))))
    assert cmds[0].startswith('summon m_1 1.1 12 2.2 {')
    assert cmds[1].startswith('summon m_1 5.5 12 2.2 {')
    assert cmds[2].startswith('summon m_2 1.1 12 -1.1 {')
    assert cmds[3].startswith('summon m_2 5.5 12 -1.1 {')
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

    mp = MobPlacer(r(1.1), r(12), r(2.2), 'North', 3.3, 4.4, tags=('gtag',), nbt={'GProp': True})
    cmds = lines(mp.summon(((Entity('m_1')), (Entity('m_2')))))
    for c in cmds:
        assert c.count('~') == 3, c
    assert 'gtag' in cmds[0]
    assert 'GProp: true' in cmds[0]

    mp = MobPlacer(d(1.1), d(12), d(2.2), 'North', 3.3, 4.4, auto_tag=False)
    cmds = lines(mp.summon(((Entity('m_1')), (Entity('m_2')))))
    assert cmds[0].count('^') == 3
    assert cmds[1].count('^') == 3
    assert cmds[2].count('^') == 3
    assert cmds[3].count('^') == 3
    assert not re.search(r'Tags:.*m_1', cmds[0])
    assert not re.search(r'Tags:.*m_1', cmds[1])
    assert not re.search(r'Tags:.*m_2', cmds[2])
    assert not re.search(r'Tags:.*m_2', cmds[3])

    mp = MobPlacer(1.1, 12, 2.2, 'North', 3.3, 4.4)
    cmds = lines(mp.summon(((Entity('m_1')), (Entity('m_2'))), on_stand=True))
    assert cmds[0].startswith('summon armor_stand 1.1 12 2.2 {')
    assert cmds[1].startswith('summon armor_stand 5.5 12 2.2 {')
    assert cmds[2].startswith('summon armor_stand 1.1 12 -1.1 {')
    assert cmds[3].startswith('summon armor_stand 5.5 12 -1.1 {')
    assert cmds[0].count('adult') == 2
    assert cmds[1].count('kid') == 2
    assert cmds[2].count('adult') == 2
    assert cmds[3].count('kid') == 2


def test_crops():
    cmds = crops(15, list(range(0, 4)) + [3, 3], 'beets', 0, 3, 0)
    assert cmds == ['fill ~0 ~3 ~0 ~2 ~3 ~0 beets[age=3]',
                    'fill ~0 ~3 ~-1 ~2 ~3 ~-1 beets[age=3]',
                    'fill ~0 ~3 ~-2 ~2 ~3 ~-2 beets[age=3]',
                    'data merge block ~3 ~2 ~-1 {Text2: "\\"Stage: 3\\""}']


def test_say_score():
    say = say_score(Score('a', 'b'), ('c', 'd'))
    assert say == ('tellraw @a [{"text": "\\"scores:\\""}, {"text": "\\"a=\\""}, {"score": '
                   '{"name": "\\"a\\"", "objective": "\\"b\\""}}, {"text": "\\"c=\\""}, '
                   '{"score": {"name": "\\"c\\"", "objective": "\\"d\\""}}]')


def test_control_book():
    restworld = Restworld('none')
    restworld.function_set.add(Room('r1', restworld, NORTH, ('Howdy')))
    restworld.function_set.add(Room('r2', restworld, NORTH, ('Doody')))
    assert re.search(r'Doody.*Howdy', str(restworld.control_book_func()))
