from __future__ import annotations

from pynecraft.base import EAST, NORTH, SOUTH, WEST, r
from pynecraft.commands import MOVE, clone, data, e, execute, fill, function, kill, s, setblock, summon, tag
from pynecraft.simpler import WallSign
from restworld.rooms import Room, label
from restworld.world import main_clock, restworld


def room():
    room = Room('enders', restworld, WEST, (None, 'The End'))

    def cage_loop(step):
        if step.i == 0:
            yield execute().at(e().tag('crystal_home')).run(fill(r(2, 7, 2), r(-2, 4, -2), 'air').replace('iron_bars'))
        else:
            yield execute().at(e().tag('crystal_home')).run(fill(r(2, 9, 2), r(-2, 6, -2), 'iron_bars').hollow())
            yield execute().at(e().tag('crystal_home')).run(fill(r(1, 8, 1), r(-1, 6, -1), 'air'))
            yield execute().at(e().tag('crystal_home')).run(clone(r(2, 9, 2), r(-2, 6, -2), r(-2, 4, -2)).masked(MOVE))

    room.loop('cage', main_clock).loop(cage_loop, range(0, 2))

    room.function('crystal_init').add(
        label(r(4, 2, 0), 'Cage'),
        execute().as_(e().tag('var_home')).run(tag(s()).add('blockers_home')))

    def crystal_loop(step):
        if step.i == 0:
            yield summon('end_crystal', r(0, 5.0, 0), {'Tags': ['crystal']})
            yield setblock(r(0, 5, 0), 'fire')
        else:
            yield kill(e().tag('crystal'))

    room.loop('crystal', main_clock).add(kill(e().tag('crystal'))).loop(crystal_loop, range(0, 2))

    room.loop('dragon_head', main_clock).loop(
        lambda step: setblock(r(0, 2, 0), 'redstone_torch' if step.i == 0 else 'air'), range(0, 2))

    room.function('dragon_init').add(
        kill(e().type('ender_dragon')),
        kill(e().type('dragon_fireball')),
        WallSign((None, 'Ender Dragon')).place(r(0, 2, -5), NORTH),
        WallSign((None, 'Dragon Fireball')).place(r(0, 2, -15), NORTH),
        room.mob_placer(r(0, 3, -5), NORTH, adults=True).summon('ender_dragon', tags=('dragon', 'dragon_thing')),
        room.mob_placer(r(0, 3, -14), NORTH, adults=True).summon(
            'dragon_fireball', tags=('dragon_thing',), nbt={'direction': {0.0, 0.0, 0.0}, 'ExplosionPower': 0}),
    )
    room.function('end_portal_init').add(
        execute().as_(e().tag('var_home')).run(tag(s()).add('blockers_home')))

    def end_portal_loop(step):
        before = 'end_portal' if step.elem else 'air'
        after = 'air' if before != 'end_portal' else 'end_portal'
        yield fill(r(2, 2, 1), r(2, 2, -1), ('end_portal_frame', {'facing': WEST, 'eye': step.elem}))
        yield fill(r(1, 2, 2), r(-1, 2, 2), ('end_portal_frame', {'facing': NORTH, 'eye': step.elem}))
        yield fill(r(-2, 2, 1), r(-2, 2, -1), ('end_portal_frame', {'facing': EAST, 'eye': step.elem}))
        yield fill(r(1, 2, -2), r(-1, 2, -2), ('end_portal_frame', {'facing': SOUTH, 'eye': step.elem}))
        yield fill(r(1, 2, 1), r(-1, 2, -1), after)
        yield fill(r(2, 2, -5), r(-2, 2, -9), after).replace(before)
        yield setblock(r(0, 6, -7), 'air' if after == 'air' else 'dragon_egg')

    room.loop('end_portal', main_clock).loop(end_portal_loop, (True, False))

    placer = room.mob_placer(r(0, 2, 0), SOUTH, adults=True)
    # Enderman requires special handling because the rain may make it run away (even with NoAI)
    room.function('enderman_enter').add(
        execute().unless().entity(e().type('enderman').distance((None, 5))).run(
            list(placer.summon('enderman'))[0]))
    room.function('enderman_init').add(function('restworld:enders/enderman_enter'))

    placer = room.mob_placer(r(0, 2, -0.2), SOUTH, adults=True)
    room.function('endermite_init').add(placer.summon('endermite'))

    # I don't know why I need to do this explicitly after setting the rotation above, but it works
    # data modify entity entity().tag('shulker').limit(1) Rotation set value  {0,0 }
    placer = room.mob_placer(r(0, 3, 0), SOUTH, adults=True)
    room.function('shulker_init').add(
        placer.summon('shulker', nbt={'Color': 16, 'Peek': 0}),
        room.mob_placer(r(1, 3, 1), SOUTH, adults=True).summon(
            'shulker_bullet', nbt={'NoGravity': True, 'TXD': 0, 'TYD': 0, 'TZD': 0, 'Steps': 0, 'Motion': [0, 0, 0]}),
        WallSign((None, 'Shulker Bullet')).place(r(1, 2, 2), SOUTH),
        label(r(1, 2, 6), 'Change Height'),
    )

    def shulker_loop(step):
        yield data().merge(e().tag('shulker').limit(1), {'Peek': step.elem})
        yield data().modify(e().tag('shulker').limit(1), 'Rotation').set().value([0, 0])

    room.loop('shulker', main_clock).loop(shulker_loop, (0, 30, 100))
