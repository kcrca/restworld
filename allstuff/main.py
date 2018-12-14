import fnmatch
import glob
import os
import re
import sys

from mako.lookup import TemplateLookup
from mako.template import Template

mc_version = '1.13'


def render_templ(tmpl, var_name, **kwargs):
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
        Stepable("Brick", "Clay", block="Bricks"),
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
    professions = ("Farmer", "Librarian", "Priest", "Smith", "Butcher", "Nitwit")

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
        professions=professions,
        text=text,
        to_nicknamed=to_nicknamed,
        to_id=to_id,
        **kwargs
    )


class Thing:
    def __init__(self, name, id=None, block_state=None):
        self.name = name.strip()  # This allows a "%s Minecart" % "" to work
        if id is None:
            id = to_id(self.name.strip())
        self.id = to_id(id.strip())
        self.block_state = block_state if block_state else ""

    def __repr__(self):
        return self.name

    def full_id(self, block_state=""):
        id = "minecraft:%s" % self.id
        state = self.block_state + ("," if block_state and self.block_state else "") + block_state
        if state:
            id += "[%s]" % state
        return id


class Nicknamed(Thing):
    def __init__(self, nickname, kind, id=None, block_state=None):
        Thing.__init__(self, ("%s %s" % (nickname, kind)).strip(), id, block_state)
        self.nickname = nickname
        self.kind = kind


class Color(Thing):
    def __init__(self, name, rgb, dye_13):
        Thing.__init__(self, name)
        self.rgb = rgb
        self.dyes = {'1.13': dye_13, '1.14': '%s_dye' % self.id, 'default': dye_13}

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


class Particles(Thing):
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
    tmpl_suffix = ".mcftmpl"
    func_suffix = ".mcfunction"
    speeds = ("main", "fast", "slow")
    misc = ("reset", "cleanup", "cur", "incr", "decr")
    categories = ("init", "enter", "exit", "tick") + speeds + tuple("finish_%s" % s for s in speeds) + misc
    category_re = re.compile(r"^(([a-z_0-9]+?)(?:_(" + "|".join(categories) + "))?)%s$" % tmpl_suffix)

    def find_files(dir, pat):
        for root, dirnames, filenames in os.walk(dir):
            for filename in fnmatch.filter(filenames, pat):
                yield os.path.join(root, filename)

    dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    tmpl_dir = os.path.join(dir, 'templates')
    func_dir = os.path.join(dir, 'functions')
    lookup = TemplateLookup(directories=['.'])
    tmpls = {}
    for f in ("home", "group", "tick", "incr", "decr", "cur"):
        tmpls[f] = Template(filename="templates/%s%s" % (f, tmpl_suffix), lookup=lookup)
    incr_funcs = ("incr", "decr", "cur")

    class Room:
        def __init__(self, dir):
            dir = dir.strip('/')
            self.dir = dir
            self.name = os.path.basename(dir)
            self.func_dir = dir.replace('templates', 'functions')
            self.lists = {"enter": []}
            self.vars = set()

        def consume(self, tmpl_path):
            m = category_re.match(os.path.basename(tmpl_path))
            var = m.group(2)
            which = m.group(3)
            func = m.group(1)
            tmpl = Template(filename=tmpl_path, lookup=lookup)
            rendered = render_templ(tmpl, var)
            write_function(self.func_dir, func, rendered)

            # The particles room is just special
            if room.name == 'particles':
                return

            write_function(self.func_dir, "%s_home" % var, tmpls["home"].render(var=var))
            if which in speeds and not os.path.exists(tmpl_path.replace("_%s." % which, "_cur.")):
                rendered = render_templ(tmpl, var, suppress_loop=True)
                write_function(self.func_dir, "%s_cur" % var, rendered)

            if which and which not in misc:
                self.vars.add(var)
                entry = [var, ]
                try:
                    self.lists[which] += entry
                except KeyError:
                    self.lists[which] = entry

        def generate(self):
            for tmpl_path in sorted(glob.glob(os.path.join(self.dir, "*%s" % tmpl_suffix))):
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
            for f in incr_funcs:
                rendered = tmpls[f].render(room=self.name, vars=self.vars)
                write_function(self.func_dir, "_%s" % f, rendered)

    rooms = []
    for room_dir in glob.glob(os.path.join(tmpl_dir, '*/')):
        room = Room(room_dir)
        room.generate()
        rooms += [room.name, ]

    for f in incr_funcs:
        write_function(func_dir, "_%s" % f, "\n".join("function v3:%s/_%s" % (r, f) for r in rooms))

    # for tmpl_path in sorted(find_files(tmpl_dir, "*%s" % tmpl_suffix)):
    #     func_name = os.path.splitext(os.path.basename(tmpl_path))[0]
    #     if func_name in ("init", 'base', 'a_sign'):
    #         continue
    #     var_name = func_name
    #     if var_name.endswith('_init'):
    #         var_name = var_name[:-5]
    #     tmpl = Template(filename=tmpl_path, lookup=lookup)
    #     rendered = render_templ(tmpl, var_name)
    #     dir = os.path.dirname(tmpl_path.replace(tmpl_dir, func_dir))
    #     write_function(dir, func_name, rendered)
    #     if not func_name.endswith("init") and has_loop(tmpl.source):
    #         rendered = render_templ(tmpl, var_name, suppress_loop=True)
    #         write_function(dir, func_name + "_cur", rendered)
    #     if var_name in vars and var_name == func_name:
    #         raise BaseException("Duplicate script/var name: %s" % var_name)
    #     vars.append(var_name)
    #
    # init_tmpl = Template(filename=os.path.join(tmpl_dir, "init.mcftmpl"), lookup=lookup)
    # write_function(func_dir, "init", init_tmpl.render(vars=vars))
    particles_dir = func_dir + "/particles"
    particle_signs(particles_dir, Template(filename="%s/particles_sign.mcftmpl" % tmpl_dir, lookup=lookup))


