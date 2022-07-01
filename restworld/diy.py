from __future__ import annotations

from pyker.commands import mc, r, EAST, FORCE, entity, Block, d, Entity
from pyker.simpler import Item
from restworld.rooms import Room, label
from restworld.world import restworld, main_clock


def room():
    room = Room('diy', restworld, EAST, ('DIY:', 'Build Your', 'Own Sequence'))

    def grow_loop(step):
        if step.i != 3:
            yield mc.clone(r(6, 2, 13), r(0, -8, -1), r(-5, -8, -1)).replace(FORCE)
            yield mc.fill(r(1, -1, 9), r(-3, -1, 3), 'air')
        else:
            yield mc.say('Memory at maximum size')
            yield room.score('grow').set(2)

    room.loop('grow').loop(grow_loop, range(0, 4))
    room.function('reset').add(
        mc.function('restworld:global/clock_off'),
        mc.execute().at(entity().tag('diy_starter')).run().fill(r(0, 5, 0), r(0, 5, -6), 'sand'),
        mc.execute().at(entity().tag('diy_ender')).run().tp(entity().tag('diy_cloner'), r(0, 2, 0)),
        mc.function("restworld:diy/_tick"))
    room.function('restore').add(
        mc.setblock(r(0, -2, 0), Block(
            'structure_block',
            nbt={"ignoreEntities": True, "name": "restworld:sequence", "mode": "SAVE", "posX": 0, "posY": 4, "posZ": -6,
                 "sizeX": 1, "sizeY": 1, "sizeZ": 7, "showboundingbox": False})),
        mc.setblock(r(0, -4, 0), 'redstone_torch'),
        mc.setblock(r(0, -4, 0), 'air'),
        mc.setblock(r(0, -2, 0), 'stone'),
        mc.execute().at(entity().tag('diy_starter')).run().setblock(r(0, -2, 0), 'redstone_torch'),
        mc.execute().at(entity().tag('diy_starter')).run().setblock(r(0, -2, 0), 'air'))
    room.function('save').add(
        mc.execute().at(entity().tag('diy_ender')).run().setblock(r(0, -1, 0), Block(
            r'structure_block',
            nbt={"ignoreEntities": True, "name": "restworld:sequence", "mode": "SAVE", "posX": 0, "posY": 7,
                 "posZ": 0, "sizeX": 1, "sizeY": 1, "sizeZ": 7, "showboundingbox": False})),
        mc.execute().at(entity().tag('diy_ender')).run().setblock(r(0, -2, 0), 'redstone_torch'),
        mc.execute().at(entity().tag('diy_ender')).run().setblock(r(0, -2, 0), 'air'),
        mc.execute().at(entity().tag('diy_ender')).run().setblock(r(0, -1, 0), 'stone'),
        mc.setblock(r(0, -4, 0), 'redstone_torch'),
        mc.setblock(r(0, -4, 0), 'air'))
    stand = Entity('armor_stand').tag('customizer', 'diy').merge_nbt(
        {'NoGravity': True, 'Small': True, 'ArmorItems': [{}, {}, {}, Item.nbt_for('turtle_helmet')], 'Rotation': [180, 0]})
    tick_init = room.function('tick_init').add(
        stand.clone().tag('diy_starter').summon(r(-1, -3, 0, )),
        stand.clone().tag('diy_ender').summon(r(-1, -3, -6, )),
        stand.clone().tag('diy_cloner').summon(r(-1, -1, 0, )),
        stand.clone().tag('diy_displayer').summon(r(2, -1, -3))
    )
    for i in range(0, 5):
        tick_init.add(label(r(-(3 + i), 2, -7), "Save"), label(r(-(3 + i), 2, 1), "Restore"))

    custom_reset = room.score('custom_reset')
    room.loop('tick', main_clock).add(
        mc.execute().at(entity().tag('diy_cloner')).run().setblock(r(0, 3, 0), 'sand'),
        custom_reset.set(0),
        mc.execute().at(entity().tag('diy_cloner')).unless().block(r(0, 0, -1), 'air').run(custom_reset.set(1)),
        mc.execute().at(entity().tag('diy_cloner')).if_().block(r(0, 4, -1), 'air').run(custom_reset.set(1)),
        mc.execute().if_().score(custom_reset).matches(1).at(entity().tag('diy_starter')
                                                             ).run().tp(entity().tag('diy_cloner'), r(0, 2, 0)),
        mc.execute().if_().score(custom_reset).matches(0).as_(entity().tag('diy_cloner')).at(
            entity().tag('diy_cloner')).run().tp(entity().tag('diy_cloner'), d(0, 0, 1)),
        mc.execute().at(entity().tag('diy_cloner')).unless().block(r(0, 4, 0), 'air').run(
        ).setblock(r(0, 3, 0), 'magenta_glazed_terracotta'),
        mc.execute().at(entity().tag('diy_cloner')).run(
        ).setblock(r(0, -1, 0), Block('structure_block',
                                      nbt={"ignoreEntities": True, "name": "restworld:singleton", "mode": "SAVE",
                                           "posX": 0, "posY": 5, "posZ": 0, "sizeX": 1, "sizeY": 1, "sizeZ": 1,
                                           "showboundingbox": False})),
        mc.execute().at(entity().tag('diy_cloner')).run().setblock(r(0, -2, 0), 'redstone_torch'),
        mc.execute().at(entity().tag('diy_cloner')).run().setblock(r(0, -2, 0), 'air'),
        mc.execute().at(entity().tag('diy_cloner')).run().setblock(r(0, -1, 0), 'stone'),
        mc.execute().at(entity().tag('diy_displayer')).run().setblock(r(0, -2, 0), 'redstone_torch'),
        mc.execute().at(entity().tag('diy_displayer')).run().setblock(r(0, -2, 0), 'air')
    )
