from __future__ import annotations

from pynecraft.__init__ import EAST, NORTH, as_facing, r
from pynecraft.commands import data, e, execute, kill, s, summon
from pynecraft.simpler import WallSign
from restworld.rooms import Room
from restworld.world import kill_em, main_clock, restworld


def room():
    wither_dir = EAST
    wither_sign_pos = r(2, 2, 0)
    skull_rot = 90
    skull_sign_pos = r(1, 2, 0)
    skull_rot_nbt = {'Rotation': [skull_rot, 0]}

    room = Room('wither', restworld, wither_dir, (None, 'Wither'))
    room.reset_at((-2, -2))
    room.change_height_at((-2, 2))

    room.function('wither_painting_init').add(
        kill(e().type('painting').distance((None, 10))),
        summon('painting', r(0, 3, 0), {'variant': 'wither', 'facing': as_facing(NORTH).number}),
        WallSign((None, 'Wither')).place(r(1, 3, 0), NORTH))
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
        yield WallSign((None, sign_text)).place(wither_sign_pos, wither_dir)

    room.loop('wither_mob', main_clock).loop(wither_loop, range(0, 3))
    room.function('wither_skull_init').add(
        kill(e().type('wither_skull')),
        room.mob_placer(r(0, 3, 0), wither_dir, adults=True).summon('Wither Skull', nbt=skull_rot_nbt),
        WallSign((None, 'Wither Skull')).place(skull_sign_pos, wither_dir))
    # Sometimes the skull gets de-rotated, so this puts it back regularly
    room.function('wither_skull_enter').add(data().merge(e().tag('wither_skull').limit(1), skull_rot_nbt))
