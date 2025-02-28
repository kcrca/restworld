from __future__ import annotations

import sys

from pynecraft.base import Arg, EAST, GT, LT, Nbt, r, seconds, to_id
from pynecraft.commands import Entity, RANDOM, REPLACE, Score, a, data, e, execute, fill, function, kill, schedule, \
    setblock, summon, tag
from pynecraft.function import Function, Loop
from pynecraft.simpler import Item, Region, Sign, WallSign
from restworld.rooms import Room, kill_em
from restworld.world import main_clock, marker_tmpl, restworld

COUNT_MIN = 1
COUNT_MAX = 5

battle_types = {'w': 1, 'c': 2, 'g': 3}


#
# I tried to use macros to simplify this, with a design like that below (kept for future reference), but it turned out
# that the difficulties of passing values to macro functions that were nbt structures kept being very difficult to the
# point where I decided it wasn't worth it when the existing system worked.
#
# Design (starting point):
#     Storage data is used to describe the current (and previous?) arena configuration:
#       type : of battle, numerically (because you can't compare anything but scores (honest!))
#       hunter:
#           id: of monster
#           nbt: for monster
#           splitter: True (if False, absent)
#       victim: (same as hunter, or absent for non-battles)
#
#     Each sign has a command that invokes "start_battle" with the new arena configuration.
#
#     start_battle stores the new arena configuration.
#       if new type is different, set up new type
#       set the new storage data values
#       adds role to data ("hunter" or "victim" (maybe 0 or 1, but I think not))
#       (misc. other stuff?)
#
#     monitor_tick runs every tick, and invokes do_monitor with storage data
#
#     do_monitor:
#       runs check_count with arena.hunter and arena.victim
#       cleans out any loose items sitting around
#       (misc. other stuff?)

def is_splitter_mob(mob):
    return mob in ('Slime', 'Magma Cube')


