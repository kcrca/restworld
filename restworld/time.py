from __future__ import annotations

from pyker.base import DAYTIME, EAST, NOON, NORTH, WEST, good_facing, r
from pyker.commands import RESULT, data, e, execute, fill, function, kill, setblock, summon, time, worldborder
from pyker.info import moon_phases
from pyker.simpler import Item, WallSign
from restworld.rooms import Room, label
from restworld.world import restworld


def room():
    room = Room('time', restworld, NORTH, (None, 'Time,', 'World', 'Boundary'))

    barriers = fill(r(1, 8, 0), r(1, 8, 8), 'barrier')

    def moon_sign(x, y, z, when, name):
        return WallSign((None, name, 'Moon'), (
            execute().at(e().tag('moon_home')).run(barriers),
            time().set(when),
            setblock(r(1, 0, 0), 'emerald_block'))).place(r(x, y, z), WEST)

    room.function('moon_init').add(
        fill(r(1, 8, 0), r(0, 8, 8), 'air'),
        barriers,
        (moon_sign(0, 8, i + (1 if i > 3 else 0), *phase) for i, phase in enumerate(moon_phases)),
        kill(e().tag('time_frame')),
        summon(('item_frame',
                {'Facing': good_facing(WEST).number, 'Item': Item.nbt_for('clock'),
                 'Tags': ['time_frame', room.name], 'Fixed': True}),
               r(0, 8, 4)),
        summon(('item_frame',
                {'Facing': good_facing(EAST).number, 'Item': Item.nbt_for('clock'),
                 'Tags': ['time_frame', room.name], 'Fixed': True}),
               r(-10, 8, 4)),
        label(r(-1, 7, 4), 'Reset', facing=4),
        label(r(-9, 7, 4), 'Reset', facing=5),
        room.score('moon').set(0),
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
        fill(r(0, 5, 1), r(2, 5, 1), 'air'),
        setblock(r(0, 5, 1), ('sticky_piston', {'facing': 'west'})),
        setblock(r(1, 5, 1), 'redstone_block'),

        label(r(0, 7, 1), 'Time Running'),
        label(r(0, 7, -1), 'Time Direction'),
        label(r(0, 7, -4), 'Reset'),
    )
    room.function('worldborder_hide').add(
        worldborder().center((0, 0)),
        worldborder().set(59999968))
    room.function('worldborder_init').add(label(r(0, 7, 0), 'World Boundary'))
    room.function('worldborder_show').add(
        worldborder().center(r(0, 0)),
        worldborder().set(9))
