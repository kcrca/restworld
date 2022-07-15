from __future__ import annotations

import collections
import copy
import json
import os
import re
from copy import deepcopy
from enum import Enum
from functools import total_ordering
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable, Iterable, Tuple

from pynecraft.base import Nbt, ROTATION_180, ROTATION_270, ROTATION_90, r, rotated_facing, to_id, to_name
from pynecraft.commands import Block, BlockDef, CLEAR, Command, Commands, Entity, EntityDef, JsonText, NEAREST, \
    Position, Score, SignText, a, comment, data, e, execute, fill, function, good_block, good_entity, good_facing, \
    good_score, kill, lines, p, schedule, scoreboard, setblock, summon, tellraw, tp, weather
from pynecraft.enums import Particle, ScoreCriteria
from pynecraft.function import DataPack, Function, FunctionSet, LATEST_PACK_VERSION, Loop
from pynecraft.simpler import Sign, WallSign


@total_ordering
class Thing:
    def __init__(self, name, id=None, block_state=None):
        self.text = name
        self.name = name.replace('|', ' ').strip()  # This allows a '%s Minecart' % '' to work
        if id is None:
            id = to_id(self.name.strip())
        self.id = to_id(id.strip())
        self.block_state = block_state if block_state else ''

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.full_id() < other.full_id()

    def __eq__(self, other):
        return self.full_id() == other.full_id()

    def full_id(self, block_state=''):
        id = '%s' % self.id
        state = self.block_state + (',' if block_state and self.block_state else '') + block_state
        if state:
            id += '[%s]' % state
        return id

    def sign_text(self, pre=None, skip=()):
        txt = self.to_sign_text()
        if pre:
            txt = [pre] + txt
        if len(txt) != 4:
            txt = [''] + txt
        txt.extend([''] * (4 - len(txt)))
        s = ''
        for i in range(0, 4):
            if i not in skip:
                if len(s) > 0:
                    s += ','
                s += 'Text%d:%s' % (i + 1, text(txt[i]))
        return s

    def to_sign_text(self):
        lines = self.text.split('|')
        return lines

    def summon(self, pos: Position, rotation):
        return Entity(self.id, nbt={'CustomName': self.name, 'Rotation': [rotation, 0]}).summon(pos)


class Nicknamed(Thing):
    def __init__(self, nickname, kind, id=None, block_state=None):
        Thing.__init__(self, ('%s %s' % (nickname, kind)).strip(), id, block_state)
        self.nickname = nickname
        self.kind = kind


class Color(Thing):
    next_color_num = 0

    def __init__(self, name, rgb):
        Thing.__init__(self, name)
        self.rgb = rgb
        self.id = name.replace(' ', '_').lower()
        self.color_num = Color.next_color_num
        Color.next_color_num += 1

    def dye_name(self):
        return '%s_dye' % self.id

    def in_id(self):
        return self.id


class Horse(Thing):
    def __init__(self, name, variant=None):
        if variant is not None:
            Thing.__init__(self, name, 'horse')
            self.tag = '%s_horses' % to_id(name)
        else:
            Thing.__init__(self, name)
            self.tag = '%ss' % self.id
        self.variant = variant


class Mob(Thing):
    def __init__(self, name, id=None, nbt=None, can_fly=False, aquatic=False):
        Thing.__init__(self, name, id=id)
        self.nbt = nbt
        self.can_fly = can_fly
        self.aquatic = aquatic

    def inner_nbt(self):
        if not self.nbt:
            return ''
        return ',%s' % self.nbt


class CommandBlock(Thing):
    def __init__(self, name, conditional):
        Thing.__init__(self, name)
        self.conditional = conditional


class Stepable(Thing):
    def __init__(self, name, base_id, block=None):
        Thing.__init__(self, name)
        self.block = to_id(block) if block else self.id
        self.base_id = to_id(base_id)


class ActionDesc:
    def __init__(self, enum: Enum, name=None, note=None, also=()):
        self.enum = enum
        if name is None:
            name = enum.__class__.display_name(enum)
        self.name = name
        self.note = '(%s)' % note if note else None
        if isinstance(also, Iterable):
            self.also = also
        else:
            self.also = (also,)

    def __str__(self):
        return self.name + ' [' + self.enum + ']'

    def __lt__(self, other):
        assert self.__class__ == other.__class__
        assert self.enum.__class__ == other.enum.__class__
        return self.name < other.name

    def sign_text(self):
        block = Block(self.enum.value, name=self.name)
        sign_text = list(block.sign_text)
        if self.note:
            sign_text.append(self.note)
        if len(sign_text) < 4:
            sign_text.insert(0, None)
        while len(sign_text) > 4:
            if sign_text[0]:
                raise ValueError('%s: Too much sign text for action' % sign_text)
            sign_text = sign_text[1:]
        return sign_text


