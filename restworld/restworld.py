from __future__ import annotations

import sys

from pyker.commands import mc, entity, JsonText, player, DARK_GREEN, Commands, r, REPLACE, self, OVERWORLD, EQ, MOD, \
    THE_END, RAIN, CREATIVE, SIDEBAR, COLORS, MULT, PLUS, RESULT, \
    LONG, Entity, all_, Block, good_color_num, INT, WHITE, SOUTH, EAST, Score, WEST, NORTH, MOVE
from pyker.enums import ScoreCriteria
from pyker.function import FunctionSet, Function, Loop
from pyker.simpler import Book, Sign, WallSign, Shield, Pattern
from rooms import Room, Clock, fishes, Thing, label, RoomPack


def kill_em(target):
    return mc.tp().to(target, entity().tag('death').limit(1))


marker_tmpl = Entity('armor_stand', {'NoGravity': True, 'Small': True, })


class Restworld(RoomPack):
    def __init__(self, path: str):
        suffixes = list(RoomPack.base_suffixes)
        suffixes.extend(list(x.name for x in self.clocks()))
        super().__init__('restworld', path, suffixes, 4)

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
        return slow_clock, main_clock, fast_clock

    def control_book_func(self) -> Function:
        cb = Book()
        cb.sign_book('Control Book', 'Restworld', 'Useful Commands')

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

    @staticmethod
    def _action(txt: str, tooltip: str, act: str) -> JsonText:
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
                func.add(mc.function(room.full_name + '/' + fname))
            yield func


class Fencelike:
    @classmethod
    def update(cls, id, text2, text3='') -> Commands:
        return (
            mc.fill(r(8, 3, 6), r(0, 2, 0), id, REPLACE).filter('#restworld:fencelike'),
            mc.data().merge(r(5, 2, 0), Sign.lines_nbt(('', text2, text3, '')))
        )


clock = Clock('clock')
slow_clock = Clock('slow', 90)
main_clock = Clock('main', 60)
fast_clock = Clock('fast', 15)
tick_clock = Clock('clock')
restworld = Restworld('/Users/kcrca/clarity/home/saves/NewRest')


def ancient_room():
    room = Room('ancient', restworld, NORTH, (None, 'Warden'))
    room.add(
        Function('warden_init').add((room.mob_placer(r(0, 2, 0), WEST, adults=True).summon('warden'),)),
    )


