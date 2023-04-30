from __future__ import annotations

from pynecraft.base import DAYTIME, EAST, NOON, NORTH, WEST, as_facing, r
from pynecraft.commands import RESULT, data, e, execute, fill, function, kill, setblock, summon, time, worldborder, \
    tag
from pynecraft.info import moon_phases
from pynecraft.simpler import Item, WallSign
from restworld.rooms import Room, label
from restworld.world import restworld, main_clock


def room():
    room = Room('time', restworld, NORTH, (None, 'Time,', 'World', 'Boundary'))

    barriers = fill(r(1, 8, 0), r(1, 8, 8), 'barrier')

    def moon_run_loop(step):
        z = step.i
        if z > 3:
            z += 1
        yield time().set(step.elem[0])
        yield setblock(r(1, 8, z), 'emerald_block')

    def moon_sign(x, y, z, when, name):
        value = z
        if z > 3:
            z += 1
        return WallSign((None, name, 'Moon'), (
            moon.score.set(value),
            execute().at(e().tag('moon_home')).run(function('restworld:time/moon_run_cur')))).place(r(x, y, z), WEST)

    moon = room.loop('moon_run', main_clock)
    moon_running = room.loop('moon_running')
    moon_init = room.function('moon_init')

    moon.add(barriers).loop(moon_run_loop, moon_phases)
    moon_init.add(
        moon_running.score.set(0),
        tag(e().tag('moon_home')).remove('moon_run_home'),
        barriers,
        (moon_sign(0, 8, i, *phase) for i, phase in enumerate(moon_phases)),
        kill(e().tag('time_frame')),
        summon(('item_frame',
                {'Facing': as_facing(WEST).number, 'Item': Item.nbt_for('clock'),
                 'Tags': ['time_frame', room.name], 'Fixed': True}),
               r(0, 8, 4)),
        summon(('item_frame',
                {'Facing': as_facing(EAST).number, 'Item': Item.nbt_for('clock'),
                 'Tags': ['time_frame', room.name], 'Fixed': True}),
               r(-10, 8, 4)),
        label(r(-2, 7, 4), 'Moon Phases'),
        label(r(-1, 7, 4), 'Reset Room', facing=WEST),
        label(r(-9, 7, 4), 'Reset Room', facing=EAST),
    )

    def moon_running_loop(step):
        if step.i == 0:
            yield tag(e().tag('moon_home')).remove('moon_run_home')
            yield execute().at(e().tag('moon_home')).run(function(moon_init))
            yield time().set(NOON)
        else:
            yield tag(e().tag('moon_home')).add('moon_run_home')
            yield execute().at(e().tag('moon_home')).run(function('restworld:time/moon_run_cur'))

    moon_running.loop(moon_running_loop, range(2))

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

        label(r(0, 7, 1), 'Time Running'),
        label(r(0, 7, -1), 'Time Direction'),
        label(r(0, 7, -4), 'Reset Room'),
    )
    room.function('worldborder_hide').add(
        worldborder().center((0, 0)),
        worldborder().set(59999968))
    room.function('worldborder_init').add(label(r(0, 7, 0), 'World Boundary'))
    room.function('worldborder_show').add(
        worldborder().center(r(0, 0)),
        worldborder().set(9))
