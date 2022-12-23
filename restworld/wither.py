from __future__ import annotations

from pynecraft.base import EAST, NORTH, WEST, good_facing, r
from pynecraft.commands import data, e, execute, kill, s, summon
from pynecraft.simpler import WallSign
from restworld.rooms import Room
from restworld.world import VERSION_1_20, kill_em, main_clock, restworld


def room():

    if restworld.version < VERSION_1_20:
        wither_dir = NORTH
        wither_sign_pos = r(0, 2, -2)
        skull_rot = 180
        skull_sign_pos = r(0, 2, -1)
    else:
        wither_dir = EAST
        wither_sign_pos = r(2, 2, 0)
        skull_rot = 90
        skull_sign_pos = r(1, 2, 0)
    skull_rot_nbt = {'Rotation': [skull_rot, 0]}

    room = Room('wither', restworld, wither_dir, (None, 'Wither'))

    room.function('painting_init').add(
        kill(e().type('painting').distance((None, 10))),
        summon('painting', r(0, 3, 0), {'variant': 'wither', 'facing': good_facing(EAST).number}),
        WallSign((None, 'Wither')).place(r(0, 3, -1), WEST))
    room.function('wither_mob_init').add(WallSign(()).place(wither_sign_pos, wither_dir))
    # Rotating the wither skull shouldn't be needed, but it is (at least as of RestWorld 1.20
    room.function('wither_mob_enter').add(
        room.mob_placer(r(0, 3, 0), wither_dir, tags=('wither_mob',), adults=True).summon('wither'),
        execute().as_(e().tag('wither_skull')).run(data().merge(s(), skull_rot_nbt)),
    )
    room.function('wither_mob_exit').add(kill_em(e().tag('wither_mob')))

    def wither_loop(step):
        if step.i == 0:
            yield data().merge(e().tag('wither_mob').limit(1), {'Health': 300, 'Invul': 100})
            sign_text = 'Invulnerable (New)'
        elif step.i == 1:
            yield data().merge(e().tag('wither_mob').limit(1), {'Health': 300, 'Invul': 0})
            sign_text = 'Healthy'
        else:
            yield data().merge(e().tag('wither_mob').limit(1), {'Health': 140, 'Invul': 0})
            sign_text = 'Armored (Hurt)'
        if restworld.version < VERSION_1_20:
            yield data().merge(wither_sign_pos, {'Text2': sign_text})
        else:
            yield WallSign((None, sign_text)).place(wither_sign_pos, wither_dir)

    room.loop('wither_mob', main_clock).loop(wither_loop, range(0, 3))
    room.function('wither_skull_init').add(
        kill(e().type('wither_skull')),
        room.mob_placer(r(0, 3, 0), wither_dir, adults=True).summon('Wither Skull', nbt=skull_rot_nbt),
        WallSign((None, 'Wither Skull')).place(skull_sign_pos, wither_dir))