def global_room():
    def use_min_fill(y, filler, filter):
        return mc.execute().at(entity().tag('min_hom')).run().fill(r(0, y, 0), r(166, y, 180), filler,
                                                                   REPLACE).filter(filter)

    def clock_lights(turn_on):
        lights = ('red_concrete', 'lime_concrete')
        before = lights[int(turn_on)]
        after = lights[1 - int(turn_on)]
        return (
            use_min_fill(100, after, before),
            mc.execute().at(entity().tag('min_home')).run().setblock((0, 105, -78), after)
        )

    def kill_if_time():
        ex = mc.execute()
        for c in restworld.clocks():
            ex = ex.unless().score(c.time).matches((0, 1))
        return ex.run().function('restworld:global/kill_em')

    def levitation_body(_: Score, i: int, _2: int) -> Commands:
        mob_rooms = ("friendlies", "monsters", "aquatic", "wither", "nether", "enders", "ancient")
        if i == 1:
            yield mc.execute().at(entity().tag('sleeping_bat')).run().clone(r(0, 1, 0), r(0, 1, 0),
                                                                            r(0, 3, 0)).replace(
                MOVE),
            yield mc.execute().at(entity().tag('turtle_eggs_home')).run().clone(r(1, 2, 0), r(-2, 2, 0),
                                                                                r(-2, -4, 0)).replace(
                MOVE),
            # yield mc.execute().at(entities().tag('brown_horses', 'kid')).run().clone(*r(2, 0, 0, 2, 0, 0, 2, 2, 0)).replace(
            #     MOVE),
            for mob_room in mob_rooms:
                room_home = mob_room + '_home'
                yield mc.execute().as_(entity().tag(room_home)).run().data().merge(
                    self(), {'Invisible': True})
                yield mc.execute().as_(entity().tag(room_home, '!blockers_home')).at(self()).run().tp().pos(
                    r(0, 2, 0),
                    self())
                yield mc.execute().as_(entity().tag(mob_room, '!passenger').type('!item_frame')).at(
                    self()).run().tp().pos(r(0, 2, 0), self())
        else:
            yield mc.execute().at(entity().tag('sleeping_bat')).run().clone(r(0, 1, 0), r(0, 1, 0),
                                                                            r(0, -1, 0)).replace(MOVE),
            yield mc.execute().at(entity().tag('turtle_eggs_home')).run().clone(
                r(1, 4, 0), r(-2, 4, 0), r(-2, 2, 0)).replace(MOVE),
            # yield mc.execute().at(entities().tag('brown_horses', 'kid')).run().clone(*r(2, 0, 0, 2, 0, 0, 2, 2, 0)).replace(
            #     MOVE),
            for mob_room in mob_rooms:
                room_home = mob_room + '_home'
                yield mc.execute().as_(entity().tag(room_home)).run().data().merge(
                    self(), {'Invisible': False})
                yield mc.execute().as_(entity().tag(room_home, '!blockers_home')).at(self()).run().tp().pos(
                    r(0, -2, 0), self())
                yield mc.execute().as_(entity().tag(mob_room, '!passenger').type('!item_frame')).at(
                    self()).run().tp().pos(r(0, -2, 0), self())

    room = Room('global', restworld)
    clock_toggle = room.score('clock_toggle')
    room.function('arena').add(
        mc.execute().in_(OVERWORLD).run().tp().pos((1126, 103, 1079), player()).facing((1139, 104, 1079)))
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
            mc.execute().at(entity().tag('clock_home')).run().setblock(r(0, -2, 1), 'redstone_block')),
        Function('clock_off').add(
            mc.execute().at(entity().tag('clock_home')).run().setblock(r(0, -2, 1), 'diamond_block')),
        Function('clock_switched_on').add(
            clock_lights(True)),
        Function('clock_switched_off').add(
            clock_lights(False),
            (c.time.operation(EQ, c.speed) for c in restworld.clocks()),
            (c.time.remove(1) for c in restworld.clocks()),
        ),
        Function('clock_toggle').add(
            clock_toggle.set(0),
            mc.execute().at(entity().tag('clock_home')).if_().block(r(0, -2, 1), 'redstone_block').run(
                clock_toggle.set(1)),
            mc.execute().if_().score(clock_toggle).matches(0).run().function('restworld:global/clock_on'),
            mc.execute().if_().score(clock_toggle).matches(1).run().function('restworld:global/clock_off'),
        ),
    )
    death_home = room.home_func('death')
    room.add(death_home)
    room.function('death_init').add(
        mc.execute().positioned((0, 1.5, 0)).run().function(death_home.full_name),
        mc.tag(entity().tag(death_home.name)).add('death'),
        mc.tag(entity().tag(death_home.name)).add('immortal'),
    )
    killables = entity().not_type('player').not_tag('death').distance((None, 30))
    room.function('kill_em').add(
        mc.execute().at(entity().tag('death')).run().kill(killables),
        mc.execute().at(entity().tag('death')).as_(killables).run().data().merge(self(),
                                                                                 {'DeathTime': -1200}),
    )

    room.function('full_finish').add(
        mc.function('restworld:_init'),
        mc.function('restworld:_cur'),
        # Some of these functions leave dropped items behind, this cleans that up'
        mc.kill(entity().type('item')),
    )
    room.function('full_reset').add(
        mc.function('restworld:global/clock_off'),
        mc.execute().positioned(r(0, -3, 0)).run().function('restworld:global/min_home'),
        mc.kill(entity().tag('home', '!min_home')),
        # Death must be ready before any other initialization
        mc.function('restworld:global/death_init'),
        use_min_fill(97, 'redstone_block', 'dried_kelp_block'),
        use_min_fill(97, 'dried_kelp_block', 'redstone_block'),
        use_min_fill(97, 'redstone_block', 'pumpkin'),
        use_min_fill(97, 'pumpkin', 'redstone_block'),
    )
    room.function('gamerules').add(
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
    )
    for p in (
            ('biomes', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('connected', OVERWORLD, (1000, 101, 1000), (990, 101, 1000)),
            ('end_home', THE_END, (100, 49, 0), (-1000, 80, -970)),
            ('home', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('nether', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('photo', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('arena', OVERWORLD, (1014, 106, -1000), (1000, 100, -1000))):
        room.function('goto_' + p[0], needs_home=False).add(
            mc.execute().in_(p[1]).run().teleport().pos(p[2], player()).facing(p[3]))
    room.function('goto_weather', needs_home=False).add(
        mc.execute().in_(OVERWORLD).run().teleport().pos((1009, 101, 1000), player()).facing((1004, 102, 1000)),
        mc.weather(RAIN))
    room.add(room.home_func('min'))

    levloop = room.loop('mob_levitation', main_clock)
    levloop.loop(levitation_body, range(0, 2))

    room.function('ready').add(
        mc.clear(player()),
        mc.gamemode(CREATIVE, player()),
        mc.function('restworld:global/control_book'),
        mc.tp().pos((0, 101, 0), player()).facing((0, 100, 5)),
        mc.scoreboard().objectives().setdisplay(SIDEBAR),
        mc.function('restworld:center/reset_clocks'),
        mc.function('restworld:global/clock_on'),
    )


def aquatic_room():
    def loop_n_fish(count: int):
        def fish_loop(_: Score, i: int, _2: int):
            for f in [f for f in fishes if len(f[1]) == count]:
                tag, variants = f
                v = variants[i]
                yield mc.data().merge(entity().tag(tag).limit(1), {'Variant': v[0], 'CustomName': v[1]})

        return fish_loop

    def all_fish_funcs(room):
        body = Score('body', 'fish')
        pattern = Score('pattern', 'fish')
        num_colors = Score('NUM_COLORS', 'fish')
        body_scale = Score('BODY_SCALE', 'fish')
        pattern_scale = Score('PATTERN_SCALE', 'fish')
        pattern_variant = Score('pattern_variant', 'fish')
        variant = Score('variant', 'fish')

        def all_fish_init():
            yield WallSign((None, 'All Possible', 'Tropical Fish', '-------->')).place(r(0, 2, 0), WEST, water=True)
            # , nbt={'Invulnerable': True}
            placer = room.mob_placer(r(0.5, 3.2, 0), WEST, -1, adults=True)
            for i in range(0, 12):
                if i == 6:
                    placer = room.mob_placer(r(1.5, 3.2, 0), WEST, -1, adults=True)
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
                yield mc.execute().store(RESULT).entity(entity().tag('fish%d' % i).limit(1), 'Variant', LONG, 1).run(
                    variant.get())
                if i == 6:
                    yield variant.add(1)
                yield variant.add(256)

        room.function('all_fish_init').add(all_fish_init())
        room.loop('all_fish', fast_clock).add(all_fish())

    def squids(_, i, _2):
        placer = room.mob_placer(r(1.8, 4, 0), WEST, adults=True, tags=('squidy',), nbt={'NoGravity': True})
        return placer.summon('squid' if i == 0 else 'glow_squid')

    room = Room('aquatic', restworld, NORTH, (None, 'Aquatic'))

    room.loop('2_fish', main_clock).loop(loop_n_fish(2), range(0, 2))
    room.loop('3_fish', main_clock).loop(loop_n_fish(3), range(0, 3))
    all_fish_funcs(room)
    t_fish = room.function('tropical_fish_init')
    for i in range(0, 12):
        tag, variants = fishes[i]
        fish = Entity('tropical_fish', nbt={'Variant': variants[0][0]}).tag(tag).set_name(variants[0][1])
        t_fish.add(room.mob_placer(r(int(i / 6) + 0.5, 3.2, int(i % 6)), WEST, adults=True).summon(fish))
    t_fish.add(WallSign(("Naturally", "Occurring", "Tropical Fish", "<--------")).place(
        r(int((len(fishes) - 1) / 6) - 1, 2, (len(fishes) - 1) % 6), WEST, water=True))
    room.function('axolotl_init').add(room.mob_placer(r(1.3, 4, 1.3), 135, (0, 0), (-1.4, -1.4)).summon('axolotl'))
    axolotls = ('Lucy', 'Wild', 'Gold', 'Cyan', 'Blue')
    room.loop('axolotl', main_clock).loop(
        lambda _, i, thing: mc.execute().as_(entity().tag('axoltol')).run().data().merge(
            self(), {'Variant': i, 'CustomName': thing + ' Axolotl'}), axolotls)
    room.function('elder_guardian_init').add(room.mob_placer(r(2, 3, 0), 225, adults=True).summon('elder_guardian'))
    room.function('guardian_init').add(room.mob_placer(r(-0.6, 3, 0), 180, adults=True).summon('guardian'))
    room.function('fishies_init').add(
        room.mob_placer(r(1.8, 4, 0), EAST, adults=True).summon(Entity('dolphin', nbt={'Invulnerable': True})),
        room.mob_placer(r(1.8, 4, -4), EAST, -1, adults=True).summon(
            ('salmon', 'cod', 'pufferfish', Entity('tadpole', nbt={'Invulnerable': True, 'Age': -2147483648}))),
    )
    room.loop('fishies', main_clock).loop(
        lambda _, _2, x: mc.data().merge(entity().tag('pufferfish').limit(1), {'PuffState': x}),
        range(0, 3), bounce=True)
    room.loop('squid', main_clock).add(kill_em(entity().tag('squidy'))).loop(squids, range(0, 2))


def arena_room():
    start_battle_type = Score('battle_type', 'arena')

    fighter_nbts = {
        'Drowned': 'HandItems:[{id:trident,Count:1}]',
        'Goat': 'IsScreamingGoat:True',
        'Hoglin': 'IsImmuneToZombification:True',
        'Magma Cube': 'Size:0',
        'Panda': 'MainGene:aggressive',
        'Phantom': 'AX:1000,AY:110,AZ:-1000',
        'Piglin Brute': 'HandItems:[{id:golden_axe,Count:1}],IsImmuneToZombification:True',
        'Piglin': 'IsImmuneToZombification:True,HandItems:[{id:golden_sword,Count:1},{}]',
        'Pillager': 'HandItems:[{id:crossbow,Count:1},{}]',
        'Skeleton': 'HandItems:[{id:bow,Count:1}],ArmorItems:[{id:iron_boots,Count:1,tag:{RepairCost:1,Enchantments:[{lvl:9,id:protection}]}},{},{},{}]',
        'Slime': 'Size:0',
        'Stray': 'HandItems:[{id:bow,Count:1}],ArmorItems:[{id:iron_boots,Count:1,tag:{RepairCost:1,Enchantments:[{lvl:9,id:protection}]}},{},{},{}]',
        'Vindicator': 'Johnny:True,HandItems:[{id:iron_axe,Count:1},{}]',
        'Wither Skeleton': 'HandItems:[{id:stone_sword,Count:1},{}]',
        'Zombified Piglin': 'HandItems:[{id:golden_sword,Count:1}]',
    }

    battles = [
        ('Axolotl:w', 'Drowned'),
        ('Blaze', 'Snow Golem'),
        ('Cat', 'Rabbit'),
        ('Cave Spider', 'Snow Golem'),
        ('Drowned:c', 'Snow Golem'),
        ('Evoker', 'Iron Golem'),
        ('Fox', 'Chicken'),
        ('Frog', 'Slime'),
        ('Goat', 'Sheep'),
        ('Hoglin', 'Vindicator'),
        ('Illusioner', 'Snow Golem'),
        ('Panda', 'Vindicator'),
        ('Parrot', 'Vindicator'),
        ('Phantom:c', 'Rabbit'),
        ('Piglin Brute', 'Vindicator'),
        ('Pillager', 'Snow Golem'),
        ('Polar Bear', 'Vindicator'),
        ('Ravager', 'Iron Golem'),
        ('Shulker', 'Vindicator'),
        ('Spider', 'Snow Golem'),
        ('Stray:c', 'Iron Golem'),
        ('Vex', 'Snow Golem'),
        ('Vindicator', 'Iron Golem'),
        ('Witch', 'Snow Golem'),
        ('Wither Skeleton', 'Piglin'),
        ('Wither', 'Pillager'),
        ('Wolf', 'Sheep'),
        ('Zoglin', 'Vindicator'),
        ('Zombie:c', 'Iron Golem'),
        ('Zombified Piglin', 'Vindicator'),
    ]
    # Lower priority ones that can be used as filler
    #    ('Axolotl:w', 'Elder Guardian'),
    #    ('Axolotl:w', 'Guardian'),
    #    ('Ocelot', 'Chicken'),
    #    ('Slime', 'Iron Golem'),
    #    ('Magma Cube', 'Iron Golem'),
    # These don't work unelss we figure out how to kill the ones that spawn when a larger is killed. For
    # now, we just make sure they are the smallest size.
    #  ('Slime', 'Iron Golem'),
    #  ('Magma Cube', 'Iron Golem'),

    stride_length = 6
    num_rows = 2
    row_length = stride_length / num_rows
    if stride_length % num_rows != 0:
        sys.stderr.write(
            'Stride length(%d) is not a multiple of the number of rows (%d)' % (stride_length, num_rows))
        sys.exit(1)
    if row_length % 2 == 0:
        # Needed so we can center on the middle sign
        sys.stderr.write("Row length(%d) is not odd" % row_length)
        sys.exit(1)
    if len(battles) % stride_length != 0:
        sys.stderr.write(
            'Stride length (%d) is not a multiple of battle count (%d)\n' % (stride_length, len(battles)))
        sys.exit(1)

    battles.sort()

    monitor_home = entity().tag('monitor_home')

    def arena_run_main(loop: Loop):
        def arena_run_loop(score: Score, i: int, thing):
            for which_dir in (-1, 1):
                to = (i + which_dir + num_pages) % num_pages
                text, z = ('<--', max_z + 1) if which_dir == -1 else ('-->', min_z - 1)
                yield WallSign((None, text), (
                    score.set(to),
                    mc.execute().at(entity().tag('controls_home')).run().function(
                        'restworld:arena/%s_cur' % score.target)
                )).glowing(True).place(r(x, 2, z), WEST)
            for s in range(0, stride_length):
                args = thing[s] + (None,) * (4 - len(thing[s]))
                y = 3 - int(s / row_length)
                z = max_z - (s % row_length)
                hunter, victim, hunter_nbt, victim_nbt = args

                battle_type = 0
                if hunter[-2] == ':':
                    battle_type = {'w': 1, 'c': 2}[hunter[-1]]
                    hunter = hunter[0:-2]

                def incr_cmd(which, mob):
                    my_nbts = ['Tags:[battler,%s]' % which]
                    added_nbt = fighter_nbts.get(mob, None)
                    if added_nbt:
                        my_nbts.append(added_nbt)
                    if which == 'hunter':
                        my_nbts.append('Rotation:[180f,0f]')
                    incr = 'summon %s ~0 ~2 ~0 {%s}' % (Thing(mob).id, ','.join(my_nbts))
                    incr_cmd = 'execute if score %s_count funcs < arena_count funcs at @e[tag=%s_home,sort=random,limit=1] run %s' % (
                        which, which, incr)
                    return incr_cmd

                vs = 'vs.'

                data_change = mc.execute().at(monitor_home).run().data()
                sign_commands = (
                    start_battle_type.set(battle_type),
                    data_change.merge(r(2, 0, 0), {'Command': incr_cmd('hunter', hunter)}),
                    data_change.merge(r(2, 0, 0), {'Command': incr_cmd('victim', victim)}),
                    mc.function('restworld:arena/start_battle')
                )
                sign = WallSign((None, hunter, vs, victim), sign_commands)
                yield sign.place(r(-2, y, z), WEST)

                run_type = Score('arena_run_type', 'arena')
                yield mc.execute().unless().score(run_type).matches((0, None)).run(run_type.set(0))

        chunks = []
        for i in range(0, len(battles), stride_length):
            chunks.append(battles[i:i + stride_length])

        num_pages = int(len(battles) / stride_length)
        end = int(row_length / 2)
        min_z = -end
        max_z = +end
        x = -2

        loop.add(mc.fill(r(x, 2, min_z - 1), r(x, 2 + num_rows - 1, max_z + 1), 'air'))
        loop.loop(arena_run_loop, chunks)
        return loop

    def random_stand(actor: str):
        var = actor + '_home'
        yield mc.kill(entity().tag(var))
        stand = marker_tmpl.clone().merge_nbt({'Tags': [var, 'home', 'arena_home']})
        for x in range(-1, 2):
            for z in range(-1, 2):
                yield stand.summon(r(x, -0.5, z))

    place_battlers = Score('place_batters', 'arena')

    def monitor(actor: str):
        other = 'hunter' if actor == 'victim' else 'victim'
        count = Score(actor + '_count', 'arena')
        close = Score(actor + '_close', 'arena')
        athome = Score(actor + '_athome', 'arena')
        return (
            mc.execute().unless().entity(entity().tag(actor)).run(place_battlers.set(1)),
            count.set(0),
            mc.execute().as_(entity().tag(actor)).run(count.add(1)),
            close.set(0),
            mc.execute().at(
                entity().tag(other + '_home')).positioned(r(-2, 0, -2)).as_(
                entity().tag(actor).delta((4, 5, 4))).run(close.add(1)),
            athome.set(0),
            mc.execute().at(
                entity().tag(actor + '_home')).positioned(r(-2, 0, -2)).as_(
                entity().tag(actor).delta((4, 5, 4))).run(athome.add(1)),
        )

    def toggle_peace(_: Score, _2: int, thing: bool):
        return (
            mc.execute().at(entity().tag('monitor_home')).run().fill(
                r(2, -1, 0), r(3, -1, 0), 'redstone_torch' if thing else 'air'),
            mc.setblock(r(0, 1, 0), '%s_concrete' % ('red' if thing else 'lime')),
        )

    room = Room('arena', restworld)

    arena_count = Score('arena_count', 'arena')

    arena_count_cur = (
        mc.function('restworld:arena/arena_count_cur'),
        mc.execute().unless().score(arena_count).matches((1, 5)).run(arena_count.set(1))
    )
    room.function('arena_count_decr').add(arena_count.remove(1), arena_count_cur)
    room.function('arena_count_incr').add(arena_count.add(1), arena_count_cur)
    room.function('arena_count_init').add(arena_count_cur)
    room.loop('arena_count', main_clock).loop(
        lambda _, i, thing: mc.execute().at(entity().tag('controls_home')).run(
        ).data().merge(r(2, 4, 0), {'Text2': '%d vs. %d' % (thing, thing)}), range(0, 6))

    room.function('arena_run_init').add(mc.function('restworld:arena/arena_run_cur'))
    # This is NOT intended to be run on the clock. It is only called "_main" because that gives us a
    # "_cur" function, which is useful when paging through the signs. Do not create the _home armor stand.
    arena_run_loop = arena_run_main(room.loop('arena_run', main_clock, needs_home=False))

    room.function('controls_init').add(
        arena_run_loop.score.set(0),
        mc.function('restworld:arena/arena_run_cur'),
        label(r(1, 3, 0), 'Go Home'),
        mc.tag(entity().tag('controls_home')).add('controls_action_home')
    )

    room.function('hunter_home').add(random_stand('hunter'))
    room.function('victim_home').add(random_stand('victim'))

    # monitor_init function looks out-of-date and unused
    room.function('monitor').add(monitor('hunter'), monitor('victim'),
                                 mc.kill(entity().type('item').distance((None, 50))),
                                 mc.kill(entity().type('experience_orb').distance((None, 50)))),

    # Types: 0-normal, 1-water, 2-undead
    fill_arena_coords = r(-12, 4), r(-12, 12, 2, 12)
    roof_coords = r(-12, 250, -12), r(12, 250, 12)
    room.function('start_battle').add(
        mc.execute().unless().score(start_battle_type).matches((0, None)).run(start_battle_type.set(0)),
        mc.execute().if_().score(start_battle_type).matches(0).at(monitor_home).run().fill(*fill_arena_coords, 'air'),
        mc.execute().if_().score(start_battle_type).matches(2).at(monitor_home).run().fill(*fill_arena_coords, 'air'),
        mc.execute().if_().score(start_battle_type).matches(1).at(monitor_home).run().fill(*fill_arena_coords, 'water'),
        mc.execute().if_().score(start_battle_type).matches((0, 1)).at(monitor_home).run().fill(*roof_coords, 'air'),
        mc.execute().if_().score(start_battle_type).matches(2).at(monitor_home).run().fill(*roof_coords, 'glowstone'),
        mc.tag(all_()).add('arena_safe'),
        mc.tag(entity().type('armor_stand')).add('arena_safe'),
        mc.kill(entity().not_tag('arena_safe').distance((None, 100))),
        mc.kill(entity().not_tag('arena_safe').distance((None, 100))),
        mc.kill(entity().not_tag('arena_safe').distance((None, 100))),
    )

    room.loop('toggle_peace').loop(toggle_peace, (True, False)).add(mc.function('restworld:arena/start_battle'))


def die(*msg: str):
    sys.stderr.write(*msg)
    sys.exit(1)


def banners_room():
    stand_tmpl = Entity('armor_stand', {
        'Invisible': True, 'NoGravity': True, 'ShowArms': True, 'Pose': {'LeftArm': [0, 90, 90]}, 'HandItems': [{}],
        'Tags': ['banner_stand']})

    # [xz]n: Adjustments (nudge) for shield's armor stand
    # b[xz]: Adjustments for banner position
    #                  x   xn  xd   z   zn  zd             bx  bz
    adjustments = {0: (1, 0.07, 1, -1, 0.30, 0, 0, 'south', 0, +1),
                   11: (13, -0.30, 0, 1, 0.07, 1, 90, 'west', -1, 0),
                   21: (11, -0.07, -1, 13, -0.30, 0, 180, 'north', 0, -1),
                   31: (-1, 0.30, 0, 11, -0.07, -1, 270, 'east', +1, 0)}

    authored_patterns = (
        (Block('blue_banner', nbt={'Patterns': [
            {'Color': 0, 'Pattern': "bri"}, {'Color': 11, 'Pattern': "hhb"}, {'Color': 15, 'Pattern': "sc"},
            {'Color': 11, 'Pattern': "sc"}, {'Color': 15, 'Pattern': "bo"}, {'Color': 11, 'Pattern': "bo"}]}),
         'Tardis', 'Pikachu'),
        (Block('purple_banner', nbt={'Patterns': [
            {'Color': 2, 'Pattern': "ss"}, {'Color': 10, 'Pattern': "bri"}, {'Color': 2, 'Pattern': "cbo"},
            {'Color': 15, 'Pattern': "bo"}]}),
         'Portail du Nether', 'Akkta'),
        (Block('white_banner', nbt={'Patterns': [
            {'Color': 15, 'Pattern': "mr"}, {'Color': 1, 'Pattern': "cbo"}, {'Color': 1, 'Pattern': "mc"},
            {'Color': 1, 'Pattern': "cre"}, {'Color': 1, 'Pattern': "tt"}, {'Color': 1, 'Pattern': "tts"}]}),
         'Fox', 'mr.crafteur'),
        (Block('white_banner', nbt={'Patterns': [
            {'Color': 15, 'Pattern': "mc"}, {'Color': 0, 'Pattern': "flo"}, {'Color': 15, 'Pattern': "tt"},
            {'Color': 0, 'Pattern': "cr"}, {'Color': 15, 'Pattern': "cbo"}, {'Color': 0, 'Pattern': "bts"}]}),
         'Rabbit', 'googolplexbyte'),
        (Block('light_blue_banner', nbt={'Patterns': [
            {'Color': 11, 'Pattern': "gra"}, {'Color': 0, 'Pattern': "cbo"}, {'Color': 0, 'Pattern': "cr"},
            {'Color': 0, 'Pattern': "mc"}, {'Color': 11, 'Pattern': "flo"}, {'Color': 0, 'Pattern': "tt"}]}),
         'Angel', 'PK?'),
        (Block('white_banner', nbt={'Patterns': [
            {'Color': 15, 'Pattern': "sc"}, {'Color': 0, 'Pattern': "sc"}, {'Color': 15, 'Pattern': "flo"},
            {'Color': 0, 'Pattern': "flo"}]}),
         'Quartz sculpte', 'Pikachu'),
        (Block('black_banner', nbt={'Patterns': [
            {'Color': 5, 'Pattern': "cbo"}, {'Color': 15, 'Pattern': "rs"}, {'Color': 14, 'Pattern': "flo"},
            {'Color': 5, 'Pattern': "ms"}, {'Color': 15, 'Pattern': "tt"}, {'Color': 5, 'Pattern': "moj"}]}),
         'DRAGON !', 'kraftime'),
        (Block('white_banner', nbt={'Patterns': [
            {'Color': 15, 'Pattern': "ts"}, {'Color': 0, 'Pattern': "sc"}, {'Color': 14, 'Pattern': "hhb"},
            {'Color': 0, 'Pattern': "bo"}, {'Color': 0, 'Pattern': "bs"}, {'Color': 4, 'Pattern': "ms"}]}),
         'Poule', 'mish80'),
        (Block('black_banner', nbt={'Patterns': [
            {'Color': 14, 'Pattern': "gru"}, {'Color': 14, 'Pattern': "bt"}, {'Color': 0, 'Pattern': "bts"},
            {'Color': 0, 'Pattern': "tts"}]}),
         'Bouche', 'entonix69'),
        (Block('lime_banner', nbt={'Patterns': [
            {'Color': 4, 'Pattern': "gra"}, {'Color': 3, 'Pattern': "gru"}, {'Color': 0, 'Pattern': "cbo"},
            {'Color': 0, 'Pattern': "cr"}, {'Color': 0, 'Pattern': "mr"}, {'Color': 5, 'Pattern': "mc"}]}),
         'Like pls ^-^', 'Harmony'),
    )

    # noinspection PyUnusedLocal
    def armor_stands(x, xn, z, zn, angle, facing, bx, bz, y_banner, y_shield, pattern, handback=None):
        shield = Shield(0).add_pattern(pattern, 9)
        stand = stand_tmpl.clone()
        stand.merge_nbt({'CustomName': ' '.join(Pattern.sign_text(pattern)), 'Rotation': [angle, 0]})
        stand.nbt['HandItems'].append(shield.nbt)
        yield stand.summon(r(x + xn, y_shield, z + zn))

    def render_banners(render, handback=None):
        # These are in the first adjustment, but python doesn't know that, so this keeps it happy
        x = z = xd = zd = xn = zn = angle = facing = bx = bz = 0
        for i, pattern in enumerate(Pattern):
            try:
                x, xn, xd, z, zn, zd, angle, facing, bx, bz = adjustments[i]
            except KeyError:
                x += xd
                z += zd
            if i > 10 and i % 10 == 6:
                x += xd
                z += zd
            yield render(x, xn, z, zn, angle, facing, bx, bz, 3.65, 3.65, pattern, handback)

    def custom_banner(x, z, nudge):
        stand1 = stand_tmpl.clone()
        stand1.nbt.get_list('Tags').extend(('banner_stand', 'banner_pattern_custom'))
        stand2 = stand_tmpl.clone()
        stand2.nbt.get_list('Tags').extend(('banner_stand', 'banner_pattern_custom_author'))
        return stand1.summon(r(x + nudge, 3.1, z + nudge)), stand2.summon(r(x + nudge, 2.8, z + nudge))

    def authored_banners(pattern, x, z, rot):
        return (
            mc.setblock(r(x, 3, z), pattern[0].merge_state({'rotation': rot})),
            mc.execute().positioned(r(x, 3, z)).as_(
                entity().tag('banner_pattern_custom').distance((None, 2))).run().data().merge(
                self(), {'CustomName': pattern[1]}),
            mc.execute().positioned(r(x, 3, z)).as_(
                entity().tag('banner_pattern_custom_author').distance((None, 2))).run().data().merge(
                self(), {'CustomName': pattern[2]}),
        )

    half = int(len(authored_patterns) / 2)

    def render_authored_banners(_: Score, i: int, _2):
        return (
            authored_banners(authored_patterns[i], 0.2, 0.2, 14),
            authored_banners(authored_patterns[i + half], 11.8, 11.8, 6),
        )

    # noinspection PyUnusedLocal
    def render_known_banner(x, xn, z, zn, angle, facing, bx, bz, y, pattern, color, ink, handback=None):
        return mc.setblock(r(x + bx, y, z + bz), Block(color + '_wall_banner', {'facing': facing},
                                                       {'Patterns': [{'Color': ink, 'Pattern': pattern}]}))

    # noinspection PyUnusedLocal
    def render_most(x, xn, z, zn, angle, facing, bx, bz, y_banner, y_shield, pattern, handback=None):
        color = handback
        return render_known_banner(x, xn, z, zn, angle, facing, bx, bz, y_banner, pattern, color, 9)

    # noinspection PyUnusedLocal
    def render_banner_ink(x, xn, z, zn, angle, facing, bx, bz, y_banner, y_shield, pattern, handback=None):
        return (
            #/execute as @e[tag=banner_stand] run execute store result entity @s HandItems[1].tag.BlockEntityTag.Patterns[0].Color int 1 run scoreboard players get banner_ink banners
            mc.execute().store(RESULT).block(r(x + bx, y_banner, z + bz), 'Patterns[0].Color', INT, 1).run(
                banner_ink.get()),
            mc.execute().as_(entity().tag('banner_stand')).run().execute().store(RESULT).entity(self(), 'HandItems[1].tag.BlockEntityTag.Patterns[0].Color', INT, 1).run(
                banner_ink.get()),
        )

    def banner_color_loop(_, _2, color: str):
        return (render_banners(render_most, handback=color),
                mc.execute().as_(entity().tag('banner_stand')).run(
                ).data().modify(self(), 'HandItems[1].tag.BlockEntityTag.Base').set().value(
                    good_color_num(color))
                )

    def banner_ink_loop(_, _2, color: str):
        return render_banners(render_banner_ink, handback=COLORS.index(color))

    def switch_banners(which):
        return (
            mc.tag(entity().tag('all_banners_home')).remove('banner_color_action_home'),
            mc.tag(entity().tag('all_banners_home')).remove('banner_color_home'),
            mc.tag(entity().tag('all_banners_home')).remove('banner_ink_action_home'),
            mc.tag(entity().tag('all_banners_home')).remove('banner_ink_home'),
            mc.tag(entity().tag('all_banners_home')).add('banner_' + which + '_action_home'),
            mc.tag(entity().tag('all_banners_home')).add('banner_' + which + '_home'),
            mc.tag(entity().tag('all_banners_home')).add('banners_action_home'),
        )

    room = Room('banners', restworld, SOUTH, (None, 'Banners &', 'Shields'))

    banner_color = room.score('banner_color')
    banner_ink = room.score('banner_ink')
    banner_color_init = mc.function('restworld:banners/switch_to_color')
    room.function('all_banners_init').add(
        banner_color.set(0),
        banner_ink.set(9),
        mc.kill(entity().tag('banner_stand')),
        mc.fill(r(-2, -2, -2), r(16, 16, 16), 'air', REPLACE).filter('#banners'),
        render_banners(armor_stands),
        mc.setblock(r(-0.2, 3, 11.8), Block('white_banner', {'rotation': 10}, {
            'Patterns': [{'Pattern': "mr", 'Color': 9}, {'Pattern': "bs", 'Color': 8}, {'Pattern': "cs", 'Color': 7},
                         {'Pattern': "bo", 'Color': 8}, {'Pattern': "ms", 'Color': 15}, {'Pattern': "hh", 'Color': 8},
                         {'Pattern': "mc", 'Color': 8}, {'Pattern': "bo", 'Color': 15}]})),
        mc.setblock(r(11.8, 3, 0.2), Block('magenta_banner', {'rotation': 2}, {
            'Patterns': [{'Pattern': "bt", 'Color': 15}, {'Pattern': "tt", 'Color': 15}]})),
        custom_banner(0.2, 0.2, 0.1),
        custom_banner(11.8, 11.8, -0.1),
        banner_color_init,
        mc.function('restworld:banners/banner_color_cur'),
    )

    if len(authored_patterns) % 2 != 0:
        die('Must have an even number of custom patterns')
    room.loop('all_banners', main_clock).add(
        mc.setblock(r(0, 3, 0), 'air'),
        mc.setblock(r(11, 3, 11), 'air'),
    ).loop(render_authored_banners, range(0, half))

    room.function('banner_color_init').add(banner_color_init)
    loop = room.loop('banner_color', main_clock).add(
        mc.fill(r(1, 3, 0), r(11, 5, 0), 'air', REPLACE).filter('#banners'),
        mc.fill(r(12, 3, 1), r(12, 5, 11), 'air', REPLACE).filter('#banners'),
        mc.fill(r(1, 3, 12), r(11, 5, 12), 'air', REPLACE).filter('#banners'),
        mc.fill(r(0, 3, 11), r(0, 5, 1), 'air', REPLACE).filter('#banners'),
    ).loop(banner_color_loop, COLORS)
    loop.add(render_banners(render_banner_ink))

    banner_controls = room.function('banner_controls').add(
        mc.function('restworld:banners/banner_controls_remove'),
        mc.function('restworld:global/clock_off'),
        WallSign((None, 'Set Banner', 'Color'), (mc.function('restworld:banners/switch_to_color', )),
                 wood='dark_oak').color(WHITE).place(r(4, 3, 1), SOUTH),
        WallSign((None, 'Set Banner', 'Ink'), (mc.function('restworld:banners/switch_to_ink', )),
                 wood='dark_oak').color(WHITE).place(r(4, 2, 2), SOUTH),
    )
    for i, c in enumerate(COLORS):
        x = i % 8
        # Leave room for the middle signs
        if x >= 4:
            x += 1
        row = int(i / 8)
        y = 3 if row == 0 else 2
        z = 1 if row == 0 else 2
        if_colors = mc.execute().at(entity().tag('banner_color_home'))
        if_ink = mc.execute().at(entity().tag('banner_ink_home'))
        banner_controls.add(
            WallSign((None, c), (
                if_colors.run(banner_color.set(i)),
                if_colors.run().function('restworld:banners/banner_color_cur'),
                if_ink.run(banner_ink.set(i)),
                if_ink.run().function('restworld:banners/banner_ink_cur'),
            )).place(r(x, y, z), SOUTH)
        )
    room.function('banner_controls_init').add(
        label(r(5, 2, 4), 'Banner / Ink'),
        label(r(3, 2, 4), 'Labels'),
        label(r(4, 2, 3), 'Controls'),
        mc.function('restworld:banners/switch_to_color'),
    )
    room.function('banner_controls_remove', needs_home=False).add(
        mc.fill(r(0, 2, 0), r(8, 4, 4), 'air', REPLACE).filter('#wall_signs'))

    room.loop('banner_ink', main_clock).loop(banner_ink_loop, COLORS)

    # ^Cyan Lozenge
    # ^Light Gray Base
    # ^Gray Pale
    # ^Light Gray Bordure
    # ^Black Fess
    # ^Light Gray Per Fess
    # ^Light Gray Roundel
    # ^Black Bordure
    room.function('ominous_banner').add(
        mc.setblock(r(0, 0, 0), Block('white_banner', nbt={
            'Patterns': [{'Pattern': "mr", 'Color': 9}, {'Pattern': "bs", 'Color': 8}, {'Pattern': "cs", 'Color': 7},
                         {'Pattern': "bo", 'Color': 8}, {'Pattern': "ms", 'Color': 15}, {'Pattern': "hh", 'Color': 8},
                         {'Pattern': "mc", 'Color': 8}, {'Pattern': "bo", 'Color': 15}]})))

    room.function('switch_to_color').add(switch_banners('color'))
    room.function('switch_to_ink').add(switch_banners('ink'))


def main():
    for f in (ancient_room, global_room, aquatic_room, arena_room, banners_room):
        f()
    restworld.save()


if __name__ == '__main__':
    main()


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
