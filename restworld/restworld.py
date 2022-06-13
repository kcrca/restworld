from __future__ import annotations

from pyker.commands import mc, entities, JsonText, player, DARK_GREEN, Commands, r, REPLACE, BlockData, NORTH, WEST, \
    Score, MOVE, EntityData, self, OVERWORLD, EQ, MOD, THE_END, RAIN, CREATIVE, SIDEBAR, COLORS, MULT, PLUS, RESULT, \
    LONG
from pyker.enums import ScoreCriteria
from pyker.function import DataPack, FunctionSet, Function
from pyker.simpler import Book, Sign
from rooms import Room, Clock, MobPlacer, fishes, Thing


def kill_em(target):
    return mc.tp().to(entities().tag('death').limit(1), target)


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


class Fencelike:
    @classmethod
    def update(self, id, text2, text3='') -> Commands:
        return (
            mc.fill(*r(8, 3, 6, 0, 2, 0), id, REPLACE).filter('#restworld:fencelike'),
            mc.data().merge(BlockData(*r(5, 2, 0)), Sign.lines_nbt(('', text2, text3, '')))
        )


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

    def levitation_body(_: Score, i: int, _2: int) -> Commands:
        if i == 1:
            yield mc.execute().at(entities().tag('sleeping_bat')).run().clone(*r(0, 1, 0, 0, 1, 0, 0, 3, 0)).replace(
                MOVE),
            yield mc.execute().at(entities().tag('turtle_eggs_home')).run().clone(
                *r(1, 2, 0, -2, 2, 0, -2, -4, 0)).replace(
                MOVE),
            # yield mc.execute().at(entities().tag('brown_horses', 'kid')).run().clone(*r(2, 0, 0, 2, 0, 0, 2, 2, 0)).replace(
            #     MOVE),
            for mob_room in ("friendlies", "monsters", "aquatic", "wither", "nether", "enders", "ancient"):
                room_home = mob_room + '_home'
                yield mc.execute().as_(entities().tag(room_home)).run().data().merge(
                    EntityData(self()), {'Invisible': True})
                yield mc.execute().as_(entities().tag(room_home, '!blockers_home')).at(self()).run().tp().pos(
                    *r(0, 2, 0),
                    self())
                yield mc.execute().as_(entities().tag(mob_room, '!passenger').type('!item_frame')).at(
                    self()).run().tp().pos(*r(0, 2, 0), self())
        else:
            yield mc.execute().at(entities().tag('sleeping_bat')).run().clone(*r(0, 1, 0, 0, 1, 0, 0, -1, 0)).replace(
                MOVE),
            yield mc.execute().at(entities().tag('turtle_eggs_home')).run().clone(
                *r(1, 4, 0, -2, 4, 0, -2, 2, 0)).replace(
                MOVE),
            # yield mc.execute().at(entities().tag('brown_horses', 'kid')).run().clone(*r(2, 0, 0, 2, 0, 0, 2, 2, 0)).replace(
            #     MOVE),
            for mob_room in ("friendlies", "monsters", "aquatic", "wither", "nether", "enders", "ancient"):
                room_home = mob_room + '_home'
                yield mc.execute().as_(entities().tag(room_home)).run().data().merge(
                    EntityData(self()), {'Invisible': False})
                yield mc.execute().as_(entities().tag(room_home, '!blockers_home')).at(self()).run().tp().pos(
                    *r(0, -2, 0),
                    self())
                yield mc.execute().as_(entities().tag(mob_room, '!passenger').type('!item_frame')).at(
                    self()).run().tp().pos(*r(0, -2, 0), self())

    room = Room('global', restworld)
    clock_toggle = room.score('clock_toggle')
    room.add(
        Function('arena').add(
            mc.execute().in_(OVERWORLD).run().tp().pos(1126, 103, 1079, player()).facing(1139, 104, 1079), ))
    room.add(
        room.home_func('clock'),
        Function('clock_init').add(
            mc.scoreboard().objectives().remove('clocks'),
            mc.scoreboard().objectives().add('clocks', ScoreCriteria.DUMMY),
            list(c.speed.set(c.init_speed) for c in restworld.clocks()),
            list(c.time.set(-1) for c in restworld.clocks()),
            tick_clock.time.set(0),
            mc.function('restworld:global/clock_off'),
        ),
        Function('clock_tick').add(
            clock.time.add(1),
            (c.time.operation(EQ, clock.time) for c in restworld.clocks()),
            (c.time.operation(MOD, c.speed) for c in restworld.clocks()),
            kill_if_time()
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
    )
    death_home = room.home_func('death')
    room.add(death_home)
    room.add(Function('death_init').add(
        mc.execute().positioned(0, 1.5, 0).run().function(death_home.full_name),
        mc.tag(entities().tag(death_home.name)).add('death'),
        mc.tag(entities().tag(death_home.name)).add('immortal'),
    ))

    room.add(
        Function('full_finish').add(
            mc.function('restworld:_init'),
            mc.function('restworld:_cur'),
            # Some of these functions leave dropped items behind, this cleans that up'
            mc.kill(entities().type('item')),
        ),
        Function('full_reset').add(
            mc.function('restworld:global/clock_off'),
            mc.execute().positioned(*r(0, -3, 0)).run().function('restworld:global/min_home'),
            mc.kill(entities().tag('home', '!min_home')),
            # Death must be ready before any other initialization
            mc.function('restworld:global/death_init'),
            use_min_fill(97, 'redstone_block', 'dried_kelp_block'),
            use_min_fill(97, 'dried_kelp_block', 'redstone_block'),
            use_min_fill(97, 'redstone_block', 'pumpkin'),
            use_min_fill(97, 'pumpkin', 'redstone_block'),
        ),
    )
    room.add(Function('gamerules').add(
        (mc.gamerule(*args) for args in (
            ('announceAdvancements', False),
            ('commandBlockOutput', False),
            ('disableRaids', True),
            ('doDaylightCycle', False),
            ('doFireTick', False),
            ('doInsomnia', False),
            ('doMobSpawning', False),
            ('doPatrolSpawning', False),
            ('doTraderSpawning', False),
            ('doWeatherCycle', False),
            ('keepInventory', True),
            ('mobGriefing', False),
            ('randomTickSpeed', 0),
            ('spawnRadius', 0),
        ))
    ))
    for p in (
            ('biomes', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('connected', OVERWORLD, (1000, 101, 1000), (990, 101, 1000)),
            ('end_home', THE_END, (100, 49, 0), (-1000, 80, -970)),
            ('home', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('nether', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('photo', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970))):
        room.add(
            Function('goto_' + p[0]).add(mc.execute().in_(p[1]).run().teleport().pos(*p[2], player()).facing(*p[3])))
    room.add(Function('goto_weather').add(
        mc.execute().in_(OVERWORLD).run().teleport().pos(1009, 101, 1000, player()).facing(1004, 102, 1000),
        mc.weather(RAIN)))
    room.add(room.home_func('min'))

    levloop = room.loop('mob_levitation', main_clock)
    levloop.loop(levitation_body, range(0, 2))

    room.add(Function('ready').add(
        mc.clear(player()),
        mc.gamemode(CREATIVE, player()),
        mc.function('restworld:global/control_book'),
        mc.tp().pos(0, 101, 0, player()).facing(0, 100, 5),
        mc.scoreboard().objectives().setdisplay(SIDEBAR),
        mc.function('restworld:center/reset_clocks'),
        mc.function('restworld:global/clock_on'),
    ))


def aquatic_room():
    def loop_n_fish(count: int):
        def fish_loop(_: Score, i: int, _2: int):
            for f in [f for f in fishes if len(f[1]) == count]:
                tag, variants = f
                v = variants[i]
                yield mc.data().merge(EntityData(entities().tag(tag).limit(1)), {'Variant': v[0], 'CustomName': v[1]})

        return fish_loop

    def tropical_fish_funcs(room):
        body = Score('body', 'fish')
        pattern = Score('pattern', 'fish')
        num_colors = Score('NUM_COLORS', 'fish')
        body_scale = Score('BODY_SCALE', 'fish')
        pattern_scale = Score('PATTERN_SCALE', 'fish')
        pattern_variant = Score('pattern_variant', 'fish')
        variant = Score('variant', 'fish')

        def all_fish_init():
            yield Sign((None, 'All Possible', 'Tropical Fish', '-------->')).place(*r(0, 2, 0), WEST, water=True)
            # , nbt={'Invulnerable': True}
            placer = MobPlacer(*r(0, 1.2, 0), WEST, 1, adults=True)
            for i in range(0, 12):
                if i == 6:
                    placer = MobPlacer(*r(1, 1.2, 0), WEST, 1)
                yield placer.summon('tropical_fish', tags=('fish%d' % i,))
            yield (
                mc.scoreboard().objectives().remove('fish'),
                mc.scoreboard().objectives().add('fish', ScoreCriteria.DUMMY),
                num_colors.set(len(COLORS)),
                body_scale.set(0x10000),
                pattern_scale.set(0x1000000),
                body.set(0),
                pattern.set(0),
            )

        def all_fish():
            yield (
                pattern.add(1),
                pattern.operation(MOD, num_colors),
                mc.execute().if_().score(pattern).matches(0).run(body.add(1)),
                body.operation(MOD, num_colors),
                pattern_variant.operation(EQ, pattern),
                pattern_variant.operation(MULT, pattern_scale),
                variant.operation(EQ, body),
                variant.operation(MULT, body_scale),
                variant.operation(PLUS, pattern_variant),
            )
            for i in range(0, 12):
                yield mc.execute().store(RESULT).entity(entities().tag('fish%d' % i).limit(1), 'Variant', LONG, 1).run(
                    variant.get())
                if i == 6:
                    yield variant.add(1)
                yield variant.add(256)

        room.add(Function('all_fish_init').add(all_fish_init()))
        room.loop('all_fish', fast_clock).add(all_fish())

    room = Room('aquatic', restworld, NORTH, (None, 'Aquatic'))

    room.loop('2_fish', main_clock).loop(loop_n_fish(2), range(0, 2))
    room.loop('3_fish', main_clock).loop(loop_n_fish(3), range(0, 3))
    tropical_fish_funcs(room)
    room.add(Function('axolotl_init').add(MobPlacer(*r(1.3, 1.5, 1.3), 135, (0, 0), (-1.4, -1.4)).summon('axolotl')))
    axolotls = ('Lucy', 'Wild', 'Gold', 'Cyan', 'Blue')
    room.loop('axolotl', main_clock).loop(
        lambda _, i, thing: mc.execute().as_(entities().tag('axoltol')).run().data().merge(
            EntityData(self()), {'Variant': i, 'CustomName': thing + ' Axolotl'}), axolotls)
    room.add(Function('elder_guardian').add(Thing('Elder Guardian').summon(*r(2, 1, 0), rotation=225)))


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


def main():
    for f in (ancient_room, global_room, aquatic_room):
        f()
    restworld.save()


if __name__ == '__main__':
    main()
