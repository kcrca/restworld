from restworld.function import *


def test_lines():
    assert (list(lines())) == []
    assert (list(lines('a'))) == ['a']
    assert (list(lines('a\n'))) == ['a', '']
    assert (list(lines('a\nb'))) == ['a', 'b']
    assert (list(lines((), 'a'))) == ['a']
    assert (list(lines(('a', 'b'), 'c'))) == ['a', 'b', 'c']
    assert (list(lines(([['a', 'b']]), 'c'))) == ['a', 'b', 'c']


def test_loop():
    def simple_loop(var, i, item):
        return '%s[%d] = %s' % (var, i, str(item))

    # Reduces the length of matching strings
    try:
        Loop.debug()._set_prefix_override(lambda i: '%d: ' % i)
        Loop.debug()._set_setup_override(lambda: 'setup')

        assert (list(Loop('foo', 'obj', ()).run(lambda var, i, item: var))) == ['setup']
        assert (list(Loop('foo', 'obj', (1,)).run(lambda var, i, item: var))) == ['setup', '0: foo']
        assert (list(Loop('foo', 'obj', (1,)).run(simple_loop))) == ['setup', '0: foo[0] = 1']
        assert (list(Loop('foo', 'obj', range(1, 4)).run(simple_loop))) == ['setup', '0: foo[0] = 1', '1: foo[1] = 2',
                                                                            '2: foo[2] = 3']
        assert (list(Loop('foo', 'obj', (1,)).before().run(simple_loop))) == ['setup', '0: foo[0] = 1']
        assert (list(Loop('foo', 'obj', (1,)).before('before', 'and then').run(simple_loop))) == ['setup', 'before',
                                                                                                  'and then',
                                                                                                  '0: foo[0] = 1']
        assert (list(Loop('foo', 'obj', (1,)).after('and then', 'after').run(simple_loop))) == ['setup',
                                                                                                '0: foo[0] = 1',
                                                                                                'and then', 'after']
        assert (list(
            Loop('foo', 'obj', (1,)).before('before', 'and then').after('and then', 'after').run(simple_loop))) == [
                   'setup', 'before', 'and then',
                   '0: foo[0] = 1',
                   'and then', 'after']
    finally:
        Loop.debug()._set_prefix_override(None)
        Loop.debug()._set_setup_override(None)


def test_loop():
    pass