colors = (
    Color('White', 0xf9fffe),
    Color('Orange', 0xf9801d),
    Color('Magenta', 0xc74ebd),
    Color('Light Blue', 0x3ab3da),
    Color('Yellow', 0xfed83d),
    Color('Lime', 0x80c71f),
    Color('Pink', 0xf38baa),
    Color('Gray', 0x474f52),
    Color('Light Gray', 0x9d9d97),
    Color('Cyan', 0x169c9c),
    Color('Purple', 0x8932b8),
    Color('Blue', 0x3c44aa),
    Color('Brown', 0x835432),
    Color('Green', 0x5e7c16),
    Color('Red', 0xb02e26),
    Color('Black', 0x1d1d21),
)
command_blocks = (
    CommandBlock('Command Block', True),
    CommandBlock('Command Block', False),
    CommandBlock('Chain Command Block', False),
    CommandBlock('Chain Command Block', True),
    CommandBlock('Repeating Command Block', True),
    CommandBlock('Repeating Command Block', False),
    CommandBlock('Command Block', False),
    CommandBlock('Command Block', True),
    CommandBlock('Chain Command Block', True),
    CommandBlock('Chain Command Block', False),
    CommandBlock('Repeating Command Block', False),
    CommandBlock('Repeating Command Block', True),
)
stepables = (
    Stepable('Sandstone', 'Sand'),
    Stepable('Red Sandstone', 'Red Sand'),
    Stepable('Quartz', 'Nether Quartz Ore', block='Quartz Block'),
    Stepable('Cobblestone', 'Stone'),
    Stepable('Stone Brick', 'Stone', block='Stone Bricks'),
    Stepable('Nether Brick', 'Netherrack', block='Nether Bricks'),
    Stepable('Brick', 'Clay', block='Bricks'),
    Stepable('Purpur', 'air', block='Purpur Block'),
    Stepable('Prismarine', 'air'),
    Stepable('Prismarine Brick', 'air', block='Prismarine Bricks'),
    Stepable('Dark Prismarine', 'air'),
)
materials = (
    'Iron', 'Coal', 'Copper', 'Gold', 'Diamond', 'Emerald', 'Chainmail', 'Redstone', 'Lapis Lazuli', 'Granite',
    'Andesite', 'Diorite', 'Netherite', 'Blackstone', 'Stone', 'Cobblestone', 'End Stone', 'Sandstone', 'Red Sandstone',
    'Bone', 'Honey', 'Honeycomb', 'Grass', 'Sticky', 'Nether')
corals = ('Horn', 'Tube', 'Fire', 'Bubble', 'Brain')
woods = ('Acacia', 'Birch', 'Jungle', 'Mangrove', 'Oak', 'Dark Oak', 'Spruce')
stems = ('Warped', 'Crimson')
fish_data = (
    ('kob',
     (917504, 'Red-White Kob'),
     (65536, 'Orange-White Kob'),
     ),
    ('sunstreak',
     (134217984, 'White-Silver Sunstreak'),
     (50790656, 'Gray-Sky SunStreak'),
     (118161664, 'Blue-Gray SunStreak'),
     ),
    ((235340288, 'Gray-Red Snooper'),),
    ('dasher',
     (117441280, 'White-Gray Dasher'),
     (101253888, 'Teal-Rose Dasher'),
     ),
    ('brinely',
     (117441536, 'White-Gray Brinely'),
     (50660352, 'Line-Sky Dasher'),
     ),
    ('spotty',
     (67110144, 'White-Yellow Spotter'),
     (50726144, 'Rose-Sky Spotty'),
     ),
    ('flopper',
     (117899265, 'Gray Flopper'),
     (67108865, 'White-Yellow Flopper'),
     ),
    ('stripey',
     (117506305, 'Orange-Gray Stripey'),
     (67371265, 'Yellow Stripey'),
     ),
    ((117441025, 'White-Gray Glitter'),),
    ('blockfish',
     (67764993, 'Plum-Yellow Blockfish'),
     (918273, 'Red-White Blockfish'),
     ),
    ((918529, 'Red-White Betty'),),
    ('clayfish',
     (234882305, 'White-Red Clayfish'),
     (16778497, 'White-Orange Clayfish'),
     ),
)
fishes = []
for f in fish_data:
    if len(f) == 1:
        fishes.append((re.sub(r'[- ]', '_', f[0][1].lower()), f))
    else:
        fishes.append((f[0], list(v for v in f[1:])))
