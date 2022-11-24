from __future__ import annotations

import math
import os
import re

from pynecraft.base import EAST, NORTH, OVERWORLD, r, to_id
from pynecraft.commands import Block, Entity, e, execute, fill, kill, p, setblock, summon, tp
from pynecraft.info import colors, corals, stems, woods
from pynecraft.simpler import Offset
from restworld.rooms import MobPlacer, Room, label
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
        fill(r(0, -1, 0), r(line_length, -20, 2), 'air')
        for i, b in enumerate(get_normal_blocks()):
            block = Block(b)
            x = i % line_length
            y = -(int(i / line_length) + 1)
            dir = y % 2 == 0
            if dir == 0:
                x = line_length - x - 1
            if '_log' in b or ('basalt' in b and 'smooth' not in b) or ('stem' in b and 'mush' not in b):
                block.merge_nbt({'axes': 'z'})
            elif 'command_block' in 'b':
                block.merge_nbt({'facing': EAST})
            elif b == 'observer':
                block.merge_nbt({'facing': NORTH})

            yield setblock(r(x, y, 0), block)
            if 'coral' in b and 'dead' not in 'b':
                if coral_stage == '0':
                    yield setblock(r(x - 1 if dir == 1 else x + 1, y, 1), 'stone')
                    coral_stage += 1
                    yield setblock(r(x, y, 1), 'water')
                    yield setblock(r(x, y, 2), 'stone')
                    yield setblock(r(x, y - 1, 1), 'stone')
                    yield setblock(r(x, y - 2, 1), Block('stone_slab', {'type': 'top'}))
                elif coral_stage == '1':
                    yield setblock(r(x, y, 1), 'stone')
                    coral_stage += 1

    room.function('all_blocks').add(all_blocks())

    mob_offset = Offset(-1, 9, 7)
    room.function('photo_mobs_init').add(
        kill(e().tag('photo_mob')),
        kill(e().type('item')),
        (Entity(m.mob, m.nbt).tag('photo_mob').merge_nbt(MobPlacer.base_nbt).summon(mob_offset.r(m.x, m.y, m.z),
                                                                                    {'Rotation': [m.rotation, 0],
                                                                                     'OnGround': True}) for m in mobs))

    room.function('photo_example_view', home=False).add(
        execute().in_(OVERWORLD).run(tp(p(), (-1004, 109, 1008)).facing((-1019.00, 93.4, 993.00))),
        kill(e().type('item'))
    )
    room.function('photo_mobs_view', home=False).add(
        tp(p(), (-997.5, 109, 1009.5)).facing((-947.5, 84, 1009.5)),
        kill(e().type('item')))
    room.function('photo_quilt_view').add(
        tp(p(), e().tag('photo_quilt_view').limit(1)),
        execute().at(e().tag('photo_quilt_view').limit(1)).run(tp(p(), r(0, 0, -0.5)).facing((-1000, 100, 1016))),
        kill(e().type('item')))

    shoot_offset = Offset(0, 4, 0)
    room.function('photo_shoot_init').add(
        kill(e().tag('photo_view')),
        summon('armor_stand', shoot_offset.r(0, 10, -3),
               {'Tags': ['photo_view', 'photo_example_view'], 'NoGravity': True, 'Small': True,
                'PersistenceRequired': True, 'Invisible': True}),
        summon('armor_stand', shoot_offset.r(0, 10, 2),
               {'Tags': ['photo_view', 'photo_quilt_view'], 'NoGravity': True, 'Small': True,
                'PersistenceRequired': True, 'Invisible': True}),
        label(shoot_offset.r(-2, 15, 6), 'Frame Example Photo'),
        label(shoot_offset.r(0, 15, 6), 'Frame Mob Photo'),
        label(shoot_offset.r(-1, 15, 7), 'Go Home'),
    )
