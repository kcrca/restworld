import collections
import fnmatch
import glob
import os
import re
import sys

from mako.lookup import TemplateLookup
from mako.template import Template

mc_version = '1.13'


class Thing:
    def __init__(self, name, id=None, block_state=None):
        self.name = name.strip()  # This allows a "%s Minecart" % "" to work
        if id is None:
            id = to_id(self.name.strip())
        self.id = to_id(id.strip())
        self.block_state = block_state if block_state else ""

    def __repr__(self):
        return self.name;

    def full_id(self):
        id = "minecraft:%s" % self.id
        if self.block_state:
            id += "[%s]" % self.block_state
        return id


class Nicknamed(Thing):
    def __init__(self, nickname, kind, id=None, block_state=None):
        Thing.__init__(self, ("%s %s" % (nickname, kind)).strip(), id, block_state)
        self.nickname = nickname
        self.kind = kind


class Color(Thing):
    _next_color = 0

    def __init__(self, name, rgb, dye_13):
        Thing.__init__(self, name)
        self.rgb = rgb
        self.dyes = {'1.13': dye_13, '1.14': '%s_dye' % self.id, 'default': dye_13}
        self.color_num = Color._next_color
        Color._next_color += 1

    def dye_name(self):
        try:
            return self.dyes[mc_version]
        except:
            return self.dyes['default']


class Horse(Thing):
    def __init__(self, name, variant=None):
        if variant is not None:
            Thing.__init__(self, name, "horse")
            self.tag = "%s_horses" % to_id(name)
        else:
            Thing.__init__(self, name)
            self.tag = "%ss" % self.id
        self.variant = variant


class CommandBlock(Thing):
    def __init__(self, name, conditional):
        Thing.__init__(self, name)
        self.conditional = conditional


class Stepable(Thing):
    def __init__(self, name, base_id, block=None):
        Thing.__init__(self, name)
        self.block = to_id(block) if block else self.id
        self.base_id = to_id(base_id)


class Effect(Thing):
    def __init__(self, name, id=None, note=None):
        Thing.__init__(self, name.replace('|', ' '), id)
        self.note = "(%s)" % note if note else None
        self.text = name

    def sign_text(self):
        t = self.text.split("|")
        if self.note:
            t += self.note.split("|")
        return t


def text(txt):
    return r'"\"%s\""' % txt


def to_id(name):
    return name.lower().replace(" ", "_")


def to_nicknamed(kind, nicknames):
    items = [Nicknamed(n, kind) for n in nicknames]
    return items


def has_loop(rendered):
    return re.search(r'<%base:(loop|bounce|increment)', rendered, flags=re.MULTILINE)


def main():
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
        Color("Black", 1908001, "ink_sack"),
    )
    structure_blocks = (
        Thing("Data", "DATA"),
        Thing("Save", "SAVE"),
        Thing("Load", "LOAD"),
        Thing("Corner", "CORNER"),
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
        Stepable("Brick", "Terracotta", block="Bricks"),
        Stepable("Purpur", "air", block="Purpur Block"),
        Stepable("Prismarine", "air"),
        Stepable("Prismarine Brick", "air", block="Prismarine Bricks"),
        Stepable("Dark Prismarine", "air"),
    )
    woods = ("Acacia", "Birch", "Jungle", "Oak", "Dark Oak", "Spruce")
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

    def find_files(dir, pat):
        for root, dirnames, filenames in os.walk(dir):
            for filename in fnmatch.filter(filenames, pat):
                yield os.path.join(root, filename)

    def render_templ(tmpl, **kwargs):
        return tmpl.render(
            var=var_name,
            func=var_name,
            Thing=Thing,
            colors=colors,
            structure_blocks=structure_blocks,
            command_blocks=command_blocks,
            steppables=stepables,
            woods=woods,
            fishes=fishes,
            horses=horses,
            other_horses=other_horses,
            small_flowers=small_flowers,
            tulips=tulips,
            text=text,
            to_nicknamed=to_nicknamed,
            to_id=to_id,
            **kwargs
        )

    dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    tmpl_dir = os.path.join(dir, 'templates')
    func_dir = os.path.join(dir, 'functions')
    lookup = TemplateLookup(directories=['.'])
    vars = []
    tmpl_suffix = ".mcftmpl"
    for tmpl_path in sorted(find_files(tmpl_dir, "*%s" % tmpl_suffix)):
        func_name = os.path.splitext(os.path.basename(tmpl_path))[0]
        if func_name == "init":
            continue
        print '----- %s' % func_name
        var_name = func_name
        if var_name.endswith('_init'):
            var_name = var_name[:-5]
        tmpl = Template(filename=tmpl_path, lookup=lookup)
        rendered = render_templ(tmpl)
        dir = os.path.dirname(tmpl_path.replace(tmpl_dir, func_dir))
        write_function(dir, func_name, rendered)
        if not func_name.endswith("init") and has_loop(tmpl.source):
            rendered = render_templ(tmpl, suppress_loop=True)
            write_function(dir, func_name + "_cur", rendered)
        vars.append(var_name)

    init_tmpl = Template(filename=os.path.join(tmpl_dir, "init.mcftmpl"), lookup=lookup)
    write_function(func_dir, "init", init_tmpl.render(vars=vars))
    effect_signs(func_dir + "/effects")


