from __future__ import annotations

import collections
from copy import deepcopy
from functools import total_ordering
from html.parser import HTMLParser

from pyker.function import *
from pyker.simpler import Sign, WallSign, Book


def to_id(name):
    return name.lower().replace(" ", "_")


@total_ordering
class Thing:
    def __init__(self, name, id=None, block_state=None):
        self.text = name
        self.name = name.replace("|", " ").strip()  # This allows a "%s Minecart" % "" to work
        if id is None:
            id = to_id(self.name.strip())
        self.id = to_id(id.strip())
        self.block_state = block_state if block_state else ""

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.full_id() < other.full_id()

    def __eq__(self, other):
        return self.full_id() == other.full_id()

    def full_id(self, block_state=""):
        id = "%s" % self.id
        state = self.block_state + ("," if block_state and self.block_state else "") + block_state
        if state:
            id += "[%s]" % state
        return id

    def sign_text(self, pre=None, skip=()):
        lines = self.to_sign_text()
        if pre:
            lines = [pre, ] + lines
        if len(lines) == 4:
            start = 0
        else:
            start = 1
            lines = ["", ] + lines
        while len(lines) < 4:
            lines += ("",)
        s = ''
        for i in range(0, 4):
            if i not in skip:
                if len(s) > 0:
                    s += ','
                s += "Text%d:%s" % (i + 1, text(lines[i]))
        return s

    def to_sign_text(self):
        lines = self.text.split("|")
        return lines


class Nicknamed(Thing):
    def __init__(self, nickname, kind, id=None, block_state=None):
        Thing.__init__(self, ("%s %s" % (nickname, kind)).strip(), id, block_state)
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
            Thing.__init__(self, name, "horse")
            self.tag = "%s_horses" % to_id(name)
        else:
            Thing.__init__(self, name)
            self.tag = "%ss" % self.id
        self.variant = variant


class Mob(Thing):
    def __init__(self, name, id=None, nbt=None, can_fly=False, acquatic=False):
        Thing.__init__(self, name, id=id)
        self.nbt = nbt
        self.can_fly = can_fly
        self.acquatic = acquatic

    def inner_nbt(self):
        if not self.nbt:
            return ""
        return ",%s" % self.nbt


class CommandBlock(Thing):
    def __init__(self, name, conditional):
        Thing.__init__(self, name)
        self.conditional = conditional


class Stepable(Thing):
    def __init__(self, name, base_id, block=None):
        Thing.__init__(self, name)
        self.block = to_id(block) if block else self.id
        self.base_id = to_id(base_id)


class ActionSign(Thing):
    def __init__(self, name, id=None, note=None, priority=None, comment=None):
        Thing.__init__(self, name, id)
        self.note = "(%s)" % note if note else None

    def to_sign_text(self):
        t = super(ActionSign, self).to_sign_text()
        if self.note:
            t += self.note.split("|")
        return t

    def __cmp__(self, other):
        my_text = ' '.join(self.to_sign_text())
        other_text = ' '.join(other.to_sign_text())
        return cmp(my_text, other_text)


colors = (
    Color("White", 0xf9fffe),
    Color("Orange", 0xf9801d),
    Color("Magenta", 0xc74ebd),
    Color("Light Blue", 0x3ab3da),
    Color("Yellow", 0xfed83d),
    Color("Lime", 0x80c71f),
    Color("Pink", 0xf38baa),
    Color("Gray", 0x474f52),
    Color("Light Gray", 0x9d9d97),
    Color("Cyan", 0x169c9c),
    Color("Purple", 0x8932b8),
    Color("Blue", 0x3c44aa),
    Color("Brown", 0x835432),
    Color("Green", 0x5e7c16),
    Color("Red", 0xb02e26),
    Color("Black", 0x1d1d21),
)
command_blocks = (
    CommandBlock("Command Block", True),
    CommandBlock("Command Block", False),
    CommandBlock("Chain Command Block", False),
    CommandBlock("Chain Command Block", True),
    CommandBlock("Repeating Command Block", True),
    CommandBlock("Repeating Command Block", False),
    CommandBlock("Command Block", False),
    CommandBlock("Command Block", True),
    CommandBlock("Chain Command Block", True),
    CommandBlock("Chain Command Block", False),
    CommandBlock("Repeating Command Block", False),
    CommandBlock("Repeating Command Block", True),
)
stepables = (
    Stepable("Sandstone", "Sand"),
    Stepable("Red Sandstone", "Red Sand"),
    Stepable("Quartz", "Nether Quartz Ore", block="Quartz Block"),
    Stepable("Cobblestone", "Stone"),
    Stepable("Stone Brick", "Stone", block="Stone Bricks"),
    Stepable("Nether Brick", "Netherrack", block="Nether Bricks"),
    Stepable("Brick", "Clay", block="Bricks"),
    Stepable("Purpur", "air", block="Purpur Block"),
    Stepable("Prismarine", "air"),
    Stepable("Prismarine Brick", "air", block="Prismarine Bricks"),
    Stepable("Dark Prismarine", "air"),
)
materials = (
    'Iron', 'Coal', 'Copper', 'Gold', 'Diamond', 'Emerald', 'Chainmail', 'Redstone', 'Lapis Lazuli', 'Granite',
    'Andesite', 'Diorite', 'Netherite', 'Blackstone', 'Stone', 'Cobblestone', 'End Stone', 'Sandstone', 'Red Sandstone',
    'Bone', 'Honey', 'Honeycomb', 'Grass', 'Sticky', 'Nether')
