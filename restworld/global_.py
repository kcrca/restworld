from __future__ import annotations

import copy
from itertools import count

from pynecraft.base import Arg, DARK_GREEN, DIRECTIONS, EAST, EQ, GAMETIME, LT, NOON, NORTH, OVERWORLD, Position, SOUTH, \
    THE_END, THE_NETHER, TimeSpec, WEST, r
from pynecraft.commands import Block, ClickEvent, Entity, FORCE, HoverEvent, MINUS, MOD, MOVE, REPLACE, RESULT, Score, \
    Text, clone, data, e, execute, fill, forceload, function, gamerule, give, kill, p, return_, s, schedule, scoreboard, \
    setblock, \
    tag, teleport, time, tp, trigger
from pynecraft.function import Function
from pynecraft.simpler import Book, VILLAGER_PROFESSIONS, WallSign
from pynecraft.values import DUMMY
from restworld.rooms import Room, kill_em
from restworld.world import clock, restworld, tick_clock

# -- Death: How it works:
#
# At the bottom of the world is an armor stand named "death". When we want to kill a mob, we teleport it to death,
# which kills everything within a few blocks of itself. It does this every tick, except those where any of the clocks
# is 0 or 1. This is because we're trying to keep the visual aspects of this away from the user up above. Killing
# things directly would be very visible, and leave items behind. The teleporting is basically invisible. But it's
# not always visually immediate. This is why the "0 or 1" exception exists: Those are the clock ticks on which
# things are being removed. If we kill on those same ticks, the user may see the mob start to die. Keeping the
# actual 'kill' command off those ticks reduces the chance of visual death.

# -- Clocks: How they work:
#
# Clocks have the following properties:
#   1. They run at specific but independent rates.
#   2. They should all start and stop together
#   3. There should be some visual feedback for whether they're running or not.
#   4. They only run when a player is in the room.
#
# The control blocks that govern this are under the middle of the world.
#
# Toggling clocks on and off is done by powering a repeating block that has the 'clock_tick' function is that does
# this arithmetic. The blocks are set such that when the redstone block that powers 'clock_tick' comes and goes it
# fires off neighboring blocks that run either 'clock_on' or 'clock_off', which switch the red/green (really lime)
# concrete blocks that indicate whether the buttons will start or stop the clock. 'clock_on' sets the block to
# redstone, and 'clock_off' sets it to something else.
#
# The clocks have their own scoreboard objects, 'clocks'. It has an overall counter 'clock' that is bumped each
# tick when the clocks are running. Each clock has a counter (e.g, 'main') and a rate ('SPEED_MAIN'). Every tick,
# 'main' is updated to clock % SPEED_MAIN.
#
# Each room has a clock trigger at its neg-x/neg-y corner. It consists of a repeating block that continuously
# checks if a player is in the room, using an 'execute at' command to run a simple command at the player in the
# room. When it successfully runs, the block generates a redstone signal, which is piped into a series of command
# blocks that run enter/exit functionality, plus the room's '_tick' function in a repeating block. When no player
# is in the room, _tick's block is unpowered and so doesn't run at all.
#
# The _tick function checks each clock for whether it is zero, and if it is, runs that room's '_main'
# (etc.) functions. These invoke every main-clock-driven function in the room, at its _home armor stand. All this
# means that on every tick, there is only one check about whether to run many functions (rather tha one
# check per function).

if_clock_running = execute().at(e().tag('clock_home')).if_().block(r(0, -2, 1), 'redstone_block')


