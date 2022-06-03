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
