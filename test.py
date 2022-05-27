import io
from contextlib import redirect_stdout
from restworld import commands, enums
from restworld.commands import *


def test_one():
    s = io.StringIO()
    with redirect_stdout(s):
        commands.advancement(Action.GIVE, Target(), Advancement.WAX_ON)
    assert s.getvalue() == 'advancement give husbandry/wax_on'
