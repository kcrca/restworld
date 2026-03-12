import re

import math

from pynecraft import info
from pynecraft.base import as_facing, EAST, NE, NORTH, OVERWORLD, r, SOUTH, SW, to_name, UP, WEST
from pynecraft.commands import Block, CREATIVE, e, Entity, execute, fill, function, gamemode, kill, p, setblock, \
    SURVIVAL, tp
from pynecraft.info import armor_equipment, small_flowers, tall_flowers
from pynecraft.simpler import Item, Offset
from restworld.rooms import MobPlacer, Room
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

    PhotoMob(4.9, -45, 'rabbit', nbt={'RabbitType': 3}),
    PhotoMob(4.3, -32, 'bee'),
    PhotoMob(4.5, -14, 'armadillo'),
    PhotoMob(5.0, 0, 'chicken'),
    PhotoMob(4.7, +22, 'spider', y=0.2),
    PhotoMob(4.5, +42, 'wolf'),

    PhotoMob(7.0, -42, 'mooshroom'),
    PhotoMob(7.0, -27, 'nautilus', y=0.2),
    PhotoMob(7.0, -13, 'copper_golem', nbt={'next_weather_age': -2}),
    PhotoMob(7.0, -1, 'sheep', nbt={'Color': 3}),
    PhotoMob(7.0, +12, 'breeze'),
    PhotoMob(7.0, +29, 'horse', nbt={'Variant': 513}),
    PhotoMob(7.0, +49, 'sniffer'),

    PhotoMob(8.7, -38, 'camel', y=1.5),
    PhotoMob(8.7, -27, 'llama', y=1.5),
    PhotoMob(8.7, -17, 'panda', y=1.5, nbt={'MainGene': 'playful'}),
    PhotoMob(8.7, +5, 'creeper', y=1.5),
    PhotoMob(8.7, +12, 'villager', y=1.5, nbt={'VillagerData': {'profession': 'weaponsmith'}}),
    PhotoMob(8.7, +19, 'piglin_brute', y=1.5,
             nbt={'LeftHanded': True, 'equipment': {'mainhand': {'id': 'golden_axe', 'Count': 1}}}),
    PhotoMob(8.7, +26, 'witch', y=1.5),
    PhotoMob(8.7, +33.5, 'creaking', y=1.5),
    PhotoMob(8.7, +41, 'iron_golem', y=1.5),

    PhotoMob(17.0, -3, 'happy_ghast', y=2.5),
)


def quilt_blocks():
    # Skip blocks where these words occur because they aren't full blocks or solid enough (or anything else). A few of
    # these are entire block names, e.g., '^bamboo$'.
    skippers = ('button', 'pressure', 'door', 'trapdoor', 'fence', 'sign', 'sapling', 'shelf', 'slab', 'stairs', 'rail',
                'cluster', 'beacon', 'dripleaf', 'barrier', 'beetroots', 'bell', 'pane', 'bed', 'candle', 'carpet',
                'banner', 'fan', 'stand', 'wall', 'bush', 'cactus', 'cake', 'sensor', 'campfire', 'carrots', 'cauldron',
                'chest', 'anvil', 'flower', 'eyeblossom', 'conduit', 'bars', 'statue', 'grate', 'lantern', 'torch',
                'head', 'fungus', 'detector', 'pot', 'ghast', '^bamboo$', 'rod', 'farmland', 'dirt path', 'frogspawn',
                'lichen', 'grindstone', 'core', 'ladder', 'bud', 'fern', 'lava', 'water', 'litter', 'lectern',
                '^light$', 'lily', 'sprouts', 'tulip', 'petals', 'pointed', 'potatoes', 'comparator', 'repeater',
                'hopper', 'wire', 'clump', 'shrieker', 'vein', 'pickle', 'seagrass', 'short', 'tall', 'blossom',
                'stonecutter', 'void', 'cane', 'tripwire', 'vines?', 'bush', 'crops?', 'azalea', 'shoot', 'egg',
                'portal', '^fire$', '^kelp$', 'lever', 'propagule', 'skull', 'soul fire', 'wildflower', 'potted',
                'cocoa', '^nether wart$', 'wildflowers', '^snow$', 'enchanting', 'hanging',
                'cobweb',) + small_flowers + tall_flowers + (
                   'leaves', 'composter', 'vault', 'spawner', 'roots', 'scaffolding',  # transparent
                   'mushroom',  # some of these are full, but most aren't, this is a simplicity thing
                   'infested', 'waxed',  # These all look the same in vanilla®
                   'powder', 'sand', 'gravel',  # Falling
                   'ice',  # Melts or is transparent, we could pick out those that don't if we cared to
                   'test', 'jigsaw', 'structure'  # Too rarely used

               )
    non_full_pat = r'\b(' + r'|'.join(skippers) + r')\b'
    non_full_re = re.compile(non_full_pat, re.IGNORECASE)
    # These find blocks we skip but which can't be detected by simple "contains word" checks.
    special_re = re.compile(r'coral(?!.*block)|chain(?!.*command)|^(\w+ )?copper$', re.IGNORECASE)
    for block in info.blocks.values():
        if not non_full_re.search(block.name) and not special_re.search(block.name):
            yield to_name(block.id)