particles = (
    Particles("Ambient Entity|Effect", "ambient"), Particles("Angry Villager"),
    Particles("Bubbles|and|Whirlpools", "bubbles"), Particles("Clouds", note="Evaporation"), Particles("Crit"),
    Particles("Damage Indicator"), Particles("Dolphin"), Particles("Dragon Breath"), Particles("Dripping Lava"),
    Particles("Dripping Water"), Particles("Dust", note="Redstone Dust"), Particles("Effect"),
    Particles("Elder Guardian"), Particles("Enchant"), Particles("Enchanted Hit"), Particles("End Rod"),
    Particles("Entity Effect"), Particles("Explosion"), Particles("Falling Dust"), Particles("Fireworks"),
    Particles("Fishing"), Particles("Flame"), Particles("Happy Villager"), Particles("Heart"),
    Particles("Explosion Emitter", note="Large Explosion"), Particles("Instant Effect"), Particles("Item Slime"),
    Particles("Item Snowball"), Particles("Large Smoke"), Particles("Lava"), Particles("Mycelium"),
    Particles("Nautilus"), Particles("Note"), Particles("Poof", note="Small Explosion"), Particles("Portal"),
    Particles("Rain|(Unimplemented)"), Particles("Smoke"), Particles("Snow|(Unimplemented)"), Particles("Spit"),
    Particles("Splash"), Particles("Squid Ink"), Particles("Sweep Attack"), Particles("Totem of Undying"),
    Particles("Underwater"), Particles("Witch"),
)


def particles_function(particle):
    base = "function allstuff:particle/%s_%%s" % particle.id
    return "\n".join(base % f for f in ("init", "fast", "main", "slow")) + "\n"


class Frame:
    def __init__(self, width, used, facing, block_at):
        self.width = width
        self.used = used
        self.facing = facing
        self.block_at = block_at
        self.start = (width - used) / 2
        self.end = width - self.start

    def to_next_wall(self):
        return "execute as @e[tag=signer] run execute at @s run teleport @s ^-%d ^0 ^0 ~90 ~" % (
                self.width - 1)


def particle_signs(func_dir, sign_tmpl):
    frames = (
        Frame(7, 5, "east", (-1, 0)),
        Frame(7, 5, "south", (0, -1)),
        Frame(7, 5, "west", (1, 0)),
        Frame(7, 5, "north", (0, 1)),
    )
    cur_frame = 0
    frame = frames[cur_frame]

    kill_command = "kill @e[tag=signer]"
    commands = [
        kill_command,
        "summon minecraft:armor_stand ~1 ~1.5 ~-1 {Tags:[signer],Rotation:[90f,0f],ArmorItems:[{},{},{},{id:turtle_helmet,Count:1}]}",
        "execute at @e[tag=signer] run fill ^0 ^0 ^0 ^-6 ^3 ^-6 air",
    ]
    x = frame.start
    y = 3
    for i, particle in enumerate(sorted(particles)):
        sign_text = particle.sign_text()
        lines = ["", ] + sign_text + [""] * (max(0, 3 - len(sign_text)))
        commands.append(sign_tmpl.render(particle=particle, lines=lines, x=-x, y=y, frame=frame).strip())
        # write_function(func_dir, particle.id, particle_function(particle))
        x += 1
        if x >= frame.end:
            y -= 1
            if y < 1:
                commands.append(frame.to_next_wall())
                cur_frame += 1
                frame = frames[cur_frame]
                y = 3
            x = frame.start
    # Get to the last wall and put the "off" sign on it
    while frame != frames[3]:
        commands.append(frame.to_next_wall())
        cur_frame += 1
        frame = frames[cur_frame]
    x = int(frame.width / 2 + 0.6)
    y = 3
    commands.append(
        sign_tmpl.render(particle=Particles("Off"), lines=['', 'Off', '', ''], x=-x, y=y, frame=frame).strip())

    commands.append(kill_command)

    write_function(func_dir, 'signs', "\n".join(commands) + "\n")


def write_function(func_dir, func_name, rendered):
    if not os.path.exists(func_dir):
        os.mkdir(func_dir)
    out_file = os.path.join(func_dir, '%s.mcfunction' % func_name)
    with open(out_file, "w") as out:
        out.write(rendered.strip() + "\n")


if __name__ == '__main__':
    main()