horses = (
    Horse('White', 0),
    Horse('Creamy', 1),
    Horse('Chestnut', 2),
    Horse('Brown', 3),
    Horse('Black', 4),
    Horse('Gray', 5),
    Horse('Dark Brown', 6),
)
other_horses = (
    Horse('Mule'),
    Horse('Donkey'),
    Horse('Skeleton Horse'),
    Horse('Zombie Horse'),
)
small_flowers = (
    Thing('Allium'),
    Thing('Azure Bluet'),
    Thing('Blue Orchid'),
    Thing('Dandelion'),
    Thing('Oxeye Daisy'),
    Thing('Poppy'),
)
tulips = (
    'Red',
    'Orange',
    'Pink',
    'White',
)
professions = (
    'Armorer',
    'Butcher',
    'Cartographer',
    'Cleric',
    'Farmer',
    'Fisherman',
    'Fletcher',
    'Leatherworker',
    'Librarian',
    'Mason',
    'Nitwit',
    'Shepherd',
    'Toolsmith',
    'Weaponsmith',
    'Unemployed',
)
patterns = (
    ('', 'None'), ('drs', 'Down Right Stripe'), ('dls', 'Down Left Stripe'), ('cr', 'Cross'),
    ('bs', 'Bottom Stripe'), ('ms', 'Middle Stripe'), ('ts', 'Top Stripe'), ('sc', 'Square Cross'),
    ('ls', 'Left Stripe'), ('cs', 'Center Stripe'), ('rs', 'Right Stripe'), ('ss', 'Small Stripes'),
    ('ld', 'Left Diagonal'), ('rud', 'Right Upside-Down|Diagonal'), ('lud', 'Left Upside-Down|Diagonal'),
    ('rd', 'Right Diagonal'),
    ('vh', 'Vertical Half|(Left)'), ('vhr', 'Vertical Half|(Right)'), ('hhb', 'Horizontal Half|(Bottom)'),
    ('hh', 'Horizontal Half|(Top)'),
    ('bl', 'Bottom Left|Corner'), ('br', 'Bottom Right|Corner'), ('tl', 'Top Left|Corner'),
    ('tr', 'Top Right|Corner'),
    ('bt', 'Bottom Triangle'), ('tt', 'Top Triangle'), ('bts', 'Bottom Triangle|Sawtooth'),
    ('tts', 'Top Triangle|Sawtooth'),
    ('mc', 'Middle Circle'), ('mr', 'Middle Rhombus'), ('bo', 'Border'), ('cbo', 'Curly Border'),
    ('gra', 'Gradient'), ('gru', 'Gradient|Upside-Down'), ('cre', 'Creeper'), ('bri', 'Brick'),
    ('sku', 'Skull'), ('flo', 'Flower'), ('moj', 'Mojang'), ('glb', 'Globe'), ('pig', 'Pig'),
)
moon_phases = (
    (206000, 'Full'),
    (38000, 'Waning Gibbous'),
    (62000, 'Three Quarters'),
    (86000, 'Waning Crescent'),
    (110000, 'New'),
    (134000, 'Waxing Crescent'),
    (158000, 'First Quarter'),
    (182000, 'Waxing Gibbous'),
)
non_inventory = tuple(Thing(s) for s in (
    'Knowledge Book',
    'Debug Stick',
    'Suspicious Stew',
    'Firework Star',
    'Bundle',
    'Jigsaw',
    'Structure Block',
    'Structure Void',
    'Barrier',
    'Light',
    'Dragon Egg',
    'Command Block',
    'Command Block Minecart',
    'Spawner',
    'Elytra',
))

biome_groups = collections.OrderedDict()
biome_groups['Temperate'] = (
    'Plains', 'Forest', 'Flower Forest', 'Birch Forest', 'Dark Forest', 'Swamp', 'Jungle', 'Mushroom Field')
