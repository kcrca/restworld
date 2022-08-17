from __future__ import annotations

from pynecraft.base import EAST, NORTH, SOUTH, WEST, r, to_id
from pynecraft.commands import Block, EQ, Entity, MOD, Score, data, e, execute, function, item, kill, s, setblock, \
    summon, tag, \
    tp
from pynecraft.info import colors, horses, music_discs, villager_professions, villager_types
from pynecraft.simpler import WallSign
from restworld.rooms import Room, label
from restworld.world import kill_em, main_clock, restworld


def room():
    room = Room('friendlies', restworld, NORTH, ('Villagers,', 'Animals,', 'Mobs,', 'Bosses'), 'Friendly Mobs')
    south_placer = r(0, 2, -0.2), SOUTH, -2, 2.2
    mid_east_placer = r(-1.2, 2, 0), EAST, 2, 2.2
    mid_west_placer = r(0.2, 2, 0), WEST, -2, 2.2

    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    room.function('allay_init').add(placer(r(0, 3.5, -1), NORTH, adults=True).summon('Allay'))
    room.function('bat_init').add(
        placer(r(0, 3, -2), NORTH, 2, adults=True).summon('bat'),
        placer(r(0, 3.5, 1), NORTH, 2, adults=True).summon('bat', nbt={'BatFlags': 1}, tags=('sleeping_bat',)))
    room.function('bee_init').add(
        placer(r(0, 3, 0), NORTH, 0, 2).summon('bee'),
        label(r(1, 2, -2), 'Stinger'),
        label(r(-1, 2, -2), 'Pollen'))

    def bee_loop(step):
        bee_house = 'beehive' if step.i == 0 else 'bee_nest'
        # The 'air' check is for if we're levitated
        yield execute().unless().block(r(0, 1, 0), 'air').at(
            e().tag('bee_home')).run(setblock(r(0, 2, 2), (bee_house, {'facing': NORTH})))
        on_ground = step.i < 2
        base = 'iron_bars' if on_ground else 'air'
        yield execute().as_(e().tag('bee')).run(data().merge(s(),
                                                             {'OnGround': on_ground, 'AngerTime': (step.i % 2) * 100000,
                                                              'CustomName': 'Bee' if step.i % 2 == 0 else 'Angry Bee'}))
        yield execute().unless().block(r(0, 1, 0), 'air').run(setblock(r(0, 2, 0), base))
        yield execute().unless().block(r(0, 1, 0), 'air').run(setblock(r(0, 2, -2), base))

    room.loop('bee', main_clock).loop(bee_loop, range(0, 4))

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
        label(r(0, 2, 3), 'Change Height')
    )

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
    room.function('frog_init').add(placer(r(0, 2, 0.2), NORTH, adults=True).summon('frog'))

    room.loop('frog', main_clock).loop(
        lambda step: execute().as_(e().tag('frog')).run(
            data().merge(s(), {'variant': step.elem.lower(), 'CustomName': f'{step.elem} Frog'})),
        ('Temperate', 'Warm', 'Cold'))

    def frogspawn_loop(step):
        if step.i == 0:
            yield kill_em(e().tag('tadpole', room.name))
            # The 'air' check is for if we're levitated
            yield execute().unless().block(r(0, 1, 0), 'air').at(
                e().tag('frogspawn_home')).run(setblock(r(0, 2, -1), 'frogspawn'))
            yield execute().unless().block(r(0, 1, 0), 'air').at(
                e().tag('frogspawn_home')).run(WallSign((None, 'Frogspawn')).place(r(1, 2, -1), NORTH))
        else:
            yield placer(r(0, 2, -1), NORTH, kids=True).summon(Entity('tadpole', {'Invulnerable': True}),
                                                               tags=('keeper',))
            yield setblock(r(0, 2, -1), 'air')
            yield setblock(r(1, 2, -1), 'air')
        yield kill_em(e().type('tadpole').not_tag('keeper'))

    room.loop('frogspawn', main_clock).loop(frogspawn_loop, range(0, 2))
    room.function('goat_init').add(placer(*south_placer).summon('goat'))
    room.loop('goat', main_clock).loop(
        lambda step: execute().as_(e().tag('goat').tag('adult')).run(
            data().merge(s(), {'HasLeftHorn': step.i & 1, 'HasRightHorn': step.i & 2})), range(0, 4))

    p = placer(r(-1.2, 2, 0), EAST, -2, 1.6, tags=('saddle',), nbt={'Tame': True})
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

    p = placer(r(-1.2, 2, 0), EAST, -2, 1.6, tags=('saddle', 'chests'))
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
    room.function('lead_off').add(kill(e().type('leash_knot')))
    room.function('lead_on').add(
        execute().as_(e().tag('white_horses').tag('!kid')).run(
            data().merge(s(), {'Leash': {'X': -12, 'Y': 101, 'Z': 35}})))
    room.loop('llamas_carpets', main_clock).loop(
        lambda step: execute().as_(e().tag('llama').tag('!kid')).run(
            data().merge(s(), {'DecorItem': {'id': step.elem.id + '_carpet', 'Count': 1}})), colors)

    room.function('llamas_init').add(
        placer(r(0, 2, 0), WEST, 0, 2).summon('llama'),
        placer(r(1, 3.5, -1), WEST, adults=True,
               nbt={'Tags': ['friendlies', 'llama', 'llama_spit'], 'TXD': 0, 'TYD': 0, 'TZD': 0, 'Steps': 0,
                    'Motion': [0, 0, 0], 'NoGravity': True}).summon('llama_spit'),
        WallSign((None, 'Llama Spit')).place(r(1, 2, -1), WEST),
        label(r(-2, 2, 1), 'Carpets'),
        label(r(-2, 2, -1), 'Chests'),
    )

    room.loop('llamas', main_clock).loop(
        lambda step: execute().as_(e().tag('llama')).run(
            data().merge(s(), {'Variant': step.i, 'CustomName': step.elem})), ('Creamy', 'White', 'Brown', 'Gray'))
    room.function('ocelot_init').add(placer(*south_placer).summon('ocelot'))
    room.function('outlines_on').add((execute().as_(
        e().tag(rm).tag('!homer').type('!item_frame')).run(data().merge(s(), {'Glowing': True})) for rm in
                                      ('friendlies', 'monsters', 'wither', 'nether', 'enders', 'aquatic', 'ancient')))
    room.function('panda_init').add(placer(*south_placer).summon('panda'))
    room.loop('panda', main_clock).loop(
        lambda step: execute().as_(e().type('panda')).run(data().merge(s(), {'CustomName': f'{step.elem} Panda',
                                                                             'MainGene': step.elem.lower(),
                                                                             'HiddenGene': step.elem.lower()})),
        ('Aggressive', 'Lazy', 'Weak', 'Worried', 'Playful', 'Normal', 'Brown'))
    room.function('parrot_init').add(
        placer(r(0, 3, 1), NORTH, adults=True).summon('parrot'),
        function('restworld:friendlies/parrot_enter'))
    room.function('parrot_enter').add(
        (item().replace().block(r(-1, 1, 0), f'container.{i:d}').with_(d) for i, d in enumerate(music_discs)))

    parrots = ('Red', 'Blue', 'Green', 'Cyan', 'Gray')
    parrot_settings = []
    for variant, p in enumerate(parrots):
        parrot_settings.append((p, False, variant))
        parrot_settings.append((p, True, variant))

    def parrot_loop(step):
        name, flying, variant = step.elem
        yield execute().as_(e().tag('parrot')).run(
            data().merge(s(), {'CustomName': name, 'Variant': variant, 'OnGround': not flying, 'Sitting': not flying}))
        yield execute().unless().block(r(0, 1, 0), 'air').run(setblock(r(0, 2, 1), 'air' if flying else 'oak_fence'))

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
        execute().at(e().tag('cat_home')).run(function('restworld:friendlies/cat_init')),
        execute().at(e().tag('cat_home')).run(function('restworld:friendlies/cat_cur')))
    p = placer(*mid_west_placer)
    room.function('sheep_init').add(
        p.summon('Sheep', tags=('colorable',)),
        p.summon(Entity('sheep', name='Sheared Sheep', nbt={'Sheared': True})),
        p.summon(Entity('sheep', name='jeb_'), auto_tag=False))
    room.function('snow_golem_init').add(
        placer(r(-1.2, 2, 0), EAST, adults=True).summon('snow_golem'))
    room.loop('snow_golem', main_clock).loop(
        lambda step: execute().as_(e().tag('snow_golem')).run(data().merge(s(), {'Pumpkin': step.elem})), (True, False))
    room.function('switch_carpets_on').add(
        execute().at(e().tag('llamas_home')).positioned(r(-2, -0.5, 0)).run(
            function('restworld:friendlies/llamas_carpets_home')),
        execute().at(e().tag('llamas_carpets_home')).run(function('restworld:friendlies/llamas_carpets_cur')))
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
    room.function('turtle_eggs_init').add(
        execute().as_(e().tag('turtle_home')).run(tag(s()).add('blockers_home')),
        WallSign((None, 'Turtle Eggs')).place(r(0, 2, 2, ), NORTH),
        label(r(1, 2, -2), 'On Sand')
    )

    def turtle_egg_loop(step):
        for count in range(4, 0, -1):
            yield setblock(r(0, 2, count - 3), ('turtle_egg', {'eggs': count, 'hatch': step.elem}))
        yield data().merge(r(0, 2, 2), {'Text3': f'Hatch Age: {step.elem:d}'})

    room.loop('turtle_eggs', main_clock).loop(turtle_egg_loop, range(0, 3), bounce=True)
    room.function('turtle_init').add(placer(r(0, 2, 0.2), NORTH, 2, 2).summon('turtle'))

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
            e().tag('cur_villagers_home')).run(function(f'restworld:friendlies/{which}_init'))

    def home_villagers(num, which):
        return execute().if_().score(which_villagers).matches(num).at(
            e().tag('which_villagers_home').limit(1)).run(summon('armor_stand', r(0, 0, 1),
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
        for i, pro in enumerate(villager_professions):
            if i == 7:
                if which == 'villager':
                    professions_init.add(p.summon(Entity('villager', name='Child', nbt={'Age': -2147483648})))
                p = placer(r(0, 2, -7), WEST, -2, tags=('villager', 'professions',), adults=True)
            professions_init.add(p.summon(Entity(
                id, name=pro, nbt={'VillagerData': {'profession': pro.lower()}}), tags=('villager',)))
        professions_init.add(
            function(f'restworld:friendlies/{which}_levels_cur'),
            function(f'restworld:friendlies/{which}_professions_cur'),
            data().merge(r(-5, 2, 0), {'Text3': kind}))

    professions_init_funcs('villager')

    def villager_professions_loop(step):
        yield execute().as_(e().tag('villager')).run(
            data().modify(s(), 'VillagerData.type').set().value(step.elem.lower()))
        yield data().merge(r(-5, 2, 0), {'Text2': step.elem})

    room.loop('villager_professions', main_clock).loop(villager_professions_loop, villager_types)

    def types_init_funcs(which):
        id, kind = kind_names(which)
        p = placer(r(-2, 2, -2), WEST, -2, tags=('villager', 'types',), adults=True)
        types_init = room.function(f'{which}_types_init').add(kill(e().tag('villager')))
        for i, ty in enumerate(villager_types):
            if i == 3:
                p = placer(r(0, 2, -3), WEST, -2, tags=('villager', 'types',), adults=True)
            types_init.add(p.summon(Entity(id, name=ty, nbt={'VillagerData': {'type': ty.lower()}})))
        types_init.add(
            function(f'restworld:friendlies/{which}_levels_cur'),
            function(f'restworld:friendlies/{which}_types_cur'),
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

    roles = villager_professions + ('Child',)
    room.loop('villager_types', main_clock).loop(villager_types_loop, roles).add(
        execute().as_(e().tag('villager')).run(execute().at(s()).as_(s()).align('xyz').run(tp(
            s(), r(0.5, 0.0, 0.5)))))

    professions_init_funcs('zombie')
    room.loop('zombie_professions', main_clock).loop(None, list()).add(
        function('restworld:friendlies/villager_professions_main'))
    types_init_funcs('zombie')
    room.loop('zombie_types', main_clock).loop(None, list()).add(
        function('restworld:friendlies/villager_types_main'))

    room.function('which_villagers_init').add(
        bool_max.set(2),
        cur_villagers_group.set(0),
        cur_villagers_zombies.set(0),
        function('restworld:friendlies/switch_villagers'),
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
        function('restworld:friendlies/switch_villagers'))
    room.function('toggle_villager_group').add(
        cur_villagers_group.add(1),
        cur_villagers_group.operation(MOD, bool_max),
        function('restworld:friendlies/switch_villagers'))
    room.function('toggle_villager_levels').add(
        cur_villagers_levels.add(1),
        cur_villagers_levels.operation(MOD, bool_max),
        execute().if_().score(cur_villagers_levels).matches(1).run(cur_villagers_zombies.set(0)),
        function('restworld:friendlies/switch_villagers'))
    room.function('toggle_villager_zombies').add(
        cur_villagers_zombies.add(1),
        cur_villagers_zombies.operation(MOD, bool_max),
        execute().if_().score(cur_villagers_zombies).matches(1).run(cur_villagers_levels.set(0)),
        function('restworld:friendlies/switch_villagers'))

    def villager_level_loop(step):
        yield execute().as_(e().tag('villager')).run(data().modify(s(), 'VillagerData.level').set().value(step.i + 1))
        yield data().merge(r(-5, 2, 0), {'Text2': f' {step.elem} Level'})

    room.loop('villager_levels', main_clock).loop(villager_level_loop, ('Stone', 'Iron', 'Gold', 'Emerald', 'Diamond'))