def room():
    room = Room('global', restworld)

    def all_fill(y, filler, filter, destroy=False):
        cmd = fill((r(0), y, r(0)), (73, y, 99), filler).replace(filter)
        if destroy:
            cmd = cmd.destroy()
        return execute().at(e().tag('full_reset_home')).run(cmd)

    def clock_blocks(turn_on):
        lights = ('red_concrete', 'lime_concrete')
        before = lights[int(turn_on)]
        after = lights[1 - int(turn_on)]
        return (
            all_fill(100, after, before),
            execute().at(e().tag('particles_action_home')).run(setblock(r(0, 6, -4), after)))

    def kill_if_time():
        ex = execute()
        for c in restworld.clocks():
            ex = ex.unless().score(c.time).matches((0, 1))
        return ex.run(function('restworld:global/kill_em'))

    room.function('power_off').add(
        (all_fill(101, Block('lever', {'face': 'floor', 'facing': dir, 'powered': False}),
                  Block('lever', {'face': 'floor', 'facing': dir, 'powered': True})) for dir in DIRECTIONS)
    )

    mob_rooms = ('mobs', 'wither', 'nether', 'enders')

    def raise_mobs_func():
        yield execute().at(e().tag('sleeping_bat')).run(clone(r(0, 1, 0), r(0, 1, 0), r(0, 3, 0)).replace(MOVE)),
        yield execute().at(e().tag('turtle_eggs_home')).run(
            clone(r(2, 2, 0), r(-1, 2, 0), r(-1, 4, 0)).replace(MOVE)),
        yield execute().at(e().tag('sniffer_home')).run(
            clone(r(0, 2, 3), r(0, 2, 3), r(0, 4, 3)).replace(MOVE)),
        for mob_room in mob_rooms:
            room_home = mob_room + '_home'
            yield execute().as_(e().tag(room_home)).run(data().merge(s(), {'Invisible': True}))
            yield execute().as_(e().tag(room_home, '!blockers_home')).at(s()).run(tp(s(), r(0, 2, 0)))
            yield execute().as_(e().tag(mob_room, '!passenger').type('!text_display')).at(s()).run(
                tp(s(), r(0, 2, 0)))

    def lower_mobs_func():
        yield execute().at(e().tag('sleeping_bat')).run(clone(r(0, 1, 0), r(0, 1, 0), r(0, -1, 0)).replace(MOVE)),
        yield execute().at(e().tag('turtle_eggs_home')).run(
            clone(r(2, 4, 0), r(-1, 4, 0), r(-1, 2, 0)).replace(MOVE)),
        yield execute().at(e().tag('sniffer_home')).run(
            clone(r(0, 4, 3), r(0, 4, 3), r(0, 2, 3)).replace(MOVE)),
        for mob_room in mob_rooms:
            room_home = mob_room + '_home'
            yield execute().as_(e().tag(room_home)).run(data().merge(s(), {'Invisible': False}))
            yield execute().as_(e().tag(room_home, '!blockers_home')).at(s()).run(tp(s(), r(0, -2, 0)))
            yield execute().as_(e().tag(mob_room, '!passenger').type('!text_display')).at(
                s()).run(tp(s(), r(0, -2, 0)))

    room.function('arena').add(
        execute().in_(OVERWORLD).run(tp(p(), (1126, 103, 1079)).facing((1139, 104, 1079))))

    # The clock functions
    clock_toggle = room.score('clock_toggle')
    room.home_func('clock'),
    room.add(Function('clock_init').add(
        scoreboard().objectives().remove('clocks'),
        scoreboard().objectives().add('clocks', DUMMY),
        list(c.speed.set(c.init_speed) for c in restworld.clocks()),
        list(c.time.set(-1) for c in restworld.clocks()),
        tick_clock.time.set(0),
        function('restworld:global/clock_off'),
    ))
    room.add(Function('clock_tick').add(
        clock.time.add(1),
        (c.time.operation(EQ, clock.time) for c in restworld.clocks()),
        (c.time.operation(MOD, c.speed) for c in restworld.clocks()),
        kill_if_time()
    ))
    room.add(Function('clock_on').add(
        execute().at(e().tag('clock_home')).run(setblock(r(0, -2, 1), 'redstone_block'))))
    room.add(Function('clock_off').add(
        execute().at(e().tag('clock_home')).run(setblock(r(0, -2, 1), 'diamond_block'))))
    room.add(Function('clock_switched_on').add(
        clock_blocks(True)))
    room.add(Function('clock_switched_off').add(
        clock_blocks(False),
        (c.time.operation(EQ, c.speed) for c in restworld.clocks()),
        (c.time.remove(1) for c in restworld.clocks())))
    room.add(Function('clock_toggle').add(
        clock_toggle.set(0),
        if_clock_running.run(clock_toggle.set(1)),
        execute().if_().score(clock_toggle).matches(0).run(function('restworld:global/clock_on')),
        execute().if_().score(clock_toggle).matches(1).run(function('restworld:global/clock_off'))))

    def clock_sign(dir):
        name = f'clock_toggle_sign_{dir}_init'
        room.function(name, home=tag(s()).add('clock_sign'), single_home=False).add(
            WallSign(state={'waterlogged': True}).messages(
                (None, 'Toggle Clocks'),
                (function('restworld:global/clock_toggle'),)).glowing(True).place(r(0, 2, 0), dir),
            setblock(r(0, 1, 0), 'lime_concrete'))

    for dir in (NORTH, SOUTH, EAST, WEST):
        clock_sign(dir)

    def func(pos: Position, which: str, dir: str, repeat=False) -> str:
        yield setblock(pos, 'air')
        block = 'Repeating Command Block' if repeat else 'Command Block'
        yield setblock(pos, Block(block, {'facing': dir},
                                  {'Command': f'function restworld:{Arg("room")}/{which}'}))

    room.function('room_bounds', home=False).add(
        func(r(-1, 0, 0), '_init', EAST),
        setblock(r(-1, -1, 0), 'pumpkin'),
        setblock(r(-1, -2, -1), 'glowstone'),
        setblock(r(-1, 0, -1), 'air'),
        setblock(r(-1, 0, -1), ('repeating_command_block', {'facing': EAST}, {'auto': True, 'Command': str(
            execute().positioned(r(0, -2, 0)).as_(p().volume((Arg('dx'), 15, Arg('dz'))).limit(1)).run(return_(0)))[1:]}
                                )),
        setblock(r(0, -1, -1), ('red_sandstone_slab', {'type': 'top'})),
        setblock(r(0, 0, -1), ('comparator', {'facing': WEST})),
        func(r(1, 0, -1), '_enter', SOUTH),
        func(r(1, 0, 0), '_tick', SOUTH, repeat=True),
        setblock(r(2, 0, -1), ('redstone_wall_torch', {'facing': EAST})),
        func(r(3, 0, -1), '_exit', SOUTH),
        setblock(r(-1, -1, -1), 'air'),
        setblock(r(3, 0, 0), 'glowstone'),

        # debug stuff commented out
        # execute().positioned(r(-1, 0, -1)).run(setblock(r(0, 10, 0), 'stone')),
        # setblock(r(Arg('dx'), 10, Arg('dz')), 'stone'),
    )

    # The death functions
    home_sign = WallSign((None, 'Go Home'), (None, function('restworld:global/goto_home')))
    killables = e().not_type('player').not_tag('death').distance((None, 30))
    killer = room.function('killer').add(
        execute().at(e().tag('death')).run(kill(killables)),
        execute().at(e().tag('death')).as_(killables).run(data().merge(s(), {'DeathTime': -1200})),
    )
    room.function('death_init', home=False).add(
        kill(e().tag('death').distance((None, 10))),
        kill(e().type('armor_stand').distance((None, 10))),
        Entity('armor_stand', nbt={'NoGravity': True}).tag('death', 'immortal').summon(r(0, 0.5, 0)),
        fill(r(-5, -5, -5), r(5, 5, 5), 'air').replace('#all_signs'),
        fill(r(-5, -5, -5), r(5, 5, 5), 'air').replace('repeating_command_block'),
        setblock(r(1, 0, 0), Block('repeating_command_block', nbt={'Command': str(function(killer)), 'auto': True})),
        setblock(r(-1, 0, 0), Block('glowstone')),
        setblock(r(0, 0, -1), Block('stone_button')),
        home_sign.place(r(0, 2, 2), NORTH),
        home_sign.place(r(0, 2, -2), SOUTH),
        home_sign.place(r(2, 2, 0), WEST),
        home_sign.place(r(-2, 2, 0), EAST),
    )

    room.function('full_finish').add(
        function('restworld:_init'),
        function('restworld:_cur'),
        # Some of these functions leave dropped items behind, this cleans that up
        kill(e().type('item')),
    )

    room.function('full_reset').add(
        function('restworld:global/clock_off'),
        execute().positioned(r(0, -3, 0)).run(function('restworld:global/full_reset_home')),
        kill(e().tag('home', '!full_reset_home')),
        # Death must be ready before any other initialization
        execute().positioned((0, 5, 0)).run(function('restworld:global/death_init')),
        all_fill(97, 'redstone_block', 'dried_kelp_block'),
        all_fill(97, 'dried_kelp_block', 'redstone_block'),
        all_fill(97, 'redstone_block', 'pumpkin'),
        all_fill(97, 'pumpkin', 'redstone_block'),
        function('restworld:/_init'),
    )

    room.function('gamerules').add(
        (gamerule(*args) for args in (
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
    for place in (
            ('biomes', OVERWORLD, (-1024, 101, -937), (-1024, 80, -907)),
            ('optifine', OVERWORLD, (1023, 101, 1024), (1023, 101, 114)),
            ('end_home', THE_END, (100, 49, 0), (90, 50, 0)),
            ('home', OVERWORLD, (0, 101, 0), (0, 101, 10)),
            ('nether', THE_NETHER, (22, 99, -13), (28, 100, -13)),
            ('arena', OVERWORLD, (1040, 106, -1026), (1036, 104, -1026))):
        room.function('goto_' + place[0], home=False).add(
            time().set(NOON),
            execute().in_(place[1]).run(teleport(p(), place[2]).facing(place[3])),
            schedule().function(f'restworld:{place[0]}/_enter', 1, REPLACE),
        )
    room.function('goto_photo').add(function('restworld:photo/photo_sample_view'))
    room.function('goto_arena', exists_ok=True).add(function('restworld:arena/arena_count_cur'))
    room.home_func('min')

    raise_mobs = room.function('raise_mobs', home=False).add(raise_mobs_func())
    lower_mobs = room.function('lower_mobs', home=False).add(lower_mobs_func())

    mobs_up = room.score('mobs_up')
    room.function('toggle_raised', home=False).add(
        execute().store(RESULT).score(mobs_up).at(e().tag('turtle_eggs_home')).if_().entity(
            e().type('turtle').distance((None, 3))),
        execute().if_().score(mobs_up).matches(0).run(function(lower_mobs)),
        execute().unless().score(mobs_up).matches(0).run(function(raise_mobs)),
    )
    room.function('reset_raised', home=False).add(
        execute().unless().score(mobs_up).matches(0).run(function(lower_mobs)),
        mobs_up.set(0))

    last_clean = room.score('last_clean_time')
    clean_time = room.score('ensure_clean_time', 600)
    clean_time_max = room.score_max('ensure_clean_time')
    ensure_clean_init = room.function('ensure_clean_init', home=False).add(
        clean_time_max.set(600)
    )
    room.function('ensure_clean').add(
        execute().store(RESULT).score(clean_time).run(time().query(GAMETIME)),
        clean_time.operation(MINUS, last_clean),
        execute().if_().score(clean_time).is_(LT, clean_time_max).run(return_()),
        execute().store(RESULT).score(last_clean).run(time().query(GAMETIME)),
        # Make sure kids don't grow up
        execute().as_(e().tag('kid')).run(data().merge(s(), {'Age': -2_147_483_648, 'IsBaby': True})),
        # Keep chickens from leaving eggs around
        execute().as_(e().type('chicken')).run(data().merge(s(), {'EggLayTime': 1000_000_000})),
        # Make sure the item in the display doesn't vanish
        execute().as_(e().tag('item_ground')).run(data().merge(s(), {'Age': -32_768, 'PickupDelay': 2_147_483_647})),
        # Frog spawning seems to just happen without the random ticks, so stop it
        execute().at(e().tag('frog_home')).run(clone(r(1, 2, 0), r(1, 2, 0), r(1, 2, 0)).replace(FORCE)),
        kill_em(e().type('tadpole').tag('!keeper')),
        kill_em(e().type('frog').tag('!frog')),
        # See https://bugs.mojang.com/browse/MC-261475 -- eventually the egg will hatch even without randomTicks, so...
        execute().at(e().tag('sniffer_home')).run(function('restworld:mobs/sniffer_cur')),  # if missing, place it.
        execute().at(e().tag('sniffer_home')).run(function('restworld:mobs/sniffer_egg_reset')),  # if there, reset
        kill_em(e().type('sniffer').tag('!keeper').distance((None, 100))),  # if spawned, kill that extra sniffer
        # Make sure the TNT never goes off
        execute().as_(e().type('tnt')).run(data().merge(s(), {'fuse': 0x7fff})),
    )

    # This is why this room must be last -- it relies on the list of rooms built by creating all of them.
    book_trigger = room.trigger('control_book_triggers')
    next_trigger = count(start=1)

    def book_action(txt: str, tooltip: str, act: str) -> Text:
        num = next(next_trigger)
        book_trigger.trigger(function('restworld:' + act), num)
        return Text.text(txt).color(DARK_GREEN).underlined().click_event(ClickEvent.run_command(
            trigger(book_trigger.objective).set(num))).hover_event(HoverEvent.show_text(tooltip))

    room.function('control_book_triggers_init').add(forceload().add(r(0, -1)))

    cb = Book()
    cb.sign_book('Control Book', 'RestWorld', 'Useful Commands')

    cb.add(r'Clock State:\n      ',
           book_action(r'|\u25c0\u25c0', 'Previous', '_decr'), r'  ',
           book_action(r'||', 'Play/Pause', 'global/clock_toggle').bold(),
           book_action(r'/\u25b6', 'Play/Pause', 'global/clock_toggle'), '  ',
           book_action(r'\u25b6\u25b6|', 'Next', '_incr'), r'\n', r'\nClock Speed:\n      ',
           book_action(r'<<', 'Slower Clock Speed', 'center/slower_clocks'), '   ',
           book_action(r'\u27f2', 'Reset Clock Speed', 'center/reset_clocks'), '   ',
           book_action(r'>>', 'Faster Clock Speed', 'center/faster_clocks'), r'\n',
           r'\nPlaces (click to visit):\n   ',
           book_action('Home', 'Starting Point', 'global/goto_home'), r'\n   ',
           book_action('Photo Shoot', 'Scenic View', 'global/goto_photo'), r'\n   ',
           book_action('Arena', 'Arena', 'global/goto_arena'), r'\n   ',
           book_action('Biome Sampler', 'Biome Sampler', 'global/goto_biomes'), r'\n   ',
           book_action('Optifine', 'Optifine Features', 'global/goto_optifine'), r'\n   ',
           book_action('Nether Home', 'Nether Starting Point', 'global/goto_nether'), r'\n   ',
           book_action('End Home', 'End Starting Point', 'global/goto_end_home'), r'\n   ',
           )

    cb.next_page()
    cb.add(r'Room travel links: \n\n')
    rooms = filter(lambda x: isinstance(x, Room) and x.title is not None, restworld.function_set.children)
    rooms = sorted(rooms, key=lambda x: x.title)
    first = True
    for rm in rooms:
        if first:
            first = False
        else:
            cb.add(Text(' ⸫ '))
        cb.add(book_action(rm.title, rm.title, rm.name + '/_goto'))

    room.function('control_book', home=False).add(give(p(), cb.as_entity()))

    # These functions only exist for my MegaVillage project which does not (yet) have its own code, and it's so small
    # that it was just easier to plunk it here and copy it.
    census = room.function('census', home=False).add(tag(e().tag('all')).remove('none'))
    middle = e().tag('census_taker')
    prof_scores = {}
    base_selector = e().type('villager').distance((None, 50))
    for profession in ('all', 'kid') + VILLAGER_PROFESSIONS:
        score = Score(profession.lower(), 'census')
        prof_scores[profession] = score
        selector = copy.deepcopy(base_selector)
        if profession == 'kid':
            selector = selector.not_nbt({'Age': 0})
        elif profession != 'all':
            selector = selector.nbt({'VillagerData': {'profession': f'minecraft:{profession}'}})
        census.add(score.set(0), execute().at(middle).as_(selector).run(score.add(1)),
                   tag(selector).add(profession))
    employed = Score('employed', 'census')
    census.add(employed.operation(EQ, prof_scores['all']), employed.operation(MINUS, prof_scores['none']),
               prof_scores['none'].operation(MINUS, prof_scores['kid']), tag(e().tag('kid')).remove('none'),
               schedule().function("minecraft:census", TimeSpec('15s'), REPLACE))