biome_groups['Warm'] = ('Desert', 'Savanna', 'Badlands')
biome_groups['Cold'] = ('Taiga', 'Stone Shore')
biome_groups['Snowy'] = ('Snowy Tundra', 'Ice Spikes', 'Snowy Taiga')
biome_groups['Ocean'] = ('Warm Ocean', 'Ocean', 'Frozen Ocean')
biome_groups['Caves and Cliffs'] = ('Lush Caves', 'Dripstone Caves')
biome_groups['Nether'] = ('Nether Wastes', 'Soul Sand Valley', 'Crimson Forest', 'Warped Forest', 'Basalt Deltas')
biome_groups['End'] = ('The End', 'End Island', 'End City')
biome_groups['Structures'] = ('Mineshaft', 'Monument', 'Stronghold', 'Bastion Remnant', 'Fortress')
biomes = [item for sublist in list(biome_groups.values()) for item in sublist]

coloring_coords = (1, 4, 6, -13, 2, -1)


def get_normal_blocks():
    modifiers = tuple(c.name for c in colors) + woods + stems + materials + tuple(
        s.name for s in stepables) + corals + ('Weathered', 'Oxidized', 'Exposed')
    modifiers = tuple(sorted(set(modifiers), key=lambda x: len(x), reverse=True))
    mod_re = re.compile(r'^(.*? ?)(\b(?:Mossy )?%s\b)($| (.*))' % '|'.join(modifiers))
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
            to_id(w).replace('_lazuli', '').replace('bale', 'block')


normal_blocks = get_normal_blocks()

used_names = {}


def text(txt):
    return r'"\"%s\""' % txt.replace('"', r'\\\"')


def rich_text(txt):
    class ToMinecraftText(HTMLParser):
        def __init__(self):
            super().__init__()
            self.attr_for = {'b': 'bold', 'i': 'italic', 'u': 'underlined', 'strike': 'strikethrough'}
            self.attrs = []
            self.out = []

        def handle_starttag(self, tag, attrs):
            self.attrs.append(self.attr_for[tag])

        def handle_endtag(self, tag):
            self.attrs.remove(self.attr_for[tag])

        def handle_data(self, data):
            node = {'text': '%s' % data}
            for a in self.attrs:
                node[a] = 'true'
            self.out.append(node)

        def result(self):
            return json.dumps(self.out)

    parser = ToMinecraftText()
    parser.feed(txt)
    parser.close()
    s = parser.result()
    return s


def text_attrs(attrs):
    if not attrs:
        return ''
    s = ''
    for k, v in attrs.items():
        s += r',\'%s\':\'%s\'' % (k, v)
    return s


def to_nicknamed(kind, nicknames):
    items = [Nicknamed(n, kind) for n in nicknames]
    return items


def commas(*args):
    return ','.join(list([s for s in args if s]))


def has_loop(rendered):
    return re.search(r'<%base:(loop|bounce|increment)', rendered, flags=re.MULTILINE)


def named_frame_item(block: BlockDef, name=None, damage=None):
    block = good_block(block)
    tag_nbt = Nbt({'display': {'Name': str(JsonText.text(str(name if name else block.name))), }})
    if damage:
        tag_nbt.update(damage)
    return Nbt({'Item': {'id': block.id, 'Count': 1, 'tag': tag_nbt}})


def ensure(pos: Position, block: BlockDef, nbt=None):
    block = good_block(block)
    to_place = block.clone()
    to_place.merge_nbt(nbt)
    return execute().unless().block(pos, block).run(setblock(pos, to_place))


def extract_arg(name, default_value, kwargs, keep=False):
    if name in kwargs:
        value = kwargs[name]
        if not keep:
            del kwargs[name]
    else:
        value = default_value
    return value, kwargs


def _to_iterable(tags):
    if tags is None:
        return tags
    if isinstance(tags, Iterable) and not isinstance(tags, str):
        return tags
    return tuple(tags)


def crops(loop_index: int, stages, crop, pos, name='age'):
    results = []
    x, y, z = pos
    for i in range(0, 3):
        stage = stages[(loop_index + i) % len(stages)]
        results.append(fill(r(x, y, z - i), r(x + 2, y, z - i), Block(crop, {name: stage})))
    stage = stages[(loop_index + 1) % len(stages)]
    text_nbt = Sign.lines_nbt((None, 'Stage: %d' % stages[stage]))
    results.append(data().merge((r(x) + 3, r(2), r(z) - 1), text_nbt))
    return lines(results)


