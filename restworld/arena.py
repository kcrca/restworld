from __future__ import annotations

import sys

from pynecraft.base import EAST, GT, LT, Nbt, r
from pynecraft.commands import Entity, RANDOM, Score, a, data, e, execute, fill, function, kill, s, setblock, summon, \
    tag
from pynecraft.function import Loop
from pynecraft.simpler import Item, Region, WallSign, Sign
from restworld.rooms import Room, label
from restworld.world import kill_em, main_clock, marker_tmpl, restworld

COUNT_MIN = 1
COUNT_MAX = 5

battle_types = {'w': 1, 'c': 2, 'g': 3}


def room():
    def protected(armor):
        return {'id': armor, 'Count': 1,
                'tag': {'RepairCost': 1, 'Enchantments': [{'lvl': 9, 'id': 'protection'}]}}

    start_battle_type = Score('battle_type', 'arena')
    fighter_nbts = {
        'Drowned': {'HandItems': [Item.nbt_for('trident')], 'ArmorItems': [{}, {}, {}, Item.nbt_for('iron_helmet')]},
        'Goat': {'IsScreamingGoat': True, 'HasLeftHorn': True, 'HasRightHorn': True},
        'Hoglin': {'IsImmuneToZombification': True},
        'Llama': {'Strength': 5},
        'Magma Cube': {'Size': 0},
        'Panda': {'MainGene': 'aggressive'},
        'Phantom': {'AX': 1000, 'AY': 110, 'AZ': -1000},
        'Piglin Brute': {'HandItems': [Item.nbt_for('golden_axe')], 'IsImmuneToZombification': 'True'},
        'Piglin': {'IsImmuneToZombification': 'True', 'HandItems': [Item.nbt_for('golden_sword'), {}]},
        'Pillager': {'HandItems': [Item.nbt_for('crossbow'), {}]},
        'Skeleton': {'HandItems': [Item.nbt_for('bow')],
                     'ArmorItems': [protected('iron_boots'), {}, {}, protected('iron_helmet')]},
        'Slime': {'Size': 0},
        'Stray': {'HandItems': [Item.nbt_for('bow')],
                  'ArmorItems': [protected('iron_boots'), {}, {}, protected('iron_helmet')]},
        'Vindicator': {'Johnny': 'True', 'HandItems': [Item.nbt_for('iron_axe'), {}]},
        'Wither Skeleton': {'HandItems': [Item.nbt_for('stone_sword'), {}]},
        'Zombie': {'ArmorItems': [{}, {}, {}, Item.nbt_for('iron_helmet')]},
        'Zombified Piglin': {'HandItems': [Item.nbt_for('golden_sword'), {}]},
    }

    battles = [
        ('Axolotl:w', 'Drowned'),  # low priority
        ('Axolotl:w', 'Elder Guardian'),
        ('Skeleton', 'Iron Golem'),
        ('Blaze', 'Snow Golem'),
        ('Cat', 'Rabbit'),
        ('Warden', 'Iron Golem'),
        ('Axolotl:w', 'Guardian'),
        ('Evoker', 'Iron Golem'),
        ('Fox', 'Chicken'),
        ('Frog', 'Slime'),
        ('Goat', 'Sheep'),  # medium priority (slow, but charging goat)
        ('Hoglin', 'Vindicator'),
        ('Ender Dragon', None),
        # ('Illusioner', 'Snow Golem'), # low priority, Illusioner isn't used
        ('Llama', 'Vindicator'),
        ('Magma Cube', 'Iron Golem'),
        ('Ocelot', 'Chicken'),
        ('Panda', 'Vindicator'),
        ('Parrot', 'Vindicator'),
        ('Phantom:c', 'Rabbit'),
        ('Piglin Brute', 'Vindicator'),
        ('Pillager', 'Snow Golem'),
        ('Polar Bear', 'Vindicator'),
        ('Ravager', 'Iron Golem'),
        ('Shulker', 'Vindicator'),
        ('Slime', 'Iron Golem'),  # Low priority, slime vs. frog
        ('Spider', 'Snow Golem'),
        ('Stray', 'Iron Golem'),
        ('Sniffer:g', None),
        ('Vindicator', 'Iron Golem'),
        ('Witch', 'Snow Golem'),
        ('Wither Skeleton', 'Piglin'),
        ('Wither', 'Pillager'),
        ('Wolf', 'Sheep'),
        ('Zoglin', 'Vindicator'),
        ('Zombie', 'Iron Golem'),
        ('Zombified Piglin', 'Vindicator'),
    ]
    # Lower priority ones that can be used as filler
    #    ('Axolotl:w', 'Elder Guardian'),
    #    ('Axolotl:w', 'Guardian'),
    #    ('Ocelot', 'Chicken'),
    #    ('Slime', 'Iron Golem'),
    #    ('Magma Cube', 'Iron Golem'),
    #    ('Goat', 'Sheep'),
    #    ('Cave Spider', 'Snow Golem'),
    #    ('Drowned', 'Snow Golem'),
    #
    # These don't work unless we figure out how to kill the ones that spawn when a larger is killed. For
    # now, we just make sure they are the smallest size.
    #  ('Slime', 'Iron Golem'),
    #  ('Magma Cube', 'Iron Golem'),

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

    def arena_run_main(loop: Loop):
        def arena_run_loop(step):
            i = step.i
            for which_dir in (-1, 1):
                to = (i + which_dir + num_pages) % num_pages
                text, z = ('<--', max_z + 1) if which_dir == -1 else ('-->', min_z - 1)
                yield WallSign().messages((None, text), (
                    step.loop.score.set(to),
                    execute().at(e().tag('controls_home')).run(
                        function(f'restworld:arena/{step.loop.score.target}_cur'))
                )).glowing(True).place(r(x, 2, z), EAST)
            for s in range(0, stride_length):
                y = 3 - int(s / row_length)
                z = max_z - (s % row_length)
                hunter, victim = step.elem[s]
                alone = victim is None

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
                        if hunter == 'Warden':
                            # Summoning warden with NBT means that it immediately burrows away, so must special case it
                            # https://bugs.mojang.com/browse/MC-249393 (also see below)
                            my_nbts = None
                    y_off = 3 if battle_type == 3 else 2
                    z_off = -4 if center else 0
                    incr = summon(Entity(mob, my_nbts), r(0, y_off, z_off))
                    incr_cmd = execute().if_().score((f'{which}_count', 'arena')).is_(LT, ('arena_count', 'arena')).at(
                        e().tag(f'{which}_home').sort('random').limit(1)).run(incr)
                    return incr_cmd

                data_change = execute().at(monitor_home)
                sign_commands = (
                    start_battle_type.set(battle_type),
                    data_change.run(data().merge(r(3, 0, 0), {'Command': incr_cmd('hunter', hunter, alone)})),
                    data_change.run(
                        data().merge(r(2, 0, 0), {'Command': incr_cmd('victim', 'marker' if alone else victim)})),
                    function('restworld:arena/start_battle')
                )
                sign = WallSign().messages((None, hunter, 'vs.', 'Nobody' if alone else victim), sign_commands)
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
                yield stand.summon(r(x, -0.5, z))

    place_battlers = Score('place_batters', 'arena')

    def monitor(actor: str):
        other = 'hunter' if actor == 'victim' else 'victim'
        count = Score(actor + '_count', 'arena')
        close = Score(actor + '_close', 'arena')
        athome = Score(actor + '_athome', 'arena')
        return (
            execute().unless().entity(e().tag(actor)).run(place_battlers.set(1)),
            count.set(0),
            execute().as_(e().tag(actor)).run(count.add(1)),
            close.set(0),
            execute().at(
                e().tag(other + '_home')).positioned(r(-2, 0, -2)).as_(
                e().tag(actor).volume((4, 5, 4))).run(close.add(1)),
            athome.set(0),
            execute().at(
                e().tag(actor + '_home')).positioned(r(-2, 0, -2)).as_(
                e().tag(actor).volume((4, 5, 4))).run(athome.add(1)),
        )

    def toggle_peace(step):
        return (
            execute().at(e().tag('monitor_home')).run(fill(
                r(2, -1, 0), r(3, -1, 0), 'redstone_torch' if step.elem else 'air')),
            setblock(r(0, 1, 0), f'{"red" if step.elem else "lime"}_concrete'),
        )

    room = Room('arena', restworld)

    arena_count = Score('arena_count', 'arena')

    arena_count_finish = room.function('arena_count_finish').add(
        execute().if_().score(arena_count).matches((None, COUNT_MIN)).run(arena_count.set(COUNT_MIN)),
        execute().if_().score(arena_count).matches((COUNT_MAX, None)).run(arena_count.set(COUNT_MAX)),
        function('restworld:arena/arena_count_cur'),
    )
    arena_count_cur = function(arena_count_finish.full_name)
    room.function('arena_count_decr', home=False).add(arena_count.remove(1), arena_count_cur)
    room.function('arena_count_incr', home=False).add(arena_count.add(1), arena_count_cur)
    room.function('arena_count_init').add(arena_count.set(1), arena_count_cur)
    room.loop('arena_count', main_clock).loop(
        lambda step: execute().at(e().tag('controls_home')).run(
            Sign.change(r(2, 4, 0), (None, f'{step.elem:d} vs. {step.elem:d}'))), range(0, COUNT_MAX + 1))

    room.function('arena_run_init').add(
        function('restworld:arena/arena_run_cur')
    )
    # This is NOT intended to be run on the clock. It is only called '_main' because that gives us a
    # '_cur' function, which is useful when paging through the signs. Do not create the _home armor stand.
    arena_run_loop = arena_run_main(room.loop('arena_run', main_clock, home=False))

    room.function('controls_init').add(
        arena_run_loop.score.set(0),
        function('restworld:arena/arena_run_cur'),
        label(r(1, 3, 0), 'Go Home'),
        tag(e().tag('controls_home')).add('controls_action_home')
    )

    room.function('hunter_home').add(random_stand('hunter'))
    room.function('victim_home').add(random_stand('victim'))

    # monitor_init function looks out-of-date and unused
    room.function('monitor').add(monitor('hunter'), monitor('victim'),
                                 kill(e().type('item').distance((None, 50))),
                                 kill(e().type('experience_orb').distance((None, 50)))),
    # For some reason, arena_count_init doesn't always get run on _init, so we make sure that value is always in range.
    cleanup = room.function('monitor_cleanup', home=False).add(
        execute().unless().score(arena_count).matches((COUNT_MIN, COUNT_MAX)).run(arena_count.set(1)),
        (execute().if_().score(room.score(f'{who}_count')).is_(GT, arena_count).run(kill(
            e().tag(who).sort(RANDOM).limit(1).distance((None, 100))))
            for who in ('hunter', 'victim')))
    # Summoning warden with NBT means that it immediately burrows away, so must special case it
    # https://bugs.mojang.com/browse/MC-249393 (also see above)
    cleanup.add(
        execute().as_(e().type('warden').distance((None, 100)).not_tag('hunter')).run(tag(s()).add('hunter')),
        execute().as_(e().type('warden').distance((None, 100)).not_tag('battler')).run(tag(s()).add('battler'))),

    # Types: 0-normal, 1-water, 2-undead
    arena = Region(r(-12, 2, -12), r(12, 4, 12))
    ground = Region(r(-12, 2, -12), r(12, 2, 12))
    sky = Region((r(-20), 250, r(-20)), (r(20), 250, r(20)))
    # See 'battle_types' map above for meanings
    room.function('start_battle').add(
        execute().unless().score(start_battle_type).matches((0, None)).run(start_battle_type.set(0)),
        execute().unless().score(start_battle_type).matches(1).at(monitor_home).run(arena.fill('air')),
        execute().if_().score(start_battle_type).matches(1).at(monitor_home).run(arena.fill('water')),
        execute().unless().score(start_battle_type).matches(2).at(monitor_home).run(sky.fill('air')),
        execute().if_().score(start_battle_type).matches(2).at(monitor_home).run(sky.fill('glowstone')),
        execute().if_().score(start_battle_type).matches(3).at(monitor_home).run(ground.fill('grass_block')),
        tag(a()).add('arena_safe'),
        tag(e().type('armor_stand')).add('arena_safe'),
        kill_em(e().not_tag('arena_safe').distance((None, 100))),
    )

    room.loop('toggle_peace').loop(toggle_peace, (True, False)).add(function('restworld:arena/start_battle'))
