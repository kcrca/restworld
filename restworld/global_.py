from __future__ import annotations

from pyker.commands import mc, entity, r, REPLACE, Score, Commands, MOVE, self, OVERWORLD, player, EQ, MOD, THE_END, \
    RAIN, CREATIVE, SIDEBAR
from pyker.enums import ScoreCriteria
from pyker.function import Function
from restworld.rooms import Room
from restworld.world import restworld, tick_clock, clock, main_clock


def room():
    def use_min_fill(y, filler, filter):
        return mc.execute().at(entity().tag('min_home')).run().fill((r(0), y, r(0)), (r(166), y, r(180)), filler,
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