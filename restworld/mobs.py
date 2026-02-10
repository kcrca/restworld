from __future__ import annotations

import copy

from titlecase import titlecase

from pynecraft.base import EAST, EQ, NE, NORTH, Nbt, SOUTH, WEST, r, to_id, to_name
from pynecraft.commands import Block, COLORS, Entity, FORCE, LONG, MOD, REPLACE, RESULT, SUCCESS, Score, as_facing, \
    clone, data, \
    e, execute, fillbiome, function, item, kill, n, p, player, return_, ride, s, schedule, scoreboard, setblock, \
    summon, \
    tag, tp
from pynecraft.info import axolotls, colors, default_skins, horses, mannequin_poses, tropical_fish, weathering_id, \
    weathering_name, \
    weathering_property, \
    weatherings, \
    wolves
from pynecraft.simpler import Item, PLAINS, Sign, VILLAGER_BIOMES, VILLAGER_PROFESSIONS, Villager, WallSign
from pynecraft.values import DISC_GROUP, DUMMY, as_disc, discs
from restworld.materials import water_biomes
from restworld.rooms import MobPlacer, Room, kill_em
from restworld.world import fast_clock, main_clock, restworld


def room():
    room = Room('mobs', restworld, NORTH, ('Villagers,', 'Animals,', 'Monsters,', 'Bosses'), 'Mobs')
    room.reset_at((0, 15))
    room.change_height_at((0, 19))
    room.change_height_at((0, 43))
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
    room.function('bat_init').add(placer(bat_pos, bat_dir, 2, adults=True).summon('bat'),
                                  placer(hang_bat_pos, bat_dir, 2, adults=True).summon('bat', nbt={'BatFlags': 1},
                                                                                       tags=('sleeping_bat',)))

    stinger_label_pos = r(-2, 2, 1)
    pollen_label_pos = r(-2, 2, -1)
    room.function('bee_init').add(
        placer(r(0, 3, 0), WEST, 0, 2).summon('bee'), room.label(stinger_label_pos, 'Stinger', WEST),
        room.label(pollen_label_pos, 'Pollen', WEST))

    def armadillo_loop(step):
        yield execute().as_(e().tag('armadillo')).run(data().modify(s(), 'state').set().value(step.elem))

    p = placer(*mid_east_placer, tags='keeper')
    room.function('armadillo_init').add(p.summon('Armadillo'))
    room.loop('armadillo', main_clock).loop(armadillo_loop, ('idle', 'scared'))

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
        p.summon(Entity('wolf', nbt={'Owner': 'dummy'}, name='Tamed Wolf'), tags=('collared',)),
        room.label(r(1, 2, 2), 'Sit', SOUTH),
        room.label(r(1, 2, 0), 'Anger', SOUTH),
        room.label(r(3, 2, 0), 'Armor', SOUTH),
    )
    room.function('canine_enter').add(
        data().modify(e().tag('wolf', 'collared').limit(1), 'Owner').set().from_(player(), 'UUID'))
    room.function('angry_wolf_on', home=False).add(
        execute().as_(e().tag('wolf', '!collared')).run(data().modify(s(), 'angry_at').set().from_(s(), 'UUID')))
    room.function('angry_wolf_off', home=False).add(
        execute().as_(e().tag('wolf')).run(
            data().modify(s(), 'anger_end_time').set().value(-1),
            data().remove(s(), 'angry_at')))

    def wolf_loop(step):
        yield execute().as_(e().tag('wolf')).run(
            data().merge(s(), {'CustomName': to_name(step.elem), 'variant': step.elem}))

    room.loop('canine', main_clock).loop(wolf_loop, wolves)
    room.function('cat_init').add(placer(*south_placer, tags=('collared',)).summon('cat'),
                                  room.label(r(-1, 2, 0), 'Cat Collar', SOUTH))
    room.loop('cat', main_clock).loop(
        lambda step: execute().as_(e().tag('cat')).run(
            data().merge(s(), {'variant': step.elem.id, 'CustomName': step.elem.name})),
        (Entity(x, name=to_name(x)) for x in
         ('tabby', 'black', 'red', 'siamese', 'british_shorthair', 'calico', 'persian', 'ragdoll', 'white', 'jellie',
          'all_black')))
    room.function('colored_mobs_init').add(room.label(r(0, 2, -1), 'Glow', NORTH))

    def colored_mobs_loop(step):
        yield execute().as_(e().tag('colorable')).run(
            data().merge(s(), {'Color': step.i, 'CustomName': step.elem.name}))
        yield execute().as_(e().tag('collared')).run(data().merge(s(), {'CollarColor': step.i}))

    room.loop('colored_mobs', main_clock).loop(colored_mobs_loop, colors)

    def mooshroom_loop(step):
        step.elem.name = 'Brown Mooshroom' if 'Type' in step.elem.nbt else 'Red Mooshroom'
        yield placer(*mid_east_placer, tags=('mooshroom',)).summon(step.elem)

    room.loop('mooshroom', main_clock).add(kill_em(e().tag('mooshroom'))).loop(mooshroom_loop, (
        Entity('mooshroom'), Entity('mooshroom', {'Type': 'brown'})))

    climate_mobs = ('frog', 'chicken', 'pig', 'cow')
    climates = ('temperate', 'warm', 'cold')

    def climate_loop(step):
        for mob in climate_mobs:
            name = titlecase(f'{step.elem} {mob}')
            yield execute().as_(e().tag('climate_mob').type(mob)).run(
                data().merge(s(), {'variant': step.elem, 'CustomName': name}))
        execute().as_(e().tag('chicken')).run(data().merge(s(), {'EggLayTime': 1000000000}))

    p = placer(*mid_west_placer, tags=('climate_mob',))
    room.function('climate_init').add(
        p.summon(Entity(x, {'variant': 'temperate'}) for x in climate_mobs),
        kill(e().tag('frog', 'kid')),
        execute().as_(e().tag('chicken')).run(data().merge(s(), {'EggLayTime': 1000000000, 'OnGround': True})),
        room.label(r(-3, 2, 1), 'Flying', WEST),
        room.label(r(-3, 2, 5), 'Saddle', WEST),
    )
    room.loop('climate', main_clock).loop(climate_loop, climates)

    fox_postures = ('Crouching', 'Sitting', 'Sleeping')

    def fox_loop(step):
        nbt = {}
        for p in fox_postures:
            nbt[p] = step.elem == p
        yield execute().as_(e().tag('fox')).run(data().merge(s(), nbt))

    room.loop('fox', main_clock).loop(fox_loop, (('',) + fox_postures))
    room.function('fox_init').add(placer(*mid_east_placer).summon('fox'), room.label(r(2, 2, -1), 'Fox Type', EAST))
    spawn_pos = r(-1, 2, 0)

    def frogspawn_loop(step):
        if step.i == 0:
            yield kill_em(e().tag('tadpole', room.name))
            # The 'air' check is for if we're levitated
            label_pos = list(spawn_pos)
            label_pos[0] -= 0.25
            yield execute().unless().block(r(0, 1, 0), 'air').at(e().tag('frogspawn_home')).run(
                setblock(spawn_pos, 'frogspawn'),
                room.label(label_pos, 'Frogspawn', WEST, tags=('frogspawn_label',)))
        else:
            yield placer(spawn_pos, WEST, kids=True).summon(Entity('tadpole', {'Invulnerable': True}),
                                                            tags=('keeper',))
            yield setblock(spawn_pos, 'air')
            yield kill(e().tag('frogspawn_label'))
        yield kill_em(e().type('tadpole').not_tag('keeper'))

    room.loop('frogspawn', main_clock).loop(frogspawn_loop, range(0, 2))
    room.function('goat_init').add(placer(*south_placer).summon('goat'))
    room.loop('goat', main_clock).loop(
        lambda step: execute().as_(e().tag('goat').tag('adult')).run(
            data().merge(s(), {'HasLeftHorn': step.i & 1, 'HasRightHorn': step.i & 2})), range(0, 4))

    p = placer(r(-1.2, 2, 0), EAST, -2, kid_delta=2.2, tags=('saddle',), nbt={'Tame': True})
    room.function('horse_init').add(
        (p.summon(Entity('horse', name=horse.name, nbt={'Variant': h}), tags=(horse.tag_name,)) for h, horse in
         enumerate(horses)), execute().at(e().tag(to_id(horses[3].tag_name), 'kid')).run(
            WallSign((None, 'Variant:')).place(r(2, 0, 0), EAST)),
        room.label(r(1, 2, 1), 'Lead', EAST),
        room.label(r(1, 2, -3), 'Riders', EAST),
        room.label(r(1, 2, -7), 'Saddles', EAST),
    )
    horse_variants = ('None', 'White', 'White Field', 'White Dots', 'Black Dots')

    def horse_loop(step):
        for h, horse in enumerate(horses):
            yield execute().as_(e().tag(horse.tag_name)).run(data().merge(s(), {'Variant': step.i * 256 + h}))
        yield execute().at(e().tag(horses[3].tag_name).tag('kid')).run(
            Sign.change(r(2, 0, 0), (None, None, horse_variants[step.i])))

    room.loop('horse', main_clock).loop(horse_loop, horse_variants)

    p = placer(r(-1.2, 2, 0), EAST, -2, kid_delta=2.2, tags=('saddle', 'chests'), nbt={'Tame': True})
    room.function('horselike_init').add(p.summon('mule'), p.summon('donkey'), room.label(r(1, 2, -1), 'Chests', EAST))
    room.function('iron_golem_init').add(
        placer(r(-0.5, 2, 0), WEST, adults=True).summon('iron_golem'),
        WallSign((None, 'Iron Golem')).place(r(-3, 2, 0), WEST))

    def iron_golem_loop(step):
        i = step.i
        yield execute().as_(e().tag('iron_golem')).run(data().merge(s(), {'Health': step.elem * 25 - 5}))
        yield Sign.change(r(-3, 2, 0), (None, None, f'Damage: {i if i < 4 else 3 - (i - 3)}'))

    room.loop('iron_golem', main_clock).loop(iron_golem_loop, range(4, 0, -1), bounce=True)

    def copper_golem_loop(step):
        yield data().modify(n().tag('copper_golem'), 'weather_state').set().value(weathering_property(step.elem))
        # The 'air' check is for if we're levitated
        yield execute().unless().block(r(0, 1, 0), 'air').at(e().tag('copper_golem_home')).run(
            setblock(r(2, 2, 0), (weathering_id(step.elem, 'cut_copper_stairs'), {'facing': EAST})))
        yield Sign.change(r(-3, 2, 0), (None, weathering_name(step.elem, base='')))

    # -2 means waxed. We can't show waxed vs. unwaxed, so this cheaply makes sure the weathering never changes. If
    # we someday can show waxed vs. unwaxed, we need a different technique.
    room.function('copper_golem_init').add(
        placer(r(-0.5, 2, 0), WEST, adults=True).summon(Entity('copper_golem', {'next_weather_age': -2})),
        WallSign((None, None, 'Copper Golem')).place(r(-3, 2, 0), WEST),
        room.label(r(-2, 2, -1), 'Flower', WEST))
    room.loop('copper_golem', main_clock).loop(copper_golem_loop, weatherings)
    clean_lead = room.function('clean_lead', home=False).add(
        kill(e().type('item').nbt({'Item': {'id': 'minecraft:lead'}})))
    room.function('lead_off', home=False).add(
        kill(e().type('leash_knot')),
        schedule().function(clean_lead, 1, REPLACE)
    )
    room.function('lead_on', home=False).add(execute().as_(e().tag('white_horses').tag('!kid')).run(
        data().merge(s(), {'leash': Nbt.TypedArray('I', (-12, 101, 35))})))
    room.loop('llamas_carpets', main_clock).loop(
        lambda step: execute().as_(e().tag('llama').tag('!kid')).run(
            data().merge(s(), {'equipment': {'body': {'id': step.elem.id + '_carpet', 'Count': 1}}})), colors)
    second_riders = room.function('second_riders_on', home=False).add(
        room.riders_on(e().tag('camel', 'adult')))
    room.function('riders_on', home=False).add(
        room.riders_on(e().tag('saddle', 'adult')),
        # Gets confused if this is done right away
        schedule().function(second_riders, 1, REPLACE)
    )
    room.function('riders_off', home=False).add(room.riders_off())

    room.function('llamas_init').add(
        placer(r(0, 2, 0), WEST, 0, 2).summon('llama', nbt={'Tame': True}),
        tag(n().tag('llama', 'adult')).add('saddle'),
        placer(r(1, 3.5, -1), WEST, adults=True,
               nbt={'Tags': ['mobs', 'llama', 'llama_spit'], 'TXD': 0, 'TYD': 0, 'TZD': 0, 'Steps': 0,
                    'Motion': [0, 0, 0], 'NoGravity': True}).summon('llama_spit'),
        WallSign((None, 'Llama Spit')).place(r(1, 2, -1), WEST),
        room.label(r(-2, 2, 1), 'Carpet', WEST), room.label(r(-2, 2, -1), 'Chest', WEST))

    room.loop('llamas', main_clock).loop(
        lambda step: execute().as_(e().tag('llama')).run(
            data().merge(s(), {'Variant': step.i, 'CustomName': step.elem})), ('Creamy', 'White', 'Brown', 'Gray'))
    room.function('ocelot_init').add(placer(*south_placer).summon('ocelot'))
    room.function('outlines_on').add(
        (execute().as_(e().tag(rm).tag('!homer').type('!item_frame')).run(
            data().merge(s(), {'Glowing': True})) for rm in ('mobs', 'wither', 'nether', 'enders')))
    room.function('panda_init').add(placer(*south_placer).summon('panda'))
    room.loop('panda', main_clock).loop(
        lambda step: execute().as_(e().tag('panda')).run(data().merge(s(), {'CustomName': f'{step.elem} Panda',
                                                                            'MainGene': step.elem.lower(),
                                                                            'HiddenGene': step.elem.lower()})),
        ('Aggressive', 'Lazy', 'Weak', 'Worried', 'Playful', 'Normal', 'Brown'))
    parrot_dir, parrot_pos = WEST, r(0, 3, 0)
    disc_chest_pos = r(1, 1, 1)
    parrot_fence_pos = list(parrot_pos)
    parrot_fence_pos[1] -= 1
    parrot_enter = room.function('parrot_enter').add(
        (item().replace().block(disc_chest_pos, f'container.{i:d}').with_(discs[as_disc(d)].value) for i, d in
         enumerate(DISC_GROUP)))
    room.function('parrot_init').add(
        placer(parrot_pos, parrot_dir, adults=True).summon('parrot'),
        function(parrot_enter),
        room.label(r(0, 2, -1), 'Dance', WEST)
    )

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
            setblock(parrot_fence_pos, 'air' if flying else 'iron_bars'))

    room.loop('parrot', main_clock).loop(parrot_loop, parrot_settings)

    room.function('polar_bear_init').add(placer(*south_placer).summon('Polar Bear'))
    room.function('rabbit_init').add(placer(*mid_east_placer).summon('rabbit'))

    def rabbit_loop(step):
        i = 99 if step.elem.startswith('Killer') else step.i
        yield execute().as_(e().tag('rabbit')).run(data().merge(s(), {'RabbitType': i, 'CustomName': step.elem}))

    room.loop('rabbit', main_clock).loop(rabbit_loop, (
        'Brown', 'White', 'Black', 'Black & White', 'Gold', 'Salt & Pepper', 'Killer Rabbit (unused)', 'Toast'))
    room.function('reset_collars').add(
        kill_em(e().tag('cat')),
        execute().at(e().tag('cat_home')).run(function('restworld:mobs/cat_init')),
        execute().at(e().tag('cat_home')).run(function('restworld:mobs/cat_cur')))
    room.function('sheep_init').add(
        placer(*mid_east_placer, tags='keeper').summon(Entity('sheep'), tags=('sheared', 'colorable',)),
        room.label(r(2, 2, 1), 'Shear Sheep', EAST))

    # The poses are really not working well. There are s few bugs, and there isn't much to see as
    # things stand. We keep the skins_pose code in case this changes sometime. Need to remove
    # 'hide_description' below for it to work.
    slim_skin = room.score('slim_skin')
    skin_mode = room.score('skin_mode')
    mannequin = n().tag('mannequin')

    def skins_who_loop(step):
        name = to_name(step.elem)
        wide_nbt = Nbt({'profile': {'texture': f'entity/player/wide/{step.elem}', 'model': 'wide'},
                        'CustomName': f'{name} (Wide)', 'NoGravity': True})
        slim_nbt = wide_nbt.clone()
        slim_nbt['profile']['texture'] = slim_nbt['profile']['texture'].replace('wide', 'slim')
        slim_nbt['profile']['model'] = 'slim'
        slim_nbt['CustomName'] = slim_nbt['CustomName'].replace('Wide', 'Slim')
        yield execute().if_().score(slim_skin).matches(0).run(data().merge(mannequin, wide_nbt))
        yield execute().unless().score(slim_skin).matches(0).run(data().merge(mannequin, slim_nbt))

    skins_who_loop = room.loop('skins_who', home=False).add(
        data().remove(n().tag('mannequin'), 'profile.model')).loop(skins_who_loop, default_skins)

    skins_pose_loop = room.loop('skins_pose', home=False).loop(
        lambda step: data().merge(mannequin, {'pose': step.elem, 'description': titlecase(step.elem)}),
        mannequin_poses)

    room.loop('skins', main_clock).add(
        execute().if_().score(skin_mode).matches(0).run(function(skins_who_loop)),
        execute().unless().score(skin_mode).matches(0).run(function(skins_pose_loop))
    )

    room.function('skins_init').add(
        slim_skin.set(0),
        skin_mode.set(0),
        placer(*south_placer, adults=True).summon(
            Entity('Mannequin', {'hide_description': True,
                                 'immovable': True, 'description': 'Standing', 'NoGravity': True,
                                 'profile': {'texture': f'entity/player/wide/{default_skins[0]}'}})),
        WallSign((None, 'Default Player', 'Textures')).place(r(0, 2, 1), NORTH),
        room.label(r(-1, 2, 0), 'Slim', SOUTH))

    room.function('sniffer_init').add(
        placer(r(0, 2, 0.5), EAST, 0, adults=True, tags='keeper').summon('sniffer'),
        WallSign((None, 'Sniffer Egg', None, '(vanilla  shows 3)')).place(r(2, 2, 3), EAST),
        room.label(r(3, 2, 0), 'Show Particles', EAST)
    )
    setblock(r(-1, 2, 2), 'Sniffer Egg'),

    egg_pos = r(0, 2, 3)

    def sniffer_egg_loop(step):
        block = Block('sniffer_egg', {'hatch': step.i})
        yield setblock(egg_pos, block)
        yield Sign.change(r(2, 2, 3), (None, None, f'Hatch: {step.i} of 3'))
        room.particle(block, 'sniffer', r(0, 3, 3), step)

    room.loop('sniffer', main_clock).loop(sniffer_egg_loop, range(3))
    # See https://bugs.mojang.com/browse/MC-261250 -- eventually the egg will hatch even without randomTicks, so...
    room.function('sniffer_egg_reset').add(clone(egg_pos, egg_pos, egg_pos).replace(FORCE))
    room.function('sniffer_kid_init').add(placer(r(-0.5, 2, 0), EAST, 0, kids=True, tags='keeper').summon('sniffer'))
    room.function('snow_golem_init').add(placer(r(-0.5, 2, 0), WEST, adults=True).summon('snow_golem'))
    room.loop('snow_golem', main_clock).loop(
        lambda step: execute().as_(e().tag('snow_golem')).run(data().merge(s(), {'Pumpkin': step.elem})), (True, False))
    room.function('switch_carpets_on', home=False).add(
        execute().at(e().tag('llamas_home')).positioned(r(-2, -0.5, 0)).run(
            function('restworld:mobs/llamas_carpets_home')),
        execute().at(e().tag('llamas_carpets_home')).run(function('restworld:mobs/llamas_carpets_cur')))
    room.function('switch_carpets_off', home=False).add(
        execute().as_(e().tag('llama')).run(data().remove(s(), 'equipment.body')),
        kill(e().tag('llamas_carpets_home')))

    room.function('trader_llama_init').add(placer(r(1, 2, -1), WEST, adults=True).summon('wandering_trader'),
                                           placer(r(0, 2, 1), WEST, 0, 2,
                                                  nbt={'DespawnDelay': 2147483647, 'Leashed': True}).summon(
                                               'trader_llama'))
    room.loop('trader_llama', main_clock).loop(
        lambda step: execute().as_(e().type('trader_llama')).run(data().modify(s(), 'Variant').set().value(step.i)),
        ('Creamy', 'White', 'Brown', 'Gray'))
    switch_label_pos = r(3, 2, 0)
    egg_sign_pos = r(-2, 2, 0, )
    egg_sign_dir = EAST
    room.function('turtle_eggs_init').add(
        tag(e().tag('turtle_eggs_home')).add('blockers_home'),
        WallSign((None, 'Turtle Eggs')).place(egg_sign_pos, egg_sign_dir),
        room.label(switch_label_pos, 'Egg Crack', EAST))

    def turtle_egg_loop(step):
        for count in range(4, 0, -1):
            eggs = ('turtle_egg', {'eggs': count, 'hatch': step.elem})
            yield setblock(r(3 - count, 2, 0), eggs)
            room.particle(eggs, 'turtle_eggs', r(count - 2, 2.5, 0), step)
        yield Sign.change(egg_sign_pos, (None, None, f'Hatch Age: {step.elem:d}'))

    room.loop('turtle_eggs', main_clock).loop(turtle_egg_loop, range(0, 3), bounce=True)
    turtle_dir = EAST
    room.function('turtle_init').add(placer(r(0, 2, 0), turtle_dir, 2, 2).summon('turtle'))

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
        kind = titlecase(kind)
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
            # Removing sexist language because I want to.
            name = 'Fisher' if pro == 'Fisherman' else pro
            professions_init.add(
                p.summon(Villager(pro, PLAINS, name=to_name(name), zombie=id[0] == 'z'), tags=('villager',)))
        professions_init.add(function(f'restworld:mobs/{which}_levels_cur'),
                             function(f'restworld:mobs/{which}_professions_cur'),
                             Sign.change(r(-5, 2, 0), (None, None, kind)))

    professions_init_funcs('villager')

    def villager_professions_loop(step):
        yield execute().as_(e().tag('villager')).run(
            data().modify(s(), 'VillagerData.type').set().value(step.elem.lower()))
        yield Sign.change(r(-5, 2, 0), (None, titlecase(step.elem)))

    room.loop('villager_professions', main_clock).loop(villager_professions_loop, VILLAGER_BIOMES)

    def types_init_funcs(which):
        id, kind = kind_names(which)
        p = placer(r(-2, 2, -2), WEST, -2, tags=('villager', 'types',), adults=True)
        types_init = room.function(f'{which}_types_init').add(kill(e().tag('villager')))
        for i, ty in enumerate(VILLAGER_BIOMES):
            if i == 3:
                p = placer(r(0, 2, -3), WEST, -2, tags=('villager', 'types',), adults=True)
            types_init.add(p.summon(Entity(id, name=to_name(ty), nbt={'VillagerData': {'type': ty.lower()}})))
        types_init.add(function(f'restworld:mobs/{which}_levels_cur'), function(f'restworld:mobs/{which}_types_cur'),
                       Sign.change(r(-5, 2, 0), (None, None, kind)))

    types_init_funcs('villager')

    def villager_types_loop(step):
        if step.elem == 'Child':
            # Skip over child for zombies, there are no zombie children
            yield execute().as_(e().tag('zombie_villager').limit(1)).run(villager_types_cur.set(0))
        yield execute().as_(e().tag('villager')).run(
            data().modify(s(), 'VillagerData.profession').set().value(step.elem.lower()))
        yield execute().as_(e().tag('villager')).run(
            data().modify(s(), 'Age').set().value(-2147483648 if step.elem == 'Child' else 0))
        yield Sign.change(r(-5, 2, 0), (None, titlecase(step.elem)))

    roles = VILLAGER_PROFESSIONS + ('Child',)
    room.loop('villager_types', main_clock).loop(villager_types_loop, roles).add(
        execute().as_(e().tag('villager')).run(execute().at(s()).as_(s()).align('xyz').run(tp(
            s(), r(0.5, 0.0, 0.5)))))

    professions_init_funcs('zombie')
    room.loop('zombie_professions', main_clock).loop(None, list()).add(
        function('restworld:mobs/villager_professions_main'))
    types_init_funcs('zombie')
    room.loop('zombie_types', main_clock).loop(None, list()).add(function('restworld:mobs/villager_types_main'))

    room.function('which_villagers_init').add(
        bool_max.set(2),
        cur_villagers_group.set(0),
        cur_villagers_zombies.set(0),
        function('restworld:mobs/switch_villagers'),
        WallSign((None, None, 'Villagers')).place(r(-5, 2, 1), WEST),
        room.label(r(-3, 2, 0), 'Profession', WEST),
        room.label(r(-3, 2, 2), 'Level', WEST),
        room.label(r(-3, 2, 4), 'Zombies', WEST))

    # Switch functions
    room.function('switch_villagers', home=False).add(
        which_villagers.set(0),
        execute().if_().score(cur_villagers_group).matches(1).run(which_villagers.add(1)),
        execute().if_().score(cur_villagers_zombies).matches(1).run(which_villagers.add(2)),
        which_villagers_needed.operation(EQ, which_villagers),
        execute().unless().score(which_villagers_needed).is_(EQ, which_villagers_needed_prev).run(
            (
                kill_em(e().tag('villager')),
                init_villagers(0, 'villager_professions'),
                init_villagers(1, 'villager_types'),
                init_villagers(2, 'zombie_professions'),
                init_villagers(3, 'zombie_types'),
                # If zombies are on, turn off level. Setting the lever off does not cause the piston to move, hence the
                # redstone block work.
                execute().if_().score(cur_villagers_zombies).matches(1).at(
                    e().tag('which_villagers_home')).run(
                    setblock(r(-3, 2, 2),
                             Block('lever', state=dict(face='floor', facing='east'))),
                    setblock(r(-3, -1, 2), 'redstone_block'),
                    setblock(r(-3, -1, 2), 'air'),
                ),
            )), which_villagers_needed_prev.operation(EQ, which_villagers_needed),
        execute().if_().score(cur_villagers_levels).matches(1).run(which_villagers.add(4)),
        kill(e().tag('cur_villagers_home')),
        home_villagers(0, 'villager_professions'),
        home_villagers(1, 'villager_types'), home_villagers(2, 'zombie_professions'),
        home_villagers(3, 'zombie_types'),
        home_villagers((4, None), 'villager_levels'))
    room.function('switch_villagers_init', home=False).add(
        which_villagers_prev.set(1),
        function('restworld:mobs/switch_villagers'))
    room.function('toggle_villager_group', home=False).add(
        cur_villagers_group.add(1), cur_villagers_group.operation(MOD, bool_max),
        function('restworld:mobs/switch_villagers'))
    room.function('toggle_villager_levels', home=False).add(
        cur_villagers_levels.add(1),
        cur_villagers_levels.operation(MOD, bool_max),
        execute().if_().score(cur_villagers_levels).matches(1).run(cur_villagers_zombies.set(0)),
        function('restworld:mobs/switch_villagers'))
    room.function('toggle_villager_zombies', home=False).add(
        cur_villagers_zombies.add(1),
        cur_villagers_zombies.operation(MOD, bool_max),
        execute().if_().score(cur_villagers_zombies).matches(1).run(cur_villagers_levels.set(0)),
        function('restworld:mobs/switch_villagers'))

    def villager_level_loop(step):
        yield execute().as_(e().tag('villager')).run(data().modify(s(), 'VillagerData.level').set().value(step.i + 1))
        yield Sign.change(r(-5, 2, 0), (None, f' {step.elem} Level'))

    room.loop('villager_levels', main_clock).loop(villager_level_loop, ('Stone', 'Iron', 'Gold', 'Emerald', 'Diamond'))


