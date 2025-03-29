from __future__ import annotations

from pynecraft.base import EAST, WEST, d, r
from pynecraft.commands import Entity, FORCE, INFINITE, MOVE, clone, e, effect, execute, fill, function, n, say, \
    setblock, tp
from pynecraft.simpler import Item
from pynecraft.values import INVISIBILITY
from restworld.rooms import Room, kill_em
from restworld.world import main_clock, restworld


def room():
    room = Room('diy', restworld, EAST, (None, 'DIY:', 'Build Your', 'Own Sequence'))

    # We use the ("invisible") breeze to show particles for DIY because there is no generic way to get the ID of a
    # block (afaict). Without that, it's not possible to use the standard technique. This seems better than nothing.
    no_particles = room.function('diy_particles_stop', home=False).add(kill_em(n().tag('diy_breeze')))
    room.function('diy_particles_start', home=False).add(
        execute().at(n().tag('diy_room_home')).run(
            Entity('breeze', {'NoAI': True}).tag('diy', 'diy_breeze').summon(r(-6, 4, 0))),
        effect().give(n().tag('diy_breeze'), INVISIBILITY, INFINITE, 1, True)
    )

    room.function('diy_room_init', exists_ok=True).add(
        fill(r(-9, 2, -3), r(-9, 2, 3), 'sand').replace('magenta_glazed_terracotta'),
        room.label(r(-3, 2, -1), 'Show Particles', WEST),
        function(no_particles)
    )

    def grow_loop(step):
        if step.i != 3:
            yield clone(r(6, 2, 13), r(0, -8, -1), r(-5, -8, -1)).replace(FORCE)
            yield fill(r(1, -1, 9), r(-3, -1, 3), 'air')
        else:
            yield say('Memory at maximum size')
            yield room.score('grow').set(2)

    room.loop('grow').loop(grow_loop, range(0, 4))
    room.function('reset').add(
        function('restworld:global/clock_off'),
        execute().at(e().tag('diy_starter')).run(fill(r(0, 5, 0), r(0, 5, -6), 'sand')),
        execute().at(e().tag('diy_ender')).run(tp(e().tag('diy_cloner'), r(0, 2, 0))),
        function('restworld:diy/_tick'))
    room.function('restore', home=False).add(
        clone(r(0, 2, 0), r(0, 2, -6), (-100, 3, 0)),
        execute().at(e().tag('diy_ender')).run(clone((-100, 3, 6), (-100, 3, 0), r(0, 6, 0)).replace(MOVE)))
    room.function('save', home=False).add(
        execute().at(e().tag('diy_ender')).run(clone(r(0, 6, 6), r(0, 6, 0), (-100, 3, 0))),
        clone((-100, 3, 6), (-100, 3, 0), r(0, 2, 0)).replace(MOVE))
    stand = Entity('armor_stand').tag('customizer', 'diy').merge_nbt(
        {'NoGravity': True, 'Small': True, 'equipment': {'head': Item.nbt_for('turtle_helmet')}, 'Rotation': [180, 0]})
    tick_init = room.function('tick_init').add(
        stand.clone().tag('diy_starter').summon(r(-1, -3, 0, )),
        stand.clone().tag('diy_ender').summon(r(-1, -3, -6, )),
        stand.clone().tag('diy_cloner').summon(r(-1, -1, 0, )),
        stand.clone().tag('diy_displayer').summon(r(2, -1, -3))
    )
    for i in range(0, 5):
        tick_init.add(room.label(r(-(3 + i), 2, -7), 'Save', WEST), room.label(r(-(3 + i), 2, 1), 'Restore', WEST))

    custom_reset = room.score('custom_reset')
    room.loop('tick', main_clock).add(
        execute().at(e().tag('diy_cloner')).run(setblock(r(0, 3, 0), 'sand')),
        custom_reset.set(0),
        execute().at(e().tag('diy_cloner')).unless().block(r(0, 0, -1), 'air').run(custom_reset.set(1)),
        execute().at(e().tag('diy_cloner')).if_().block(r(0, 4, -1), 'air').run(custom_reset.set(1)),
        execute().if_().score(custom_reset).matches(1).at(e().tag('diy_starter')
                                                          ).run(tp(e().tag('diy_cloner'), r(0, 2, 0))),
        execute().if_().score(custom_reset).matches(0).as_(e().tag('diy_cloner')).at(
            e().tag('diy_cloner')).run(tp(e().tag('diy_cloner'), d(0, 0, 1))),
        execute().at(e().tag('diy_cloner')).unless().block(r(0, 4, 0), 'air').run(
            setblock(r(0, 3, 0), 'magenta_glazed_terracotta')),
        execute().at(e().tag('diy_cloner')).run(clone(r(0, 4, 0), r(0, 4, 0), (0, 90, 0))),
        execute().at(e().tag('diy_displayer')).run(clone((0, 90, 0), (0, 90, 0), r(0, 4, 0))),
    )
