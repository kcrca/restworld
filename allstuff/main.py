import glob
import os
import sys

from mako.lookup import TemplateLookup
from mako.template import Template

mc_version = '1.13'


class Item:
    def __init__(self, name, id=None, block_state=None):
        if id is None:
            id = to_id(name)
        self.name = name
        self.id = id
        self.block_state = block_state if block_state else ""


class Color(Item):
    def __init__(self, name, rgb, dye_13):
        Item.__init__(self, name)
        self.rgb = rgb
        self.dyes = {'1.13': dye_13, '1.14': '%s_dye' % self.id, 'default': dye_13}

    def dye_name(self):
        try:
            return self.dyes[mc_version]
        except:
            return self.dyes['default']


class CommandBlock(Item):
    def __init__(self, name, conditional):
        Item.__init__(self, name)
        self.conditional = conditional


class Stepable(Item):
    def __init__(self, name, base_id, block=None):
        Item.__init__(self, name)
        self.block = to_id(block) if block else self.id
        self.base_id = to_id(base_id)


def text(txt):
    return r'"\"%s\""' % txt


def to_id(name):
    return name.lower().replace(" ", "_")


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
        Item("Data", "DATA"),
        Item("Save", "SAVE"),
        Item("Load", "LOAD"),
        Item("Corner", "CORNER"),
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

    dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    tmpl_dir = os.path.join(dir, 'templates')
    func_dir = os.path.join(dir, 'functions')
    lookup = TemplateLookup(directories=['.'])
    for tmpl_path in glob.glob(os.path.join(tmpl_dir, "*.mcftmpl")):
        func_name = os.path.splitext(os.path.basename(tmpl_path))[0]
        print '----- %s' % func_name
        var_name = func_name
        if var_name.endswith('_init'):
            var_name = var_name[:-5]
        tmpl = Template(filename=tmpl_path, lookup=lookup)
        rendered = tmpl.render(
            var=var_name,
            Item=Item,
            colors=colors,
            text=text,
            structure_blocks=structure_blocks,
            command_blocks=command_blocks,
            steppables=stepables,
        )
        # print rendered

        with open(os.path.join(func_dir, '%s.mcfunction' % func_name), "w") as out:
            out.write(rendered)


if __name__ == '__main__':
    main()