def sorted_quilt_blocks():
    block_list = tuple(quilt_blocks())
    # Sorting is done in ranks, these are listed in ascending order. For example, all corals are together, within that
    # all dead vs. non-dead ones are grouped.
    ranks = [
        (
            'Moss Block', 'Command Block', 'Stained Glass', 'Dead.*Coral', 'Coral', 'Resin', 'Azalea', 'Amethyst',
            'Froglight', 'Sponge', 'Ore', 'Copper(?!.Ore|Raw)', 'Wool', 'Glazed', 'Shulker', 'Concrete', 'Brick', 'Bee',
            'Pumpkin|Jack|Melon', 'Raw', 'Log|Stem', 'Stripped', 'Bricks', 'Bookshelf', 'Sandstone', 'Piston',
            'Polished', 'Terracotta',
            '(Coal|Iron|Emerald|Lapis|Redstone|Gold|Diamond) Block',
            'Table|Barrel|Furnace|Loom|Smoker|Crafter|Dispenser|Dropper|Observer',
        ),
        (
            'Glass', 'Coral', 'Wood|Hyphae', 'Planks', 'Terracotta',
        ),
        (
            'Log|Stripped|Planks',
        )
    ]

    # Replacements that allow bamboo to be sorted with the regular wood
    special = {'Bamboo Block': 'Bamboo Log', 'Stripped Bamboo Block': 'Stripped Bamboo Log',
               'Bamboo Mosaic': 'Bamboo Mosaic Planks', }

    def key_func(block):
        key = block
        if key in special:
            key = special[key]
        for pats in ranks:
            for p in pats:
                if re.search(p, key):
                    key = f'{p}-{key}'
                    break
        return key

    return sorted(block_list, key=key_func)


def armor(kind):
    armors = {}
    for place, which in armor_equipment.items():
        armors[place] = Item.nbt_for(f'{kind}_{which}')
    return Entity('armor_stand', nbt={'equipment': armors}).tag('photo')


def room():
    room = Room('photo', restworld)

    # There is no obvious place to put a "home" stand for the quilt. So it is built by putting a command block above the
    # upper left corner of it, setting the command to 'function restworld:photo/quilt_init' and then using a button to
    # trigger it. If a better idea suggests itself, I'll use it.
    def quilt():
        coral_stage = 0
        line_length = 25
        yield fill(r(0, -1, -2), r(line_length, -20, 2), 'air')
        blocks = tuple(sorted_quilt_blocks())
        if len(blocks) % line_length % line_length != 0:
            print('WARNING: quilt size will not fit in full rows')
        # Special states for matching blocks
        states = {
            'Log|Stem|^Basalt|Stripped Bamboo|Bamboo Block': {'axis': 'z'},
            'Command Block': {'facing': EAST},
            'Furnace|Dispenser|Dropper|Observer|Loom|Barrel|Smoker|Bee|Chiseled Bookshelf': {'facing': SOUTH},
            'Piston': {'facing': UP},
        }
        for i, name in enumerate(blocks):
            block = Block(name)
            x = i % line_length
            y = -(int(i / line_length) + 1)
            dir = y % 2 == 0
            if dir == 0:
                x = line_length - x - 1
            for p, state in states.items():
                if re.search(p, name):
                    block.merge_state(state)

            yield setblock(r(x, y, 0), block)
            # Put water behind the live coral so it stays alive
            if 'Coral' in name and 'Dead' not in name:
                if coral_stage == 0:
                    yield setblock(r(x - 1 if dir == 1 else x + 1, y, -1), 'stone')
                    coral_stage += 1
                yield setblock(r(x, y, -1), 'water')
                yield setblock(r(x, y, -2), 'stone')
                yield setblock(r(x, y - 1, -1), 'stone')
                yield setblock(r(x, y - 2, -1), Block('stone_slab', {'type': 'top'}))
            elif coral_stage == 1:
                yield setblock(r(x, y, -1), 'stone')
                coral_stage += 1

    room.function('quilt_init', home=False).add(quilt())

    mob_offset = Offset(-6, -6, 0)
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
    room.function('photo_mobs_view', home=False).add(
        execute().in_(OVERWORLD).run(tp(p(), (-1006.5, 109, 1036.5)).facing((-955.5, 88, 1036.5))),
        function(do_drop),
        kill(e().type('item')))
    room.function('photo_sample_view', home=False).add(
        execute().in_(OVERWORLD).run(tp(p(), (-1008.001, 109, 1043)).facing((-1008.001, 105, 1057))),
        function(do_drop))
    room.function('photo_quilt_view', home=False).add(
        execute().in_(OVERWORLD).run(tp(p(), (-1008, 109.51, 1029.39)).facing((-1008, 109.2, 1000))),
        function(do_drop))

    room.function('photo_shoot_init').add(
        room.label(r(1, 2, 0), 'Mob Photo', WEST),
        room.label(r(0, 2, 3), 'Go Home', NORTH),
        room.label(r(0, 2, 3), 'Go Home', SOUTH),
        room.label(r(0, 2, 7), 'Sample Photo', NORTH),
        room.label(r(0, 2, -2), 'Reset Room', SOUTH),
        room.label(r(0, 2, -6), 'Quilt Photo', SOUTH),
    )

    room.function('sampler_init').add(
        kill(e().tag('example')),
        kill(e().type('item')),
        room.mob_placer(r(-4, 2, 0), as_facing(NE), adults=True, tags='example').summon('creeper'),
        room.mob_placer(r(-1, 2, 0), as_facing(NE), adults=True, tags='example').summon('minecart'),
        room.mob_placer(r(4.5, 2, 0), as_facing(SW), adults=True, tags='example').summon('oak_chest_boat'),
    )
