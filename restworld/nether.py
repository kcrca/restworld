from __future__ import annotations

from pynecraft.base import NORTH, SOUTH, WEST, r
from pynecraft.commands import Entity, data, e, execute, function, ride, s, setblock
from pynecraft.simpler import Item, WallSign
from restworld.rooms import Room, kill_em
from restworld.world import main_clock, restworld


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
        'wither_skeleton', nbt={'equipment': {'mainhand': Item.nbt_for('stone_sword')}}))
    fireball = Entity('Fireball', {'direction': [0, 0, 0], 'ExplosionPower': 0})
    room.function('fireball_init').add(
        placer(r(1, 3, 0), rhs_dir, adults=True).summon(fireball),
        WallSign((None, 'Fireball')).place(r(0, 2, 0), WEST))
    ghast_height, ghast_dir = 6, WEST

    def ghast_loop(step):
        yield from room.mob_placer(r(1.5, ghast_height, 0), ghast_dir, adults=True, tags='ghastly').summon(step.elem)
        if step.elem.startswith('Happy'):
            yield from room.mob_placer(r(0.5, ghast_height, 4), ghast_dir, kids=True, tags='ghastly').summon(step.elem)

    room.loop('ghast', main_clock).add(kill_em(e().tag('ghastly'))).loop(ghast_loop, ('Ghast', 'Happy Ghast'))
    room.function('magma_cube_init').add(placer(r(0, 3, 0), SOUTH, adults=True).summon('magma_cube'))
    room.loop('magma_cube', main_clock).loop(
        lambda step: data().modify(e().tag('magma_cube').limit(1), 'Size').set().value(step.elem),
        range(0, 3), bounce=True)
    room.function('piglin_brute_init').add(
        placer(r(0, 2, 0), lhs_dir, adults=True).summon(
            Entity('Piglin Brute', {'equipment': {'mainhand': Item.nbt_for('golden_axe')}})))

    hoglin_riders = room.score('hoglin_riders')
    room.function('piglin_init').add(room.label(r(-1, 2, -3), 'Riders', SOUTH))

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

    piglins = (Entity('Piglin', nbt={'equipment': {'mainhand': Item.nbt_for('golden_sword')}}), 'Zombified Piglin')
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
        room.label(r(-1, 2, 0), 'Saddle', SOUTH))

    room.function('piglin_head_init').add(setblock(r(0, 2, 0), 'nether_bricks'), setblock(r(0, 3, 0), 'piglin_head'))
    room.loop('piglin_head', main_clock).loop(
        lambda step: setblock(r(0, 2, 0), 'redstone_block' if step.elem else 'nether_bricks'), (True, False))