corals = ('Horn', 'Tube', 'Fire', 'Bubble', 'Brain')
woods = ("Acacia", "Birch", "Jungle", "Mangrove", "Oak", "Dark Oak", "Spruce")
stems = ("Warped", "Crimson")
fish_data = (
    ("kob",
     (917504, "Red-White Kob"),
     (65536, "Orange-White Kob"),
     ),
    ("sunstreak",
     (134217984, "White-Silver Sunstreak"),
     (50790656, "Gray-Sky SunStreak"),
     (118161664, "Blue-Gray SunStreak"),
     ),
    ((235340288, "Gray-Red Snooper"),),
    ("dasher",
     (117441280, "White-Gray Dasher"),
     (101253888, "Teal-Rose Dasher"),
     ),
    ("brinely",
     (117441536, "White-Gray Brinely"),
     (50660352, "Line-Sky Dasher"),
     ),
    ("spotty",
     (67110144, "White-Yellow Spotter"),
     (50726144, "Rose-Sky Spotty"),
     ),
    ("flopper",
     (117899265, "Gray Flopper"),
     (67108865, "White-Yellow Flopper"),
     ),
    ("stripey",
     (117506305, "Orange-Gray Stripey"),
     (67371265, "Yellow Stripey"),
     ),
    ((117441025, "White-Gray Glitter"),),
    ("blockfish",
     (67764993, "Plum-Yellow Blockfish"),
     (918273, "Red-White Blockfish"),
     ),
    ((918529, "Red-White Betty"),),
    ("clayfish",
     (234882305, "White-Red Clayfish"),
     (16778497, "White-Orange Clayfish"),
     ),
)
fishes = []
for f in fish_data:
    if len(f) == 1:
        fishes.append((re.sub(r'[- ]', '_', f[0][1].lower()), f))
    else:
        fishes.append((f[0], list(v for v in f[1:])))
horses = (
    Horse("White", 0),
    Horse("Creamy", 1),
    Horse("Chestnut", 2),
    Horse("Brown", 3),
    Horse("Black", 4),
    Horse("Gray", 5),
    Horse("Dark Brown", 6),
)
other_horses = (
    Horse("Mule"),
    Horse("Donkey"),
    Horse("Skeleton Horse"),
    Horse("Zombie Horse"),
)
small_flowers = (
    Thing("Allium"),
    Thing("Azure Bluet"),
    Thing("Blue Orchid"),
    Thing("Dandelion"),
    Thing("Oxeye Daisy"),
    Thing("Poppy"),
)
tulips = (
    "Red",
    "Orange",
    "Pink",
    "White",
)
professions = (
    "Armorer",
    "Butcher",
    "Cartographer",
    "Cleric",
    "Farmer",
    "Fisherman",
    "Fletcher",
    "Leatherworker",
    "Librarian",
    "Mason",
    "Nitwit",
    "Shepherd",
    "Toolsmith",
    "Weaponsmith",
    "Unemployed",
)
patterns = (
    ("", "None"), ("drs", "Down Right Stripe"), ("dls", "Down Left Stripe"), ("cr", "Cross"),
    ("bs", "Bottom Stripe"), ("ms", "Middle Stripe"), ("ts", "Top Stripe"), ("sc", "Square Cross"),
    ("ls", "Left Stripe"), ("cs", "Center Stripe"), ("rs", "Right Stripe"), ("ss", "Small Stripes"),
    ("ld", "Left Diagonal"), ("rud", "Right Upside-Down|Diagonal"), ("lud", "Left Upside-Down|Diagonal"),
    ("rd", "Right Diagonal"),
    ("vh", "Vertical Half|(Left)"), ("vhr", "Vertical Half|(Right)"), ("hhb", "Horizontal Half|(Bottom)"),
    ("hh", "Horizontal Half|(Top)"),
    ("bl", "Bottom Left|Corner"), ("br", "Bottom Right|Corner"), ("tl", "Top Left|Corner"),
    ("tr", "Top Right|Corner"),
    ("bt", "Bottom Triangle"), ("tt", "Top Triangle"), ("bts", "Bottom Triangle|Sawtooth"),
    ("tts", "Top Triangle|Sawtooth"),
    ("mc", "Middle Circle"), ("mr", "Middle Rhombus"), ("bo", "Border"), ("cbo", "Curly Border"),
    ("gra", "Gradient"), ("gru", "Gradient|Upside-Down"), ("cre", "Creeper"), ("bri", "Brick"),
    ("sku", "Skull"), ("flo", "Flower"), ("moj", "Mojang"), ("glb", "Globe"), ("pig", "Pig"),
)
moon_phases = (
    (206000, "Full"),
    (38000, "Waning Gibbous"),
    (62000, "Three Quarters"),
    (86000, "Waning Crescent"),
    (110000, "New"),
    (134000, "Waxing Crescent"),
    (158000, "First Quarter"),
    (182000, "Waxing Gibbous"),
)
non_inventory = tuple(Thing(s) for s in (
    "Knowledge Book",
    "Debug Stick",
    "Suspicious Stew",
    "Firework Star",
    "Bundle",
    "Jigsaw",
    "Structure Block",
    "Structure Void",
    "Barrier",
    "Light",
    "Dragon Egg",
    "Command Block",
    "Command Block Minecart",
    "Spawner",
    "Elytra",
))

