from __future__ import annotations

from pynecraft.base import EAST, NORTH, SOUTH, WEST, r
from pynecraft.commands import Entity, data, e, execute, setblock
from pynecraft.simpler import Item, WallSign
from restworld.rooms import Room, label
from restworld.world import VERSION_1_20, kill_em, main_clock, restworld


def room():
    if restworld.version < VERSION_1_20:
        room = Room('nether', restworld, EAST, (None, 'Nether', 'Monsters,', 'Wither'))
    else:
       room = Room('nether', restworld, WEST, (None, 'Nether', 'Mobs'))

    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    lhs_dir = EAST if restworld.version < VERSION_1_20 else NORTH
    rhs_dir = WEST if restworld.version < VERSION_1_20 else SOUTH

    room.function('blaze_init').add(placer(r(-0.2, 2, 0), rhs_dir, adults=True).summon('blaze'))
    room.function('wither_skeleton_init').add(placer(r(-0.2, 2, 0), rhs_dir, adults=True).summon(
        'wither_skeleton', nbt={'HandItems': [Item.nbt_for('stone_sword')]}))
    fireball = Entity('Fireball', {'direction': [0, 0, 0], 'ExplosionPower': 0})
    if restworld.version < VERSION_1_20:
        ghast_height, ghast_dir = 5, SOUTH
        room.function('ghast_init').add(
            placer(r(-4, 3, 0), SOUTH, adults=True).summon(fireball),
            WallSign((None, 'Fireball')).place(r(-4, 2, 1), SOUTH))
    else:
        ghast_height, ghast_dir = 6, WEST
        room.function('fireball_init').add(
            placer(r(1, 3, 0), rhs_dir, adults=True).summon(fireball),
            WallSign((None, 'Fireball')).place(r(0, 2, 0), rhs_dir)        )
    room.function('ghast_init', exists_ok=True).add(
        placer(r(-0.5, ghast_height, 0), ghast_dir, adults=True).summon('Ghast'))
    cube_dir = EAST if restworld.version < VERSION_1_20 else SOUTH
    room.function('magma_cube_init').add(placer(r(0, 3, 0), cube_dir, adults=True).summon('magma_cube'))
    room.loop('magma_cube', main_clock).loop(
        lambda step: data().modify(e().tag('magma_cube').limit(1), 'Size').set().value(step.elem),
        range(0, 3), bounce=True)
    room.function('piglin_brute_init').add(
        placer(r(0, 2, 0), lhs_dir, adults=True).summon(
            Entity('Piglin Brute', {'HandItems': [Item.nbt_for('golden_axe')]})))
    piglins = (Entity('Piglin', nbt={'HandItems': [Item.nbt_for('golden_sword')]}), 'Zombified Piglin')
    hoglins = ('Hoglin', 'Zoglin')

    def piglin_loop(step):
        p = placer(r(0, 2, 0), lhs_dir, 3, 3, tags=('piglin',))
        yield p.summon(step.elem)
        yield p.summon(hoglins[step.i])

    room.loop('piglin', main_clock).add(kill_em(e().tag('piglin'))).loop(piglin_loop, piglins)
    room.function('strider_init').add(
        placer(r(0, 2, 0), lhs_dir, 0, 3).summon('strider'),
        label(r(3, 2, 1), 'Saddle'),
        label(r(6, 2, -5), 'Change Height'),
        label(r(6, 2, -3), 'Reset Room'))

    def strider_loop(step):
        kid_lava = r(3, 1, 0) if restworld.version < VERSION_1_20 else r(0, 1, -3)
        yield execute().if_().score(('mob_levitation', 'global')).matches(0).run(setblock(r(0, 1, 0), step.elem))
        yield execute().if_().score(('mob_levitation', 'global')).matches(0).run(setblock(kid_lava, step.elem))

    room.loop('strider', main_clock).loop(strider_loop, ('lava', 'netherrack'))
