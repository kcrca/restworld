from __future__ import annotations

from restworld.new_main import *


def test_unclocked_room():
    room = Room('dp:foo')
    room.loop('bar').loop(lambda var, i, item: Command().say('var %s, i %s, item %s' % (var, i, item)), range(0, 5))
    funcs = room.functions()
    func_names = sorted(list(x.name for x in funcs))
    assert sorted(func_names) == ['dp:foo/_cur', 'dp:foo/_decr', 'dp:foo/_enter', 'dp:foo/_exit', 'dp:foo/_finish',
                                  'dp:foo/_incr', 'dp:foo/_init', 'dp:foo/bar', 'dp:foo/bar_cur', 'dp:foo/bar_home']


def test_clocked_room():
    room = Room('dp:foo')
    clock = Clock('main')
    room.loop('bar', clock).loop(lambda var, i, item: Command().say('var %s, i %s, item %s' % (var, i, item)),
                                 range(0, 5))
    funcs = room.functions()
    func_names = sorted(list(x.name for x in funcs))
    assert sorted(func_names) == ['dp:foo/_cur', 'dp:foo/_decr', 'dp:foo/_enter', 'dp:foo/_exit', 'dp:foo/_finish',
                                  'dp:foo/_incr', 'dp:foo/_init', 'dp:foo/_main', 'dp:foo/_tick', 'dp:foo/bar',
                                  'dp:foo/bar_cur', 'dp:foo/bar_home']


def test_mob_placer():
    mp = MobPlacer(1.1, 12, 2.2, 'North', 3.3, 4.4, ('gtag',))
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
