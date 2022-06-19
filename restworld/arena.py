from __future__ import annotations

import sys

from pyker.commands import Score, entity, mc, r, WEST, all_
from pyker.function import Loop
from pyker.simpler import WallSign
from restworld.rooms import Thing, Room, label
from restworld.world import marker_tmpl, restworld, main_clock


def room():
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
        def arena_run_loop(step):
            for which_dir in (-1, 1):
                to = (i + which_dir + num_pages) % num_pages
                text, z = ('<--', max_z + 1) if which_dir == -1 else ('-->', min_z - 1)
                yield WallSign((None, text), (
                    step.loop.score.set(to),
                    mc.execute().at(entity().tag('controls_home')).run().function(
                        'restworld:arena/%s_cur' % step.loop.score.target)
                )).glowing(True).place(r(x, 2, z), WEST)
            for s in range(0, stride_length):
                args = step.item[s] + (None,) * (4 - len(step.item[s]))
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

    def toggle_peace(step):
        return (
            mc.execute().at(entity().tag('monitor_home')).run().fill(
                r(2, -1, 0), r(3, -1, 0), 'redstone_torch' if step.item else 'air'),
            mc.setblock(r(0, 1, 0), '%s_concrete' % ('red' if step.item else 'lime')),
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
        lambda step: mc.execute().at(entity().tag('controls_home')).run(
        ).data().merge(r(2, 4, 0), {'Text2': '%d vs. %d' % (step.item, step.item)}), range(0, 6))

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
