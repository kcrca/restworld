from __future__ import annotations

import math

from pynecraft.base import OVERWORLD
from pynecraft.commands import Entity, e, execute, kill, p, tp, gamemode, CREATIVE, SURVIVAL, function
from pynecraft.simpler import Offset
from restworld.rooms import MobPlacer, Room, label
from restworld.world import restworld


class PhotoMob:
    def __init__(self, dist, degrees, mob, nbt=None, y=0.0):
        if nbt is None:
            nbt = {}
        radians = math.radians(degrees)
        self.x = dist * math.cos(radians)
        self.z = dist * math.sin(radians)
        self.rotation = degrees + 90 + 50
        self.y = 8 + y
        self.mob = mob
        self.nbt = nbt


mobs = (
    PhotoMob(3.5, -42, 'parrot'),
    PhotoMob(3, -25, 'cat'),
    PhotoMob(3, 0, 'axolotl'),
    PhotoMob(3, +29, 'ocelot'),
    PhotoMob(3.2, +47, 'fox'),

    PhotoMob(4.9, -45, 'frog'),
    PhotoMob(4.3, -33, 'rabbit', nbt={'RabbitType': 3}),
    PhotoMob(4.5, -20, 'bee'),
    PhotoMob(5.0, 0, 'chicken'),
    PhotoMob(4.7, +22, 'spider', y=0.2),
    PhotoMob(4.5, +42, 'wolf'),

    PhotoMob(7.0, -42, 'mooshroom'),
    PhotoMob(7.0, -27, 'cow'),
    PhotoMob(7.0, -13, 'pig'),
    PhotoMob(7.0, -1, 'sheep', nbt={'Color': 3}),
    PhotoMob(7.0, +14, 'donkey'),
    PhotoMob(7.0, +29, 'mule'),
    PhotoMob(7.0, +43, 'horse', nbt={'Variant': 513}),

    PhotoMob(8.7, -38, 'camel', y=1.5),
    PhotoMob(8.7, -27, 'llama', y=1.5),
    PhotoMob(8.7, -17, 'panda', y=1.5, nbt={'MainGene': 'playful'}),
    PhotoMob(8.7, +5, 'creeper', y=1.5),
    PhotoMob(8.7, +12, 'villager', y=1.5, nbt={'VillagerData': {'profession': 'weaponsmith'}}),
    PhotoMob(8.7, +19, 'piglin_brute', y=1.5,
             nbt={'LeftHanded': True, 'HandItems': [{'id': 'golden_axe', 'Count': 1}, {}]}),
    PhotoMob(8.7, +26, 'witch', y=1.5),
    PhotoMob(8.7, +33.5, 'iron_golem', y=1.5),
    PhotoMob(8.7, +41, 'enderman', y=1.5),

    PhotoMob(17.0, 0, 'ghast', y=1.5),
)


def room():
    room = Room('photo', restworld)

    mob_offset = Offset(-1, 9, 7)
    room.function('photo_mobs_init').add(
        kill(e().tag('photo_mob')),
        kill(e().type('item')),
        (Entity(m.mob, m.nbt).tag('photo_mob').merge_nbt(MobPlacer.base_nbt).summon(
            mob_offset.r(m.x, m.y, m.z), {'Rotation': [m.rotation, 0], 'OnGround': True}) for m in mobs))

    drop = room.score('heeds_drop')
    do_drop = room.function('drop_if_needed', home=False).add(
        drop.set(0),
        execute().as_(p().gamemode(CREATIVE)).run(drop.set(1)),
        # Using 'as server' means that it won't report the changes to the player
        execute().if_().score(drop).matches(1).as_('server').run(gamemode(SURVIVAL, p()), gamemode(CREATIVE, p())))
    room.function('photo_complete_view', home=False).add(
        # /execute in overworld run tp @p -1002 108 1009 facing -1019.0 93 993.0
        execute().in_(OVERWORLD).run(tp(p(), (-1002, 109, 1009)).facing((-1019.00, 93, 993.00))),
        function(do_drop),
        kill(e().type('item'))
    )
    room.function('photo_mobs_view', home=False).add(
        execute().in_(OVERWORLD).run(tp(p(), (-998.5, 109, 1009.5)).facing((-947.5, 88, 1007))),
        function(do_drop),
        kill(e().type('item')))
    room.function('photo_sample_view', home=False).add(
        execute().in_(OVERWORLD).run(tp(p(), (-1000.001, 109, 1016)).facing((-1000.001, 105, 1030))),
        function(do_drop))

    shoot_offset = Offset(0, 4, 0)
    room.function('photo_shoot_init').add(
        label(shoot_offset.r(-1, 15, 6), 'Frame Complete Photo'),
        label(shoot_offset.r(1, 15, 6), 'Frame Mob Photo'),
        label(shoot_offset.r(0, 15, 10), 'Go Home'),
        label(shoot_offset.r(0, 15, 13), 'Frame Sample Photo'),
    )
