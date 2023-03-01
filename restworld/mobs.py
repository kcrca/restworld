from __future__ import annotations

import copy

from pynecraft.base import EAST, EQ, NORTH, SOUTH, WEST, r, to_id
from pynecraft.commands import Block, COLORS, Entity, LONG, MOD, RESULT, Score, data, e, execute, function, good_facing, \
    item, kill, s, scoreboard, setblock, summon, tag, tp
from pynecraft.enums import ScoreCriteria
from pynecraft.info import axolotls, colors, horses, music_discs, tropical_fish
from pynecraft.simpler import Item, PLAINS, VILLAGER_BIOMES, VILLAGER_PROFESSIONS, Villager, WallSign
from restworld.rooms import MobPlacer, Room, label
from restworld.world import fast_clock, kill_em, main_clock, restworld


def room():
    room = Room('mobs', restworld, NORTH, ('Villagers,', 'Animals,', 'Mobs,', 'Bosses'), 'Mobs')
    room.resetAt((0, 15))
    friendlies(room)
    monsters(room)
    aquatic(room)


def friendlies(room):
    south_placer = r(0, 2, -0.2), SOUTH, -2, 2.2
    mid_east_placer = r(-1.2, 2, 0), EAST, 2, 2.2
    mid_west_placer = r(0.2, 2, 0), WEST, -2, 2.2

    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    allay_dir = WEST
    allay_pos = r(0, 3, 0)
    room.function('allay_init').add(placer(allay_pos, allay_dir, adults=True).summon('Allay'))
    bat_dir, bat_pos, hang_bat_pos = WEST, r(-2, 3, 0), r(0, 3.5, 0)
    room.function('bat_init').add(
        placer(bat_pos, bat_dir, 2, adults=True).summon('bat'),
        placer(hang_bat_pos, bat_dir, 2, adults=True).summon('bat', nbt={'BatFlags': 1}, tags=('sleeping_bat',)))

    stinger_label_pos = r(-2, 2, 1)
    pollen_label_pos = r(-2, 2, -1)
    room.function('bee_init').add(
        placer(r(0, 3, 0), WEST, 0, 2).summon('bee'),
        label(stinger_label_pos, 'Stinger'),
        label(pollen_label_pos, 'Pollen'))

    def bee_loop(step):
        bee_house = 'beehive' if step.i == 0 else 'bee_nest'
        # The 'air' check is for if we're levitated
        yield execute().unless().block(r(0, 1, 0), 'air').at(
            e().tag('bee_home')).run(setblock(r(2, 2, 0), (bee_house, {'facing': WEST})))
        on_ground = step.i < 2
        base = 'iron_bars' if on_ground else 'air'
        yield execute().as_(e().tag('bee')).run(data().merge(
            s(), {'OnGround': on_ground, 'AngerTime': (step.i % 2) * 100000,
                  'CustomName': 'Bee' if step.i % 2 == 0 else 'Angry Bee'}))
        yield execute().unless().block(r(0, 1, 0), 'air').run(setblock(r(0, 2, 0), base))
        yield execute().unless().block(r(0, 1, 0), 'air').run(setblock(r(-2, 2, 0), base))

    room.loop('bee', main_clock).loop(bee_loop, range(0, 4))

    room.function('camel_init').add(placer(*mid_east_placer, tags=('saddle',)).summon('camel'))

    p = placer(*south_placer)
    room.function('canine_init').add(
        p.summon('wolf'),
        p.summon(Entity('wolf', nbt={'Owner': 'dummy'}, name='Dog'), tags=('collared',)),
        label(r(1, 2, 2), 'Sit'))

    room.loop('canine', main_clock).loop(
        lambda step: execute().as_(e().tag('wolf')).run(data().merge(s(), {'Angry': step.elem})), (True, False))
    room.function('cat_init').add(
        placer(*south_placer, tags=('collared',)).summon('cat'),
        label(r(1, 2, 2), 'Cat Collar'))
    room.loop('cat', main_clock).loop(
        lambda step: execute().as_(e().tag('cat')).run(
            data().merge(s(), {'variant': step.elem.id, 'CustomName': step.elem.name})),
        (
            Entity('tabby', name='Tabby'),
            Entity('black', name='Tuxedo'),
            Entity('red', name='Red'),
            Entity('siamese', name='Siamese'),
            Entity('british_shorthair', name='British Shorthair'),
            Entity('calico', name='Calico'),
            Entity('persian', name='Persian'),
            Entity('ragdoll', name='Ragdoll'),
            Entity('white', name='White'),
            Entity('jellie', name='Jellie'),
            Entity('all_black', name='Black'),
        ))
    room.function('chicken_exit').add(
        execute().as_(e().type('chicken')).run(data().merge(s(), {'EggLayTime': 1000000000})))
    room.function('chicken_init').add(
        placer(*mid_east_placer).summon('chicken'),
        execute().as_(e().tag('chicken')).run(data().merge(s(), {'EggLayTime': 1000000000}))
    )
    room.loop('chicken', main_clock).loop(
        lambda step: execute().as_(e().tag('chicken')).run(
            data().merge(s(), {'OnGround': step.elem, 'EggLayTime': 1000000000})), (True, False))
    room.function('colored_mobs_init').add(
        label(r(0, 2, -1), 'Glow'),
        label(r(0, 2, 7), 'Change Height'))

    def colored_mobs_loop(step):
        yield execute().as_(e().tag('colorable')).run(
            data().merge(s(), {'Color': step.i, 'CustomName': step.elem.name}))
        yield execute().as_(e().tag('collared')).run(data().merge(s(), {'CollarColor': step.i}))

    room.loop('colored_mobs', main_clock).loop(colored_mobs_loop, colors)
    room.loop('cow', main_clock).add(kill_em(e().tag('cowish'))).loop(
        lambda step: placer(*mid_east_placer, tags=('cowish',)).summon(step.elem),
        ('cow', 'mooshroom', Entity('mooshroom', {'Type': 'brown'})))
    room.function('fox_init').add(placer(*mid_east_placer).summon('fox'))

    fox_postures = ('Crouching', 'Sitting', 'Sleeping')

    def fox_loop(step):
        which = 'red' if step.i < len(fox_postures) + 1 else 'snow'
        nbt = {'Type': which, 'CustomName': f'{which.title()} Fox'}
        for p in fox_postures:
            nbt[p] = step.elem == p
        yield execute().as_(e().tag('fox')).run(data().merge(s(), nbt))

    room.loop('fox', main_clock).loop(fox_loop, (('',) + fox_postures) * 2)
    frog_pos, spawn_pos, sign_pos, frog_dir = r(0, 2, 0), r(1, 2, 0), r(1, 2, 1), EAST
    room.function('frog_init').add(placer(
        frog_pos, frog_dir, adults=True).summon('frog'))

    room.loop('frog', main_clock).loop(
        lambda step: execute().as_(e().tag('frog')).run(
            data().merge(s(), {'variant': step.elem.lower(), 'CustomName': f'{step.elem} Frog'})),
        ('Temperate', 'Warm', 'Cold'))

    def frogspawn_loop(step):
        if step.i == 0:
            yield kill_em(e().tag('tadpole', room.name))
            # The 'air' check is for if we're levitated
            yield execute().unless().block(r(0, 1, 0), 'air').at(e().tag('frogspawn_home')).run(
                setblock(spawn_pos, 'frogspawn'),
                WallSign((None, 'Frogspawn')).place(sign_pos, frog_dir))
        else:
            yield placer(spawn_pos, frog_dir, kids=True).summon(Entity('tadpole', {'Invulnerable': True}),
                                                                tags=('keeper',))
            yield setblock(spawn_pos, 'air')
            yield setblock(sign_pos, 'air')
        yield kill_em(e().type('tadpole').not_tag('keeper'))

    room.loop('frogspawn', main_clock).loop(frogspawn_loop, range(0, 2))
    room.function('goat_init').add(placer(*south_placer).summon('goat'))
    room.loop('goat', main_clock).loop(
        lambda step: execute().as_(e().tag('goat').tag('adult')).run(
            data().merge(s(), {'HasLeftHorn': step.i & 1, 'HasRightHorn': step.i & 2})), range(0, 4))

    p = placer(r(-1.2, 2, 0), EAST, -2, kid_delta=2.2, tags=('saddle',), nbt={'Tame': True})
    room.function('horse_init').add(
        (p.summon(Entity('horse', name=horse.name, nbt={'Variant': h}), tags=(horse.tag,)) for h, horse in
         enumerate(horses)),
        execute().at(e().tag(to_id(horses[3].tag), 'kid')).run(
            WallSign((None, 'Variant:')).place(r(2, 0, 0), EAST)),
        label(r(1, 2, 1), 'Lead'),
        label(r(1, 2, -7), 'Saddles'),
    )
    horse_variants = ('None', 'White', 'White Field', 'White Dots', 'Black Dots')

    def horse_loop(step):
        for h, horse in enumerate(horses):
            yield execute().as_(e().tag(horse.tag)).run(data().merge(s(), {'Variant': step.i * 256 + h}))
        yield execute().at(e().tag(horses[3].tag).tag('kid')).run(
            data().merge(r(2, 0, 0), {'Text3': horse_variants[step.i]}))

    room.loop('horse', main_clock).loop(horse_loop, horse_variants)

    p = placer(r(-1.2, 2, 0), EAST, -2, kid_delta=2.2, tags=('saddle', 'chests'))
    room.function('horselike_init').add(
        p.summon('mule'),
        p.summon('donkey'),
        label(r(2, 2, -1), 'Chests'))
    room.function('iron_golem_init').add(
        placer(r(-1.2, 2, 0), EAST, adults=True).summon('iron_golem'),
        WallSign((None, 'Iron Golem')).place(r(2, 2, 0), EAST))

    def iron_golem_loop(step):
        i = step.i
        yield execute().as_(e().tag('iron_golem')).run(data().merge(s(), {'Health': step.elem * 25 - 5}))
        yield data().merge(r(2, 2, 0), {'Text3': f'Damage: {i if i < 4 else 3 - (i - 3):d}'})

    room.loop('iron_golem', main_clock).loop(iron_golem_loop, range(4, 0, -1), bounce=True)
    room.function('lead_off', home=False).add(kill(e().type('leash_knot')))
    room.function('lead_on', home=False).add(
        execute().as_(e().tag('white_horses').tag('!kid')).run(
            data().merge(s(), {'Leash': {'X': -12, 'Y': 101, 'Z': 35}})))
    room.loop('llamas_carpets', main_clock).loop(
        lambda step: execute().as_(e().tag('llama').tag('!kid')).run(
            data().merge(s(), {'DecorItem': {'id': step.elem.id + '_carpet', 'Count': 1}})), colors)

    room.function('llamas_init').add(
        placer(r(0, 2, 0), WEST, 0, 2).summon('llama'),
        placer(r(1, 3.5, -1), WEST, adults=True,
               nbt={'Tags': ['mobs', 'llama', 'llama_spit'], 'TXD': 0, 'TYD': 0, 'TZD': 0, 'Steps': 0,
                    'Motion': [0, 0, 0], 'NoGravity': True}).summon('llama_spit'),
        WallSign((None, 'Llama Spit')).place(r(1, 2, -1), WEST),
        label(r(-2, 2, 1), 'Carpet'),
        label(r(-2, 2, -1), 'Chest'),
    )

    room.loop('llamas', main_clock).loop(
        lambda step: execute().as_(e().tag('llama')).run(
            data().merge(s(), {'Variant': step.i, 'CustomName': step.elem})), ('Creamy', 'White', 'Brown', 'Gray'))
    room.function('ocelot_init').add(placer(*south_placer).summon('ocelot'))
    room.function('outlines_on').add((execute().as_(
        e().tag(rm).tag('!homer').type('!item_frame')).run(data().merge(s(), {'Glowing': True})) for rm in
                                      ('mobs', 'monsters', 'wither', 'nether', 'enders', 'aquatic', 'ancient')))
    room.function('panda_init').add(placer(*south_placer).summon('panda'))
    room.loop('panda', main_clock).loop(
        lambda step: execute().as_(e().type('panda')).run(data().merge(s(), {'CustomName': f'{step.elem} Panda',
                                                                             'MainGene': step.elem.lower(),
                                                                             'HiddenGene': step.elem.lower()})),
        ('Aggressive', 'Lazy', 'Weak', 'Worried', 'Playful', 'Normal', 'Brown'))
    parrot_dir, parrot_pos = WEST, r(0, 3, 0)
    disc_chest_pos = r(-1, 1, 1)
    parrot_fence_pos = list(parrot_pos)
    parrot_fence_pos[1] -= 1
    room.function('parrot_init').add(
        placer(parrot_pos, parrot_dir, adults=True).summon('parrot'),
        function('restworld:mobs/parrot_enter'))
    room.function('parrot_enter').add(
        (item().replace().block(disc_chest_pos, f'container.{i:d}').with_(d) for i, d in enumerate(music_discs)))

    parrots = ('Red', 'Blue', 'Green', 'Cyan', 'Gray')
    parrot_settings = []
    for variant, p in enumerate(parrots):
        parrot_settings.append((p, False, variant))
        parrot_settings.append((p, True, variant))

    def parrot_loop(step):
        name, flying, variant = step.elem
        yield execute().as_(e().tag('parrot')).run(
            data().merge(s(), {'CustomName': name, 'Variant': variant, 'OnGround': not flying, 'Sitting': not flying}))
        yield execute().unless().block(r(0, 1, 0), 'air').run(
            setblock(parrot_fence_pos, 'air' if flying else 'oak_fence'))

    room.loop('parrot', main_clock).loop(parrot_loop, parrot_settings)
    room.function('pig_init').add(placer(*mid_west_placer).summon('pig'))
    room.loop('pig', main_clock).loop(
        lambda step: execute().as_(e().tag('pig').tag('!kid')).run(data().merge(s(), {'Saddle': step.i})),
        (True, False))
    room.function('polar_bear_init').add(placer(*south_placer).summon('Polar Bear'))
    room.function('rabbit_init').add(placer(*mid_east_placer).summon('rabbit'))

    def rabbit_loop(step):
        i = 99 if step.elem.startswith('Killer') else step.i
        yield execute().as_(e().tag('rabbit')).run(data().merge(s(), {'RabbitType': i, 'CustomName': step.elem}))

    room.loop('rabbit', main_clock).loop(rabbit_loop, (
        'Brown', 'White', 'Black', 'Black & White', 'Gold', 'Salt & Pepper', 'Killer Rabbit (unused)'))
    room.function('reset_collars').add(
        kill_em(e().tag('cat')),
        execute().at(e().tag('cat_home')).run(function('restworld:mobs/cat_init')),
        execute().at(e().tag('cat_home')).run(function('restworld:mobs/cat_cur')))
    p = placer(*mid_west_placer)
    sheep = room.function('sheep_init').add(
        p.summon('Sheep', tags=('colorable',)),
        p.summon(Entity('sheep', name='Sheared Sheep', nbt={'Sheared': True})))
    sheep.add(p.summon(Entity('sheep', name='jeb_'), auto_tag=False))
    room.function('sniffer_init').add(placer(r(0, 2, 0.5), WEST, 0, adults=True).summon('sniffer'))
    room.function('sniffer_kid_init').add(placer(r(0, 2, 0), WEST, 0, kids=True).summon('sniffer'))
    room.function('snow_golem_init').add(
        placer(r(-1.2, 2, 0), EAST, adults=True).summon('snow_golem'))
    room.loop('snow_golem', main_clock).loop(
        lambda step: execute().as_(e().tag('snow_golem')).run(data().merge(s(), {'Pumpkin': step.elem})), (True, False))
    room.function('switch_carpets_on').add(
        execute().at(e().tag('llamas_home')).positioned(r(-2, -0.5, 0)).run(
            function('restworld:mobs/llamas_carpets_home')),
        execute().at(e().tag('llamas_carpets_home')).run(function('restworld:mobs/llamas_carpets_cur')))
    room.function('switch_carpets_off').add(
        execute().as_(e().tag('llama')).run(data().merge(s(), {'DecorItem': {'id': 'white_carpet', 'Count': 0}})),
        kill(e().tag('llamas_carpets_home')))

    room.function('trader_llama_init').add(
        placer(r(0, 2, -2), WEST, adults=True).summon('wandering_trader'),
        placer(r(0, 2, 0), WEST, adults=True,
               nbt={'DespawnDelay': 2147483647, 'Leashed': True}).summon('trader_llama'),
    )
    room.loop('trader_llama', main_clock).loop(
        lambda step: execute().as_(e().type('trader_llama')).run(data().modify(s(), 'Variant').set().value(step.i)),
        ('Creamy', 'White', 'Brown', 'Gray'))
    switch_label_pos = r(3, 2, 0)
    egg_sign_pos = r(-2, 2, 0, )
    egg_sign_dir = EAST
    room.function('turtle_eggs_init').add(
        tag(e().tag('turtle_eggs_home')).add('blockers_home'),
        WallSign((None, 'Turtle Eggs')).place(egg_sign_pos, egg_sign_dir),
        label(switch_label_pos, 'On Sand'),
        tag(s().tag('turtle_egg_home')).add('blockers_home')
    )

    def turtle_egg_loop(step):
        for count in range(4, 0, -1):
            eggs = ('turtle_egg', {'eggs': count, 'hatch': step.elem})
            yield setblock(r(3 - count, 2, 0), eggs)
        yield data().merge(egg_sign_pos, {'Text3': f'Hatch Age: {step.elem:d}'})

    room.loop('turtle_eggs', main_clock).loop(turtle_egg_loop, range(0, 3), bounce=True)
    turtle_dir = EAST
    room.function('turtle_init').add(placer(r(0, 2, 0.2), turtle_dir, 2, 2).summon('turtle'))

    villager_funcs(room)


