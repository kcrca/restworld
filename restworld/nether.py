from __future__ import annotations

from pynecraft.base import NORTH, SOUTH, WEST, r
from pynecraft.commands import Entity, data, e, execute, function, ride, s
from pynecraft.simpler import Item, WallSign
from restworld.rooms import Room, label
from restworld.world import kill_em, main_clock, restworld


def room():
    room = Room('nether', restworld, WEST, (None, 'Nether', 'Mobs'))
    room.reset_at((13, 0))
    room.change_height_at((10, 0))

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
        WallSign((None, 'Fireball')).place(r(0, 2, 0), WEST))
    room.function('ghast_init', exists_ok=True).add(
        placer(r(-0.5, ghast_height, 0), ghast_dir, adults=True).summon('Ghast'))
    room.function('magma_cube_init').add(placer(r(0, 3, 0), SOUTH, adults=True).summon('magma_cube'))
    room.loop('magma_cube', main_clock).loop(
        lambda step: data().modify(e().tag('magma_cube').limit(1), 'Size').set().value(step.elem),
        range(0, 3), bounce=True)
    room.function('piglin_brute_init').add(
        placer(r(0, 2, 0), lhs_dir, adults=True).summon(
            Entity('Piglin Brute', {'HandItems': [Item.nbt_for('golden_axe')]})))

    hoglin_riders = room.score('hoglin_riders')
    room.function('piglin_init').add(label(r(-1, 2, -3), 'Riders', SOUTH))

    def add_rider(riders, num, on_tag):
        new_tag = f'hoglin_rider_{num}'
        riders.add(execute().if_().entity(e().tag(*on_tag).limit(1)).run(
            Entity('piglin', {'NoAI': True, 'NoGravity': True, 'IsBaby': True, 'Silent': True,
                              'Tags': [room.name, 'hoglin_rider', new_tag]}).summon(
                r(0, 2.25 + num, -3), facing=NORTH),
            ride(e().tag(new_tag).limit(1)).mount(e().tag(*on_tag).limit(1))))
        return new_tag

    riders = room.function('ride_hoglin', home=False).add(hoglin_riders.set(1))
    t0 = add_rider(riders, 0, ('hoglin', 'kid'))
    t1 = add_rider(riders, 1, (t0,))
    add_rider(riders, 2, (t1,))
    room.function('unride_hoglin', home=False).add(
        hoglin_riders.set(0),
        execute().as_(e().tag('hoglin_rider')).run(ride(s()).dismount()),
        kill_em(e().tag('hoglin_rider')))

    piglins = (Entity('Piglin', nbt={'HandItems': [Item.nbt_for('golden_sword')]}), 'Zombified Piglin')
    hoglins = ('Hoglin', 'Zoglin')

    def piglin_loop(step):
        p = placer(r(0, 2, 0), lhs_dir, 3, 3, tags=('piglin',))
        yield p.summon(hoglins[step.i])
        if step.i == 0:
            yield execute().if_().score(hoglin_riders).matches(1).run(function(riders)),
        yield p.summon(step.elem)

    room.loop('piglin', main_clock).add(kill_em(e().tag('piglin'))).loop(piglin_loop, piglins)

    room.function('strider_init').add(
        placer(r(0, 2, 0), lhs_dir, 0, 3).summon('strider'),
        label(r(-1, 2, 0), 'Saddle', SOUTH))
