from __future__ import annotations

from pynecraft.base import DAYTIME, EAST, NOON, NORTH, SOUTH, WEST, as_facing, r
from pynecraft.commands import RESULT, data, e, execute, fill, function, kill, setblock, summon, tag, time, worldborder
from pynecraft.info import moon_phases
from pynecraft.simpler import Item, WallSign
from restworld.rooms import Room
from restworld.world import main_clock, restworld


def room():
    room = Room('time', restworld, NORTH, (None, 'Time,', 'World', 'Boundary'))

    reset_moon = (
        fill(r(1, 8, 0), r(1, 8, 8), 'barrier'),
        (data().modify(r(0, 8, z), 'front_text.has_glowing_text').set().value(False) for z in range(0, 9))
    )

    def moon_run_loop(step):
        z = step.i
        if z > 3:
            z += 1
        yield time().set(step.elem[0])
        yield setblock(r(1, 8, z), 'emerald_block')
        yield data().modify(r(0, 8, z), 'front_text.has_glowing_text').set().value(True)

    def moon_sign(x, y, z, name):
        value = z
        if z > 3:
            z += 1
        return WallSign((None, name, 'Moon'), (
            moon_run.score.set(value),
            execute().at(e().tag('moon_home')).run(function('restworld:time/moon_run_cur')))).place(r(x, y, z), WEST)

    moon_run = room.loop('moon_run', main_clock, home=False)
    moon_init = room.function('moon_init')

    room.function('moon_run_on', home=False).add(
        tag(e().tag('moon_home')).add('moon_run_home'),
        execute().at(e().tag('moon_home')).run(function('restworld:time/moon_run_cur')),
    )
    room.function('moon_run_off', home=False).add(
        tag(e().tag('moon_home')).remove('moon_run_home'),
        execute().at(e().tag('moon_home')).run(function(moon_init)),
        time().set(NOON),
    )

    moon_run.add(reset_moon).loop(moon_run_loop, moon_phases)
    moon_init.add(
        tag(e().tag('moon_home')).remove('moon_run_home'),
        reset_moon,
        (moon_sign(0, 8, i, phase[1]) for i, phase in enumerate(moon_phases)),
        kill(e().tag('time_frame')),
        summon(('item_frame',
                {'Facing': as_facing(WEST).number, 'Item': Item.nbt_for('clock'),
                 'Tags': ['time_frame', room.name], 'Fixed': True}),
               r(0, 8, 4)),
        summon(('item_frame',
                {'Facing': as_facing(EAST).number, 'Item': Item.nbt_for('clock'),
                 'Tags': ['time_frame', room.name], 'Fixed': True}),
               r(-10, 8, 4)),
        room.label(r(-2, 7, 4), 'Moon Phases', WEST),
        room.label(r(0, 7, 4), 'Reset Room', WEST, vertical=True, bump=0.52),
        room.label(r(-10, 7, 4), 'Reset Room', EAST, vertical=True,  bump=0.52),
    )

    slow, norm = 3, 30
    morn = (21900, 24600)
    even = (11500, 14200)
    noon = 6000
    day = 24000
    time_score = room.score('time')
    time_forward = room.score('run_time_forward')
    room.function('run_time').add(
        execute().unless().score(time_forward).matches((0, None)).run(function('restworld:time/time_init')),
        execute().store(RESULT).score(time_score).run(time().query(DAYTIME)),
        execute().if_().score(time_score).matches((None, noon)).run(time_score.add(day)),

        execute().if_().score(time_score).matches(morn).if_().score(time_forward).matches((1, None)).run(
            time().add(slow)),
        execute().if_().score(time_score).matches(even).if_().score(time_forward).matches((1, None)).run(
            time().add(slow)),
        execute().unless().score(time_score).matches(even).unless().score(time_score).matches(morn).if_().score(
            time_forward).matches((1, None)).run(time().add(norm)),

        # New moon phase each day, so to preserve the moon phase we have to go back nearly 8 days, not nearly 1.
        execute().if_().score(time_score).matches(morn).unless().score(time_forward).matches((1, None)).run(
            time().add(8 * day - slow)),
        execute().if_().score(time_score).matches(even).unless().score(time_forward).matches((1, None)).run(
            time().add(8 * day - slow)),
        execute().unless().score(time_score).matches(even).unless().score(time_score).matches(morn).unless().score(
            time_forward).matches((1, None)).run(time().add(8 * day - norm)),
    )

    room.function('run_time_init').add(
        time_forward.set(1),
        time().set(NOON),
        fill(r(0, 7, 1), r(0, 7, -1), 'air'),
        setblock(r(0, 7, 1), ('lever', {'face': 'floor', 'facing': WEST})),
        setblock(r(0, 7, -1), ('lever', {'face': 'floor', 'facing': WEST})),
        data().merge(r(0, 5, 1), {'powered': 0}),

        room.label(r(0, 7, 1), 'Time Running', EAST),
        room.label(r(0, 7, -1), 'Time Direction', EAST),
        room.label(r(0, 7, -4), 'Reset Room', SOUTH),
    )
    room.function('worldborder_hide').add(
        worldborder().center((0, 0)),
        worldborder().set(59999968))
    room.function('worldborder_init').add(room.label(r(0, 7, 0), 'World Border', EAST))
    room.function('worldborder_show').add(
        worldborder().center(r(0, 0)),
        worldborder().set(9))
