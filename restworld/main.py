import collections
import glob
import json
import os
import random
import re
import sys
from functools import total_ordering
from html.parser import HTMLParser

from mako.lookup import TemplateLookup
from mako.template import Template

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

    def sign_text(self, skip=()):
        lines = self.to_sign_text()
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
    Color("Light Gray", 10329495, "light_gray_dye"),
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
woods = ("Acacia", "Birch", "Jungle", "Oak", "Dark Oak", "Spruce")
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
    "Sculk Sensor",
    "Spawner",
))

villager_types = ("Desert", "Jungle", "Plains", "Savanna", "Snow", "Swamp", "Taiga")
villager_data = []
for t in villager_types:
    for p in professions:
        villager_data += ['profession:%s,type:%s' % (p.lower(), t.lower()), ]
    random.shuffle(villager_data)

biome_groups = collections.OrderedDict()
biome_groups['Temperate'] = (
    'Plains', 'Forest', 'Flower Forest', 'Birch Forest', 'Dark Forest', 'Swamp', 'Jungle', 'Mushroom Field')
biome_groups['Warm'] = ('Desert', 'Savanna', 'Badlands')
biome_groups['Cold'] = ('Tiaga', 'Stone Shore')
biome_groups['Snowy'] = ('Snowy Tundra', 'Ice Spikes', 'Snowy Tiaga')
biome_groups['Ocean'] = ('Warm Ocean', 'Ocean', 'Frozen Ocean')
biome_groups['Nether'] = ('Nether Wastes', 'Soul Sand Valley', 'Crimson Forest', 'Warped Forest', 'Basalt Deltas')
biome_groups['End'] = ('The End', 'End Island', 'End City')
biome_groups['Structures'] = ('Mineshaft', 'Monument', 'Stronghold', 'Bastion Remnant', 'Fortress')
biomes = [item for sublist in list(biome_groups.values()) for item in sublist]


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
        **kwargs
    )