def villager_funcs(room):
    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    which_villagers = room.score('which_villagers')
    which_villagers_prev = room.score('which_villagers_prev')
    which_villagers_needed = room.score('which_villagers_needed')
    which_villagers_needed_prev = room.score('which_villagers_needed_prev')
    cur_villagers_levels = room.score('cur_villager_levels')
    cur_villagers_group = room.score('cur_villager_group')
    cur_villagers_zombies = room.score('cur_villager_zombies')
    bool_max = Score('bool', room.name + '_max')
    villager_types_cur = room.score('villager_types')

    def init_villagers(num, which):
        return execute().if_().score(which_villagers).matches(num).at(
            e().tag('cur_villagers_home')).run(function(f'restworld:mobs/{which}_init'))

    def home_villagers(num, which):
        return execute().if_().score(which_villagers).matches(num).at(e().tag('which_villagers_home').limit(1)).run(
            summon('armor_stand', r(0, 0, 1),
                   {'Tags': [f'{which}_home', 'cur_villagers_home'],
                    'Small': True, 'NoGravity': True}))

    # Init & Loop functions
    def kind_names(which):
        kind = which
        id = which
        if kind[0] == 'z':
            kind += ' Villagers'
            id += '_villager'
        else:
            kind = 'villagers'
        kind = kind.title()
        return id, kind

    def professions_init_funcs(which):
        id, kind = kind_names(which)
        professions_init = room.function(f'{which}_professions_init').add(kill(e().tag('villager')))
        p = placer(r(-2, 2, -6), WEST, -2, tags=('villager', 'professions',), adults=True)
        for i, pro in enumerate(VILLAGER_PROFESSIONS):
            if i == 7:
                if which == 'villager':
                    professions_init.add(p.summon(Entity('villager', name='Child', nbt={'Age': -2147483648})))
                p = placer(r(0, 2, -7), WEST, -2, tags=('villager', 'professions',), adults=True)
            professions_init.add(p.summon(Villager(pro, PLAINS, name=pro, zombie=id[0] == 'z'), tags=('villager',)))
        professions_init.add(
            function(f'restworld:mobs/{which}_levels_cur'),
            function(f'restworld:mobs/{which}_professions_cur'),
            data().merge(r(-5, 2, 0), {'Text3': kind}))

    professions_init_funcs('villager')

    def villager_professions_loop(step):
        yield execute().as_(e().tag('villager')).run(
            data().modify(s(), 'VillagerData.type').set().value(step.elem.lower()))
        yield data().merge(r(-5, 2, 0), {'Text2': step.elem})

    room.loop('villager_professions', main_clock).loop(villager_professions_loop, VILLAGER_BIOMES)

    def types_init_funcs(which):
        id, kind = kind_names(which)
        p = placer(r(-2, 2, -2), WEST, -2, tags=('villager', 'types',), adults=True)
        types_init = room.function(f'{which}_types_init').add(kill(e().tag('villager')))
        for i, ty in enumerate(VILLAGER_BIOMES):
            if i == 3:
                p = placer(r(0, 2, -3), WEST, -2, tags=('villager', 'types',), adults=True)
            types_init.add(p.summon(Entity(id, name=ty, nbt={'VillagerData': {'type': ty.lower()}})))
        types_init.add(
            function(f'restworld:mobs/{which}_levels_cur'),
            function(f'restworld:mobs/{which}_types_cur'),
            data().merge(r(-5, 2, 0), {'Text3': kind})
        )

    types_init_funcs('villager')

    def villager_types_loop(step):
        if step.elem == 'Child':
            # Skip over child for zombies, there are no zombie children
            yield execute().as_(e().tag('zombie_villager').limit(1)).run(villager_types_cur.set(0))
        yield execute().as_(e().tag('villager')).run(
            data().modify(s(), 'VillagerData.profession').set().value(step.elem.lower()))
        yield execute().as_(e().tag('villager')).run(
            data().modify(s(), 'Age').set().value(-2147483648 if step.elem == 'Child' else 0))
        yield data().merge(r(-5, 2, 0), {'Text2': step.elem})

    roles = VILLAGER_PROFESSIONS + ('Child',)
    room.loop('villager_types', main_clock).loop(villager_types_loop, roles).add(
        execute().as_(e().tag('villager')).run(execute().at(s()).as_(s()).align('xyz').run(tp(
            s(), r(0.5, 0.0, 0.5)))))

    professions_init_funcs('zombie')
    room.loop('zombie_professions', main_clock).loop(None, list()).add(
        function('restworld:mobs/villager_professions_main'))
    types_init_funcs('zombie')
    room.loop('zombie_types', main_clock).loop(None, list()).add(
        function('restworld:mobs/villager_types_main'))

    room.function('which_villagers_init').add(
        bool_max.set(2),
        cur_villagers_group.set(0),
        cur_villagers_zombies.set(0),
        function('restworld:mobs/switch_villagers'),
        WallSign((None, None, 'Villagers')).place(r(-5, 2, 1), WEST),
        label(r(-3, 2, 0), 'Profession'),
        label(r(-3, 2, 2), 'Level'),
        label(r(-3, 2, 4), 'Zombies'),
    )

    # Switch functions
    room.function('switch_villagers').add(
        which_villagers.set(0),
        execute().if_().score(cur_villagers_group).matches(1).run(which_villagers.add(1)),
        execute().if_().score(cur_villagers_zombies).matches(1).run(which_villagers.add(2)),
        which_villagers_needed.operation(EQ, which_villagers),

        # Replace the villagers being shown if they've changed
        execute().unless().score(which_villagers_needed).is_(EQ, which_villagers_needed_prev).run((
            kill_em(e().tag('villager')),
            init_villagers(0, 'villager_professions'),
            init_villagers(1, 'villager_types'),
            init_villagers(2, 'zombie_professions'),
            init_villagers(3, 'zombie_types'),
            # If zombies are on, turn off level. Setting the lever off does not cause the piston to move, hence the
            # redstone block work.
            execute().if_().score(cur_villagers_zombies).matches(1).at(e().tag('which_villagers_home')).run(
                setblock(r(-3, 2, 2), Block('lever', state=dict(face='floor', facing='east'))),
                setblock(r(-3, -1, 2), 'redstone_block'),
                setblock(r(-3, -1, 2), 'air'),
            ),
        )),
        which_villagers_needed_prev.operation(EQ, which_villagers_needed),
        execute().if_().score(cur_villagers_levels).matches(1).run(which_villagers.add(4)),

        kill(e().tag('cur_villagers_home')),
        home_villagers(0, 'villager_professions'),
        home_villagers(1, 'villager_types'),
        home_villagers(2, 'zombie_professions'),
        home_villagers(3, 'zombie_types'),
        home_villagers((4, None), 'villager_levels'),
    )
    room.function('switch_villagers_init').add(
        which_villagers_prev.set(1),
        function('restworld:mobs/switch_villagers'))
    room.function('toggle_villager_group').add(
        cur_villagers_group.add(1),
        cur_villagers_group.operation(MOD, bool_max),
        function('restworld:mobs/switch_villagers'))
    room.function('toggle_villager_levels').add(
        cur_villagers_levels.add(1),
        cur_villagers_levels.operation(MOD, bool_max),
        execute().if_().score(cur_villagers_levels).matches(1).run(cur_villagers_zombies.set(0)),
        function('restworld:mobs/switch_villagers'))
    room.function('toggle_villager_zombies').add(
        cur_villagers_zombies.add(1),
        cur_villagers_zombies.operation(MOD, bool_max),
        execute().if_().score(cur_villagers_zombies).matches(1).run(cur_villagers_levels.set(0)),
        function('restworld:mobs/switch_villagers'))

    def villager_level_loop(step):
        yield execute().as_(e().tag('villager')).run(data().modify(s(), 'VillagerData.level').set().value(step.i + 1))
        yield data().merge(r(-5, 2, 0), {'Text2': f' {step.elem} Level'})

    room.loop('villager_levels', main_clock).loop(villager_level_loop, ('Stone', 'Iron', 'Gold', 'Emerald', 'Diamond'))


