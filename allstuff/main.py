import glob
import os
import random
import re
import sys

from mako.lookup import TemplateLookup
from mako.template import Template

mc_version = '1.14'


def render_tmpl(tmpl, var_name, **kwargs):
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
        ("gra", "Gradient"), ("gru", "Gradient|Upside-Down"), ("cre", "Creeper"), ("bri", "Bick"),
        ("sku", "Skull"), ("flo", "Flower"), ("moj", "Mojang"), ("glb", "Globe"),
    )

    villager_types = ("Desert", "Jungle", "Plains", "Savanna", "Snow", "Swamp", "Taiga")
    villager_data = []
    for t in villager_types:
        for p in professions:
            villager_data += ['profession:%s,type:%s' % (p, t), ]
    random.shuffle(villager_data)

    return tmpl.render(
        var=var_name,
        func=var_name,
        Thing=Thing,
        Mob=Mob,
        colors=colors,
        command_blocks=command_blocks,
        steppables=stepables,
        woods=woods,
        fishes=fishes,
        horses=horses,
        other_horses=other_horses,
        small_flowers=small_flowers,
        tulips=tulips,
        patterns=patterns,
        professions=professions,
        text=text,
        text_attrs=text_attrs,
        to_nicknamed=to_nicknamed,
        to_id=to_id,
        commas=commas,
        villager_data=villager_data,
        villager_types=villager_types,
        **kwargs
    )


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

    def full_id(self, block_state=""):
        id = "minecraft:%s" % self.id
        state = self.block_state + ("," if block_state and self.block_state else "") + block_state
        if state:
            id += "[%s]" % state
        return id

    def sign_text(self):
        return self.text.split("|")


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
        self.id = name.replace(' ', '_').lower()

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


class Particles(object, Thing):
    def __init__(self, name, id=None, note=None):
        Thing.__init__(self, name, id)
        self.note = "(%s)" % note if note else None

    def sign_text(self):
        t = super(Particles, self).sign_text()
        if self.note:
            t += self.note.split("|")
        return t

    def __cmp__(self, other):
        my_text = ' '.join(self.sign_text())
        other_text = ' '.join(other.sign_text())
        return cmp(my_text, other_text)


def text(txt):
    return r'"\"%s\""' % txt.replace('"', r'\\\"')


def text_attrs(attrs):
    if not attrs:
        return ""
    s = ""
    for k, v in attrs.iteritems():
        s += r',\"%s\":\"%s\"' % (k, v)
    return s


def to_id(name):
    return name.lower().replace(" ", "_")


def to_nicknamed(kind, nicknames):
    items = [Nicknamed(n, kind) for n in nicknames]
    return items


def commas(*args):
    return ",".join(list([s for s in args if s]))


