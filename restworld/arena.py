from __future__ import annotations

import sys
from random import randint
from typing import Tuple

from pynecraft.base import Arg, EAST, EQ, GT, LT, NORTH, Nbt, SOUTH, WEST, r, seconds, to_name
from pynecraft.commands import Block, DIV, INFINITE, INT, MINUS, MOD, RANDOM, REPLACE, RESULT, Score, a, data, e, \
    effect, execute, fill, function, kill, random, return_, s, schedule, scoreboard, setblock, summon, tag
from pynecraft.function import Function, Loop
from pynecraft.info import colors, weathering_id, weatherings
from pynecraft.simpler import Item, Region, Sign, WallSign
from pynecraft.values import DUMMY, REGENERATION
from restworld.rooms import Room, kill_em
from restworld.world import main_clock, marker_tmpl, restworld

COUNT_MIN = 1
COUNT_MAX = 5

NO_VARIANT = 1000

# Lower priority ones can be used as filler
battles = [
    ('axolotl', 'drowned'),
    ('axolotl', 'guardian'),
    # ('axolotl', 'elder_guardian'), # medium priority: attack for elder guardian is same as guardian
    ('blaze', 'snow_golem'),
    ('bogged', 'iron_golem'),
    ('breeze', 'iron_golem'),
    ('cat', 'rabbit'),
    # ('cave_spider', 'snow_golem'),  # medium priority
    ('copper_golem', None),
    ('creaking', 'you'),
    ('ender_dragon', None),
    ('evoker', 'iron_golem'),
    ('fox', 'chicken'),
    # ('frog', 'slime'),  # low priority
    ('goat', 'sheep'),  # medium priority (slow, but charging goat)
    ('hoglin', 'vindicator'),
    ('illusioner', 'snow_golem'),  # medium priority, illusioner isn't used in vanilla, but some folks use it
    ('llama', 'vindicator'),  # Wolves don't work, they just run away, only rarely getting involved
    ('magma_cube', 'iron_golem'),
    # ('ocelot', 'chicken'),  # low priority
    ('panda', 'vindicator'),
    ('phantom', None),
    ('piglin_brute', 'vindicator'),
    ('pillager', 'snow_golem'),
    # ('polar_bear', 'vindicator'), # low priority, polar bears hardly agro, don't to anything special when they are
    ('ravager', 'iron_golem'),
    ('shulker', 'vindicator'),
    ('skeleton', 'iron_golem'),
    ('slime', 'iron_golem'),
    ('sniffer', None),
    ('spider', 'snow_golem'),
    ('stray', 'iron_golem'),
    ('vindicator', 'iron_golem'),
    ('warden', 'iron_golem'),
    ('witch', 'snow_golem'),
    ('wither_skeleton', 'piglin'),
    ('wither', 'pillager'),
    ('wolf', 'sheep'),  # medium priority, the wolf doesn't really do much
    ('zoglin', 'vindicator'),
    ('zombie', 'iron_golem'),
    ('zombified_piglin', 'vindicator'),
]


def is_splitter_mob(mob):
    return mob in ('slime', 'magma_cube')


# Split this out as a separate function because it's pretty complicated and long
def copper_golem_init_cmds(room):
    stride = int(len(colors) / 4)
    block = 'glazed_terracotta'
    for i in range(4):
        chest_items = []
        for n in range(stride):
            chest_items.append(Item.nbt_for(f'{colors[i * stride + n].name}_{block}').merge({'Slot': n}))
        copper_chest_items = []
        for n in range(27):
            copper_chest_items.append(
                Item.nbt_for(f'{colors[randint(0, len(colors) - 1)]}_{block}', count=randint(1, 3)).merge(
                    {'Slot': n}))
        x = i - 2
        if i > 1:
            x += 1
        yield execute().at(e().tag('monitor_home')).run(
            setblock(r(x, 2, 3), Block('chest', {'facing': NORTH}, {'Items': chest_items})),
            setblock(r(x, 2, -3), Block(weathering_id(weatherings[i], 'copper_chest'), {'facing': SOUTH},
                                        {'Items': copper_chest_items}))
        )
    poppy = room.function('copper_golem_poppy', home=False).add(
        data().modify(e().type('copper_golem').sort(RANDOM).limit(1), 'equipment.saddle.id').set().value('poppy'))
    # We have to wait until there are golems to work with
    yield schedule().function(poppy, 8, REPLACE)


