from __future__ import annotations

from pyker.commands import mc, e, r, Commands, MOVE, s, OVERWORLD, EQ, MOD, THE_END, \
    RAIN, CREATIVE, SIDEBAR, GAMETIME, RESULT, p
from pyker.enums import ScoreCriteria
from pyker.function import Function
from restworld.rooms import Room
from restworld.world import restworld, tick_clock, clock, kill_em


def room():
    def use_min_fill(y, filler, filter):
        return mc.execute().at(e().tag('min_home')).run().fill((r(0), y, r(0)), (r(166), y, r(180)),
                                                               filler).replace(filter)

    def clock_blocks(turn_on):
        lights = ('red_concrete', 'lime_concrete')
        before = lights[int(turn_on)]
        after = lights[1 - int(turn_on)]
        return (
            use_min_fill(100, after, before),
            mc.execute().at(e().tag('min_home')).run().setblock((0, 105, -78), after),
            mc.execute().at(e().tag('aquatic_anchor')).run().fill(
                r(-7, -1, 0), r(7, 5, 20), after).replace(before),
        )

    def kill_if_time():
        ex = mc.execute()
        for c in restworld.clocks():
            ex = ex.unless().score(c.time).matches((0, 1))
        return ex.run().function('restworld:global/kill_em')

    def mob_levitation_loop(step) -> Commands:
        mob_rooms = ('friendlies', 'monsters', 'aquatic', 'wither', 'nether', 'enders', 'ancient')
        if step.i == 1:
            yield mc.execute().at(e().tag('sleeping_bat')).run().clone(
                r(0, 1, 0), r(0, 1, 0), r(0, 3, 0)).replace(MOVE),
            yield mc.execute().at(e().tag('turtle_eggs_home')).run().clone(
                r(1, 2, 0), r(-2, 2, 0), r(-2, -4, 0)).replace(MOVE),
            # yield mc.execute().at(entities().tag('brown_horses', 'kid')).run().clone(*r(2, 0, 0, 2, 0, 0, 2, 2, 0)).replace(
            #     MOVE),
            for mob_room in mob_rooms:
                room_home = mob_room + '_home'
                yield mc.execute().as_(e().tag(room_home)).run().data().merge(
                    s(), {'Invisible': True})
                yield mc.execute().as_(e().tag(room_home, '!blockers_home')).at(s()).run().tp(s(),
                                                                                              r(0, 2, 0))
                yield mc.execute().as_(e().tag(mob_room, '!passenger').type('!item_frame')).at(
                    s()).run().tp(s(), r(0, 2, 0))
        else:
            yield mc.execute().at(e().tag('sleeping_bat')).run().clone(
                r(0, 1, 0), r(0, 1, 0), r(0, -1, 0)).replace(MOVE),
            yield mc.execute().at(e().tag('turtle_eggs_home')).run().clone(
                r(1, 4, 0), r(-2, 4, 0), r(-2, 2, 0)).replace(MOVE),
            # yield mc.execute().at(entities().tag('brown_horses', 'kid')).run().clone(*r(2, 0, 0, 2, 0, 0, 2, 2, 0)).replace(
            #     MOVE),
            for mob_room in mob_rooms:
                room_home = mob_room + '_home'
                yield mc.execute().as_(e().tag(room_home)).run().data().merge(
                    s(), {'Invisible': False})
                yield mc.execute().as_(e().tag(room_home, '!blockers_home')).at(s()).run().tp(s(),
                                                                                              r(0, -2, 0))
                yield mc.execute().as_(e().tag(mob_room, '!passenger').type('!item_frame')).at(
                    s()).run().tp(s(), r(0, -2, 0))

    room = Room('global', restworld)
    clock_toggle = room.score('clock_toggle')
    room.function('arena').add(
        mc.execute().in_(OVERWORLD).run().tp(p(), (1126, 103, 1079)).facing((1139, 104, 1079)))
    room.home_func('clock'),
    room.add(
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
            mc.execute().at(e().tag('clock_home')).run().setblock(r(0, -2, 1), 'redstone_block')),
        Function('clock_off').add(
            mc.execute().at(e().tag('clock_home')).run().setblock(r(0, -2, 1), 'diamond_block')),
        Function('clock_switched_on').add(
            clock_blocks(True)),
        Function('clock_switched_off').add(
            clock_blocks(False),
            (c.time.operation(EQ, c.speed) for c in restworld.clocks()),
            (c.time.remove(1) for c in restworld.clocks()),
        ),
        Function('clock_toggle').add(
            clock_toggle.set(0),
            mc.execute().at(e().tag('clock_home')).if_().block(r(0, -2, 1), 'redstone_block').run(
                clock_toggle.set(1)),
            mc.execute().if_().score(clock_toggle).matches(0).run().function('restworld:global/clock_on'),
            mc.execute().if_().score(clock_toggle).matches(1).run().function('restworld:global/clock_off'),
        ),
    )
    death_home = room.home_func('death')
    room.function('death_init').add(
        mc.execute().positioned((0, 1.5, 0)).run().function(death_home.full_name),
        mc.tag(e().tag(death_home.name)).add('death'),
        mc.tag(e().tag(death_home.name)).add('immortal'),
    )
    killables = e().not_type('player').not_tag('death').distance((None, 30))
    room.function('kill_em').add(
        mc.execute().at(e().tag('death')).run().kill(killables),
        mc.execute().at(e().tag('death')).as_(killables).run().data().merge(s(),
                                                                            {'DeathTime': -1200}),
    )

    room.function('full_finish').add(
        mc.function('restworld:_init'),
        mc.function('restworld:_cur'),
        # Some of these functions leave dropped items behind, this cleans that up'
        mc.kill(e().type('item')),
    )
    room.function('full_reset').add(
        mc.function('restworld:global/clock_off'),
        mc.execute().positioned(r(0, -3, 0)).run().function('restworld:global/min_home'),
        mc.kill(e().tag('home', '!min_home')),
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
    for place in (
            ('biomes', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('connected', OVERWORLD, (1000, 101, 1000), (990, 101, 1000)),
            ('end_home', THE_END, (100, 49, 0), (-1000, 80, -970)),
            ('home', OVERWORLD, (0, 101, 0), (0, 101, 10)),
            ('nether', OVERWORLD, (-1000, 101, -1000), (-1000, 80, -970)),
            ('arena', OVERWORLD, (1014, 106, -1000), (1000, 100, -1000))):
        room.function('goto_' + place[0], home=False).add(
            mc.execute().in_(place[1]).run().teleport(p(), place[2]).facing(place[3]))
    room.function('goto_photo').add(mc.function('restworld:photo/photo_example_view'))
    room.function('goto_weather', home=False).add(
        mc.execute().in_(OVERWORLD).run().teleport(p(), (1009, 101, 1000)).facing((1004, 102, 1000)),
        mc.weather(RAIN))
    room.home_func('min')

    room.loop('mob_levitation').loop(mob_levitation_loop, range(0, 2))

    room.function('ready').add(
        mc.clear(p()),
        mc.gamemode(CREATIVE, p()),
        mc.function('restworld:global/control_book'),
        mc.tp(p(), (0, 101, 0)).facing((0, 100, 5)),
        mc.scoreboard().objectives().setdisplay(SIDEBAR),
        mc.function('restworld:center/reset_clocks'),
        mc.function('restworld:global/clock_on'),
    )

    clean_time = room.score('ensure_clean_time')
    clean_time_max = room.score_max('ensure_clean_time')
    room.function('ensure_clean_init').add(clean_time_max.set(10_000))
    room.loop('ensure_clean', tick_clock).add(
        mc.execute().store(RESULT).score(clean_time).run().time().query(GAMETIME),
        clean_time.operation(MOD, clean_time_max),
        mc.execute().if_().score(clean_time).matches(0).run().function('restworld:global/ensure_clean_run')
    ).loop(None, None)
    room.function('ensure_clean_run', home=False).add(
        # Make sure kids don't grow up
        mc.execute().as_(e().tag('kid')).run().data().merge(s(), {'Age': -2147483648, 'IsBaby': True}),
        # Keep chickens from leaving eggs around
        mc.execute().as_(e().type('chicken')).run().data().merge(s(), {'EggLayTime': 1000000000}),
        # Frog spawning seems to just happen without the random ticks, so stop it
        mc.execute().at(e().tag('frog_home')).run().fill(r(-2, 2, -2), r(2, 2, 2), 'frogspawn').replace(
            'frogspawn'),
        kill_em(e().type('tadpole').tag('!keeper')),
        kill_em(e().type('frog').tag('!frog')),
    )
