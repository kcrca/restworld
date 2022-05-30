from restworld.function import *


def test_lines():
    assert (list(lines())) == []
    assert (list(lines('a'))) == ['a']
    assert (list(lines('a\n'))) == ['a', '']
    assert (list(lines('a\nb'))) == ['a', 'b']
    assert (list(lines((), 'a'))) == ['a']
    assert (list(lines(('a', 'b'), 'c'))) == ['a', 'b', 'c']
    assert (list(lines(([['a', 'b']]), 'c'))) == ['a', 'b', 'c']