def label(pos: Position, txt: str, facing=1, invis=True, tags=(), block=Block('stone_button')) -> Commands:
    tags = list(tags)
    tags.append('label')
    return (
        execute().positioned(pos).run(
            kill(e().type('item_frame').tag('label').sort(NEAREST).distance((None, 1)).limit(1))),
        summon('item_frame', pos,
               named_frame_item(block, txt).merge(
                   {'Invisible': invis, 'Facing': facing, 'Tags': tags, 'Fixed': True})),
    )


class Clock:
    def __init__(self, name: str, init_speed: int = None):
        self.name = name
        self.time = Score(name, 'clocks')
        self.speed = Score('SPEED_' + name.upper(), 'clocks')
        self.init_speed = init_speed
        self._funcs = []

    @classmethod
    def stop_all_clocks(cls) -> Command:
        return setblock((0, 1, 0), 'redstone_block')

    def add(self, function: Function):
        self._funcs.append(function)

    def tick_cmds(self, other_funcs=()):
        # execute at @e[tag=cage_home] run function restworld:enders/cage_main
        for f in self._funcs:
            yield execute().at(e().tag(self._tag(f))).run(function(f.name))
        yield '\n'
        for f in self._funcs:
            loop_finish = f.name[-len(self.name):] + 'finish'
            if loop_finish in other_funcs:
                yield execute().at(e().tag(self._tag(f))).run(schedule().function(loop_finish, 1))

    @staticmethod
    def _tag(f):
        return f.name.split(':')[-1]


def _to_list(obj):
    if not isinstance(obj, list):
        if isinstance(obj, str):
            return [obj]
        return list(obj)
    return obj


class RoomPack(DataPack):
    base_suffixes = ('tick', 'init', 'enter', 'incr', 'decr', 'cur', 'exit', 'finish')
    base_suffixes_re = re.compile(r'(\w+)_(' + '|'.join(base_suffixes) + ')')

    def __init__(self, name: str, path: Path | str, suffixes: Iterable[str, ...] = None,
                 format_version: int = LATEST_PACK_VERSION, /):
        super().__init__(name, path, format_version)
        if suffixes is None:
            suffixes = RoomPack.base_suffixes
        self._suffixes = suffixes

    @property
    def suffixes(self):
        return self._suffixes