def room():
    room = Room('arena', restworld)

    def protected(armor):
        return {'id': armor, 'components': {'repair_cost': 1, 'enchantments': {'protection': 5}}}

    start_battle_type = Score('battle_type', 'arena')
    skeleton_nbts = {'equipment': {'mainhand': Item.nbt_for('bow'), 'feet': protected('iron_boots'),
                                   'head': protected('iron_helmet')}}
    fighter_nbts = {
        'Drowned': {'equipment': {'mainhand': Item.nbt_for('trident')}},
        'Goat': {'IsScreamingGoat': True, 'HasLeftHorn': True, 'HasRightHorn': True},
        'Hoglin': {'IsImmuneToZombification': True},
        'Llama': {'Strength': 5},
        'Magma Cube': {'Size': 3},
        'Slime': {'Size': 3},
        'Panda': {'MainGene': 'aggressive'},
        'Phantom': {'AX': 1000, 'AY': 110, 'AZ': -1000},
        'Piglin Brute': {'equipment': {'mainhand': Item.nbt_for('golden_axe')}, 'IsImmuneToZombification': 'True'},
        'Piglin': {'IsImmuneToZombification': 'True', 'equipment': {'mainhand': Item.nbt_for('golden_sword')}},
        'Pillager': {'equipment': {'mainhand': Item.nbt_for('crossbow')}},
        'Skeleton': skeleton_nbts,
        'Stray': skeleton_nbts,
        'Bogged': skeleton_nbts,
        'Vindicator': {'Johnny': 'True', 'equipment': {'mainhnad': Item.nbt_for('iron_axe')}},
        'Wither Skeleton': {'equipment': {'mainhand': Item.nbt_for('stone_sword')}},
        'Zombie': {'equipment': {'head': Item.nbt_for('iron_helmet')}},
        'Zombified Piglin': {'equipment': {'mainhand': Item.nbt_for('golden_sword')}},
    }

    # Lower priority ones can be used as filler
    battles = [
        ('Axolotl:w', 'Drowned'),
        ('Creaking', 'You'),
        ('Axolotl:w', 'Guardian'),
        ('Blaze', 'Snow Golem'),
        ('Bogged', 'Iron Golem'),
        ('Breeze', 'Iron Golem'),
        ('Cat', 'Rabbit'),
        # ('Cave Spider', 'Snow Golem'), # low priority
        # ('Drowned', 'Snow Golem'), # lwo priority
        ('Ender Dragon', None),
        ('Evoker', 'Iron Golem'),
        ('Fox', 'Chicken'),
        # ('Frog', 'Slime'),  # low priority
        ('Goat', 'Sheep'),  # medium priority (slow, but charging goat)
        ('Hoglin', 'Vindicator'),
        # ('Illusioner', 'Snow Golem'), # low priority, Illusioner isn't used
        ('Llama', 'Vindicator'),
        ('Magma Cube', 'Iron Golem'),
        # ('Ocelot', 'Chicken'),  # low priority
        ('Panda', 'Vindicator'),
        ('Parrot', 'Vindicator'),  # low priority
        ('Phantom:c', None),
        ('Piglin Brute', 'Vindicator'),
        ('Pillager', 'Snow Golem'),
        ('Polar Bear', 'Vindicator'),
        ('Ravager', 'Iron Golem'),
        ('Shulker', 'Vindicator'),
        ('Skeleton', 'Iron Golem'),
        ('Slime', 'Iron Golem'),
        ('Sniffer:g', None),
        ('Spider', 'Snow Golem'),
        ('Stray', 'Iron Golem'),
        ('Vindicator', 'Iron Golem'),
        ('Warden', 'Iron Golem'),
        ('Witch', 'Snow Golem'),
        ('Wither Skeleton', 'Piglin'),
        ('Wither', 'Pillager'),
        ('Wolf', 'Sheep'),
        ('Zoglin', 'Vindicator'),
        ('Zombie', 'Iron Golem'),
        ('Zombified Piglin', 'Vindicator'),
    ]
    # With Slime and Magma Cube it _mostly_ works, but not perfectly. These are handled by giving a custom name to
    # the summoned mob, which is inherited by its descendants. We then see, if the count is at least 3, whether there
    # is any mob labelled "3" (say). If not a new top-level "3"" is summoned. This way each mob will only be replaced
    # when all its descendants are gone. But... the problem is there is a gap in time between when "3" is killed and
    # its kids are spawned, during which time there is no "3". So a new one is summoned. Thus, the actual count of
    # slimes and magma cubes is off a bit. If I figure out a way to fix this, I'll fix it. For now it seems mildly
    # annoying, but better than the previous alternative where only the smallest slimes and cubes could be summoned,
    # since that could be handled by the general algorithm.

    stride_length = 6
    num_rows = 2
    row_length = stride_length / num_rows
    if stride_length % num_rows != 0:
        sys.stderr.write(f'rows ({num_rows:d}) is not a multiple of stride length ({stride_length:d})')
        sys.exit(1)
    if row_length % 2 == 0:
        # Needed so we can center on the middle sign
        sys.stderr.write(f'Row length({row_length:d}) is not odd')
        sys.exit(1)
    if len(battles) % stride_length != 0:
        sys.stderr.write(
            f'Stride length ({stride_length:d}) is not a multiple of battle count ({len(battles):d})\n')
        sys.exit(1)

    battles.sort()

    monitor_home = e().tag('monitor_home')

    left_arrow = '<--'
    right_arrow = '-->'

    def arena_run_main(loop: Loop):
        def arena_run_loop(step):
            i = step.i
            for which_dir in (-1, 1):
                to_front = (i + which_dir + num_pages) % num_pages
                to_back = (i - which_dir + num_pages) % num_pages
                text, z = (left_arrow, max_z + 1) if which_dir == -1 else (right_arrow, min_z - 1)
                back_text = left_arrow if text == right_arrow else right_arrow
                run_cur = execute().at(e().tag('controls_home')).run(
                    function(f'restworld:arena/{step.loop.score.target}_cur'))
                yield WallSign().front((None, text), (step.loop.score.set(to_front), run_cur)).back(
                    (None, back_text), (step.loop.score.set(to_back), run_cur)).glowing(True).place(r(x, 2, z), EAST)
            for s in range(0, stride_length):
                y = 3 - int(s / row_length)
                z = max_z - (s % row_length)
                hunter, victim = step.elem[s]

                battle_type = 0
                if hunter[-2] == ':':
                    battle_type = battle_types[hunter[-1]]
                    hunter = hunter[0:-2]

                def incr_cmd(which, mob, center=False):
                    my_nbts = Nbt({'Tags': ['battler', which]})
                    added_nbt = fighter_nbts.get(mob, None)
                    if added_nbt:
                        my_nbts = my_nbts.merge(added_nbt)
                    if which == 'hunter':
                        my_nbts = my_nbts.merge({'Rotation': [180, 0]})
                    splitter_mob = is_splitter_mob(mob)
                    y_off = 3 if battle_type == 3 else 2
                    z_off = -4 if center else 0
                    if splitter_mob:
                        f = room.function(f'incr_{to_id(mob)}_{which}', home=False)
                        for i in range(COUNT_MIN, COUNT_MAX + 1):
                            incr = summon(Entity(mob, my_nbts).merge_nbt(
                                {'CustomName': str(i), 'CustomNameVisible': False}), r(0, y_off, z_off))
                            f.add(execute().if_().score(arena_count).matches((i, COUNT_MAX)).unless().entity(
                                e().nbt({'CustomName': str(i)}).limit(1)).run(incr))
                        return function(f)
                    incr = summon(Entity(mob, my_nbts), r(0, y_off, z_off))
                    incr_cmd = execute().if_().score((f'{which}_count', 'arena')).is_(LT, arena_count).at(
                        e().tag(f'{which}_home').sort('random').limit(1)).run(incr)
                    return incr_cmd

                data_change = execute().at(monitor_home)
                alone = victim is None or victim == 'You'
                sign_commands = (
                    data_change.run(data().merge(r(3, 0, 0), {'Command': incr_cmd('hunter', hunter, alone)})),
                    data_change.run(
                        data().merge(r(2, 0, 0), {'Command': incr_cmd('victim', 'marker' if alone else victim)})),
                    start_battle_type.set(battle_type),
                    function('restworld:arena/start_battle', {'hunter_is_splitter': is_splitter_mob(hunter),
                                                              'victim_is_splitter': is_splitter_mob(victim)})
                )
                sign = WallSign().messages((None, hunter, 'vs.', victim if victim else 'Nobody'), sign_commands)
                yield sign.place(r(-2, y, z), EAST)

                run_type = Score('arena_run_type', 'arena')
                yield execute().unless().score(run_type).matches((0, None)).run(run_type.set(0))

        chunks = []
        for i in range(0, len(battles), stride_length):
            chunks.append(battles[i:i + stride_length])

        num_pages = int(len(battles) / stride_length)
        end = int(row_length / 2)
        min_z = -end
        max_z = +end
        x = -2

        loop.add(fill(r(x, 2, min_z - 1), r(x, 2 + num_rows - 1, max_z + 1), 'air'))
        loop.loop(arena_run_loop, chunks)
        return loop

    def random_stand(actor: str):
        var = actor + '_home'
        yield kill(e().tag(var))
        stand = marker_tmpl.clone().merge_nbt({'Tags': [var, 'home', 'arena_home']})
        for x in range(-1, 2):
            for z in range(-1, 2):
                yield stand.summon(r(x, 0.5, z))

    def counter(battler: str, splitter: Score) -> Function:
        count = room.score(f'{battler}_count')
        func = room.function(f'count_{battler}', home=False).add(
            count.set(0),
            execute().if_().score(splitter).matches(0).as_(e().tag(battler)).run(count.add(1))
        )
        for i in range(COUNT_MIN, COUNT_MAX + 1):
            func.add(execute().unless().score(splitter).matches(0).if_().entity(
                e().nbt({'CustomName': str(i)}).limit(1)).run(count.add(1)))
        return func

    def toggle_peace(step):
        yield execute().at(e().tag('monitor_home')).run(fill(
            r(2, -1, 0), r(3, -1, 0), 'redstone_block' if step.elem else 'air')),
        if not step.elem:
            yield function(clean_out),
        yield setblock(r(0, 1, 0), f'{"red" if step.elem else "lime"}_concrete'),

    arena_count = room.score('arena_count', 5)

    arena_count_finish = room.function('arena_count_finish', home=False).add(
        execute().if_().score(arena_count).matches((None, COUNT_MIN)).run(arena_count.set(COUNT_MIN)),
        execute().if_().score(arena_count).matches((COUNT_MAX, None)).run(arena_count.set(COUNT_MAX)),
        function('restworld:arena/arena_count_cur'),
    )
    arena_count_cur = function(arena_count_finish.full_name)
    room.function('arena_count_decr', home=False).add(arena_count.remove(1), arena_count_cur)
    room.function('arena_count_incr', home=False).add(arena_count.add(1), arena_count_cur)
    room.function('arena_count_init', home=False).add(arena_count.set(5), arena_count_cur)
    room.loop('arena_count', main_clock, home=False).loop(
        lambda step: execute().at(e().tag('controls_home')).run(
            Sign.change(r(2, 4, 0), (None, f'{step.elem:d} vs. {step.elem:d}'))), range(0, COUNT_MAX + 1))

    room.function('arena_run_init').add(
        function('restworld:arena/arena_run_cur'),
    )

    # This is NOT intended to be run on the clock. It is only called '_main' because that gives us a
    # '_cur' function, which is useful when paging through the signs. Do not create the _home armor stand.
    arena_run_loop = arena_run_main(room.loop('arena_run', main_clock, home=False))

    room.function('controls_init').add(
        arena_run_loop.score.set(0),
        function('restworld:arena/arena_run_cur'),
        room.label(r(1, 3, 0), 'Go Home', EAST),
        tag(e().tag('controls_home')).add('controls_action_home'),
        # This init func won't get run because there is no home
        function('restworld:arena/arena_count_init'),
    )

    room.function('hunter_home').add(random_stand('hunter'))
    room.function('victim_home').add(random_stand('victim'))

    h_is_splitter = room.score('hunter_is_splitter')
    v_is_splitter = room.score('victim_is_splitter')
    h_counter = counter('hunter', h_is_splitter)
    v_counter = counter('victim', v_is_splitter)

    room.function('monitor').add(
        function(h_counter),
        function(v_counter),
        kill(e().type('experience_orb').distance((None, 50))),
    )
    # For some reason, arena_count_init doesn't always get run on _init, so we make sure that value is always in range.
    room.function('monitor_cleanup', home=False).add(
        execute().unless().score(arena_count).matches((COUNT_MIN, COUNT_MAX)).run(arena_count.set(1)),
        (execute().if_().score(room.score(f'{who}_count')).is_(GT, arena_count).run(kill(
            e().tag(who).sort(RANDOM).limit(1).distance((None, 100))))
            for who in ('hunter', 'victim')),
        (execute().if_().score(room.score(f'{who}_count')).is_(LT, arena_count).run(
            execute().at(e().tag(f'{who}_home')).run(setblock(r(-3, -1, 0), 'redstone_block'),
                                                     setblock(r(-3, -1, 0), 'air')))
            for who in ('hunter', 'victim')),
    )

    # The splitters create a problem -- if a splitter was killed but, before its kids are spawned, a new battle is
    # started, those kids will spawn into the new battle. We clean this up by figuring out if we are switching from
    # an old battle with splitters to a new one without, and if so, we schedule a killing of holdover splitters a
    # second later. There is a standard "frog_food" entity tag that includes all splitters, which we use for killing
    # them; otherwise we'd invent one. But we can't use an "if entity" on them to see if the old battle has splitters
    # because of a tiny chance that the only such entity was just killed, so the entity wouldn't be found at the "if"
    # test.
    arena = Region(r(-12, 2, -12), r(12, 4, 12))
    ground = Region(r(-12, 2, -12), r(12, 2, 12))
    sky = Region((r(-20), 250, r(-20)), (r(20), 250, r(20)))
    is_splitters = room.score('is_splitters')
    was_splitters = room.score('was_splitters')
    kill_splitters = room.function('kill_splitters', home=False).add(
        execute().at(monitor_home).run(kill_em(e().type('#frog_food').distance((None, 100))))
    )
    kill_splitters = schedule().function(kill_splitters, seconds(1), REPLACE)
    clean_out = room.function('clean_out', home=False).add(
        execute().at(monitor_home).run(tag(e().type('armor_stand').distance((None, 100))).add('arena_safe')),
        execute().at(monitor_home).run(kill_em(e().not_tag('arena_safe').distance((None, 100)))),
        kill_splitters,
    )
    # Battle types: 0-normal, 1-water, 2-undead
    room.function('start_battle', home=False).add(
        kill(e().type('item').distance((None, 50))),
        was_splitters.set(h_is_splitter + v_is_splitter),
        h_is_splitter.set(Arg('hunter_is_splitter')),
        v_is_splitter.set(Arg('victim_is_splitter')),
        is_splitters.set(h_is_splitter + v_is_splitter),
        execute().unless().score(was_splitters).matches(0).if_().score(is_splitters).matches(0).run(kill_splitters),
        execute().unless().score(start_battle_type).matches((0, None)).run(start_battle_type.set(0)),
        execute().unless().score(start_battle_type).matches(1).at(monitor_home).run(arena.fill('air')),
        execute().if_().score(start_battle_type).matches(1).at(monitor_home).run(arena.fill('water')),
        execute().unless().score(start_battle_type).matches(2).at(monitor_home).run(sky.fill('air')),
        execute().if_().score(start_battle_type).matches(2).at(monitor_home).run(sky.fill('glowstone')),
        execute().if_().score(start_battle_type).matches(3).at(monitor_home).run(ground.fill('grass_block')),
        tag(a()).add('arena_safe'),
        function(clean_out),
    )

    room.loop('toggle_peace', home=False).loop(toggle_peace, (True, False)).add(
        function('restworld:arena/start_battle'))