def effect_function(effect):
    base = "function allstuff:effect/%s_%%s" % effect.id
    return "\n".join(base % f for f in ("init", "fast", "main", "slow"))


def effect_signs(func_dir):
    effects = (
        Effect("Ambient Entity|Effect", "ambient"), Effect("Angry Villager"),
        Effect("Bubbles|and|Whirlpools", "bubbles"),
        Effect("Clouds", note="Evaporation"), Effect("Crit"), Effect("Damage Indicator"), Effect("Dolphin"),
        Effect("Dragon Breath"), Effect("Dripping Lava"), Effect("Dripping Water"),
        Effect("Dust", note="Redstone Dust"),
        Effect("Effect"), Effect("Elder Guardian"), Effect("Enchant"), Effect("Enchanted Hit"), Effect("End Rod"),
        Effect("Entity Effect"), Effect("Explosion"), Effect("Falling Dust"), Effect("Fireworks"), Effect("Fishing"),
        Effect("Flame"), Effect("Happy Villager"), Effect("Heart"), Effect("Explosion Emitter"),
        Effect("Instant Effect"),
        Effect("Item Slime"), Effect("Item Snowball"), Effect("Large Smoke"), Effect("Lava"), Effect("Mycelium"),
        Effect("Nautilus"), Effect("Note"), Effect("Poof", note="Small Explosion"), Effect("Portal"), Effect("Rain"),
        Effect("Smoke"), Effect("Snow"), Effect("Splash"), Effect("Squid Ink"), Effect("Sweep Attack"),
        Effect("Totem of Undying"), Effect("Underwater"), Effect("Witch"),
    )

    per_x = (5, 5, 5, 5)
    widths = (7, 7, 7, 7)
    # per_x = (5, 7, 5, 2)
    # widths = (7, 7, 7, 2)
    # per_x = (1, 2, 1)
    # widths = (2, 2, 2)
    facings = ("east", "south", "west", "north")
    frame = 0

    def enter_frame():
        x = (widths[frame] - per_x[frame]) / 2
        return (x, x + per_x[frame], 3, facings[frame])

    kill_command = "kill @e[type=armor_stand,distance=..10]"
    commands = [
        kill_command,
        "summon minecraft:armor_stand ~1 ~0.5 ~-1 {Tags:[signer],Rotation:[90f,0f],ArmorItems:[{},{},{},{id:turtle_helmet,Count:1}]}",
        "execute at @e[tag=signer] run fill ^0 ^0 ^0 ^-6 ^4 ^-6 air",
    ]
    (first_x, end_x, y, facing) = enter_frame()
    x = first_x
    print "effects #", len(effects)
    for i, effect in enumerate(sorted(effects)):
        sign_text = effect.sign_text()
        sign_nbt = r'Text2:"{\"text\":\"%s\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/%s\"}}"' % (
            sign_text[0], effect.id)
        for i, line in enumerate(sign_text[1:]):
            sign_nbt += ",Text%d:%s" % (i + 3, text(line))
        commands.append(
            "execute at @e[tag=signer] run setblock ^%d ^%d ^ wall_sign[facing=%s]{%s}" % (-x, y, facing, sign_nbt))
        write_function(func_dir, effect.id, effect_function(effect))
        x += 1
        if x >= end_x:
            y -= 1
            if y < 1:
                commands.append(
                    "execute as @e[tag=signer] run execute at @s run teleport @s ^-%d ^0 ^0 ~90 ~" % (
                            widths[frame] - 1))
                frame += 1
                (first_x, end_x, y, facing) = enter_frame()
            x = first_x

    commands.append(kill_command)

    write_function(func_dir, 'signs', "\n".join(commands))


def write_function(func_dir, func_name, rendered):
    if not os.path.exists(func_dir):
        os.mkdir(func_dir)
    out_file = os.path.join(func_dir, '%s.mcfunction' % func_name)
    with open(out_file, "w") as out:
        out.write(rendered)


if __name__ == '__main__':
    main()