villager_types = ("Desert", "Jungle", "Plains", "Savanna", "Snow", "Swamp", "Taiga")
villager_data = []
for t in villager_types:
    for p in professions:
        villager_data += ['profession:%s,type:%s' % (p.lower(), t.lower()), ]
    # random.shuffle(villager_data)

biome_groups = collections.OrderedDict()
biome_groups['Temperate'] = (
    'Plains', 'Forest', 'Flower Forest', 'Birch Forest', 'Dark Forest', 'Swamp', 'Jungle', 'Mushroom Field')
biome_groups['Warm'] = ('Desert', 'Savanna', 'Badlands')
biome_groups['Cold'] = ('Tiaga', 'Stone Shore')
biome_groups['Snowy'] = ('Snowy Tundra', 'Ice Spikes', 'Snowy Tiaga')
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
        block = block_re.sub(r'\1 Block', block)  # "Block of Foo" -> "Foo Block"
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
            # "M" to move it away from corals so the water trough behind the coral doesn't overlap
            name = 'MGlass ' + name
        elif 'Copper' in block and 'Deepslate' not in block and name not in ('Ore', 'Raw Block'):
            name = 'Copper'

        if name not in blocks:
            blocks[name] = []
        blocks[name] += (block,)
    for b in sorted(blocks):
        for w in sorted(blocks[b]):
            yield w.lower().replace(' ', '_').replace('_lazuli', '').replace('bale', 'block')


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
                node[a] = "true"
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
        return ""
    s = ""
    for k, v in attrs.items():
        s += r',\"%s\":\"%s\"' % (k, v)
    return s


def to_nicknamed(kind, nicknames):
    items = [Nicknamed(n, kind) for n in nicknames]
    return items


def commas(*args):
    return ",".join(list([s for s in args if s]))


def has_loop(rendered):
    return re.search(r'<%base:(loop|bounce|increment)', rendered, flags=re.MULTILINE)


def render_tmpl(tmpl, var_name, **kwargs):
    return tmpl.render(
        var=var_name,
        func=var_name,
        Thing=Thing,
        Mob=Mob,
        colors=colors,
        command_blocks=command_blocks,
        steppables=stepables,
        woods=woods,
        stems=stems,
        fishes=fishes,
        horses=horses,
        other_horses=other_horses,
        small_flowers=small_flowers,
        tulips=tulips,
        patterns=patterns,
        professions=professions,
        text=text,
        rich_text=rich_text,
        text_attrs=text_attrs,
        to_nicknamed=to_nicknamed,
        to_id=to_id,
        commas=commas,
        villager_data=villager_data,
        villager_types=villager_types,
        biome_groups=biome_groups,
        biomes=biomes,
        normal_blocks=normal_blocks,
        effects=effects,
        moon_phases=moon_phases,
        non_inventory=non_inventory,
        coloring_coords=coloring_coords,
        **kwargs
    )


def kill_em(target):
    return mc.tp().to(entities().tag('death').limit(1), target)


def named_frame_item(thing: Thing, name=None, damage=None):
    # <%def name="named_frame_item(thing, name=None, damage=None)">Item:{id:${thing.id},Count:1,tag:{display:{Name:'{"text":"${name if name else thing.name}"}'}${damage if damage else ""}}},Fixed:True</%def>
    tag_nbt = Nbt({'display': {'Name': {'"text"': '"' + str(name if name else thing.name) + '"'}, }})
    if damage:
        tag_nbt.update(damage)
    return Nbt({'Item': {'id': thing.id, 'Count': 1, 'tag': tag_nbt}})


