from __future__ import annotations

from pynecraft.base import NORTH, SOUTH, WEST, r
from pynecraft.commands import Entity, data, e, execute, setblock
from pynecraft.simpler import Item, WallSign
from restworld.rooms import Room, label
from restworld.world import kill_em, main_clock, restworld


def room():
    room = Room('nether', restworld, WEST, (None, 'Nether', 'Mobs'))

    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    lhs_dir = NORTH
    rhs_dir = SOUTH

    room.function('blaze_init').add(placer(r(-0.2, 2, 0), rhs_dir, adults=True).summon('blaze'))
    room.function('wither_skeleton_init').add(placer(r(-0.2, 2, 0), rhs_dir, adults=True).summon(
        'wither_skeleton', nbt={'HandItems': [Item.nbt_for('stone_sword')]}))
    fireball = Entity('Fireball', {'direction': [0, 0, 0], 'ExplosionPower': 0})
    ghast_height, ghast_dir = 6, WEST
    room.function('fireball_init').add(
        placer(r(1, 3, 0), rhs_dir, adults=True).summon(fireball),
        WallSign((None, 'Fireball')).place(r(0, 2, 0), rhs_dir))
    room.function('ghast_init', exists_ok=True).add(
        placer(r(-0.5, ghast_height, 0), ghast_dir, adults=True).summon('Ghast'))
    room.function('magma_cube_init').add(placer(r(0, 3, 0), SOUTH, adults=True).summon('magma_cube'))
    room.loop('magma_cube', main_clock).loop(
        lambda step: data().modify(e().tag('magma_cube').limit(1), 'Size').set().value(step.elem),
        range(0, 3), bounce=True)
    room.function('piglin_brute_init').add(
        placer(r(0, 2, 0), lhs_dir, adults=True).summon(
            Entity('Piglin Brute', {'HandItems': [Item.nbt_for('golden_axe')]})))
    piglins = (Entity('Piglin', nbt={'HandItems': [Item.nbt_for('golden_sword')]}), 'Zombified Piglin')
    hoglins = ('Hoglin', 'Zoglin')

    def piglin_loop(step):
        p = placer(r(0, 2, 0), lhs_dir, 2, 3, tags=('piglin',))
        yield p.summon(hoglins[step.i])
        yield p.summon(step.elem)

    room.loop('piglin', main_clock).add(kill_em(e().tag('piglin'))).loop(piglin_loop, piglins)
    room.function('strider_init').add(
        placer(r(0, 2, 0), lhs_dir, 0, 3).summon('strider'),
        label(r(6, 2, -5), 'Change Height'),
        label(r(6, 2, -3), 'Reset Room'))

    def strider_loop(step):
        yield execute().if_().score(('mob_levitation', 'global')).matches(0).run(setblock(r(0, 1, 0), step.elem))
        yield execute().if_().score(('mob_levitation', 'global')).matches(0).run(setblock(r(0, 1, -3), step.elem))

    room.loop('strider', main_clock).loop(strider_loop, ('lava', 'netherrack'))