class Room(FunctionSet):
    def __init__(self, name: str, dp: RoomPack, facing: str = None, text: SignText = None, room_name: str = None):
        super().__init__(name, dp.function_set)
        self._pack = dp
        self._clocks = {}
        self._scores = set()
        self._homes = set()
        self._home_stand = Entity('armor_stand', {
            'Tags': ['homer', '%s_home' % self.name], 'NoGravity': True, 'Small': True})
        self.title = None
        self._player_in_room_setup()
        if facing:
            self._room_setup(facing, text, room_name)

    def _player_in_room_setup(self):
        player_home = self.home_func(f'{self.name}_player')
        self.function('_enter', exists_ok=True).add(
            execute().positioned(r(1, -1, 1)).run(function(player_home.full_name)))
        self.function('_exit', exists_ok=True).add(kill(e().tag(f'{self.name}_player_home')))

    def _room_setup(self, facing, text, room_name):
        text = _to_list(text)
        self._record_room(text, room_name)
        text = tuple((JsonText.text(x).bold().italic() if x else x) for x in text)
        sign = WallSign(text)
        facing = good_facing(facing)
        x, z, rot = facing.dx, facing.dz, facing.yaw
        anchor = '%s_anchor' % self.name
        anchor_rot = rotated_facing(facing.name, ROTATION_180)
        stand = Entity('armor_stand',
                       {'Rotation': anchor_rot.rotation, 'Tags': [anchor, 'anchor'], 'Invisible': True, 'Small': True})
        self.add(Function('%s_room_init' % self.name).add(
            sign.place(r(x, 6, z), facing),
            kill(e().tag(anchor)),
            summon(stand, r(0, 2, 0))
        ))
        self.function('_goto').add(
            tp(p(), e().tag(anchor).limit(1))
        )
        self.home_func(self.name + '_room')

    def _record_room(self, text, room_name):
        while len(text) > 0 and text[0] is None:
            text = text[1:]
        if not room_name:
            room_name = text[0]
            if text[0][-1] == '&':
                room_name += ' ' + text[1]
            room_name = room_name.replace(',', '').replace(':', '')
        self.title = room_name

    def home_func(self, name):
        home_marker_comment = 'Default home function'
        marker_tag = '%s_home' % name
        if marker_tag in self.functions:
            f = self.functions[marker_tag]
            for c in f.commands():
                if home_marker_comment in c:
                    return
        marker = deepcopy(self._home_stand)
        tags = marker.nbt.get_list('Tags')
        tags.extend((marker_tag, self.name + '_home', 'homer'))
        return self.function(marker_tag, home=False, exists_ok=True).add(
            comment(home_marker_comment),
            kill(e().tag(marker_tag)),
            execute().positioned(r(-0.5, 0, 0.5)).run(kill(e().type('armor_stand').volume((1, 2, 1)))),
            marker.summon(r(0, 0.5, 0)),
        )

    def mob_placer(self, *args, **kwargs):
        tag_list = kwargs.setdefault('tags', [])
        if not isinstance(tag_list, list):
            tag_list = list(tag_list)
        tag_list.append(self.name)
        kwargs['tags'] = tag_list
        return MobPlacer(*args, **kwargs)

    def function(self, name: str, clock: Clock = None, /, home=True, exists_ok=False) -> Function:
        base_name, name = self._base_name(name, clock)
        if exists_ok and name in self.functions:
            return self.functions[name]
        if home:
            if base_name[0] == '_' or base_name in self._homes:
                home = False
        return self._add_func(Function(name, base_name), name, clock, home)

    def loop(self, name: str, clock: Clock = None, /, home=True, score=None) -> Loop:
        base_name, name = self._base_name(name, clock)
        if not score:
            score = Score(base_name, self.name)
        loop = self._add_func(Loop(score, name=name, base_name=base_name), name, clock, home)
        if not base_name + '_cur' in self.functions:
            self.function(base_name + '_cur').add(loop.cur())
        self._scores.add(loop.score)
        self._scores.add(loop._to_incr)
        return loop

    def _add_func(self, func, name, clock, home):
        base_name, name = self._base_name(name, clock)
        if clock:
            self._clocks.setdefault(clock, []).append(func)
            clock.add(func)

        self.add(func)

        if home and base_name not in self._homes:
            self.home_func(base_name)
        return func

    def add(self, *functions: Function) -> FunctionSet:
        for f in functions:
            if f.name.endswith('_home'):
                self._homes.add(f.name[:-len('_home')])
        return super().add(*functions)

    def _base_name(self, name, clock):
        if not clock:
            base_name = name
        else:
            if not name.endswith('_' + clock.name):
                base_name = name
                name += '_' + clock.name
            else:
                base_name = name[:-len(clock.name) - 1]
            return base_name, name
        if name[0] != '_':
            for s in self._pack.suffixes:
                tail = '_' + s
                if name.endswith(tail):
                    base_name = name[:-len(tail)]
                    break
        return base_name, name

    def finalize(self):
        self.add_room_funcs()

    def add_room_funcs(self):
        self._add_clock_funcs()
        self._add_loop_funcs()
        self._add_other_funcs()

    def _add_clock_funcs(self):
        tick_func = self.function('_tick')
        for clock, loops in self._clocks.items():
            name = '_%s' % clock.name
            clock_func = self.function(name).add((
                execute().at(e().tag(x.base_name + '_home')).run(function(x.full_name)) for x in loops))
            tick_func.add(execute().if_().score(clock.time).matches(0).run(function(clock_func.full_name)))
        tick_func.add(function(x.full_name) for x in filter(
            lambda x: self._is_func_type(x, '_tick'), self.functions.values()))

        finish_funcs = {}
        clock_re = str('(' + '|'.join(x.name for x in self._clocks.keys()) + ')')
        finish_funcs_re = re.compile('(.*)_finish_%s$' % clock_re)
        for f in self.functions.values():
            m = finish_funcs_re.match(f.name)
            if m:
                finish_funcs.setdefault('_finish_' + m.group(2), []).append(f)
        self.function('_finish').add((function(self._path(x)) for x in finish_funcs.keys()))
        for cf in finish_funcs.keys():
            self.function(cf).add((function(x.full_name) for x in finish_funcs[cf]))

    def _path(self, name):
        return self.full_name + '/' + name

    def _add_loop_funcs(self):
        incr_f = self.function('_incr')
        decr_f = self.function('_decr')
        loops = filter(lambda x: isinstance(x, Loop), self.functions.values())
        for loop in loops:
            home_f = loop.base_name + '_home'
            at_home = execute().at(e().tag(home_f))
            incr_f.add(at_home.run(loop.score.add(1)))
            decr_f.add(at_home.run(loop.score.remove(1)))
        cur_f = self.full_name + '/_cur'
        incr_f.add(function(cur_f))
        decr_f.add(function(cur_f))

    def _add_other_funcs(self):
        to_incr = self.score('_to_incr')
        before_commands = {
            'init': [scoreboard().objectives().add(self.name, ScoreCriteria.DUMMY),
                     scoreboard().objectives().add(self.name + '_max', ScoreCriteria.DUMMY),
                     (x.set(0) for x in sorted(self._scores, key=lambda x: str(x))),
                     to_incr.set(1)] + [tp(e().tag(self.name), e().tag('death').limit(1))]}
        after_commands = {
            'enter': [weather(CLEAR)],
            'init': [function('%s/_cur' % self.full_name)],
        }
        clock_suffixes = set(x.name for x in self._clocks)
        clock_suffixes.add('tick')
        for f in self._pack.suffixes:
            if f in clock_suffixes:
                continue
            f_name = '_' + f
            relevant = filter(lambda x: self._is_func_type(x, f_name), self.functions.values())
            commands = []
            commands.extend(before_commands.setdefault(f, []))
            commands.extend(
                (execute().at(e().tag(self._home_func_name(x.name))).run(function(x.full_name)) for x in
                 relevant))
            commands.extend(after_commands.setdefault(f, []))
            if len(commands) > 0:
                self.function(f_name, exists_ok=True).add(*commands)

    @staticmethod
    def _is_func_type(x, f_name):
        return x.name.endswith(f_name) and len(x.name) > len(f_name)

    def score(self, name):
        score = Score(name, self.name)
        self._scores.add(score)
        return score

    def score_max(self, name):
        score = Score(name, '%s_max' % self.name)
        return score

    def _home_func_name(self, base):
        return self.pack._home_func_name(base)