rooms = ('funcs')


def ensure(x, y, z, block, nbt=None):
    mc.execute().unless().block(x, y, z, block).run().setblock(x, y, z, block).nbt(
        Nbt.as_nbt(nbt)
    )


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
    return (tags,)


def crops(loop_index: int, stages, crop, x, y, z, name='age'):
    results = []
    for i in range(0, 3):
        stage = stages[(loop_index + i) % len(stages)]
        results.append(mc.fill(r(x), r(y), r(z) - i, r(x) + 2, r(y), r(z) - i, Block(crop, {name: stage})))
    stage = stages[(loop_index + 1) % len(stages)]
    text_nbt = Sign.lines_nbt((None, 'Stage: %d' % stages[stage]))
    results.append(mc.data().merge(BlockData(r(x) + 3, r(2), r(z) - 1), text_nbt))
    return lines(results)


#     return mc.execute().positioned(x, y, z).run().kill(entities().type('item_frame').tag('label'),sort=NEAREST,limit=1)
def label(x: Coord, y: Coord, z: Coord, txt: str, facing) -> Commands:
    return (
        mc.execute().positioned(x, y, z).run().
            kill(entities().type('item_frame').tag('label'), sort=NEAREST, limit=1),
        mc.summon('item_frame', x, y, z,
                  {'Invisible': True, 'Facing': facing, 'Tags': [label, named_frame_item(Thing('stone_button'), txt)]}),
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
        return mc.setblock(0, 1, 0, 'redstone_block')

    def add(self, function: Function):
        self._funcs.append(function)

    def tick_cmds(self, other_funcs=()):
        # execute at @e[tag=cage_home] run function restworld:enders/cage_main
        for f in self._funcs:
            yield mc.execute().at(entities().tag(self._tag(f))).run().function(f.name)
        yield '\n'
        for f in self._funcs:
            loop_finish = f.name[-len(self.name):] + 'finish'
            if loop_finish in other_funcs:
                yield mc.execute().at(entities().tag(self._tag(f))).run(). \
                    schedule().function(loop_finish, 1).replace()

    def _tag(self, f):
        return f.name.split(':')[-1]


def _to_list(text):
    if not isinstance(text, list):
        if isinstance(text, str):
            return [text]
        return list(text)
    return text


class Restworld(DataPack):
    def __init__(self, dir: str):
        super().__init__('restworld', dir, 4)
        self._suffixes = ['tick', 'init', 'enter', 'incr', 'decr', 'cur', 'exit', 'finish']
        self._suffixes.extend(list(x.name for x in self.clocks()))

    def finalize(self):
        for kid in self.function_set.children():
            if isinstance(kid, Room):
                kid.finalize()

    def save(self):
        self.finalize()
        gs = self.function_set.child('global')
        if gs is None:
            gs = FunctionSet('global', self.function_set)
        gs.add(self.control_book_func())
        self.function_set.add(*self.world_funcs())
        super().save()

    def clocks(self):
        return (slow_clock, main_clock, fast_clock)

    def control_book_func(self) -> Function:
        cb = Book()
        cb.sign('Control Book', 'Restworld', 'Useful Commands')

        cb.add(r'Clock State:\\n      ',
               self._action(r'|\\u25c0\\u25c0', 'Previous', '_decr').extra('  '),
               self._action(r'||', 'Play/Pause', 'global/clock_toggle').bold(),
               self._action(r'/\\u25b6', 'Play/Pause', 'global/clock_toggle').extra('  '),
               self._action(r'\\u25b6\\u25b6|', 'Next', '_incr').extra(r'\\n', r'\\nClock Speed:\\n      '),
               self._action(r'<<', 'Slower Clock Speed', 'center/slower_clocks').extra('   '),
               self._action(r'\\u27f2', 'Reset Clock Speed', 'center/reset_clocks').extra('   '),
               self._action(r'>>', 'Faster Clock Speed', 'center/faster_clocks').extra(r'\\n', r'\\nPlaces:\\n   '),
               self._action('Home', 'Starting Point', 'global/go_home').extra(r'\\n   '),
               self._action('Photo Shoot', 'Scenic View', 'global/go_photo').extra(r'\\n   '),
               self._action('Battle Arena', 'Battle Arena', 'arena/go_arena').extra(r'\\n   '),
               self._action('Biome Sampler', 'Biome Sampler', 'global/go_biomes').extra(r'\\n   '),
               self._action('Connected Textures', 'Connected Textures', 'global/go_connected').extra(r'\\n   '),
               self._action('Nether Home', 'Nether Starting Point', 'global/go_nether_home').extra(r'\\n   '),
               self._action('End Home', 'End Starting Point', 'global/go_end_home').extra(r'\\n   '),
               )

        cb.next_page()
        cb.add(r'Click on room name to go there: \\n\\n')
        rooms = filter(lambda x: isinstance(x, Room) and x.title is not None, self.function_set.children())
        rooms = sorted(rooms, key=lambda x: x.title)
        first = True
        for r in rooms:
            if first:
                first = False
            else:
                cb.add(', ')
            cb.add(self._action(r.title, r.title, r.name + '/_goto'))

        cb.next_page()
        cb.add(
            r'Credits:\\n\\n',
            JsonText.text(r'BlueMeanial:\\n').bold(),
            r'  Command Blocks\\n  Software Design\\n  Programming\\n\\n',
            JsonText.text(r'JUMBOshrimp277:\\n').bold(),
            r'  World Design\\n  Testing\\n  Rubber Duck\\n',
            r'\\nMinecraft Version:\\n   1.19, May 2022',
        )

        return Function('control_book').add(mc.give(player(), cb.item()))

    def _action(self, txt: str, tooltip: str, act: str, more=None) -> JsonText:
        return JsonText.text(txt).color(DARK_GREEN).underlined().click_event().run_command(
            mc.function('restworld:' + act)).hover_event().show_text(tooltip)

    def _home_func_name(self, base):
        for f in self._suffixes:
            if base.endswith('_' + f):
                base = base[:-(len(f) + 1)]
                break
        return base + '_home'

    def world_funcs(self):
        for f in self._suffixes:
            fname = '_' + f
            func = Function(fname)
            for room in self.function_set.children():
                func.add(
                    list(mc.function(x.full_name) for x in filter(lambda x: x.name == fname, room.functions()))
                )
            yield func


class Room(FunctionSet):
    def __init__(self, name: str, dp: DataPack, facing: str = None, text: SignText = None):
        super().__init__(name, dp.function_set)
        self._pack = dp
        self._clocks = {}
        self._home_stand = Entity('armor_stand', {
            'tags': ['homer', '%s_homer' % self.name], 'NoGravity': True, 'Small': True})
        self.title = None
        if facing:
            self._room_sign(facing, text)

    def _room_sign(self, facing, text):
        text = _to_list(text)
        self._record_room(text)
        text = tuple((JsonText.text(x).bold().italic() if x else x) for x in text)
        sign = WallSign(text)
        x, z, rot, _ = facing_info(facing)
        # I think this score is unused, but not sure, so I'm commenting it out.
        # score = Score('ancient', 'goto')
        self.add(Function('%s_room_init' % self.name).add(
            sign.place(*r(x, 6, z), facing),
            # score.init(),
            # score.set(rot),
        ))
        self.add(self.home_func(self.name + '_room'))

    def _record_room(self, text):
        while len(text) > 0 and text[0] is None:
            text = text[1:]
        room_name = text[0]
        if text[0][-1] == '&':
            room_name += ' ' + text[1]
        room_name = room_name.replace(',', '').replace(':', '')
        self.title = room_name

    def home_func(self, name):
        marker_tag = '%s_home' % name
        marker = deepcopy(self._home_stand)
        tags = marker.nbt().get_list('Tags')
        tags.append(marker_tag)
        return Function(marker_tag).add(
            mc.kill(entities().tag(marker_tag)),
            mc.execute().positioned(r(-0.5), r(0), r(0.5)).run().
                kill(entities().type('armor_stand').delta(1, 2, 1)),
            marker.summon(r(0), r(0.5), r(0)),
        )

    def loop(self, name: str, clock: Clock = None, needs_home=True) -> Loop:
        loop = Loop(name, self.name)
        if clock:
            self._clocks.setdefault(clock, []).append(loop)
            name += '_' + clock.name
            clock.add(loop)

        self.add(loop)

        if needs_home:
            self.add(self.home_func(loop.name))
        return loop

    def finalize(self):
        self.add(*(self.room_funcs()))

    def room_funcs(self):
        return list(self._functions) + list(self._room_funcs())

    def _room_funcs(self):
        yield from self._yield_clock_funcs()
        yield from self._yield_loop_funcs()
        yield from self._yield_other_funcs()

    def _yield_clock_funcs(self):
        tick_func = Function('_tick')
        for clock, loops in self._clocks.items():
            name1 = '_' + clock.name
            yield Function(name1)
            name = '_%s' % clock.name
            tick_func.add(
                mc.execute().if_().score(clock.time).matches(0).run().function(name))
        # The '1' is for the generated warning
        if len(list(tick_func.commands())) > 1:
            yield tick_func
        finish_funcs = {}
        clock_re = str('(' + '|'.join(x.name for x in self._clocks.keys()) + ')')
        finish_funcs_re = re.compile('(.*)_finish_%s$' % clock_re)
        for f in self._functions:
            m = finish_funcs_re.match(f.name)
            if m:
                finish_funcs.setdefault('_finish_' + m.group(2), []).append(f)
        yield Function('_finish').add((mc.function(x) for x in finish_funcs.keys()))
        for cf in finish_funcs.keys():
            yield Function(cf).add((mc.function(x) for x in finish_funcs))

    def _homes(self):
        return filter(lambda x: x.name.endswith('_home'), self._functions)

    def _yield_loop_funcs(self):
        loops = filter(lambda x: isinstance(x, Loop), self._functions)
        homes = self._homes()
        for loop in loops:
            name = loop.name + '_cur'
            yield Function(name)
            yield Function('_cur').add(
                (mc.execute().at(entities().tag(x)).run().function(loop.name) for x in homes),
                mc.function('_finish'))
            yield Function('_incr').add(
                (mc.execute().at(entities().tag(x)).run(loop.score.add(1)) for x in homes),
                mc.function('_cur'))
            yield Function('_decr').add(
                (mc.execute().at(entities().tag(x)).run(loop.score.remove(1)) for x in homes),
                mc.function('_cur'))

    def _yield_other_funcs(self):
        added_commands = {}
        added_commands['_enter'] = (mc.weather(CLEAR),)
        for f in self._pack._suffixes:
            f_name = '_' + f
            relevant = filter(lambda x: self.is_f(x, f_name), self._functions)
            func = Function(f_name)
            func.add((mc.execute().at(entities().tag(self._home_func_name(x.name))).run().function(x.full_name) for x in
                      relevant))
            func.add(added_commands.setdefault(f, tuple()))
            if len(func.commands()) > 1:
                yield func

    def is_f(self, x, f_name):
        return x.name.endswith(f_name)

    def score(self, name):
        return Score(name, self.name)

    def _home_func_name(self, base):
        return self.pack._home_func_name(base)


class MobPlacer:
    _armor_stand_tmpl = Entity('armor_stand').merge_nbt({'Invisible': True, 'Small': True, 'NoGravity': True})

    def __init__(self,
                 start_x: Coord, start_y: Coord, start_z: Coord,
                 mob_facing: str,
                 delta: float = 2, kid_delta: float = 1.2, *,
                 tags: Tuple[str, ...] = None,
                 nbt=None, kids=None, adults=None, auto_tag=True):
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
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
        try:
            self.delta_x, self.delta_z, self.rotation, _ = facing_info(mob_facing, delta)
            self.kid_x, self.kid_z, _, _ = facing_info(mob_facing, kid_delta, ROTATION_90)
        except KeyError:
            raise ValueError('%s: Unknown dir' % mob_facing)
        self._cur = [start_x, start_y, start_z]

    def summon(self, mobs: Iterable[EntityDef] | EntityDef, *, on_stand: bool | Callable[Entity] = False) -> Tuple[
        Command, ...]:
        if isinstance(mobs, (Entity, str)):
            mobs = (mobs,)
        for mob in mobs:
            mob = good_entity(mob)
            tmpl = mob.clone()
            if self.nbt:
                tmpl.merge_nbt(self.nbt)
            rotation___ = {'NoAI': True, 'PersistenceRequired': True, 'Silent': True, 'Rotation': [self.rotation, 0.0]}
            tmpl.merge_nbt(
                rotation___)
            tmpl.set_name_visible(True)
            if self.tags:
                tmpl.tag(*self.tags)
            if self.auto_tag:
                tmpl.tag(tmpl.kind)

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

    def _do_summoning(self, tmpl, on_stand, pos):
        if on_stand:
            stand = MobPlacer._armor_stand_tmpl.clone()
            stand.tag(*tmpl.nbt().get('Tags'))
            tmpl.merge_nbt({'id': tmpl.full_id()})
            stand.nbt().get_list('Passengers').append(tmpl.nbt())
            tmpl = stand
        return tmpl.summon(*pos)


class Fencelike:
    @classmethod
    def update(self, id, text2, text3='') -> Commands:
        return (
            mc.fill(*r(8, 3, 6, 0, 2, 0), id, REPLACE).filter('#restworld:fencelike'),
            mc.data().merge(BlockData(*r(5, 2, 0)), Sign.lines_nbt(('', text2, text3, '')))
        )


def say_score(*scores):
    say = []
    say.append(JsonText.text("scores:"))
    for s in scores:
        s = good_score(s)
        say.append(JsonText.text(str(s.target) + '='))
        say.append(JsonText.score(s))
    return mc.tellraw(all(), *say)


clock = Clock('clock')
slow_clock = Clock('slow', 90)
main_clock = Clock('main', 60)
fast_clock = Clock('fast', 15)
tick_clock = Clock('clock')
restworld = Restworld('/Users/kcrca/clarity/home/saves/NewRest')


def ancient_room():
    Room('ancient', restworld, NORTH, (None, 'Warden')).add(
        Function('warden_mob_init').add((MobPlacer(*r(0, 2, 0), WEST, adults=True).summon('warden'),)),
    )


def global_room():
    def use_min_fill(y, filler, fillee):
        # execute at @e[tag=min_home] run fill ~0 ${y} ~0 ~166 ${y} ~180 ${filler}                                                  |
        return mc.execute().at(entities().tag('min_hom')).run().fill(r(0), y, r(0), r(166), y, r(180), filler,
                                                                     REPLACE).filter(fillee)

    def clock_lights(turn_on):
        lights = ('red_concrete', 'lime_concrete')
        before = lights[int(turn_on)]
        after = lights[1 - int(turn_on)]
        return (
            use_min_fill(100, after, before),
            mc.execute().at(entities().tag('min_home')).run().setblock(0, 105, -78, after)
        )

    def kill_if_time():
        ex = mc.execute()
        for c in restworld.clocks():
            ex = ex.unless().score(c.time).matches((0, 1))
        return ex.run().function('restworld:global/kill_em')

    room = Room('global', restworld)
    clock_toggle = room.score('clock_toggle')
    room.add(
        Function('arena').add(
            mc.execute().in_(OVERWORLD).run().tp().pos(1126, 103, 1079, player()).facing(1139, 104, 1079), ),
        room.home_func('clock'),
        Function('clock_init').add(
            mc.scoreboard().objectives().remove('clocks'),
            mc.scoreboard().objectives().add('clocks', ScoreCriteria.DUMMY),
            list(c.speed.set(c.init_speed) for c in restworld.clocks()),
            list(c.time.set(-1) for c in restworld.clocks()),
            tick_clock.time.set(0),
            mc.function('restworld:global/clock_off'),
        ),
        Function('clock_on').add(
            mc.execute().at(entities().tag('clock_home')).run().setblock(*r(0, -2, 1), 'redstone_block')),
        Function('clock_off').add(
            mc.execute().at(entities().tag('clock_home')).run().setblock(*r(0, -2, 1), 'diamond_block')),
        Function('clock_switched_on').add(
            clock_lights(True)),
        Function('clock_switched_off').add(
            clock_lights(False),
            (c.time.operation(EQ, c.speed) for c in restworld.clocks()),
            (c.time.remove(1) for c in restworld.clocks()),
        ),
        Function('clock_toggle').add(
            clock_toggle.set(0),
            mc.execute().at(entities().tag('clock_home')).if_().block(*r(0, -2, 1), 'redstone_block').run(
                clock_toggle.set(1)),
            mc.execute().if_().score(clock_toggle).matches(0).run().function('restworld:global/clock_on'),
            mc.execute().if_().score(clock_toggle).matches(1).run().function('restworld:global/clock_off'),
        ),
        Function('clock_tick').add(
            clock.time.add(1),
            (c.time.operation(EQ, clock.time) for c in restworld.clocks()),
            (c.time.operation(MOD, c.speed) for c in restworld.clocks()),
            kill_if_time()
        ),
    )


def main():
    for f in (ancient_room, global_room):
        f()
    restworld.save()


particles = [
    ActionSign("Ambient Entity|Effect", "ambient"),
    ActionSign("Angry Villager"),
    ActionSign("Ash"),
    ActionSign("Barrier", priority=2, comment="not hard to find"),
    ActionSign("Bubbles|Currents|Whirlpools", "bubbles"),
    ActionSign("Clouds", note="Evaporation"),
    ActionSign("Composter"),
    ActionSign("Crimson Spore"),
    ActionSign("Crit"),
    ActionSign("Damage Indicator"),
    ActionSign("Dolphin"),
    ActionSign("Dragon Breath"),
    ActionSign("Dripping Lava", note="Falling, Landing"),
    ActionSign("Dripping Water", note="Falling"),
    ActionSign("Dripping|Obsidian Tear", note="Falling, Landing"),
    ActionSign("Dripping Honey", note="Falling, Landing"),
    ActionSign("Dust", note="Redstone Dust"),
    ActionSign("Effect"),
    ActionSign("Electric Spark"),
    ActionSign("Enchant"),
    ActionSign("Enchanted Hit"),
    ActionSign("End Rod"),
    ActionSign("Entity Effect"),
    ActionSign("Explosion"),
    ActionSign("Explosion Emitter"),
    ActionSign("Falling Dust"),
    ActionSign("Falling Nectar", priority=2, comment="shown with bees"),
    ActionSign("Fireworks", note="and Flash"),
    ActionSign("Fishing"),
    ActionSign("Flame", priority=2, comment="seen with blocks"),
    ActionSign("Happy Villager"),
    ActionSign("Heart"),
    ActionSign("Instant Effect"),
    ActionSign("Item Slime"),
    ActionSign("Item Snowball"),
    ActionSign("Large Smoke"),
    ActionSign("Lava", priority=2, comment="seen in materials, with ores"),
    ActionSign("Light"),
    ActionSign("Mycelium", priority=2, comment="seen in plants"),
    ActionSign("Nautilus", note="with Conduit"),
    ActionSign("Poof", note="Small Explosion"),
    ActionSign("Sculk Sensor"),
    ActionSign("Sculk Soul"),
    ActionSign("Shriek"),
    ActionSign("Smoke", priority=2, comment="seen with items in blocks"),
    ActionSign("Sneeze"),
    ActionSign("Snow and Rain"),
    ActionSign("Soul"),
    ActionSign("Spit"),
    ActionSign("Spore Blossom"),
    ActionSign("Splash"),
    ActionSign("Squid Ink", note="and Glow Squid"),
    ActionSign("Sweep Attack"),
    ActionSign("Totem of Undying"),
    ActionSign("Underwater"),
    ActionSign("Wax", note="and Copper"),
    ActionSign("Warped Spore"),
    ActionSign("White Ash"),
    ActionSign("Witch"),
]
particles.sort()

effects = (
    ActionSign("Speed"),
    ActionSign("Slowness", note="Negative"),
    ActionSign("Haste"),
    ActionSign("Mining Fatigue", note="Negative"),
    ActionSign("Strength"),
    ActionSign("Weakness", note="Negative"),
    ActionSign("Instant Health"),
    ActionSign("Instant Damage", note="Negative"),
    ActionSign("Jump Boost"),
    ActionSign("Nausea", note="Negative"),
    ActionSign("Regeneration"),
    ActionSign("Resistance"),
    ActionSign("Fire Resistance"),
    ActionSign("Water Breathing"),
    ActionSign("Invisibility"),
    ActionSign("Blindness", note="Negative"),
    ActionSign("Night Vision"),
    ActionSign("Hunger", note="Negative"),
    ActionSign("Poison", note="Negative"),
    ActionSign("Wither", note="Negative"),
    ActionSign("Health Boost"),
    ActionSign("Absorption"),
    ActionSign("Saturation"),
    ActionSign("Glowing", note="Neutral"),
    ActionSign("Levitation", note="Negative"),
    ActionSign("Luck"),
    ActionSign("Bad Luck", id="unluck", note="Negative"),
    ActionSign("Slow Falling"),
    ActionSign("Conduit Power"),
    ActionSign("Dolphin's Grace", id="dolphins_grace"),
    ActionSign("Bad Omen", note="Negative"),
    ActionSign("Hero|of the Village"),
    ActionSign("Darkness"),
)


class Wall:
    def __init__(self, width, used, facing, block_at, y_first=3, y_last=1, used_widths=None, start=None, skip=None):
        self.width = width
        self.provided_start = start
        self.facing = facing
        self.block_at = block_at
        self.y_first = y_first
        self.y_last = y_last
        if used_widths is None:
            used_widths = (used,) * 10
        self.used_widths = used_widths
        self.skip = skip if skip else {}
        self.line = 0
        self.set_line_range()

    def set_line_range(self):
        self.start = self.provided_start
        if not self.start:
            self.start = int((self.width - self.used_widths[self.line]) / 2)
        self.end = self.start + self.used_widths[self.line]

    def to_next_wall(self, tag):
        return "execute as @e[tag=%s] run execute at @s run teleport @s ^-%d ^0 ^0 ~90 ~" % (
            tag, self.width - 1)

    def start_pos(self):
        return self.start, self.y_first

    def next_pos(self, x, y):
        # The top row is sparse
        x += 1
        try:
            skip = self.skip[y]
            while skip and x - self.start in range(skip[0], skip[1] + 1):
                x += 1
        except KeyError:
            pass
        if y == 4 and x == 3:
            # Skip the middle position
            x += 1
        if x >= self.end:
            self.line += 1
            if self.line >= len(self.used_widths):
                return None, None
            self.set_line_range()
            y -= 1
            x = self.start
            if y < self.y_last:
                return None, None
        return x, y


def write_function(func_dir, func_name, rendered):
    if not os.path.exists(func_dir):
        os.mkdir(func_dir)
    out_file = os.path.join(func_dir, '%s.mcfunction' % func_name)
    with open(out_file, "w") as out:
        out.write(rendered.strip() + "\n")


if __name__ == '__main__':
    main()
