from __future__ import annotations

from pyker.commands import NORTH, r, WEST, mc, e, good_facing, EAST
from pyker.simpler import WallSign
from restworld.rooms import Room
from restworld.world import restworld, kill_em, main_clock


def room():
    room = Room('wither', restworld, NORTH, (None, 'Wither'))

    room.function('painting_init').add(
        mc.kill(e().type('painting').distance((None, 10))),
        mc.summon('painting', r(0, 3, 0), {'variant': 'wither', 'facing': good_facing(EAST).number}),
        WallSign((None, 'Wither')).place(r(0, 3, -1), WEST))
    room.function('wither_mob_enter').add(
        room.mob_placer(r(0, 3, 0), NORTH, tags=('wither_mob',), adults=True).summon('wither'))
    room.function('wither_mob_exit').add(kill_em(e().tag('wither_mob')))

    def wither_loop(step):
        if step.i == 0:
            yield mc.data().merge(e().tag('wither_mob').limit(1), {'Health': 300, 'Invul': 100})
            yield mc.data().merge(r(0, 2, -2), {'Text2': 'Invulnerable (New)'})
        elif step.i == 1:
            yield mc.data().merge(e().tag('wither_mob').limit(1), {'Health': 300, 'Invul': 0})
            yield mc.data().merge(r(0, 2, -2), {'Text2': 'Healthy'})
        else:
            yield mc.data().merge(e().tag('wither_mob').limit(1), {'Health': 140, 'Invul': 0})
            yield mc.data().merge(r(0, 2, -2), {'Text2': 'Armored (Hurt)'})

    room.loop('wither_mob', main_clock).loop(wither_loop, range(0, 3))
    room.function('wither_skull_init').add(
        mc.kill(e().type('wither_skull')),
        room.mob_placer(r(0, 3, 0), NORTH, adults=True).summon('Wither Skull'),
        WallSign((None, 'Wither Skull')).place(r(0, 2, -1), NORTH))