def monsters(room):
    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    east_placer = list(r(-0.2, 2, 0)), EAST, 2, 2.2
    west_placer = list(r(0.2, 2, 0)), WEST, -2, 2.2
    south_placer = list(r(0, 2, -0.2)), SOUTH, -2, 2.2

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

    # Later code assumes Evoker comes first
    illagers = (Entity('Evoker'), Entity('Vindicator'), Entity('Pillager'),
                Entity('Pillager', nbt={'equipment': {'mainhand': Item.nbt_for('crossbow')}}),
                Entity('illusioner', name='Illusioner (unused)'))
    tags = ('illager',)

    illager_dir = SOUTH
    fangs = room.function('fangs', home=False)
    illager_loop_func = room.loop('illager', main_clock)

    def illager_loop(step):
        place = list(copy.deepcopy(west_placer))
        place[0][2] -= 0.5
        place[0][0] += 0.5
        place[1] = illager_dir
        yield placer(*place, adults=True, tags=tags).summon(step.elem)
        if step.elem.id == 'evoker':
            yield placer(r(1.5, 3.5, -1.5), illager_dir, adults=True, tags=tags).summon(
                Entity('vex', nbt={'equipment': {'mainhand': Item.nbt_for('iron_sword')}, 'LifeTicks': 2147483647}))
            fangs.add(
                execute().unless().score(illager_loop_func.score).matches(0).run(return_()),
                execute().at(e().tag('illager_home')).run(
                    placer(r(-1 + 2.5 * 1, 2, 1), illager_dir, adults=True, tags=tags).summon(
                        Entity('Evoker Fangs', nbt={'Warmup': 0}))),
                schedule().function(fangs, 25, REPLACE)),
            yield function(fangs)

    illager_loop_func.add(kill_em(e().tag(*tags))).loop(illager_loop, illagers)

    room.function('phantom_init').add(placer(r(-0.2, 4, 0), NORTH, adults=True).summon('phantom'))

    def ravager_loop(step):
        ravager = Entity('ravager')
        if step.elem is not None:
            ravager.passenger(Entity(step.elem, {'Rotation': as_facing(WEST).rotation}).merge_nbt(MobPlacer.base_nbt))
        yield placer(r(1, 2, 0), WEST, adults=True).summon(ravager)

    room.loop('ravager', main_clock).add(kill_em(e().tag('ravager'))).loop(
        ravager_loop, (None, 'Pillager', 'Vindicator', 'Evoker'))

    silverfish_dir = method_name()
    room.function('silverfish_init').add(placer(r(0, 2, 0), silverfish_dir, adults=True).summon('silverfish'))

    place = list(copy.deepcopy(east_placer))
    place[0][2] += 0.5

    # noinspection SpellCheckingInspection
    ench_helmet = {'id': 'iron_helmet', 'components': {'repair_cost': 1, 'enchantments': {'unbreaking': 3}}}

    def skeleton_horse_loop(step):
        if step.i == 1:
            bow = {'id': 'bow', 'components': {'repair_cost': 1, 'enchantments': {'unbreaking': 3}}}
            skel = Entity('Skeleton', nbt={'equipment': {'head': ench_helmet, 'mainhand': bow}})
            yield from room.riders_on(n().tag('skeleton_horse'), 'skeleton_horse_rider', rider=skel)
        else:
            yield from room.riders_off('skeleton_horse_rider')

    room.function('skeleton_horse_init').add(placer(*place).summon(Entity('Skeleton Horse').tag('monster_saddle')))
    room.loop('skeleton_horse', main_clock).loop(skeleton_horse_loop, range(0, 2))

    helmet = Item.nbt_for('iron_helmet')

    def zombie_horse_loop(step):
        if step.i == 1:
            zombie = Entity('Zombie', nbt={'equipment': {'head': helmet, 'mainhand': {'id': 'iron_spear'}}})
            yield from room.riders_on(n().tag('zombie_horse'), 'zombie_horse_rider', rider=zombie)
        else:
            yield from room.riders_off('zombie_horse_rider')

    room.function('zombie_horse_init').add(
        placer(r(0.7, 2, 0.5), NORTH, kid_delta=2).summon(
            Entity('zombie_horse', name='Zombie Horse').tag('monster_saddle')),
        room.label(r(0, 2, -2), 'Saddles', NORTH)
    )
    room.loop('zombie_horse', main_clock).loop(zombie_horse_loop, range(0, 2))

    bow = Item.nbt_for('bow')
    spear = Item.nbt_for('iron_spear')
    spider_rider = Entity('Skeleton', nbt={'equipment': {'head': helmet, 'mainhand': bow}}).merge_nbt(
        MobPlacer.base_nbt)

    armorable_tag = 'armorable'
    room.loop('skeleton', main_clock).add(kill_em(e().tag('skeletal'))).loop(
        lambda step: placer(*east_placer, adults=True).summon(
            Entity(step.elem, nbt={'equipment': {'mainhand': bow}}).tag('skeletal', armorable_tag)),
        ('Skeleton', 'Stray', 'Bogged', 'Parched'))
    room.function('skeleton_init').add(room.label(r(2, 2, 0), 'Armor', EAST))

    chr2 = room.function('camel_husk_rider2', home=False).add(
        room.riders_on(n().tag('camel_husk'),
                       rider=Entity('parched', {'NoAI': True, 'equipment': {'mainhand': bow}}).tag('husk_rider')))

    def camel_husk_loop(step):
        if step.elem:
            yield room.riders_on(n().tag('camel_husk'), tags='husk_rider',
                                 rider=Entity('husk', {'NoAI': True, 'equipment': {'mainhand': spear}}))
            yield schedule().function(chr2, 1, REPLACE)
        else:
            yield room.riders_off('husk_rider')

    room.function('camel_husk_init').add(
        placer(r(0, 2, 0), NE, adults=True).summon(Entity('camel_husk').tag('monster_saddle')))
    room.loop('camel_husk', main_clock).loop(camel_husk_loop, (True, False))

    def spider_loop(step):
        if step.i == 1:
            yield room.riders_on(e().tag('spiders'), 'spider_riders', rider=spider_rider)
        else:
            yield room.riders_off('spider_riders')

    room.loop('spiders', main_clock).loop(spider_loop, range(0, 2))
    spider_placer = placer(r(-0.75, 2.5, -0.2), NORTH, -3, nbt={'Tags': ['spiders']}, adults=True)
    room.function('spiders_init').add(
        spider_placer.summon('Spider'),
        spider_placer.summon('Cave Spider')
    )
    place = list(copy.deepcopy(south_placer))
    place[0][0] += 0.5
    place[0][2] -= 0.3
    room.function('witch_init').add(placer(*place, adults=True).summon('witch'))

    def armorable_loop(step):
        if step.i == 0:
            cmd = data().remove(s(), 'equipment')
        else:
            cmd = data().merge(s(),
                               {'equipment': {'feet': Item.nbt_for('iron_boots'), 'legs': Item.nbt_for('iron_leggings'),
                                              'chest': Item.nbt_for('iron_chestplate'),
                                              'head': Item.nbt_for('iron_helmet')}})
        yield execute().as_(e().tag(armorable_tag)).run(cmd)

    room.loop('mob_armor').loop(armorable_loop, range(2))

    zombie_jockey_chicken_tag = 'zombie_jockey_chicken'
    zombie_jockey_chicken = e().tag('zombie_jockey_chicken').limit(1)

    zombie_kid = e().tag('zombieish', 'kid')

    def zombie_jockey_loop(step):
        if step.i == 0:
            yield ride(zombie_kid.limit(1)).dismount()
            yield kill_em(zombie_jockey_chicken)
            yield tp(zombie_kid, r(2, 2, 0))
        else:
            place = list(copy.deepcopy(east_placer))
            place[0][0] += 2
            p = placer(*place, adults=True)
            yield p.summon(Entity('chicken').tag(zombie_jockey_chicken_tag, 'zombieish'))
            yield ride(zombie_kid.limit(1)).mount(zombie_jockey_chicken)

    room.loop('zombie_jockey', home=False).loop(zombie_jockey_loop, range(2))
    room.function('zombie_init').add(room.label(r(2, 2, 1), 'Jockey', EAST))

    def zombie_loop(step):
        yield kill_em(e().tag('zombieish'))
        yield kill(e().tag('zombieish'))
        p = placer(r(0.2, 2, 0), EAST, 0, 1.8, tags=('zombieish',))
        yield p.summon(Entity(step.elem))
        hand_item = {'Drowned': 'trident', 'Husk': 'iron_sword', 'Zombie': 'iron_shovel'}[step.elem]
        yield execute().as_(e().tag('zombieish').tag('adult')).run(
            tag(s()).add(armorable_tag),
            data().merge(s(),
                         {'LeftHanded': step.elem == 'Zombie', 'equipment': {'mainhand': Item.nbt_for(hand_item)}}))

    room.loop('zombie', main_clock).add(kill_em(e().tag('zombieish'))).loop(
        zombie_loop, ('Zombie', 'Husk', 'Drowned')).add(function('restworld:mobs/mob_armor_cur'),
                                                        function('restworld:mobs/zombie_jockey_cur'))

    def enderman_loop(step):
        placer = room.mob_placer(r(0, 2, 0), NORTH, adults=True)
        if step.elem:
            yield data().modify(n().tag('enderman'), 'angry_at').set().from_(n().tag('enderman'), 'UUID')
            yield data().modify(n().tag('enderman'), 'CustomName').set().value('Angry Enderman')
        else:
            yield kill_em(e().tag('enderman'))
            yield list(placer.summon('enderman'))[0]

    placer = room.mob_placer(r(0, 2, 0), NORTH, adults=True)
    room.function('enderman_init').add(
        execute().unless().entity(e().type('enderman').distance((None, 5))).run(list(placer.summon('enderman'))[0]))
    room.loop('enderman', main_clock).loop(enderman_loop, (True, False))

    placer = room.mob_placer(r(0, 3, 0.2), NORTH, adults=True)
    room.function('breeze_init').add(placer.summon('breeze'))

    placer = room.mob_placer(r(0, 2, 0.2), NORTH, adults=True)
    room.function('endermite_init').add(placer.summon('endermite'))

    room.function('warden_init').add((room.mob_placer(r(0, 2, -0.5), WEST, adults=True).summon('warden'),))
    room.function('creaking_init').add((room.mob_placer(r(0, 2, -0.5), EAST, adults=True).summon('creaking'),))


