from __future__ import annotations

import math
import os
import re

from pynecraft.base import OVERWORLD, to_id, EAST, NORTH, as_facing, NE, r, SW
from pynecraft.commands import Entity, e, execute, kill, p, tp, gamemode, CREATIVE, SURVIVAL, function, fill, Block, \
    setblock
from pynecraft.info import colors, woods, stems, corals
from pynecraft.simpler import Offset
from restworld.rooms import MobPlacer, Room, label
from restworld.world import restworld

materials = (
    'Iron', 'Coal', 'Copper', 'Gold', 'Diamond', 'Emerald', 'Chainmail', 'Redstone', 'Lapis Lazuli', 'Granite',
    'Andesite', 'Diorite', 'Netherite', 'Blackstone', 'Stone', 'Cobblestone', 'End Stone', 'Sandstone', 'Red Sandstone',
    'Bone', 'Honey', 'Honeycomb', 'Grass', 'Sticky', 'Nether')
stepables = (
    'Sandstone', 'Red Sandstone', 'Quartz', 'Cobblestone', 'Stone Brick', 'Nether Brick', 'Brick', 'Purpur',
    'Prismarine', 'Prismarine Brick', 'Dark Prismarine',)


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
    PhotoMob(7.0, +29, 'horse', nbt={'Variant': 513}),
    PhotoMob(7.0, +49, 'sniffer'),

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


def get_normal_blocks():
    modifiers = tuple(c.name for c in colors) + woods + stems + materials + stepables + corals + (
        'Weathered', 'Oxidized', 'Exposed')
    modifiers = tuple(sorted(set(modifiers), key=lambda x: len(x), reverse=True))
    mod_re = re.compile(fr'^(.*? ?)(\b(?:Mossy )?{"|".join(modifiers)}\b)($| (.*))')
    block_re = re.compile(r'Block of (.*)')
    command_re = re.compile(r'(.*)Command Block')
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'some_blocks')) as f:
        lines = f.readlines()
    good_blocks = {}
    for block in lines:
        if block[0] == '#':
            continue
        block = block.strip()
        block = block_re.sub(r'\1 Block', block)  # 'Block of Foo' -> 'Foo Block'
        m = mod_re.match(block)
        if not m:
            m = command_re.match(block)
            if not m:
                name = block
            else:
                name = 'Command Block'
        else:
            name = (m.group(1) + m.group(3))
        name = name.replace('  ', ' ').strip()

        # Special cases to force grouping and sometimes placement.
        if 'Azalea' in name:
            name = 'Azalea ' + name
        if 'Amethyst' in name:
            name = 'Amethyst ' + name
        if 'Coral' in name:
            name = 'E-Coral ' + name
        elif name in ('Dropper', 'Dispenser', 'Furnace', 'Observer'):
            name = 'Furnace ' + name
        elif 'Froglight' in name:
            name = f'Froglight {name}'
        elif 'Sponge' in name:
            name = f'Sponge {name}'
        elif 'Ore' in name:
            name = f'Ore {name}'
        elif name in (
                'Crafting Table', 'Cartography Table', 'Smithing Table', 'Fletching Table', 'Smoker', 'Blast Furnace',
                'Cauldron'):
            name = 'Profession ' + name
        elif 'Glass' in name:
            # 'M' to move it away from corals so the water trough behind the coral doesn't overlap
            name = 'CGlass ' + name
        elif 'Copper' in block and 'Deepslate' not in block and name not in ('Ore', 'Raw Block'):
            name = 'Copper'

        if name not in good_blocks:
            good_blocks[name] = []
        good_blocks[name] += (block,)
    for b in sorted(good_blocks):
        for w in sorted(good_blocks[b]):
            yield to_id(w).replace('_lazuli', '').replace('bale', 'block')


def room():
    room = Room('photo', restworld)

    # Currently it seems rally hard to figure out where to put a home stand for the quilt, so I'm just
    # using absolute coordinates. I can fix this later if I get tired o fit.
    def quilt():
        coral_stage = 0
        line_length = 25
        p = Offset(-1061, 113, 1040)
        yield fill(p.p(0, -1, -2), p.p(line_length, -20, 2), 'air')
        for i, b in enumerate(get_normal_blocks()):
            block = Block(b)
            z = i % line_length
            y = -(int(i / line_length) + 1)
            dir = y % 2 == 0
            if dir == 0:
                z = line_length - z - 1
            if '_log' in b or ('basalt' in b and 'smooth' not in b) or ('stem' in b and 'mush' not in b):
                block.merge_state({'axis': 'z'})
            elif 'command_block' in 'b':
                block.merge_nbt({'facing': EAST})
            elif b == 'observer':
                block.merge_nbt({'facing': NORTH})

            yield setblock(p.p(z, y, 0), block)
            if 'coral' in b and 'dead' not in b:
                if coral_stage == 0:
                    yield setblock(p.p(z - 1 if dir == 1 else z + 1, y, 1), 'stone')
                    coral_stage += 1
                yield setblock(p.p(z, y, 1), 'water')
                yield setblock(p.p(z, y, 2), 'stone')
                yield setblock(p.p(z, y - 1, 1), 'stone')
                yield setblock(p.p(z, y - 2, 1), Block('stone_slab', {'type': 'top'}))
            elif coral_stage == 1:
                yield setblock(p.p(z, y, 1), 'stone')
                coral_stage += 1

    room.function('quilt_init').add(
        quilt(),
        label((-1049, 104, 1028), 'Quilt Photo'),
        label((-1049, 104, 1027), 'Back to Platform'))

    mob_offset = Offset(-1, 9, 7)
    room.function('photo_mobs_init').add(
        kill(e().tag('photo_mob')),
        kill(e().type('item')),
        (Entity(m.mob, m.nbt).tag('photo_mob').merge_nbt(MobPlacer.base_nbt).summon(
            mob_offset.r(m.x, m.y, m.z), {'Rotation': [m.rotation, 0], 'OnGround': True}) for m in mobs))

    drop = room.score('needs_drop')
    do_drop = room.function('drop_if_needed', home=False).add(
        drop.set(0),
        execute().as_(p().gamemode(CREATIVE)).run(drop.set(1)),
        # Using 'as server' means that it won't report the changes to the player
        execute().if_().score(drop).matches(1).run(gamemode(SURVIVAL, p()), gamemode(CREATIVE, p())))
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
    room.function('photo_quilt_view').add(
        execute().in_(OVERWORLD).run(tp(p(), (-1049, 104.51, 1029.61)).facing((-1049, 104.51, 1045))),
        function(do_drop))

    shoot_offset = Offset(0, 4, 0)
    room.function('photo_shoot_init').add(
        label(shoot_offset.r(-1, 15, 6), 'Complete Photo'),
        label(shoot_offset.r(1, 15, 6), 'Mob Photo'),
        label(shoot_offset.r(0, 15, 8), 'Quilt Photo'),
        label(shoot_offset.r(0, 15, 10), 'Go Home'),
        label(shoot_offset.r(0, 15, 13), 'Sample Photo'),
    )

    room.function('sampler_init').add(
        room.mob_placer(r(-4, 2, 0), as_facing(NE), adults=True).summon('creeper'),
        room.mob_placer(r(-1, 2, 0), as_facing(NE), adults=True).summon('minecart'),
        room.mob_placer(r(4.5, 2, 0), as_facing(SW), adults=True).summon('chest_boat'),
    )