def main():
    tmpl_suffix = ".mcftmpl"
    incr_funcs = ("incr", "decr", "cur", "finish")
    speeds = ("main", "fast", "slow")
    misc = ("reset", "cleanup") + incr_funcs
    categories = ("init", "enter", "exit", "tick") + speeds + tuple("finish_%s" % s for s in speeds) + misc
    category_re = re.compile(r"^(([a-z_0-9]+?)(?:_(" + "|".join(categories) + "))?)%s$" % tmpl_suffix)

    src_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    tmpl_dir = os.path.join(src_dir, 'templates')
    func_dir = os.path.join(src_dir, 'functions')
    lookup = TemplateLookup(directories=['.'])
    tmpls = {}
    for f in ("home", "group", "tick") + incr_funcs:
        tmpls[f] = Template(filename="templates/%s%s" % (f, tmpl_suffix), lookup=lookup)

    class Room:
        def __init__(self, dir_name):
            dir_name = dir_name.strip('/')
            self.room_dir = dir_name
            self.name = os.path.basename(dir_name)
            self.func_dir = dir_name.replace('templates', 'functions')
            self.lists = {"exit": []}
            self.vars = set()

        def consume(self, tmpl_path):
            """
            Consume one single template file, remembering whatever type it is.
            :param tmpl_path:
            :return:
            """
            m = category_re.match(os.path.basename(tmpl_path))
            var = m.group(2)
            if var == self.name:
                raise NameError("Cannot name script the same as room name: %s" % var)
            which = m.group(3)
            func = m.group(1)
            tmpl = Template(filename=tmpl_path, lookup=lookup)
            rendered = render_tmpl(tmpl, var, room=self.name)
            write_function(self.func_dir, func, rendered)

            # particle room is just different
            if self.name != 'particles':
                if var in used_names and used_names[var] != self.name:
                    raise NameError("Name collision in two rooms: %s in %s, %s" % (var, self.name, used_names[var]))
                used_names[var] = self.name

            write_function(self.func_dir, "%s_home" % var, tmpls["home"].render(var=var, room=self.name))
            if which in speeds and not os.path.exists(tmpl_path.replace("_%s." % which, "_cur.")):
                rendered = render_tmpl(tmpl, var, suppress_loop=True, room=self.name)
                write_function(self.func_dir, "%s_cur" % var, rendered)

            if which and which not in misc:
                self.vars.add(var)
                entry = [var, ]
                try:
                    self.lists[which] += entry
                except KeyError:
                    self.lists[which] = entry

        def generate(self):
            """
            Generate all the files for a single room (directory). First generate any specified templates. Next
            consume all the files, then generate all the room-wide files.
            :return:
            """
            self.run_shell_scripts()
            for tmpl_path in sorted(glob.glob(os.path.join(self.room_dir, "*%s" % tmpl_suffix))):
                self.consume(tmpl_path)
            on_tick = []
            after_tick = []
            for which in self.lists:
                files = self.lists[which]
                rendered = tmpls["group"].render(room=self.name, funcs=files, which=which, vars=self.vars)
                write_function(self.func_dir, "_%s" % which, rendered)
                if which[-4:] in speeds:
                    if len(which) == 4:
                        on_tick += [which, ]
                    else:
                        after_tick += [which[-4:], ]
            if on_tick or after_tick:
                rendered = tmpls["tick"].render(room=self.name, on_tick=on_tick, after_tick=after_tick)
                write_function(self.func_dir, "_tick", rendered)
                rendered = tmpls["finish"].render(room=self.name, on_tick=on_tick, after_tick=after_tick)
                write_function(self.func_dir, "_finish", rendered)
            for func in incr_funcs:
                if func == "finish":
                    continue
                rendered = tmpls[func].render(room=self.name, vars=self.vars)
                write_function(self.func_dir, "_%s" % func, rendered)
            rendered = tmpls["home"].render(var="finis", room=self.name)
            write_function(func_dir, "finish_home", rendered)

        def run_shell_scripts(self):
            """
            Run any shell scripts in the dir before generating templates. This is used to work around the fact that
            Minecraft equates one function per file, so to generate multiple functions, I have to generate multiple
            files. This seemed like a job for shell scripts.

            I thought of doing this using mako to generate mako templates, but the quoting issues....
            """
            for script in glob.glob(os.path.join(self.room_dir, "*.py]")):
                if exec(compile(open(script, "rb").read(), script, 'exec')) != 0:
                    sys.exit(-1)

    rooms = []
    for room_dir in glob.glob(os.path.join(tmpl_dir, '*/')):
        room = Room(room_dir)
        room.generate()
        rooms += [room.name, ]

    for f in incr_funcs + ("init",):
        write_function(func_dir, "_%s" % f, "\n".join("function restworld:%s/_%s" % (r, f) for r in rooms))

    def sign_room(name, things, walls, button=False):
        return room_signs('%s/%s' % (func_dir, name),
                          name,
                          Template(filename="%s/%s_sign%s" % (tmpl_dir, name, tmpl_suffix), lookup=lookup),
                          sorted(things, key=lambda x: x.name.replace('|', ' ')),
                          walls,
                          (1, 1.5, -1),
                          button)

    sign_room("particles", particles, (
        Wall(7, 5, "east", (-1, 0)),
        Wall(7, 7, "south", (0, -1), y_first=4),
        Wall(7, 5, "west", (1, 0)),
        Wall(7, 5, "north", (0, 1)),
    ), button=True)
    commands = sign_room("effects", effects, (
        Wall(7, 5, "east", (-1, 0), used_widths=(3, 5, 3)),
        Wall(7, 5, "south", (0, -1), used_widths=(5, 5), y_first=2),
        Wall(7, 5, "west", (1, 0), used_widths=(3, 5, 3)),
        Wall(7, 5, "north", (0, 1)),
    ))
    all_effects = []
    for c in commands:
        if " air " in c:
            continue
        elif " oak_wall_sign" in c:
            all_effects.append(re.sub("oak_wall_sign.*", "emerald_block", c).replace(" ^0 ", " ^1 "))
        else:
            all_effects.append(c)
    write_function("%s/%s" % (func_dir, "effects"), "effects_all_shown", "\n".join(all_effects) + "\n")


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
)


class Wall:
    def __init__(self, width, used, facing, block_at, y_first=3, y_last=1, used_widths=None):
        self.width = width
        self.facing = facing
        self.block_at = block_at
        self.start = int((width - used) / 2)
        self.end = width - self.start
        self.y_first = y_first
        self.y_last = y_last
        if used_widths is None:
            used_widths = (used,) * 10
        self.used_widths = used_widths
        self.line = 0
        self.set_line_range()

    def set_line_range(self):
        self.start = int((self.width - self.used_widths[self.line]) / 2)
        self.end = self.width - self.start

    def to_next_wall(self, tag):
        return "execute as @e[tag=%s] run execute at @s run teleport @s ^-%d ^0 ^0 ~90 ~" % (
            tag, self.width - 1)

    def start_pos(self):
        return self.start, self.y_first

    def next_pos(self, x, y):
        # The top row is sparse
        x += 1
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
        commands.append("execute at @e[tag=%s] run setblock ^%d ^%d ^%d stone_button[facing=south]" % (
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