def method_name():
    silverfish_dir = NORTH
    return silverfish_dir


def aquatic(room):
    def fish_water_loop(step):
        yield fillbiome(r(0, 1, 0), r(12, 10, 16), step.elem)
        yield Sign.change(r(6, 2, 1), (None, None, to_name(step.elem)))

    room.function('fish_water_base')
    room.function('fish_water_base_init').add(
        room.label(r(6, 2, -1), 'Water Biomes', NORTH),
        WallSign((None, 'Water Biome:', 'Plains')).glowing(True).place(r(6, 2, 1), SOUTH, water=True)
    )
    room.loop('fish_water', main_clock, home=False).loop(fish_water_loop, water_biomes)

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
    t_fish.add(WallSign().messages(('Naturally', 'Occurring', u'Tropical Fish', u'→ → →')).glowing(True).place(
        r(1, 2, (len(tropical_fish) - 1) % 4), EAST, water=True))

    axolotl_placer = room.mob_placer(r(-0.4, 3, 0), WEST, None, 1.8)
    room.function('axolotl_init').add(axolotl_placer.summon('axolotl'), execute().at(e().tag('axolotl_dry_home')).run(
        room.mob_placer(r(0, 3, 0), EAST, kid_delta=2).summon('axolotl')))
    room.function('axolotl_dry')
    room.loop('axolotl', main_clock).loop(
        lambda step: execute().as_(e().tag('axolotl')).run(data().merge(
            s(), {'Variant': step.i, 'CustomName': step.elem + ' Axolotl'})), axolotls)
    room.function('guardian_init').add(room.mob_placer(r(-1, 3, 0.7), WEST, adults=True).summon('guardian'))
    room.function('elder_guardian_init').add(room.mob_placer(r(-0.7, 3, 1), WEST, adults=True).summon('elder_guardian'))

    room.function('nautilus_mob_enter').add(execute().as_(e().tag('saddleable_nautilus')).run(
        data().modify(s(), 'Owner').set().from_(p(), 'UUID')))
    nr_on = room.function('nautilus_riders_on', home=False).add(
        room.riders_on(n().tag('zombie_nautilus'), tags='nautilus_rider',
                       rider=Entity('Drowned', {'equipment': {'mainhand': Item.nbt_for('trident')}})),
        room.riders_on(n().tag('nautilus', 'adult'), tags='nautilus_rider'),
    )
    nr_off = room.function('nautilus_riders_off', home=False).add(room.riders_off('nautilus_rider'))
    ns_on = room.function('nautilus_saddles_on', home=False).add(
        execute().as_(e().tag('saddleable_nautilus')).run(item().replace().entity(s(), 'saddle').with_('saddle')))
    ns_off = room.function('nautilus_saddles_off', home=False).add(
        execute().as_(e().tag('saddleable_nautilus')).run(
            item().replace().entity(s(), 'saddle').with_('air')))
    nautilus_placer = room.mob_placer(r(0, 3, -0.5), SOUTH, delta=2, kid_delta=2.2, tags='saddleable_nautilus')

    def nautilus_loop(step):
        name = 'Coral Zombie Nautilus' if step.elem == 'warm' else 'Zombie Nautilus'
        yield data().merge(n().tag('zombie_nautilus'), {'CustomName': name, 'variant': step.elem}),

    nautilus_riders_score = room.score('nautilus_riders')
    nautilus_saddles_score = room.score('nautilus_saddles')
    room.function('nautilus_mob_init').add(
        nautilus_placer.summon('nautilus'),
        nautilus_placer.summon('zombie_nautilus', kids=False),
        WallSign((None, 'Nautilus Saddle', 'On / Off'), (
            execute().store(SUCCESS).score(nautilus_saddles_score).run(
                tag(e().tag('nautilus').nbt({'equipment': {'saddle': {'id': 'minecraft:saddle'}}})).list()),
            execute().if_().score(nautilus_saddles_score).matches(0).run(function(ns_on)),
            execute().unless().score(nautilus_saddles_score).matches(0).run(function(ns_off))
        )).glowing(True).place(r(-1, 2, 1), NORTH, True),
        WallSign((None, 'Riders', 'On / Off'), (
            execute().store(SUCCESS).score(nautilus_riders_score).run(tag(e().tag('nautilus_rider')).list()),
            execute().if_().score(nautilus_riders_score).matches(0).run(function(nr_on)),
            execute().unless().score(nautilus_riders_score).matches(0).run(function(nr_off))
        )).glowing(True).place(r(-2, 2, 1), NORTH, True),
    )
    room.loop('nautilus_mob', main_clock).loop(nautilus_loop, ('temperate', 'warm'))

    def squids_loop(step):
        placer = room.mob_placer(r(2.6, 4, 0.2), WEST, None, kid_delta=1.8, tags=('squidy',), nbt={'NoGravity': True})
        return placer.summon('squid' if step.i == 0 else 'glow_squid')

    room.loop('squid', main_clock).add(kill_em(e().tag('squidy'))).loop(squids_loop, range(0, 2))

    dolphin_placer = room.mob_placer(r(1.35, 3, 2.9), NORTH, kid_delta=2)
    fish_placer = room.mob_placer(r(0, 3, 1), NORTH, -1, adults=True)
    room.function('fishies_init').add(
        kill(e().tag('pufferfish')),
        dolphin_placer.summon(Entity('dolphin', nbt={'Invulnerable': True})),
        fish_placer.summon(
            ('salmon', 'cod', 'pufferfish',
             Entity('tadpole', nbt={'Invulnerable': True, 'Age': -2147483648}).tag('kid', 'keeper'))),
    )

    def fishies_loop(step):
        yield data().merge(e().tag('pufferfish').limit(1), {'PuffState': step.i})
        # Over time, the pufferfish and salmon creep downward, so we have to put them back
        fish_pos = r(-2, 3, 1)
        fish_facing = r(-2, 3, -5)
        yield tp(e().tag('pufferfish'), fish_pos).facing(fish_facing)
        fish_pos = (fish_pos[0] + r(2),) + fish_pos[1:]
        fish_facing = (fish_facing[0] + r(2),) + fish_facing[1:]
        # A bug in 1.21.4 has a salmon that is being teleported isn't killed by the _init function. I don't know why
        # or even how to report it. But I have to work around it. I teleport all the salmon to death but rescue one.
        yield kill_em(e().tag('salmon'))
        yield data().merge(n().tag('salmon'), {'type': step.elem})
        # noinspection PyTypeChecker
        yield tp(n().tag('salmon'), fish_pos).facing(fish_facing)

    room.loop('fishies', main_clock).loop(fishies_loop, ('small', 'medium', 'large'), bounce=True)


def all_fish_funcs(room):
    pattern = Score('pattern', 'fish')
    num_colors = Score('NUM_COLORS', 'fish')
    body_scale = Score('BODY_SCALE', 'fish')
    overlay_scale = Score('OVERLAY_SCALE', 'fish')
    pattern_size = Score('PATTERN_SIZE', 'fish')
    variant = Score('variant', 'fish')

    kinds = tuple(tropical_fish.keys())

    def all_fish_init():
        yield WallSign().messages((None, 'All Possible', 'Tropical Fish', '← ← ←')).glowing(True).place(r(0, 2, 0),
                                                                                                        EAST,
                                                                                                        water=True)
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
            scoreboard().objectives().add('fish', DUMMY),
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