def _name_for(mob):
    if mob.name:
        return mob.name
    return to_name(mob.id)


class MobPlacer:
    _armor_stand_tmpl = Entity('armor_stand').merge_nbt({'Invisible': True, 'Small': True, 'NoGravity': True})

    base_nbt = {'NoAI': True, 'PersistenceRequired': True, 'Silent': True}

    def __init__(self, start: Position, facing: str | float,
                 delta: float | tuple[float, float] = None, kid_delta: float | tuple[float, float] = None, *,
                 tags: Tuple[str, ...] = None,
                 nbt=None, kids=None, adults=None, auto_tag=True):
        self.start = start
        self.nbt = nbt if nbt else Nbt()
        self.tags = _to_iterable(tags)
        if (kids, adults) == (None, None):
            kids, adults = True, True
        elif kids is None:
            kids = False
        elif adults is None:
            adults = False
        self.kids = kids
        self.adults = adults
        self.auto_tag = auto_tag
        if isinstance(facing, str):
            delta = delta if delta else 2
            kid_delta = kid_delta if kid_delta else 1.2
            try:
                if not isinstance(delta, (float, int)) or not isinstance(kid_delta, (float, int)):
                    raise ValueError('Deltas must be floats when using "facing" name')
                self.delta_x, _, self.delta_z = rotated_facing(facing, ROTATION_90).scale(delta)
                kid_rot = rotated_facing(facing)
                self.kid_x, _, self.kid_z = kid_rot.scale(kid_delta)
                self.rotation = kid_rot.yaw
            except KeyError:
                raise ValueError('%s: Unknown "facing" with no "rotation"' % facing)
        else:
            delta = delta if delta else (0, 0)
            kid_delta = kid_delta if kid_delta else (0, 0)
            self.rotation = facing
            self.delta_x, self.delta_z = delta
            self.kid_x, self.kid_z = kid_delta
        self._cur = list(self.start)

    def clone(self) -> MobPlacer:
        return copy.deepcopy(self)

    def summon(self, mobs: Iterable[EntityDef] | EntityDef, *, on_stand: bool | Callable[[Entity], bool] = False,
               tags=None, nbt=None, auto_tag=None) -> Tuple[Command, ...]:
        if isinstance(mobs, (Entity, str)):
            mobs = (mobs,)
        if tags and isinstance(tags, str):
            tags = list(tags)
        for mob in mobs:
            mob = good_entity(mob)
            tmpl = mob.clone()
            if self.nbt:
                tmpl.merge_nbt(self.nbt)
            if nbt:
                tmpl.merge_nbt(nbt)
            tmpl.merge_nbt(MobPlacer.base_nbt)
            tmpl.custom_name(True)
            tmpl.merge_nbt({'Rotation': [self.rotation, 0]})
            tmpl.name = _name_for(mob)
            if self.tags:
                tmpl.tag(*self.tags)
            if tags:
                tmpl.tag(*tags)
            if auto_tag is None:
                auto_tag = self.auto_tag
            if auto_tag:
                tmpl.tag(tmpl.id)

            if self.adults:
                adult = tmpl.clone()
                adult.tag('adult')
                yield self._do_summoning(adult, on_stand, self._cur)
            if self.kids:
                kid = tmpl.clone()
                kid.tag('kid')
                kid.merge_nbt({'IsBaby': True, 'Age': -2147483648})
                pos = self._cur
                if self.adults:
                    pos = pos[0] + self.kid_x, pos[1], pos[2] + self.kid_z
                yield self._do_summoning(kid, on_stand, pos)

            self._cur[0] += self.delta_x
            self._cur[2] += self.delta_z

    @staticmethod
    def _do_summoning(tmpl, on_stand, pos):
        if on_stand:
            stand = MobPlacer._armor_stand_tmpl.clone()
            stand.tag(*tmpl.nbt.get('Tags'))
            tmpl.merge_nbt({'id': tmpl.full_id()})
            stand.nbt.get_list('Passengers').append(tmpl.nbt())
            tmpl = stand
        return tmpl.summon(pos)

    @classmethod
    def adult(cls, which: EntityDef, pos, facing: str | float, **kwargs):
        if isinstance(facing, (float, int)):
            delta = kid_delta = (0, 0)
        else:
            delta = kid_delta = 0
        return MobPlacer(pos, facing, delta, kid_delta, adults=True, **kwargs).summon([which])


