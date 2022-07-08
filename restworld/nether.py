from __future__ import annotations

from pyker.base import WEST, EAST, SOUTH, r
from pyker.commands import Entity, mc, e
from pyker.simpler import WallSign, Item
from restworld.rooms import Room, label
from restworld.world import restworld, main_clock, kill_em


def room():
    room = Room('nether', restworld, EAST, (None, 'Nether', 'Monsters,', 'Wither'))

    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    room.function('blaze_init').add(placer(r(-0.2, 2, 0), WEST, adults=True).summon('blaze'))
    room.function('wither_skeleton_init').add(placer(r(-0.2, 2, 0), WEST, adults=True).summon('wither_skeleton'))
    room.function('ghast_init').add(
        placer(r(-0.5, 5, 0), SOUTH, adults=True).summon('Ghast'),
        placer(r(-4, 3, 0), SOUTH, adults=True).summon(
            Entity('Fireball', {'direction': [0, 0, 0], 'ExplosionPower': 0})),
        WallSign((None, 'Fireball')).place(r(-4, 2, 1), SOUTH))
    room.function('magma_cube_init').add(placer(r(0, 3, 0), EAST, adults=True).summon('magma_cube'))
    room.loop('magma_cube', main_clock).loop(
        lambda step: mc.data().modify(e().tag('magma_cube').limit(1), 'Size').set().value(step.elem),
        range(0, 3), bounce=True)
    room.function('piglin_brute_init').add(
        placer(r(0, 2, 0), EAST, adults=True).summon(
            Entity('Piglin Brute', {'HandItems': [Item.nbt_for('golden_axe')]})))
    piglins = ('Piglin', 'Zombified Piglin')
    hoglins = ('Hoglin', 'Zoglin')

    def piglin_loop(step):
        p = placer(r(0, 2, 0), EAST, 3, 3, tags=('piglin',))
        yield p.summon(step.elem)
        yield p.summon(hoglins[step.i])

    room.loop('piglin', main_clock).add(kill_em(e().tag('piglin'))).loop(piglin_loop, piglins)
    room.function('strider_init').add(
        placer(r(0, 2, 0), EAST, 0, 3).summon('strider'),
        label(r(3, 2, 1), 'Saddle'),
        label(r(6, 2, -4), 'Change Height'))

    def strider_loop(step):
        yield mc.execute().if_().score(('mob_levitation', 'global')).matches(0).run().setblock(r(0, 1, 0), step.elem)
        yield mc.execute().if_().score(('mob_levitation', 'global')).matches(0).run().setblock(r(3, 1, 0), step.elem)

    room.loop('strider', main_clock).loop(strider_loop, ('lava', 'netherrack'))
