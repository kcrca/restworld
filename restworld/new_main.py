from __future__ import annotations

import collections
from copy import deepcopy
from functools import total_ordering

from pyker.function import *

mc_version = '1.14'


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

    def __init__(self, name, rgb, dye_13):
        Thing.__init__(self, name)
        self.rgb = rgb
        self.dyes = {'1.13': dye_13, '1.14': '%s_dye' % self.id, 'default': dye_13}
        self.id = name.replace(' ', '_').lower()
        self.color_num = Color.next_color_num
        Color.next_color_num += 1

    def dye_name(self):
        try:
            return self.dyes[mc_version]
        except KeyError:
            return self.dyes['default']

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
    Color("White", 16383998, "bone_meal"),
    Color("Orange", 16351261, "orange_dye"),
    Color("Magenta", 13061821, "magenta_dye"),
    Color("Light Blue", 3847130, "light_blue_dye"),
    Color("Yellow", 16701501, "dandelion_yellow"),
    Color("Lime", 8439583, "lime_dye"),
    Color("Pink", 15961002, "pink_dye"),
    Color("Gray", 4673362, "gray_dye"),
    Color("Light Gray", 10329495, "light_g/ray_dye"),
    Color("Cyan", 1481884, "cyan_dye"),
    Color("Purple", 8991416, "purple_dye"),
    Color("Blue", 3949738, "lapis_lazuli"),
    Color("Brown", 8606770, "cocoa_beans"),
    Color("Green", 6192150, "cactus_green"),
    Color("Red", 11546150, "rose_red"),
    Color("Black", 1908001, "ink_sac"),
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
    def __init__(self, name: str):
        self.name = name
        self.score = Score(name, 'clocks')
        self._loops = []

    @classmethod
    def stop_all_clocks(cls) -> Command:
        return mc.setblock(0, 1, 0, 'redstone_block')

    def add(self, loop: Loop):
        self._loops.append(loop)

    def tick_cmds(self, other_funcs=()):
        # execute at @e[tag=cage_home] run function restworld:enders/cage_main
        for loop in self._loops:
            yield mc.execute().at(entities().tag(self._tag(loop))).run().function(loop.name)
        yield '\n'
        for loop in self._loops:
            loop_finish = loop.name[-len(self.name):] + 'finish'
            if loop_finish in other_funcs:
                yield mc.execute().at(entities().tag(self._tag(loop))).run(). \
                    schedule().function(loop_finish, 1).replace()

    def _tag(self, loop):
        return loop.name.split(':')[-1]


class Room:
    def __init__(self, name: str):
        self.name = name
        self.solo_name = name.split(':')[-1]
        self._funcs = {}
        self._loops = {}
        self._clocks = {}
        self._homes = set()
        self._home_marker = Entity('armor_stand', {
            'tags': ['homer', '%s_homer' % self.name], 'NoGravity': True, 'Small': True})

    def _func(self, name):
        return self.name + '/' + name

    def _home_func(self, name):
        marker_tag = '%s_home' % name
        marker = deepcopy(self._home_marker)
        tags = marker.nbt().get_list('Tags')
        tags.append(marker_tag)
        assert marker_tag not in self._homes
        self._homes.add(marker_tag)
        return Function(self._func(marker_tag)).add(
            mc.kill(entities().tag(marker_tag)),
            mc.execute().positioned(r(-0.5), r(0), r(0.5)).run().
                kill(entities().type('armor_stand').delta(1, 2, 1)),
            marker.summon(r(0), r(0.5), r(0)),
        )

    def loop(self, name: str, clock: Clock = None, needs_home=True) -> Loop:
        base = name
        loop = Loop(base, self.solo_name)
        if clock:
            self._clocks.setdefault(clock, []).append(loop)
            name += '_' + clock.name
            clock.add(loop)

        self._loops[name] = loop

        if needs_home:
            self.add(self._home_func(loop.name))
        return loop

    def add(self, *funcs: Function):
        for f in funcs:
            self._funcs[f.name] = f

    def functions(self):
        return list(self._funcs.values()) + list(self._room_funcs())

    def _room_funcs(self):
        tick_func = Function(self._func('_tick'))
        for clock, loops in self._clocks.items():
            yield Function(self._func('_' + clock.name), clock.tick_cmds())
            # execute if score main clocks matches 0 run function restworld:enders/_main
            tick_func.add(
                mc.execute().if_().score(clock.score).matches(0).run().function(self._func('_%s' % clock.name)))
        # The '1' is for the generated warning
        if len(list(tick_func.commands())) > 1:
            yield tick_func
        for loop_name in self._loops.keys():
            loop = self._loops[loop_name]
            yield Function(self._func(loop.name), loop.commands())
            yield Function(self._func(loop.name + '_cur'), loop.cur())
            yield Function(self._func('_cur')).add(
                (mc.execute().at(entities().tag(x)).run().function(self._func(loop_name)) for x in self._homes),
                mc.function(self._func('_finish')))
            yield Function(self._func('_incr')).add(
                (mc.execute().at(entities().tag(x)).run(loop.score.add(1)) for x in self._homes),
                mc.function(self._func('_cur')))
            yield Function(self._func('_decr')).add(
                (mc.execute().at(entities().tag(x)).run(loop.score.remove(1)) for x in self._homes),
                mc.function(self._func('_cur')))

        finish_funcs = {}
        clock_re = str('(' + '|'.join(x.name for x in self._clocks.keys()) + ')' )
        finish_funcs_re = re.compile('(.*)_finish_%s$' % clock_re)
        for f in self._funcs.keys():
            m = finish_funcs_re.match(f)
            if m:
                finish_funcs.setdefault('_finish_' + m.group(2), []).append(f)
        yield Function(self._func('_finish')).add((mc.function(x) for x in finish_funcs.keys()))
        for cf in finish_funcs.keys():
            yield Function(self._func(cf)).add((mc.function(x) for x in finish_funcs))

        added_commands = {}
        added_commands['_enter'] = (mc.weather(CLEAR),)
        for f in ('init', 'enter', 'exit'):
            f_name = '_' + f
            relevant_funcs = filter(lambda x: x.endswith(f_name), self._funcs.keys())
            func = Function(self._func(f_name))
            if relevant_funcs:
                func.add((mc.execute().at(entities().tag(x)).run().function(self._funcs[x]) for x in relevant_funcs))
            func.add(added_commands.setdefault(f, tuple()))
            cmds = func.commands()
            if cmds:
                yield func


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


