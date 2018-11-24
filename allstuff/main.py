import glob
import os
import re
import sys

from mako.lookup import TemplateLookup
from mako.template import Template

mc_version = '1.13'


class Thing:
    def __init__(self, name, id=None, block_state=None):
        if id is None:
            id = to_id(name)
        self.name = name
        self.id = id
        self.block_state = block_state if block_state else ""

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


def text(txt):
    return r'"\"%s\""' % txt


def to_id(name):
    return name.lower().replace(" ", "_")


def to_nicknamed(kind, nicknames):
    items = [Nicknamed(n, kind) for n in nicknames]
    return items


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
    for tmpl_path in sorted(glob.glob(os.path.join(tmpl_dir, "*.mcftmpl"))):
        func_name = os.path.splitext(os.path.basename(tmpl_path))[0]
        if func_name == "init":
            continue
        print '----- %s' % func_name
        var_name = func_name
        if var_name.endswith('_init'):
            var_name = var_name[:-5]
        tmpl = Template(filename=tmpl_path, lookup=lookup)
        rendered = render_templ(tmpl)
        write_function(func_dir, func_name, rendered)
        if not func_name.endswith("init"):
            rendered = render_templ(tmpl, suppress_loop=True)
            write_function(func_dir, func_name + "_cur", rendered)
        vars.append(var_name)

    init_tmpl = Template(filename=os.path.join(tmpl_dir, "init.mcftmpl"), lookup=lookup)
    write_function(func_dir, "init", init_tmpl.render(vars=vars))


def write_function(func_dir, func_name, rendered):
    with open(os.path.join(func_dir, '%s.mcfunction' % func_name), "w") as out:
        out.write(rendered)


if __name__ == '__main__':
    main()