def has_loop(rendered):
    return re.search(r'<%base:(loop|bounce|increment)', rendered, flags=re.MULTILINE)


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

            # The effects room is just special
            if room.name == 'effects':
                return

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
            Generate all the files for a single room (directory). First consume all the files, then generate all the
            room-wide files.
            :return:
            """
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

    rooms = []
    for room_dir in glob.glob(os.path.join(tmpl_dir, '*/')):
        room = Room(room_dir)
        room.generate()
        rooms += [room.name, ]

    for f in incr_funcs + ("init",):
        write_function(func_dir, "_%s" % f, "\n".join("function v3:%s/_%s" % (r, f) for r in rooms))

    particle_signs(func_dir + "/particles", Template(filename="%s/particles_sign.mcftmpl" % tmpl_dir, lookup=lookup))


particles = (
    Particles("Ambient Entity|Effect", "ambient"), Particles("Angry Villager"), Particles("Bee Pollen"),
    Particles("Bubbles|and|Whirlpools", "bubbles"), Particles("Clouds", note="Evaporation"), Particles("Crit"),
    Particles("Damage Indicator"), Particles("Dolphin"), Particles("Dragon Breath"), Particles("Dripping Honey"),
    Particles("Dripping Lava"), Particles("Dripping Water"), Particles("Dust", note="Redstone Dust"),
    Particles("Effect"), Particles("Elder Guardian"), Particles("Enchant"), Particles("Enchanted Hit"),
    Particles("End Rod"), Particles("Entity Effect"), Particles("Explosion"), Particles("Falling Dust"),
    Particles("Fireworks"), Particles("Fishing"), Particles("Flame"), Particles("Happy Villager"), Particles("Heart"),
    Particles("Explosion Emitter", note="Large Explosion"), Particles("Instant Effect"), Particles("Item Slime"),
    Particles("Item Snowball"), Particles("Large Smoke"), Particles("Lava"), Particles("Mycelium"),
    Particles("Nautilus"), Particles("Note"), Particles("Poof", note="Small Explosion"), Particles("Portal"),
    Particles("Campfire|Smoke"), Particles("Sneeze"), Particles("Smoke"), Particles("Spit"), Particles("Splash"),
    Particles("Squid Ink"), Particles("Sweep Attack"), Particles("Totem of Undying"), Particles("Underwater"),
    Particles("Witch"),
)


class Wall:
    def __init__(self, width, used, facing, block_at, y_first=3, y_last=1):
        self.width = width
        self.used = used
        self.facing = facing
        self.block_at = block_at
        self.start = (width - used) / 2
        self.end = width - self.start
        self.y_first = y_first
        self.y_last = y_last

    def to_next_wall(self):
        return "execute as @e[tag=signer] run execute at @s run teleport @s ^-%d ^0 ^0 ~90 ~" % (
                self.width - 1)

    def start_pos(self):
        return self.start, self.y_first

    def next_pos(self, x, y):
        x += 1
        end = self.end + 1 if self.facing == 'south' and y == self.y_first - 1 else self.end
        if x >= end:
            y -= 1
            x = self.start - 1 if self.facing == 'south' and y == self.y_first - 1 else self.start
            if y < self.y_last:
                return None, None
        return x, y


def particle_signs(func_dir, sign_tmpl):
    walls = (
        Wall(7, 5, "east", (-1, 0)),
        Wall(7, 5, "south", (0, -1)),
        Wall(7, 5, "west", (1, 0)),
        Wall(7, 5, "north", (0, 1)),
    )
    room_signs(func_dir, "particles", sign_tmpl, sorted(particles), walls, (1, 1.5, -1, 90), do_off_sign=True)


def room_signs(func_dir, room, sign_tmpl, subjects, walls, start, do_off_sign=False, label=None):
    cur_wall = 0
    wall = walls[cur_wall]
    kill_command = "kill @e[tag=signer]"
    commands = [
        kill_command,
        "summon minecraft:armor_stand ~%f ~%f ~%f {Tags:[signer],Rotation:[%df,0f],ArmorItems:[{},{},{},{id:turtle_helmet,Count:1}]}" % start,
        "execute at @e[tag=signer] run fill ^0 ^0 ^0 ^%d ^%d ^%d air" % (
            -(walls[0].width - 1), wall.y_first + 1, -(walls[1].width - 1)),
    ]
    if label:
        commands += [
            "execute at @e[tag=signer] run setblock ^%d ^%d ^%d wall_sign[facing=%s]{Text2:%s}" % (
                -int(walls[0].width / 2), wall.y_first + 1, -int(walls[1].width / 2), wall.facing, text(label)),
        ]
    x, y = wall.start_pos()
    for i, subj in enumerate(subjects):
        sign_text = subj.sign_text()
        lines = ["", ] + sign_text + [""] * (max(0, 3 - len(sign_text)))
        commands.append(sign_tmpl.render(room=room, subj=subj, lines=lines, x=-x, y=y, z=0, wall=wall).strip())
        x, y = wall.next_pos(x, y)
        if x is None:
            commands.append(wall.to_next_wall())
            cur_wall += 1
            wall = walls[cur_wall]
            x, y = wall.start_pos()
    if do_off_sign:
        # Get to the last wall and put the "off" sign on it
        while cur_wall < len(walls) - 1:
            commands.append(wall.to_next_wall())
            cur_wall += 1
            wall = walls[cur_wall]
        x = int(wall.width / 2 + 0.6)
        y = 3
        commands.append(
            sign_tmpl.render(room=room, subj=Particles("Off"), lines=['', 'Off', '', ''], x=-x, y=y, z=2,
                             wall=wall).strip())
        commands.append(kill_command)
    write_function(func_dir, "signs", "\n".join(commands) + "\n")


def write_function(func_dir, func_name, rendered):
    if not os.path.exists(func_dir):
        os.mkdir(func_dir)
    out_file = os.path.join(func_dir, '%s.mcfunction' % func_name)
    with open(out_file, "w") as out:
        out.write(rendered.strip() + "\n")


if __name__ == '__main__':
    main()
