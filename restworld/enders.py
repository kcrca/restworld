from __future__ import annotations

from pynecraft.base import EAST, NORTH, SOUTH, WEST, as_facing, r
from pynecraft.commands import Entity, MOVE, clone, data, e, execute, fill, kill, s, setblock, summon, tag
from pynecraft.simpler import WallSign
from restworld.rooms import Room
from restworld.world import main_clock, restworld


def room():
    room_dir = NORTH
    room = Room('enders', restworld, room_dir, (None, 'The End'))
    room.reset_at((-2, 5))
    room.change_height_at((2, 5))

    def cage_loop(step):
        if step.i == 0:
            yield execute().at(e().tag('crystal_home')).run(fill(r(2, 7, 2), r(-2, 4, -2), 'air').replace('iron_bars'))
        else:
            yield execute().at(e().tag('crystal_home')).run(fill(r(2, 9, 2), r(-2, 6, -2), 'iron_bars').hollow())
            yield execute().at(e().tag('crystal_home')).run(fill(r(1, 8, 1), r(-1, 6, -1), 'air'))
            yield execute().at(e().tag('crystal_home')).run(clone(r(2, 9, 2), r(-2, 6, -2), r(-2, 4, -2)).masked(MOVE))
            room.particle('iron_bars', 'crystal', r(0, 8, -2), step)

    room.loop('cage', main_clock).loop(cage_loop, range(0, 2))

    room.function('crystal_init', exists_ok=True).add(
        room.label(r(0, 2, -4), 'Cage', SOUTH),
        execute().as_(e().tag('crystal_home')).run(tag(s()).add('blockers_home')))

    def crystal_loop(step):
        if step.i == 0:
            yield summon('end_crystal', r(0, 5.0, 0), {'Tags': ['crystal']})
            yield setblock(r(0, 5, 0), 'fire')
        else:
            yield kill(e().tag('crystal'))
            yield setblock(r(0, 5, 0), 'air')

    room.loop('crystal', main_clock).add(kill(e().tag('crystal'))).loop(crystal_loop, range(0, 2))

    room.loop('dragon_head', main_clock).loop(
        lambda step: setblock(r(0, 2, 0), 'redstone_torch' if step.i == 0 else 'air'), range(0, 2))
    room.particle('dragon_head', 'dragon_head', r(0, 4, 0))

    # Currently, "Rotation" does not affect the dragon, so it will always face north, so arrange things accordingly.
    dragon_pos = r(0, 4, 0)
    room.function('dragon_init').add(
        kill(e().type('ender_dragon')),
        WallSign((None, 'Ender Dragon')).place(r(0, 2, -5), NORTH),
        room.mob_placer(dragon_pos, NORTH, adults=True).summon('ender_dragon', tags=('dragon', 'dragon_thing'))
    )

    dragon_fireball = Entity('dragon_fireball')
    fireball_pos = r(0, 3, 0)
    room.function('dragon_fireball_init').add(
        kill(e().type('dragon_fireball')),
        WallSign((None, 'Dragon Fireball')).place(r(0, 2, -1), NORTH),
        room.mob_placer(
            fireball_pos, NORTH, adults=True).summon(dragon_fireball, tags=('dragon_thing',)))

    room.function('end_portal_init', exists_ok=True).add(
        execute().as_(e().tag('end_portal_home')).run(tag(s()).add('blockers_home')),
        room.label(r(-6, 2, 5), 'Show Particles', SOUTH))

    def end_portal_loop(step):
        before = 'end_portal' if step.elem else 'air'
        after = 'air' if before != 'end_portal' else 'end_portal'
        yield fill(r(2, 2, 1), r(2, 2, -1), ('end_portal_frame', {'facing': WEST, 'eye': step.elem}))
        yield fill(r(1, 2, 2), r(-1, 2, 2), ('end_portal_frame', {'facing': NORTH, 'eye': step.elem}))
        yield fill(r(-2, 2, 1), r(-2, 2, -1), ('end_portal_frame', {'facing': EAST, 'eye': step.elem}))
        yield fill(r(1, 2, -2), r(-1, 2, -2), ('end_portal_frame', {'facing': SOUTH, 'eye': step.elem}))
        yield fill(r(1, 2, 1), r(-1, 2, -1), after)
        yield fill(r(2, 2, -5), r(-2, 2, -9), after).replace(before)
        room.particle('end_portal_frame', 'end_portal', r(0, 3, 2), step)

    room.particle('dragon_egg', 'end_portal', r(0, 7, 11))

    room.loop('end_portal', main_clock).loop(end_portal_loop, (True, False))

    shulker_dir = WEST
    bullet_loc = r(-1, 3, 1)
    bullet_sign_loc = r(-1, 2, 2)
    placer = room.mob_placer(r(0, 3, 0), shulker_dir, adults=True)
    room.function('shulker_init').add(
        placer.summon('shulker', nbt={'Color': 16, 'Peek': 0}),
        room.mob_placer(
            bullet_loc, shulker_dir, adults=True).summon(
            'shulker_bullet', nbt={'NoGravity': True, 'TXD': 0, 'TYD': 0, 'TZD': 0, 'Steps': 0, 'Motion': [0, 0, 0]}),
        WallSign((None, 'Shulker Bullet')).place(bullet_sign_loc, shulker_dir),
    )

    shulker_facing = as_facing(shulker_dir)

    def shulker_loop(step):
        yield data().merge(e().tag('shulker').limit(1), {'Peek': step.elem})
        yield data().modify(e().tag('shulker').limit(1), 'Rotation').set().value(shulker_facing.rotation)

    room.loop('shulker', main_clock).loop(shulker_loop, (0, 30, 100))