def room():
    room = Room('arena', restworld)

    battle_type = Score('battle_type', 'arena')

    def protected(armor):
        return {'id': armor, 'components': {'repair_cost': 1, 'enchantments': {'protection': 5}}}

    skeleton_nbts = {'equipment': {'mainhand': Item.nbt_for('bow'), 'feet': protected('iron_boots'),
                                   'head': protected('iron_helmet')}}
    fighter_nbts = {
        'drowned': {'equipment': {'mainhand': Item.nbt_for('trident')}},
        'goat': {'IsScreamingGoat': True, 'HasLeftHorn': True, 'HasRightHorn': True},
        'hoglin': {'IsImmuneToZombification': True},
        'llama': {'Strength': 1, 'Health': 1000},
        'magma_cube': {'Size': 3},
        'slime': {'Size': 3},
        'phantom': {'AX': 1000, 'AY': 110, 'AZ': -1000},
        'piglin_brute': {'equipment': {'mainhand': Item.nbt_for('golden_axe')}, 'IsImmuneToZombification': 'True'},
        'piglin': {'IsImmuneToZombification': 'True', 'equipment': {'mainhand': Item.nbt_for('golden_sword')}},
        'pillager': {'equipment': {'mainhand': Item.nbt_for('crossbow')}},
        'shulker': {'home_pos': [1026, 101, -1026], 'home_radius': 12},
        'skeleton': skeleton_nbts,
        'stray': skeleton_nbts,
        'bogged': skeleton_nbts,
        'vindicator': {'Johnny': 'True', 'equipment': {'mainhand': Item.nbt_for('iron_axe')}},
        'wither_skeleton': {'equipment': {'mainhand': Item.nbt_for('stone_sword')}},
        'warden': {'Brain': {'memories': {"minecraft:dig_cooldown": {'value': {}, 'ttl': Nbt.MAX_LONG}}}},
        'zombie': {'equipment': {'head': Item.nbt_for('iron_helmet')}},
        'zombified_piglin': {'equipment': {'mainhand': Item.nbt_for('golden_sword')}},
    }

    init_battle = ('copper_golem', None)

    # With Slime and Magma Cube it _mostly_ works, but not perfectly. These are handled by giving a custom name to
    # the summoned mob, which is inherited by its descendants. We then see, if the count is at least 3, whether there
    # is any mob labelled "3" (say). If not a new top-level "3"" is summoned. This way each mob will only be replaced
    # when all its descendants are gone. But... the problem is there is a gap in time between when "3" is killed and
    # its kids are spawned, during which time there is no "3". So a new one is summoned. Thus, the actual count of
    # slimes and magma cubes is off a bit. If I figure out a way to fix this, I'll fix it. For now it seems mildly
    # annoying, but better than the previous alternative where only the smallest slimes and cubes could be summoned,
    # since that could be handled by the general algorithm.

    # 0: water, 1: covered (e.g., undead), 2: ground (sniffer needs this)
    hunter_battle_types = {'axolotl': 1, 'phantom': 2, 'sniffer': 3}

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
            f'Battle count ({len(battles):d}) is not a multiple of stride length ({stride_length:d}))\n')
        sys.exit(1)

    battles.sort(key=lambda v: v[0])

    monitor_home = e().tag('monitor_home')
    peace = room.score('peace', None)

    ids = set()
    for b in battles:
        ids.add(b[0])
        ids.add(b[1])

    cats = ['white', 'black', 'red', 'siamese', 'british_shorthair', 'calico', 'persian', 'ragdoll', 'tabby',
            'all_black', 'jellie']
    wolves = ['pale', 'ashen', 'black', 'chestnut', 'rusty', 'snowy', 'spotted', 'striped', 'woods']
    foxes = ['red', 'snow']
    temps = ['cold', 'temperate', 'warm']
    pandas = ['normal', 'lazy', 'worried', 'playful', 'brown', 'weak', 'aggressive']

    # This is the main part of the system that can randomize values for battlers. This maps entity IDs to a description
    # of what varies and how. For each ID, `values` is the name of the list of possible values (which can be shared,
    # such as with 'nums' for numbers); 'variant' is the name of the property to be set, and 'max' is the maximum index
    # into the named values array (the actual max, not one more than the max as is typical).
    #
    # When a battler is generated, a random value is generated from [0..max], and the value at that index in the named
    # list is the one used for that value.
    #
    # The named lists are stored in this room's storage area by the monitor_init function below.
    #
    # Currently ,this can only handle one varying property for each battler type.
    fighters_specs = {
        'axolotl': {'values': 'nums', 'variant': 'Variant', 'max': 5},
        'sheep': {'values': 'nums', 'variant': 'Color', 'max': 15},
        'cat': {'values': 'cats', 'variant': 'variant', 'max': len(cats) - 1},
        'rabbit': {'values': 'nums', 'variant': 'RabbitType', 'max': 5},
        'wolf': {'values': 'wolves', 'variant': 'variant', 'max': len(wolves) - 1},
        'fox': {'values': 'foxes', 'variant': 'Type', 'max': len(foxes) - 1},
        'chicken': {'values': 'temps', 'variant': 'variant', 'max': len(temps) - 1},
        'cow': {'values': 'temps', 'variant': 'variant', 'max': len(temps) - 1},
        'pig': {'values': 'temps', 'variant': 'variant', 'max': len(temps) - 1},
        'frog': {'values': 'temps', 'variant': 'variant', 'max': len(temps) - 1},
        'llama': {'values': 'nums', 'variant': 'Variant', 'max': 3},
        'panda': {'values': 'pandas', 'variant': 'MainGene', 'max': len(pandas) - 1},
        'parrot': {'values': 'nums', 'variant': 'Variant', 'max': 4},
        'copper_golem': {'values': 'weatherings', 'variant': 'weather_state', 'max': len(weatherings) - 1},
        # 'copper_golem': {'values': 'flowers', 'variant': 'equipment', 'max': len(flowers) - 1},
    }

    for id in ids:
        if id in fighters_specs:
            fighters_specs[id]['id'] = id
        if id not in fighter_nbts:
            fighter_nbts[id] = {}
        merge = Nbt(fighter_nbts[id]).merge({'id': id, 'Tags': ['battler']})
        fighter_nbts[id] = merge

    fighters = [v for v in fighter_nbts.values()]
    specs = [v for v in fighters_specs.values()]
    kills_objective = 'arena_killed'
    hunters_killed = Score('hunters', kills_objective)
    victims_killed = Score('victims', kills_objective)
    ten = Score('ten', 'arena_max')
    prev_hunters_killed = room.score('prev_hunters_killed')
    prev_victims_killed = room.score('prev_victims_killed')
    room.function('monitor_init', home=False).add(
        data().remove(room.store, 'mobs'),
        data().modify(room.store, 'mobs').set().value({
            'nums': list(range(16)),
            'temps': temps,
            'cats': cats,
            'wolves': wolves,
            'foxes': foxes,
            'pandas': pandas,
            'nbts': fighters,
            'specs': specs,
            'splitters': [{'id': 'slime'}, {'id': 'magma_cube'}],
            'hunter_names': [f'hunter_{i}' for i in range(COUNT_MIN, COUNT_MAX + 1)],
            'victim_names': [f'victim_{i}' for i in range(COUNT_MIN, COUNT_MAX + 1)],
            'weatherings': weatherings,
        }),
        ten.set(10),
        scoreboard().objectives().add(kills_objective, DUMMY, "Killed"),
    )

    actor_is_splitter = room.score('$(actor)_is_splitter')
    is_empty = room.score('is_empty')
    # Function invoked to configure one of the participants
    configure_actor = room.function('configure_actor', home=False).add(
        data().modify(room.store, '$(actor)_prev').set().from_(room.store, '$(actor)'),
        data().remove(room.store, '$(actor)'),
        is_empty.set('$(is_empty)'),
        execute().unless().score(is_empty).matches(0).run(return_()),
        data().merge(room.store, {
            '$(actor)': {'id': '$(id)', 'actor': '$(actor)', 'i': 0, 'y': 2, 'z': '$(z)', 'max': NO_VARIANT,
                         'variant': '', 'values': ''}}),
        data().modify(room.store, '$(actor).nbt').set().from_(room.store, 'mobs.nbts[{id:$(id)}]'),
        data().modify(room.store, '$(actor).nbt.Tags').append().value('$(actor)'),
        data().modify(room.store, '$(actor).nbt.Rotation').set().value('$(rot)'),
        execute().if_().data(room.store, 'mobs.specs[{id:$(id)}]').run(
            data().modify(room.store, '$(actor)').merge().from_(room.store, 'mobs.specs[{id:$(id)}]')),
        actor_is_splitter.set(0),
    )

    # Commands invoked by the sign to configure the battle
    is_alone = room.score('is_alone')
    configure = room.function('configure', home=False).add(
        function(configure_actor,
                 {'actor': 'hunter', 'id': '$(hunter_id)', 'rot': [180.0, 0.0], 'is_empty': False, 'z': '$(z)'}),
        function(configure_actor,
                 {'actor': 'victim', 'id': '$(victim_id)', 'rot': [0.0, 0.0], 'is_empty': False, 'z': 0}),
        battle_type.set(Arg('battle_type')),
        is_alone.set(Arg('is_alone')),
    )

    # Create any per-hunter setup functions
    room.function('copper_golem_init', home=False).add(copper_golem_init_cmds(room))

    # function summon with restworld.arena actor
    max_variant = room.score('max_variant')
    actors_kills = Score('$(actor)s', kills_objective)
    actual_summon = room.function('actual_summon', home=False).add(
        execute().at(e().tag(f'$(actor)_home').sort('random').limit(1)).run(
            summon('$(id)', r(0, '$(y)', '$(z)'), '$(nbt)')),
        scoreboard().players().add(actors_kills, 1),
    )
    do_summon = room.function('summon', home=False).add(
        max_variant.set('$(max)'),
        execute().unless().score(max_variant).matches(NO_VARIANT).run(
            execute().store(RESULT).storage(room.store, '$(actor).i', INT).run(random().value((0, '$(max)'))),
            data().modify(room.store, '$(actor).nbt.$(variant)').set().from_(room.store, 'mobs.$(values)[$(i)]'),
            # This is required for pandas, a no-op for everything else
            data().modify(room.store, '$(actor).nbt.HiddenGene').set().from_(room.store, '$(actor).nbt.MainGene')),
        execute().if_().score(actor_is_splitter).matches(1).run(
            data().modify(room.store, '$(actor).nbt.CustomName').set().from_(room.store, '$(actor).avail[0]'),
        ),
        function(actual_summon).with_().storage(room.store, '$(actor)')
    )

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
                alone = victim is None or victim == 'You'
                sign_commands = (
                    function(configure, {'hunter_id': hunter, 'victim_id': victim, 'is_alone': int(alone),
                                         'battle_type': hunter_battle_types.get(hunter, 0), 'z': -4 if alone else 0}),
                    function('restworld:arena/start_battle', {'hunter_is_splitter': is_splitter_mob(hunter),
                                                              'victim_is_splitter': is_splitter_mob(victim)})
                )
                if (hunter, victim) == init_battle:
                    room.function('monitor_init', exists_ok=True).add(sign_commands)
                sign = WallSign().messages((None, to_name(hunter), 'vs.', to_name(victim) if victim else 'Nobody'),
                                           sign_commands)
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
        center = stand.clone()
        center.nbt['Tags'].append(f'{var}_center')
        for x in range(-1, 2):
            for z in range(-1, 2):
                yield (center if x == 0 and z == 0 else stand).summon(r(x, 0.5, z))

    def toggle_peace(step):
        block = 'air' if step.elem else 'redstone_torch'
        yield execute().at(e().tag('monitor_home')).run(setblock(r(1, -1, 1), block))
        yield peace.set(int(step.elem))
        if step.elem:
            yield function(clean_out),
        yield execute().at(e().tag('controls_home')).run(
            setblock(r(-1, 2, 0), f'{"lime" if step.elem else "red"}_concrete'))

    arena_count = room.score('arena_count', 5)

    arena_count_finish = room.function('arena_count_finish', home=False).add(
        execute().if_().score(arena_count).matches((None, COUNT_MIN)).run(arena_count.set(COUNT_MIN)),
        execute().if_().score(arena_count).matches((COUNT_MAX, None)).run(arena_count.set(COUNT_MAX)),
        function('restworld:arena/arena_count_cur'),
    )
    arena_count_cur = function(arena_count_finish.full_name)
    room.function('arena_count_decr', home=False).add(arena_count.remove(1), arena_count_cur)
    room.function('arena_count_incr', home=False).add(
        arena_count.add(1), arena_count_cur,
        # These counteract the "add" that happens when a mob is summoned because that won't be in response to a kill
        scoreboard().players().remove(hunters_killed, 1),
        scoreboard().players().remove(victims_killed, 1),
    )
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
        room.label(r(1, 3, 0), 'Go Home', WEST),
        tag(e().tag('controls_home')).add('controls_action_home'),
        # These init funcs won't get run otherwise because there is no home
        function('restworld:arena/arena_count_init'),
    )

    room.function('hunter_home').add(random_stand('hunter'))
    room.function('victim_home').add(random_stand('victim'))

    def count_func(actor: str, splitter: Score) -> Tuple[Function, Score]:
        count = room.score(f'{actor}_count')
        func = room.function(f'count_{actor}', home=False).add(
            count.set(0),
            execute().if_().score(splitter).matches(0).as_(e().tag(actor)).run(count.add(1)),
            data().remove(room.store, f'{actor}.avail'),
        )
        for i in range(COUNT_MIN, COUNT_MAX + 1):
            func.add(
                execute().unless().score(splitter).matches(0).if_().entity(
                    e().nbt({'CustomName': f'{actor}_{i}'}).limit(1)).run(count.add(1)),
                execute().unless().score(splitter).matches(0).unless().entity(
                    e().nbt({'CustomName': f'{actor}_{i}'}).limit(1)).run(
                    data().modify(room.store, f'{actor}.avail').append().from_(room.store,
                                                                               f'mobs.{actor}_names[{i - 1}]'),
                ),
            )
        return func, count

    h_is_splitter = room.score('hunter_is_splitter')
    v_is_splitter = room.score('victim_is_splitter')
    h_counter, hunter_count = count_func('hunter', h_is_splitter)
    v_counter, victim_count = count_func('victim', v_is_splitter)

    ones = room.score('$(actor)s_1')
    tens = room.score('$(actor)s_10')
    cents = room.score('$(actor)s_100')
    room.function('hunter_show_score')
    room.function('victim_show_score')
    show_digits = room.function('show_digits', home=False).add(
        data().modify(r(0, 10, 0), 'name').set().value('restworld:num_$(ones)'),
        setblock(r(-1, 10, 0), 'redstone_block'),
        setblock(r(-1, 10, 0), 'air'),
        data().modify(r(0, 10, 4), 'name').set().value('restworld:num_$(tens)'),
        setblock(r(-1, 10, 4), 'redstone_block'),
        setblock(r(-1, 10, 4), 'air'),
        data().modify(r(0, 10, 8), 'name').set().value('restworld:num_$(cents)'),
        setblock(r(-1, 10, 8), 'redstone_block'),
        setblock(r(-1, 10, 8), 'air'),
    )
    prev_actors_kills = room.score('prev_$(actor)s_kills')
    kills = room.score('kills')
    show_score = room.function('show_score').add(
        kills.set(actors_kills),
        execute().if_().score(actors_kills).matches((1000, None)).run(kills.set(999)),
        execute().if_().score(actors_kills).is_(EQ, prev_actors_kills).run(return_()),  # can happen for 999
        ones.set(kills),
        ones.operation(MOD, ten),
        tens.set(kills),
        tens.operation(DIV, ten),
        cents.set(tens),  # to avoid recalculating this value for cents separately
        tens.operation(MOD, ten),
        cents.operation(DIV, ten),
        execute().store(RESULT).storage(room.store, 'digits.ones', INT).run(ones.get()),
        execute().store(RESULT).storage(room.store, 'digits.tens', INT).run(tens.get()),
        execute().store(RESULT).storage(room.store, 'digits.cents', INT).run(cents.get()),
        execute().at(e().tag('$(actor)_show_score_home')).run(
            function(show_digits).with_().storage(room.store, 'digits'),
        ),
        prev_actors_kills.set(actors_kills)
    )

    room.function('monitor').add(
        execute().unless().score(peace).matches(0).run(return_()),
        execute().unless().score(arena_count).matches((COUNT_MIN, COUNT_MAX)).run(arena_count.set(1)),
        function(h_counter),
        function(v_counter),
        kill(e().type('experience_orb').distance((None, 50))),
        execute().if_().score(hunter_count).is_(LT, arena_count).run(
            function(do_summon).with_().storage(room.store, 'hunter')),
        execute().if_().score(victim_count).is_(LT, arena_count).run(
            function(do_summon).with_().storage(room.store, 'victim')),
        ((
            execute().if_().score(room.score(f'{actor}_count')).is_(GT, arena_count).run(
                kill_em(
                    e().tag(actor).sort(RANDOM).limit(1).distance((None, 100)))),
            execute().if_().score(room.score(f'{actor}_count')).is_(LT, arena_count).run(
                execute().at(e().tag(f'{actor}_home')).run(
                    setblock(r(-3, -1, 0), 'redstone_block'),
                    setblock(r(-3, -1, 0), 'air'))))
            for actor in ('hunter', 'victim')),
        execute().unless().score(hunters_killed).is_(EQ, prev_hunters_killed).run(
            function(show_score, {'actor': 'hunter'})),
        execute().unless().score(victims_killed).is_(EQ, prev_victims_killed).run(
            function(show_score, {'actor': 'victim'})),
        execute().as_(e().type('item').tag('!limited')).run(
            data().modify(s(), 'Age').set().value(6000 - 150),
            tag(s()).add('limited')
        ),
        effect().give(e().type('llama').tag('battler'), REGENERATION, INFINITE, 100, True)
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
        execute().at(monitor_home).run(tag(e().type('armor_stand').distance((None, 100))).add('immortal')),
        execute().at(monitor_home).run(tag(e().type('text_display').distance((None, 100))).add('immortal')),
        kill_em(e().not_tag('immortal').distance((None, 100))))
    init_wrapper = room.function('init_wrapper', home=False).add(function('restworld:arena/$(id)_init'))
    start_battle = room.function('start_battle', home=False).add(
        kill(e().type('item').distance((None, 50))),
        was_splitters.set(is_splitters),
        h_is_splitter.set(Arg('hunter_is_splitter')),
        v_is_splitter.set(Arg('victim_is_splitter')),
        is_splitters.set(h_is_splitter + v_is_splitter),
        execute().unless().score(was_splitters).matches(0).if_().score(is_splitters).matches(0).run(kill_splitters),
        execute().unless().score(battle_type).matches((0, None)).run(battle_type.set(0)),
        execute().unless().score(battle_type).matches(1).at(monitor_home).run(arena.fill('air')),
        execute().if_().score(battle_type).matches(1).at(monitor_home).run(arena.fill('water')),
        execute().unless().score(battle_type).matches(2).at(monitor_home).run(sky.fill('air')),
        execute().if_().score(battle_type).matches(2).at(monitor_home).run(sky.fill('glowstone')),
        execute().if_().score(battle_type).matches(3).at(monitor_home).run(ground.fill('grass_block')),
        tag(a()).add('arena_safe'),
        # These counteract the "add" that happens when a mob is summoned because that won't be in response to a kill
        hunters_killed.set(0),
        prev_hunters_killed.set(-1000),
        hunters_killed.operation(MINUS, arena_count),
        victims_killed.set(0),
        prev_victims_killed.set(-1000),
        execute().if_().score(is_alone).matches(0).run(victims_killed.operation(MINUS, arena_count)),
        function(clean_out),
        function(init_wrapper).with_().storage(room.store, 'hunter'),
    )

    room.loop('toggle_peace', home=False).loop(toggle_peace, (True, False)).add(
        execute().if_().score(peace).matches(0).run(function(start_battle)))