def monsters(room):
    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    east_placer = list(r(-0.2, 2, 0)), EAST, 2, 2.2
    west_placer = list(r(0.2, 2, 0)), WEST, -2, 2.2

    room.function('creeper_init').add(placer(*west_placer, adults=True).summon('creeper'))
    room.loop('creeper', main_clock).loop(
        lambda step: execute().as_(e().tag('creeper').limit(1)).run(data().merge(s(), {'powered': step.elem})),
        (True, False))

    slime_placer = copy.deepcopy(west_placer)
    slime_placer[0][1] = r(3)
    room.function('slime_init').add(placer(*slime_placer, adults=True).summon('slime'))
    room.loop('slime', main_clock).loop(
        lambda step: data().modify(e().tag('slime').limit(1), 'Size').set().value(step.elem),
        range(0, 3), bounce=True)

    illagers = (Entity('Vindicator'), Entity('Evoker'), Entity('Pillager'),
                Entity('Pillager', nbt={'HandItems': [Item.nbt_for('crossbow')]}),
                Entity('illusioner', name='Illusioner (unused)'))
    tags = ('illager',)

    def illager_loop(step):
        place = list(copy.deepcopy(west_placer))
        dir = EAST
        place[0][2] -= 0.5
        place[1] = dir
        yield placer(*place, adults=True, tags=tags).summon(step.elem)
        if step.elem.id == 'evoker':
            yield placer(r(1, 3.5, -1.5), dir, adults=True, tags=tags).summon(
                Entity('vex', nbt={'HandItems': [Item.nbt_for('iron_sword')], 'LifeTicks': 2147483647}))
            yield placer(r(-1 + 2 * 1, 2, 1), dir, adults=True, tags=tags).summon(
                Entity('Evoker Fangs', nbt={'Warmup': 0}))

    room.loop('illager', main_clock).add(kill_em(e().tag(*tags))).loop(illager_loop, illagers)

    room.function('phantom_init').add(placer(r(-0.5, 4, 0), NORTH, adults=True).summon('phantom'))

    def ravager_loop(step):
        ravager = Entity('ravager')
        if step.elem is not None:
            ravager.passenger(Entity(step.elem, {'Rotation': good_facing(EAST).rotation}).merge_nbt(MobPlacer.base_nbt))
        yield placer(r(1, 2, 0), EAST, adults=True).summon(ravager)

    room.loop('ravager', main_clock).add(kill_em(e().tag('ravager'))).loop(
        ravager_loop, (None, 'Pillager', 'Vindicator', 'Evoker'))

    silverfish_dir = method_name()
    room.function('silverfish_init').add(placer(r(0.2, 2, 0), silverfish_dir, adults=True).summon('silverfish'))

    east = good_facing(EAST)
    east_rot = {'Rotation': east.rotation, 'Facing': east.name}

    def skeleton_horse_loop(step):
        horse = Entity('Skeleton Horse')
        if step.i == 1:
            helmet = {'id': 'iron_helmet', 'Count': 1, 'tag': {'RepairCost': 1, 'Enchantments': [
                {'lvl': 3, 'id': 'unbreaking'}]}}
            bow = {'id': 'bow', 'Count': 1,
                   'tag': {'RepairCost': 1, 'Enchantments': [{'lvl': 3, 'id': 'unbreaking'}]}}
            skel = Entity('Skeleton', nbt={'ArmorItems': [{}, {}, {}, helmet], 'HandItems': [bow, {}]})
            skel.merge_nbt(MobPlacer.base_nbt).merge_nbt(east_rot)
            skel.tag('mobs', 'passenger')
            horse.passenger(skel)
        yield placer(*east_placer, adults=True).summon(horse)

    room.loop('skeleton_horse').add(
        kill_em(e().tag('skeleton_horse', '!kid'))
    ).loop(skeleton_horse_loop, range(0, 2))

    room.function('skeleton_horse_init').add(
        placer(*east_placer).summon('Skeleton Horse'),
        label(r(2, 2, -1), 'Rider'))

    bow = Item.nbt_for('bow')
    helmet = Item.nbt_for('iron_helmet')
    rider = Entity('Skeleton', nbt={'ArmorItems': [{}, {}, {}, helmet], 'HandItems': [bow, {}]}).merge_nbt(
        MobPlacer.base_nbt)

    room.loop('skeleton', main_clock).add(
        kill_em(e().tag('skeletal'))
    ).loop(lambda step: placer(*west_placer, adults=True).summon(
        Entity(step.elem, nbt={'HandItems': [bow]}).tag('skeletal')), ('Skeleton', 'Stray'))

    spider_dir = NORTH
    spider_facing = good_facing(spider_dir)
    spider_rot = {'Rotation': spider_facing.rotation, 'Facing': spider_facing.name}

    def spider_loop(step):
        p = placer(r(-0.2, 2.5, -0.2), spider_dir, -2.5, nbt={'Tags': ['spiders']}, adults=True)
        for s in ('Spider', 'Cave Spider'):
            spider = Entity(s)
            if step.i == 1:
                spider.passenger(rider.merge_nbt(spider_rot).merge_nbt(MobPlacer.base_nbt))
            yield p.summon(spider)

    room.loop('spiders').add(
        kill_em(e().tag('spiders'))
    ).loop(spider_loop, range(0, 2))
    room.function('spiders_init').add(
        function('restworld:mobs/spiders_cur'),
        label(r(-2, 2, -1), 'Jockey'))
    place = list(copy.deepcopy(west_placer))
    place[0][2] -= 0.5
    room.function('witch_init').add(placer(*place, adults=True).summon('witch'))
    place = list(copy.deepcopy(east_placer))
    place[0][2] -= 0.5
    room.function('zombie_horse_init').add(
        placer(*place).summon(Entity('zombie_horse', name='Zombie Horse (Unused)')))
    zombie_jockey = room.score('zombie_jockey')
    room.function('zombie_init').add(
        zombie_jockey.set(0),
        execute().as_(e().tag('zombie_home')).run(tag(s()).add('zombie_home_selector')),
        execute().as_(e().tag('zombie_jockey_home')).run(tag(s()).add('zombie_home_selector')),
        label(r(2, 2, -1), 'Jockey'))

    def zombie_loop(step):
        p = placer(r(0.2, 2, 0), EAST, 0, 1.8, tags=('zombieish',))
        yield execute().if_().score(zombie_jockey).matches(0).run(p.summon(Entity(step.elem)))

        p = placer(r(0.2, 2, 0), EAST, 0, 2.2, tags=('zombieish',), adults=True)
        yield execute().if_().score(zombie_jockey).matches(1).run(p.summon(Entity(step.elem)))
        chicken = Entity('Chicken').passenger(
            Entity(step.elem, {'Tags': ['kid', room.name], 'IsBaby': True, 'Age': -2147483648}).merge_nbt(
                east_rot).merge_nbt(MobPlacer.base_nbt))
        p = placer(r(2.0, 2, 0), EAST, 0, 2.2, tags=('zombieish',), kids=True)
        yield execute().if_().score(zombie_jockey).matches(1).run(p.summon(chicken))
        if step.elem == 'Drowned':
            yield execute().as_(e().tag('zombieish').tag('!kid')).run(
                data().merge(s(), {'HandItems': [Item.nbt_for('trident')]}))

    room.loop('zombie', main_clock).add(kill_em(e().tag('zombieish'))).loop(
        zombie_loop, ('Zombie', 'Husk', 'Drowned'))

    placer = room.mob_placer(r(0, 2, 0), NORTH, adults=True)
    room.function('enderman_init').add(
        execute().unless().entity(e().type('enderman').distance((None, 5))).run(list(placer.summon('enderman'))[0]))

    # room.function('silverfish_init').add(placer(r(0.2, 2, 0), silverfish_dir, adults=True).summon('silverfish'))
    placer = room.mob_placer(r(0, 2, 0.2), NORTH, adults=True)
    room.function('endermite_init').add(placer.summon('endermite'))

    room.function('warden_init').add((room.mob_placer(r(0, 2, -0.5), NORTH, adults=True).summon('warden'),))