def say_score(*scores):
    say = [JsonText.text('scores:')]
    for s in scores:
        s = good_score(s)
        say.append(JsonText.text(str(s.target) + '='))
        say.append(JsonText.score(s))
    return tellraw(a(), *say)


class Wall:
    def __init__(self, width, facing, x, z, used):
        self.width = width
        self.facing = good_facing(facing)
        self.used = used
        self.x = x
        self.z = z

    def signs(self, desc_iter, get_sign):
        dx, _, dz = rotated_facing(self.facing, ROTATION_270).scale(1)
        for y in self.used.keys():
            for h in self.used[y]:
                sign = get_sign(next(desc_iter), self)
                x = self.x + h * dx
                z = self.z + h * dz
                yield sign.place(r(x, y, z), self.facing)


class SignedRoom(Room):
    def __init__(self, name: str, dp: RoomPack, facing, sign_txt, get_sign, signs: Iterable[ActionDesc],
                 walls: Iterable[Wall]):
        super().__init__(name, dp, facing, sign_txt)
        self.get_sign = get_sign
        self.walls = walls
        self.function('signs').add(self.init(signs))

    def init(self, descs):
        i = iter(descs)
        try:
            for w in self.walls:
                yield from w.signs(i, self.get_sign)
        except StopIteration:
            return None
        try:
            desc = next(i)
            raise ValueError('%s...: Remaining descs after all signs are placed' % desc.name)
        except StopIteration:
            return


def span(start, end):
    return range(start, end + 1)


particle_note = {
    'Ambient Entity|Effect': 'ambient',
    'Bubbles|Currents|Whirlpools': 'bubbles',
    'Clouds': 'Evaporation',
    'Dripping Lava': 'Falling, Landing',
    'Dripping Water': 'Falling',
    'Dripping|Obsidian Tear': 'Falling, Landing',
    'Dripping Honey': 'Falling, Landing',
    'Dust': 'Redstone Dust',
    'Fireworks': 'and Flash',
    'Nautilus': 'with Conduit',
    'Poof': 'Small Explosion',
    'Squid Ink': 'and Glow Squid',
    'Wax': 'and Copper'}
particles = [ActionDesc(e, particle_note.get(e, None)) for e in Particle]


def write_function(func_dir, func_name, rendered):
    if not os.path.exists(func_dir):
        os.mkdir(func_dir)
    out_file = os.path.join(func_dir, '%s.mcfunction' % func_name)
    with open(out_file, 'w') as out:
        out.write(rendered.strip() + '\n')
