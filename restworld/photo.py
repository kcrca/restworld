from __future__ import annotations

import math
import os
import re

from pyker.base import to_id
from pyker.commands import r, mc, Block, EAST, NORTH, OVERWORLD, p, e, Entity
from pyker.info import colors, woods, stems, corals
from restworld.rooms import Room, MobPlacer, label
from restworld.world import restworld

materials = (
    'Iron', 'Coal', 'Copper', 'Gold', 'Diamond', 'Emerald', 'Chainmail', 'Redstone', 'Lapis Lazuli', 'Granite',
    'Andesite', 'Diorite', 'Netherite', 'Blackstone', 'Stone', 'Cobblestone', 'End Stone', 'Sandstone', 'Red Sandstone',
    'Bone', 'Honey', 'Honeycomb', 'Grass', 'Sticky', 'Nether')
stepables = (
    'Sandstone', 'Red Sandstone', 'Quartz', 'Cobblestone', 'Stone Brick', 'Nether Brick', 'Brick', 'Purpur',
    'Prismarine',
    'Prismarine Brick', 'Dark Prismarine',)


class Mob:
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
    Mob(3.5, -42, 'parrot'),
    Mob(3, -25, 'cat'),
    Mob(3, 0, 'axolotl'),
    Mob(3, +29, 'ocelot'),
    Mob(3.2, +47, 'fox'),

    Mob(4.9, -45, 'frog'),
    Mob(4.3, -33, 'rabbit', nbt={'RabbitType': 3}),
    Mob(4.5, -20, 'bee'),
    Mob(5.0, 0, 'chicken'),
    Mob(4.7, +22, 'spider', y=0.2),
    Mob(4.5, +42, 'wolf'),

    Mob(7.0, -42, 'mooshroom'),
    Mob(7.0, -27, 'cow'),
    Mob(7.0, -13, 'pig'),
    Mob(7.0, -1, 'sheep', nbt={'Color': 3}),
    Mob(7.0, +14, 'donkey'),
    Mob(7.0, +29, 'mule'),
    Mob(7.0, +43, 'horse', nbt={'Variant': 513}),

    Mob(8.7, -38, 'llama', y=1.5),
    Mob(8.7, -27, 'polar_bear', y=1.5),
    Mob(8.7, -17, 'panda', y=1.5, nbt={'MainGene': 'playful'}),
    Mob(8.7, +5, 'creeper', y=1.5),
    Mob(8.7, +12, 'villager', y=1.5, nbt={'VillagerData': {'profession': 'weaponsmith'}}),
    Mob(8.7, +19, 'piglin_brute', y=1.5, nbt={'LeftHanded': True, 'HandItems': [{'id': 'golden_axe', 'Count': 1}, {}]}),
    Mob(8.7, +26, 'witch', y=1.5),
    Mob(8.7, +33.5, 'iron_golem', y=1.5),
    Mob(8.7, +41, 'enderman', y=1.5),

    Mob(17.0, 0, 'ghast', y=1.5),
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
    blocks = {}
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
        if name == 'Tinted Glass':
            name = 'Glass ' + name
        if 'Azalea' in name:
            name = 'Azalea ' + name
        if 'Amethyst' in name:
            name = 'Amethyst ' + name
        if 'Coral' in name:
            name = 'E-Coral ' + name
        elif name in ('Dropper', 'Dispenser', 'Furnace', 'Observer'):
            name = 'Furnace ' + name
        elif name in (
                'Crafting Table', 'Cartography Table', 'Smithing Table', 'Fletching Table', 'Smoker', 'Blast Furnace',
                'Cauldron'):
            name = 'Profession ' + name
        elif 'Glass' in name:
            # 'M' to move it away from corals so the water trough behind the coral doesn't overlap
            name = 'MGlass ' + name
        elif 'Copper' in block and 'Deepslate' not in block and name not in ('Ore', 'Raw Block'):
            name = 'Copper'

        if name not in blocks:
            blocks[name] = []
        blocks[name] += (block,)
    for b in sorted(blocks):
        for w in sorted(blocks[b]):
            yield to_id(w).replace('_lazuli', '').replace('bale', 'block')


def room():
    room = Room('photo', restworld)

    def all_blocks():
        coral_stage = 0
        line_length = 23
        mc.fill(r(0, -1, 0), r(line_length, -20, 2), 'air')
        for i, b in enumerate(get_normal_blocks()):
            block = Block(b)
            x = i % line_length
            y = -(int(i / line_length) + 1)
            dir = y % 2 == 0
            if dir == 0:
                x = line_length - x - 1
            if '_log' in b or ('basalt' in b and 'smooth' not in b) or ('stem' in b and 'mush' not in b):
                block.merge_nbt({'axies': 'z'})
            elif 'command_block' in 'b':
                block.merge_nbt({'facing': EAST})
            elif b == 'observer':
                block.merge_nbt({'facing': NORTH})

            yield mc.setblock(r(x, y, 0), block)
            if 'coral' in b and 'dead' not in 'b':
                if coral_stage == '0':
                    yield mc.setblock(r(x - 1 if dir == 1 else x + 1, y, 1), 'stone')
                    coral_stage += 1
                    yield mc.setblock(r(x, y, 1), 'water')
                    yield mc.setblock(r(x, y, 2), 'stone')
                    yield mc.setblock(r(x, y - 1, 1), 'stone')
                    yield mc.setblock(r(x, y - 2, 1), Block('stone_slab', {'type': 'top'}))
                elif coral_stage == '1':
                    yield mc.setblock(r(x, y, 1), 'stone')
                    coral_stage += 1

    room.function('all_blocks').add(all_blocks())

    room.function('photo_mobs_init').add(
        mc.tp(e().tag('photo_mob'), r(0, 15, 0)),
        mc.kill(e().tag('photo_mob')),
        mc.kill(e().type('item')),
        (Entity(m.mob, m.nbt).tag('photo_mob').merge_nbt(MobPlacer.base_nbt).summon(r(m.x, m.y, m.z),
                                                                                    {'Rotation': [m.rotation, 0],
                                                                                     'OnGround': True}) for m in mobs))

    room.function('photo_example_view').add(
        mc.execute().in_(OVERWORLD).run().tp(p(), (-1000, 100, 1000)).facing((-1011, 93, 989)),
        mc.kill(e().type('item'))
    )
    room.function('photo_mobs_view').add(
        mc.tp(p(), (-996.5, 100, 1002.5)).facing((-950.5, 78, 1002.5)),
        mc.kill(e().type('item')))
    room.function('photo_quilt_view').add(
        mc.tp(p(), e().tag('photo_quilt_view').limit(1)),
        mc.execute().at(e().tag('photo_quilt_view').limit(1)).run().tp(
            p(), r(0, 0, -0.5)).facing((-1000, 100, 1016)),
        mc.kill(e().type('item')))

    room.function('photo_shoot_init').add(
        mc.kill(e().tag('photo_view')),
        mc.summon('armor_stand', r(0, 10, -3),
                  {'Tags': ['photo_view', 'photo_example_view'], 'NoGravity': True, 'Small': True,
                   'PersistenceRequired': True, 'Invisible': True}),
        mc.summon('armor_stand', r(0, 10, 2),
                  {'Tags': ['photo_view', 'photo_quilt_view'], 'NoGravity': True, 'Small': True,
                   'PersistenceRequired': True, 'Invisible': True}),
        label(r(-1, 10, -1), 'Reset Example Photo'),
        label(r(1, 10, -1), 'Reset Mob Photo'),
        label(r(0, 10, 0), 'Go Home'),
        label(r(0, 10, 1), 'Reset Quilt Photo'),
    )