def method_name():
    silverfish_dir = NORTH
    return silverfish_dir


def aquatic(room):
    def n_fish_loop(count: int):
        def fish_loop(step):
            for kind, breeds in tropical_fish.items():
                if len(breeds) == count:
                    fish = breeds[step.i]
                    fish.custom_name(True)
                    yield data().merge(e().tag(kind.lower()).limit(1), fish.nbt)

        return fish_loop

    room.loop('2_fish', main_clock).loop(n_fish_loop(2), range(2))
    room.loop('3_fish', main_clock).loop(n_fish_loop(3), range(3))
    room.loop('4_fish', main_clock).loop(n_fish_loop(4), range(4))
    all_fish_funcs(room)
    t_fish = room.function('tropical_fish_init')
    for i, (kind, breeds) in enumerate(tropical_fish.items()):
        fish = breeds[0]
        fish.custom_name(True)
        fish.tag(kind.lower())
        placer = room.mob_placer(r(-int(i / 4), 3.2, int(i % 4)), EAST, adults=True)
        t_fish.add(placer.summon(fish))
    t_fish.add(WallSign(('Naturally', 'Occurring', u'Tropical Fish', u'→ → →')).place(
        r(1, 2, (len(tropical_fish) - 1) % 4), EAST, water=True))

    axolotl_placer = room.mob_placer(r(-0.4, 3, 0), WEST, None, 1.8)
    room.function('axolotl_init').add(
        axolotl_placer.summon('axolotl'),
        execute().at(e().tag('axolotl_dry_home')).run(
            room.mob_placer(r(0, 3, 0), EAST, kid_delta=2).summon('axolotl')))
    room.function('axolotl_dry')
    room.loop('axolotl', main_clock).loop(
        lambda step: execute().as_(e().tag('axolotl')).run(data().merge(
            s(), {'Variant': step.i, 'CustomName': step.elem + ' Axolotl'})), axolotls)
    guardian_pos = elder_guardian_pos = r(0, 3, 0)
    guardian_rot = elder_guardian_rot = SOUTH
    room.function('guardian_init').add(room.mob_placer(guardian_pos, guardian_rot, adults=True).summon('guardian'))
    room.function('elder_guardian_init').add(
        room.mob_placer(elder_guardian_pos, elder_guardian_rot, adults=True).summon('elder_guardian'))

    def squids_loop(step):
        placer = room.mob_placer(r(1.8, 4, 0.2), WEST, adults=True, tags=('squidy',), nbt={'NoGravity': True})
        return placer.summon('squid' if step.i == 0 else 'glow_squid')

    room.loop('squid', main_clock).add(kill_em(e().tag('squidy'))).loop(squids_loop, range(0, 2))

    dolphin_placer = room.mob_placer(r(1.35, 3, 1.1), NORTH, adults=True)
    fish_placer = room.mob_placer(r(0, 3, 1), NORTH, -1, adults=True)
    room.function('fishies_init').add(
        # For some reason, at 1.19 the kill-off in the _init function misses the pufferfish
        kill(e().tag('pufferfish')),
        dolphin_placer.summon(Entity('dolphin', nbt={'Invulnerable': True})),
        fish_placer.summon(
            ('salmon', 'cod', 'pufferfish',
             Entity('tadpole', nbt={'Invulnerable': True, 'Age': -2147483648}).tag('kid', 'keeper'))),
    )

    def fishies_loop(step):
        yield data().merge(e().tag('pufferfish').limit(1), {'PuffState': step.elem})
        # Over time, the pufferfish creeps downward, so we have to put it back
        puffer_pos = r(-2, 3, 1)
        puffer_facing = r(-2, 3, -5)
        yield tp(e().tag('pufferfish'), puffer_pos).facing(puffer_facing)

    room.loop('fishies', main_clock).loop(fishies_loop, range(0, 3), bounce=True)