room_names = set()


def record_room(text):
    while len(text) > 0 and text[0] is None:
        text = text[1:]
    room_name = text[0]
    if text[0][-1] == '&':
        room_name += ' ' + text[1]
    room_name = room_name.replace(',', '').replace(':', '')
    room_names.add(room_name)


def room_sign(facing, text):
    record_room(text)
    text = tuple((JsonText.text(x).bold().italic() if x else x) for x in text)
    sign = WallSign(text)
    x, z, rot, _ = facing_info(facing)
    score = Score('ancient', 'goto')
    return (
        sign.place(*r(x, 6, z), facing),
        score.init(),
        score.set(rot),
    )


def main():
    rooms = {}
    restworld = DataPack('restworld', '/tmp/r')
    room = Room('restworld:ancient')
    rooms['warden'] = room
    rm = rooms['warden']
    rm.add(
        Function('warden_mob_init').add((MobPlacer(*r(0, 2, 0), WEST, adults=True).summon('warden'),)),
        Function('warden_room_init').add(room_sign(WEST, (None, 'Warden'))),
    )
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


def room_signs(func_dir, room, sign_tmpl, subjects, walls, start, button=False):
    cur_wall = 0
    wall = walls[cur_wall]
    tag = '%s_signer' % room
    kill_command = "kill @e[tag=%s]" % tag
    top = walls[0].y_first + 1
    depth = walls[1].width - 1
    width = walls[0].width - 1
    commands = [
        kill_command,
        "summon armor_stand ~%f ~%f ~%f {Tags:[%s],Rotation:[90f,0f],ArmorItems:[{},{},{},{id:turtle_helmet,Count:1}]}" % tuple(
            start + (tag,)),
        "execute at @e[tag=%s] run fill ^0 ^0 ^0 ^%d ^%d ^%d air replace oak_wall_sign" % (
            tag, -depth, top, -width),
    ]
    if button:
        commands.append("execute at @e[tag=%s] run setblock ^%d ^%d ^%d stone_button[mob_facing=south]" % (
            tag, -depth, top, -width / 2))
    x, y = wall.start_pos()
    for i, subj in enumerate(subjects):
        sign_text = subj.to_sign_text()
        lines = ["", ] + sign_text + [""] * (max(0, 3 - len(sign_text)))
        commands.append(sign_tmpl.render(room=room, subj=subj, lines=lines, x=-x, y=y, z=0, wall=wall).strip())
        x, y = wall.next_pos(x, y)
        if x is None:
            commands.append(wall.to_next_wall(tag))
            cur_wall += 1
            wall = walls[cur_wall]
            x, y = wall.start_pos()
    commands.append(kill_command)
    write_function(func_dir, "signs", "\n".join(commands) + "\n")
    return commands


def write_function(func_dir, func_name, rendered):
    if not os.path.exists(func_dir):
        os.mkdir(func_dir)
    out_file = os.path.join(func_dir, '%s.mcfunction' % func_name)
    with open(out_file, "w") as out:
        out.write(rendered.strip() + "\n")


if __name__ == '__main__':
    main()