def all_fish_funcs(room):
    pattern = Score('pattern', 'fish')
    num_colors = Score('NUM_COLORS', 'fish')
    body_scale = Score('BODY_SCALE', 'fish')
    overlay_scale = Score('OVERLAY_SCALE', 'fish')
    pattern_size = Score('PATTERN_SIZE', 'fish')
    variant = Score('variant', 'fish')

    kinds = tuple(tropical_fish.keys())

    def all_fish_init():
        yield WallSign((None, 'All Possible', 'Tropical Fish', '← ← ←')).place(r(0, 2, 0), EAST, water=True)
        start, facing, delta = r(0, 3.2, 0), EAST, 1
        placer = room.mob_placer(start, facing, delta, adults=True)
        for i in range(0, 12):
            if i % 4 == 0:
                x, y, z = start
                start = (x - delta, y, z)
                placer = room.mob_placer(start, facing, delta, adults=True)
            fish = Entity('tropical_fish', name=kinds[i])
            summon = placer.summon(fish, tags=(f'fish{i}',))
            yield summon
        yield (
            scoreboard().objectives().remove('fish'),
            scoreboard().objectives().add('fish', ScoreCriteria.DUMMY),
            num_colors.set(len(COLORS)),
            pattern.set(0),
            pattern_size.set(len(COLORS) ** 2),
            body_scale.set(0x10000),
            overlay_scale.set(0x1000000),
        )

    def all_fish():
        yield (
            pattern.set((pattern + 1) % pattern_size),
            variant.set((pattern // num_colors) * body_scale + (pattern % num_colors) * overlay_scale))
        for i in range(0, 6):
            yield from fish_variant(i)
            if i < 5:
                yield variant.add(256)
        yield variant.add(1)
        for i in range(6, 12):
            yield from fish_variant(i)
            if i < 11:
                yield variant.remove(256)

    def fish_variant(i):
        yield execute().store(RESULT).entity(e().tag(f'fish{i:d}').limit(1), 'Variant', LONG, 1).run(variant.get())

    room.function('all_fish_init').add(all_fish_init())
    room.loop('all_fish', fast_clock).add(all_fish())
