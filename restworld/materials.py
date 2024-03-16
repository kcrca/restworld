from __future__ import annotations

import re

from pynecraft import info
from pynecraft.base import Arg, EAST, EQ, NE, NORTH, NW, Nbt, NbtDef, SOUTH, WEST, as_facing, r, to_id
from pynecraft.commands import Block, BlockDef, Entity, LONG, MOD, PLUS, RESULT, as_block, data, e, execute, fill, \
    fillbiome, function, item, kill, random, s, scoreboard, setblock, summon, tag
from pynecraft.function import BLOCKS
from pynecraft.info import colors, stems, trim_materials, trim_patterns
from pynecraft.simpler import Item, ItemFrame, Region, SWAMP, Sign, WallSign
from pynecraft.values import COLD_OCEAN, FROZEN_OCEAN, LUKEWARM_OCEAN, MANGROVE_SWAMP, MEADOW, OCEAN, WARM_OCEAN, biomes
from restworld.rooms import Room, label
from restworld.world import fast_clock, kill_em, main_clock, restworld


def room():
    room = Room('materials', restworld, WEST, ('Materials', '& Tools,', 'Time, GUI,', 'Redstone, Maps'))
    room.reset_at((3, 0))

    room.function('all_sand_init').add(WallSign((None, None, 'and Sandstone')).place(r(0, 2, 3), WEST))

    blocks = []
    slabs = []
    stairs = []
    walls = []
    for thing in ('', 'Red '):
        ty = thing + 'Sand'
        subtypes = (
            '%sstone' % ty,
            'Smooth %sstone' % ty,
            'Cut %sstone' % ty)
        blocks.append((ty, 'Chiseled %sstone' % ty) + subtypes)
        slabs.append((None, None) + tuple('%s Slab' % b for b in subtypes))
        stairs.append((None, None) + tuple(('%s Stairs' % b if 'Cut' not in b else None) for b in subtypes))
        walls.append('%sstone Wall' % ty)
    assert len(blocks) == 2  # allows us to use 'replace previous type' because there are only two types

    volume = Region(r(0, 1, 0), r(10, 6, 7))

    def all_sand_loop(step):
        i = step.i
        o = 1 - i
        for j in range(0, len(blocks[i])):
            yield from volume.replace(walls[i], walls[o])
            yield from volume.replace(blocks[i][j], blocks[o][j])
            if slabs[i][j]:
                yield from volume.replace_slabs(slabs[i][j], slabs[o][j])
            if stairs[i][j]:
                # noinspection PyTypeChecker
                yield from volume.replace_stairs(stairs[i][j], stairs[o][j])
        yield Sign.change(r(0, 2, 3), (None, blocks[i][0]))

    room.loop('all_sand', main_clock).loop(all_sand_loop, range(0, 2))

    room.function('arrows_init').add(WallSign(()).place(r(1, 2, 0), EAST), label(r(0, 2, -1), 'Fire'))

    fire_arrow = room.score('fire_arrow')

    def arrows_loop(step):
        nbt = {'Tags': ['arrow'], 'NoGravity': True}
        yield summon(step.elem, r(0, 3, 0.25), nbt)
        if step.i == 2:
            # Choose a random color
            yield execute().store(RESULT).entity(e().tag('arrow').limit(1),
                                                 'item.components.minecraft:potion_contents.custom_color', LONG).run(
                random().value((0, 0xffffff)))
        yield execute().if_().score(fire_arrow).matches((1, None)).as_(e().tag('arrow')).run(
            data().modify(s(), 'HasVisualFire').set().value(True))
        yield Sign.change(r(1, 2, 0), (None, step.elem.name))

    room.loop('arrows', main_clock).add(
        kill(e().tag('arrow'))
    ).loop(arrows_loop, (
        Block('Arrow'),
        Block('Spectral Arrow'),
        Block('arrow', name='Tipped Arrow',
              nbt={'item': {'components': {'potion_contents': {'potion': 'poison'}}, 'id': 'tipped_arrow'},
                   'NoGravity': True})))
    room.function('arrow_fire', home=False).add(
        fire_arrow.set(Arg('on')), data().modify(e().tag('arrow').limit(1), 'HasVisualFire').set().value(Arg('on'))
    )

    points = (2, 6, 16, 36, 72, 148, 306, 616, 1236, 2476, 32767)

    def experience_orbs_loop(step):
        i = step.i
        p = points[i]
        f = -32768 if i == 0 else points[i - 1]
        yield summon('experience_orb', r(0, 3, 0), {'Value': p, 'Age': 6000 - 40})
        yield Sign.change(r(1, 2, 0), (None, None, f'Size {i + 1}', f'{f} - {p}'))

    room.loop('experience_orbs', fast_clock).loop(experience_orbs_loop, points)
    room.function('experience_orbs_init').add(WallSign((None, 'Experience Orb')).place(r(1, 2, 0), EAST))
    ingot_frame = 'ores_ingot_frame'
    frame = ItemFrame(SOUTH, nbt={'Tags': [room.name, ingot_frame]})
    room.function('ores_init').add(
        summon(frame, r(3, 3, 3)),
        summon(frame.merge_nbt({'Invisible': True}), r(4, 3, 3)),
        label(r(3, 2, 7), 'Deepslate'))

    raw_frame = 'ore_raw_frame'
    volume = Region(r(7, 5, 6), r(0, 2, 0))
    deepslate_materials = room.score('deepslate_materials')

    def ore_loop(step):
        ore, block, item, raw = (Block(x) if x else None for x in step.elem)
        yield from volume.replace(block.id, '#restworld:ore_blocks')
        yield Sign.change(r(3, 2, 6), (None, ore.name.replace(' Ore', '')))
        if 'Nether' in ore.name or 'Ancient' in ore.name:
            yield volume.replace(ore.id, '#restworld:ores')
            yield volume.replace('netherrack', '#restworld:ore_background')
            yield volume.replace('soul_sand', 'dirt')
            yield volume.replace('soul_soil', 'andesite')
            yield volume.replace('blackstone', 'diorite')
            yield volume.replace('basalt', 'granite')
        else:
            yield execute().if_().score(deepslate_materials).matches(0).run(
                volume.replace(ore.id, '#restworld:ores'))
            yield execute().if_().score(deepslate_materials).matches(0).run(
                volume.replace('stone', '#restworld:ore_background'))
            yield execute().if_().score(deepslate_materials).matches(1).run(
                volume.replace('deepslate_%s' % ore.id, '#restworld:ores'))
            yield execute().if_().score(deepslate_materials).matches(1).run(
                volume.replace('deepslate', '#restworld:ore_background'))
            yield volume.replace('dirt', 'soul_sand')
            yield volume.replace('andesite', 'soul_soil')
            yield volume.replace('diorite', 'blackstone')
            yield volume.replace('granite', 'basalt')

        if 'Netherite' in item.name:
            yield Sign.change(r(3, 2, 6), (None, None, '/ Netherite'))
        if raw:
            if 'Raw' in raw.name:
                yield setblock(r(3, 4, 2), '%s_block' % raw.id)
            yield summon(ItemFrame(SOUTH, nbt={'Tags': [raw_frame, room.name]}).named(raw.name),
                         r(3, 4, 3))
        else:
            yield kill(e().tag(raw_frame))
        yield execute().as_(e().tag(ingot_frame)).run(
            data().merge(s(), {'Item': Item.nbt_for(item.id)}))

    room.loop('ores', main_clock).add(
        kill(e().tag(raw_frame)),
        Sign.change(r(3, 2, 6), (None, None, '')),
        setblock(r(3, 4, 2), 'air')
    ).loop(ore_loop, (
        ('Coal Ore', 'Coal Block', 'Coal', None),
        ('Iron Ore', 'Iron Block', 'Iron Ingot', 'Raw Iron'),
        ('Copper Ore', 'Copper Block', 'Copper Ingot', 'Raw Copper'),
        ('Gold Ore', 'Gold Block', 'Gold Ingot', 'Raw Gold'),
        ('Redstone Ore', 'Redstone Block', 'Redstone', None),
        ('Lapis Ore', 'Lapis Block', 'Lapis Lazuli', None),
        ('Diamond Ore', 'Diamond Block', 'Diamond', None),
        ('Emerald Ore', 'Emerald Block', 'Emerald', None),
        ('Nether Gold Ore', 'Gold Block', 'Gold Nugget', None),
        ('Nether Quartz Ore', 'Quartz Block', 'Quartz', None),
        ('Ancient Debris', 'Netherite Block', 'Netherite Ingot', 'Netherite Scrap'),
    ))

    def water_loop(step):
        yield fillbiome(r(-1, 0, -5), r(9, 6, 1), step.elem)
        yield fill(r(-1, 0, -5), r(9, 6, 1), 'water').replace('ice')
        yield fill(r(-1, 0, -5), r(9, 6, 1), 'air').replace('snow')
        yield Sign.change(r(0, 2, 0), (None, None, None, biomes[step.elem].name))

    water_biomes = (MEADOW, FROZEN_OCEAN, COLD_OCEAN, OCEAN, LUKEWARM_OCEAN, WARM_OCEAN, SWAMP, MANGROVE_SWAMP)
    room.function('water_init').add(
        WallSign((None, 'Flowing Water', 'Biome:')).place(r(0, 2, 0), WEST),
        WallSign((None, 'Flowing Lava')).place(r(0, 2, 6), WEST),
    )
    room.loop('water', main_clock).loop(water_loop, water_biomes)

    basic_functions(room)
    fencelike_functions(room)
    wood_functions(room)
    copper_functions(room)
    trim_functions(room)


def basic_functions(room):
    stand = Entity('armor_stand', {'Tags': ['basic_stand', 'material_static'], 'ShowArms': True, 'NoGravity': True})
    invis_stand = stand.clone().merge_nbt({'Tags': ['material_static'], 'Invisible': True})
    basic_init = room.function('basic_init').add(kill(e().tag('material_static')),
                                                 stand.summon(r(0, 2.0, 0), facing=NORTH,
                                                              nbt={'CustomNameVisible': True}))
    for i in range(0, 5):
        basic_init.add(invis_stand.summon(r(-(0.8 + i * 0.7), 2.0, 0), facing=NORTH,
                                          nbt={'Tags': ['material_%d' % (4 + i), 'material_static']}))
        if i < 4:
            basic_init.add(invis_stand.summon(r(+(0.6 + i * 0.7), 2.0, 0), facing=NORTH,
                                              nbt={'Tags': ['material_%d' % (3 - i), 'material_static']}))

    basic_init.add(fill(r(-3, 2, 2), r(-3, 5, 2), 'stone'), kill(e().tag('armor_frame')),
                   summon('item_frame', r(-3, 2, 1),
                          {'Facing': 2, 'Tags': ['armor_boots', 'enchantable', 'armor_frame']}),
                   summon('item_frame', r(-3, 3, 1),
                          {'Facing': 2, 'Tags': ['armor_leggings', 'enchantable', 'armor_frame']}),
                   summon('item_frame', r(-3, 4, 1),
                          {'Facing': 2, 'Tags': ['armor_chestplate', 'enchantable', 'armor_frame']}),
                   summon('item_frame', r(-3, 5, 1),
                          {'Facing': 2, 'Tags': ['armor_helmet', 'enchantable', 'armor_frame']}),
                   summon('item_frame', r(3, 2, 1), {'Facing': 2, 'Tags': ['armor_gem', 'armor_frame']}),
                   summon('item_frame', r(4, 4, 1),
                          {'Facing': 2, 'Tags': ['armor_horse_frame', 'enchantable', 'armor_frame']}),
                   label(r(5, 2, -2), 'Saddle'), label(r(3, 2, -2), 'Enchanted'), label(r(1, 2, -2), 'Turtle Helmet'),
                   label(r(-1, 2, -2), 'Elytra'))

    materials = (
        ('wooden', 'leather', True, Block('oak_planks'), 'oak_sign'),
        ('stone', 'chainmail', False, Block('stone'), 'stone'),
        ('iron', 'iron', True, Block('iron_block'), 'iron_ingot'),
        ('golden', 'golden', True, Block('gold_block'), 'gold_ingot'),
        ('diamond', 'diamond', True, Block('diamond_block'), 'diamond'),
        ('netherite', 'netherite', False, Block('netherite_block'), 'netherite_ingot'),
    )

    enchanted = room.score('enchanted')

    def enchanter(value, tag, command):
        return execute().if_().score(enchanted).matches(value).as_(e().tag(tag)).run(command)

    def enchant(on):
        if on:
            value, cmd = 1, lambda path: data().modify(s(), path).merge().value(
                {'enchantments': {'levels': {'mending': 1}}})
        else:
            value, cmd = 0, lambda path: data().remove(s(), path)

        yield enchanter(value, 'enchantable', cmd('Item.components'))
        yield enchanter(value, 'armor_horse', cmd('body_armor_item.components'))
        yield enchanter(value, 'material_static', cmd('body_armor_item.components'))
        yield enchanter(value, 'material_static', cmd('ArmorItems[].components'))
        yield enchanter(value, 'material_static', cmd('HandItems[].components'))

    horse_saddle = room.score('horse_saddle')
    turtle_helmet = room.score('turtle_helmet')
    elytra = room.score('elytra')

    def basic_loop(step):
        material, armor, horse_armor, background, gem = step.elem

        yield data().merge(
            e().tag('basic_stand').limit(1), {
                'CustomName': material.capitalize(),
                'ArmorItems': [{'id': '%s_boots' % armor, 'Count': 1}, {'id': '%s_leggings' % armor, 'Count': 1},
                               {'id': '%s_chestplate' % armor, 'Count': 1},
                               {'id': '%s_helmet' % armor, 'Count': 1}]})

        yield fill(r(-3, 2, 2), r(-3, 5, 2), background.id)
        yield setblock(r(3, 2, 2), background.id)
        yield setblock(r(4, 4, 2), background.id)

        yield data().merge(e().tag('armor_boots').limit(1), {
            'Item': {'id': '%s_boots' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield data().merge(e().tag('armor_leggings').limit(1), {
            'Item': {'id': '%s_leggings' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield data().merge(e().tag('armor_chestplate').limit(1), {
            'Item': {'id': '%s_chestplate' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield data().merge(e().tag('armor_helmet').limit(1), {
            'Item': {'id': '%s_helmet' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield data().merge(e().tag('armor_gem').limit(1), {
            'Item': {'id': gem, 'Count': 1}, 'ItemRotation': 0})

        if horse_armor:
            yield execute().unless().entity(e().tag('armor_horse').distance((None, 10))).run(
                room.mob_placer(r(4.5, 2, 0.5), NORTH, adults=True).summon(
                    'horse', nbt={'Variant': 1, 'Tame': True, 'Tags': ['armor_horse', 'material_static']}))
            yield data().merge(e().tag('armor_horse').limit(1).sort('nearest'), {
                'body_armor_item': {'id': '%s_horse_armor' % armor, 'Count': 1}})
            yield data().merge(e().tag('armor_horse_frame').limit(1),
                               {'Item': {'id': '%s_horse_armor' % armor, 'Count': 1}, 'ItemRotation': 0})
            yield execute().if_().score(horse_saddle).matches(1).run(
                item().replace().entity(e().tag('armor_horse'), 'horse.saddle').with_('saddle'))
            yield execute().if_().score(horse_saddle).matches(0).run(
                item().replace().entity(e().tag('armor_horse'), 'horse.saddle').with_('air'))
        else:
            yield data().remove(e().tag('armor_horse_frame').limit(1), 'Item')
            yield execute().if_().entity(e().tag('armor_horse').distance((None, 10))).run(
                kill_em(e().tag('armor_horse')))

        yield data().merge(e().tag('basic_stand').limit(1), {
            'HandItems': [{'id': '%s_sword' % material, 'Count': 1}, {'id': 'shield', 'Count': 1}]})

        hands_row = [None, None, '%s_shovel' % material, '%s_pickaxe' % material, '%s_hoe' % material,
                     '%s_axe' % material, None, None]
        if material == 'wooden':
            hands_row[0] = 'stick'
            hands_row[1] = 'bow'
            hands_row[6] = 'fishing_rod'
            hands_row[7] = 'crossbow'
        elif material == 'iron':
            hands_row[1] = 'flint_and_steel'
            hands_row[6] = 'shears'
            hands_row[7] = 'compass'
        elif material == 'golden':
            hands_row[6] = 'clock'
        hands = list({'id': h} if h else {} for h in hands_row)

        for j in range(0, 4):
            yield data().merge(e().tag('material_%d' % j).limit(1), {'HandItems': [hands[j], {}]})
        for j in range(4, 8):
            yield data().merge(e().tag('material_%d' % j).limit(1), {'HandItems': [{}, hands[j]]})
        yield data().merge(r(-2, 0, 1), {'name': f'restworld:material_{material}', 'mode': 'LOAD'})

    room.loop('basic', main_clock).add(
        fill(r(2, 2, 2), r(-2, 5, 4), 'air'),
        kill_em(e().tag('material_thing'))
    ).loop(
        basic_loop, materials).add(enchant(True), enchant(False), execute().if_().score(turtle_helmet).matches(1).run(
        data().modify(e().tag('basic_stand').limit(1), 'ArmorItems[3].id').set().value('turtle_helmet')),
                                   execute().if_().score(turtle_helmet).matches(1).run(
                                       data().modify(e().tag('armor_helmet').limit(1), 'Item.id').set().value(
                                           'turtle_helmet')), execute().if_().score(elytra).matches(1).run(
            data().modify(e().tag('basic_stand').limit(1), 'ArmorItems[2].id').set().value('elytra')),
                                   execute().if_().score(elytra).matches(1).run(
                                       data().modify(e().tag('armor_chestplate').limit(1), 'Item.id').set().value(
                                           'elytra')), fill(r(-2, 2, 2), r(2, 4, 4), 'air'),
                                   setblock(r(-2, 0, 0), 'redstone_block'),
                                   execute().positioned(r(-2, 0, 2)).run(kill(e().type('item').volume((5, 3, 4)))))

    room.function('basic_update').add(
        execute().at(e().tag('basic_home')).run(function('restworld:materials/basic_cur')),
        execute().at(e().tag('basic_home')).run(function('restworld:materials/basic_finish_main')))


def fencelike_functions(room):
    volume = Region(r(8, 3, 6), r(0, 2, 0))

    room.function('fencelike_init').add(WallSign(()).place(r(6, 2, 0), NORTH), label(r(6, 2, -2), 'Change Height'),
                                        label(r(4, 2, -2), 'Glass Panes'), label(r(3, 2, -2), 'Walls'),
                                        label(r(2, 2, -2), 'Fences'))

    def fencelike(block: BlockDef):
        block = as_block(block)
        yield volume.replace(block, '#restworld:fencelike')
        yield execute().at(e().tag('fencelike_home')).run(data().merge(r(6, 2, 0), block.sign_nbt()))

    def switch_to_fencelike(which):
        room.function(f'switch_to_{which}', home=False).add(kill(e().tag('which_fencelike_home')),
                                                            execute().at(e().tag('fencelike_home')).positioned(
                                                                r(1, -0.5, 0)).run(
                                                                function('restworld:materials/%s_home' % which)),
                                                            tag(e().tag('%s_home' % which)).add('which_fencelike_home'),
                                                            execute().at(e().tag('%s_home' % which)).run(
                                                                function('restworld:materials/%s_cur' % which)))

    def fence_loop(step):
        yield from fencelike(step.elem)
        if step.elem[:-len(' Fence')] in info.woods + stems:
            yield volume.replace_facing(step.elem + ' Gate', '#fence_gates')

    room.loop('panes', main_clock).loop(lambda step: fencelike(step.elem),
                                        tuple(f'{x.name}|Stained Glass|Pane' for x in colors) + (
                                            'Glass Pane', 'Iron Bars'))
    switch_to_fencelike('panes')
    room.loop('fences', main_clock).loop(fence_loop,
                                         tuple(f'{x} Fence' for x in info.woods + stems + ('Nether Brick',)))
    switch_to_fencelike('fences')
    room.loop('walls', main_clock).loop(lambda step: fencelike(step.elem), (x + ' Wall' for x in (
        'Cobblestone', 'Mossy|Cobblestone', 'Sandstone', 'Red|Sandstone', 'Brick', 'Mud|Brick', 'Stone|Brick',
        'Mossy Stone|Brick', 'Nether|Brick', 'Red Nether|Brick', 'End Stone|Brick', 'Polished|Blackstone|Brick',
        'Polished|Blackstone', 'Blackstone', 'Andesite', 'Granite', 'Diorite', 'Deepslate|Brick', 'Deepslate|Tile',
        'Cobbled|Deepslate', 'Polished|Deepslate', 'Prismarine',
    )))
    switch_to_fencelike('walls')


def copper_functions(room):
    tags = restworld.tags(BLOCKS)

    def copper_tags(type) -> None:
        blocks = list(re.sub('^_', '', f'{v}{type}') for v in ('', 'exposed_', 'weathered_', 'oxidized_'))
        if blocks[0] == 'copper':
            blocks[0] += '_block'
        tag_name = type
        if tag_name[-1] != 's':
            tag_name += 's'
        blocks.extend(list('waxed_' + b for b in blocks))
        tags[tag_name] = {'values': blocks}

    volume = Region(r(0, 1, 0), r(4, 5, 6))
    copper_tags('copper')
    copper_tags('cut_copper')
    copper_tags('chiseled_copper')
    copper_tags('copper_grate')
    copper_tags('copper_bulb')
    copper_tags('cut_copper_stairs')
    copper_tags('cut_copper_slab')
    copper_tags('copper_door')
    copper_tags('copper_trapdoor')

    def copper_loop(step):
        type: str = step.elem.lower()
        basic = 'copper'
        if type in ('', 'waxed'):
            basic += '_block'
        if len(type) > 0:
            type += '_'
        yield from volume.replace(type + basic, '#restworld:coppers')
        yield from volume.replace(type + 'cut_copper', '#restworld:cut_coppers')
        yield from volume.replace(type + 'chiseled_copper', '#restworld:chiseled_coppers')
        yield from volume.replace(type + 'copper_grate', '#restworld:copper_grates')
        yield from volume.replace(type + 'copper_bulb', '#restworld:copper_bulbs', {'lit': True})
        yield from volume.replace(type + 'copper_bulb', '#restworld:copper_bulbs', {'lit': False})
        yield from volume.replace_stairs(type + 'cut_copper_stairs', '#restworld:cut_copper_stairs')
        yield from volume.replace_slabs(type + 'cut_copper_slab', '#restworld:cut_copper_slabs')
        # doors can't be generically replaced, see below for the manual placement
        yield from volume.replace_trapdoors(type + 'copper_trapdoor', '#restworld:copper_trapdoors')

        # The door won't be set unless we manually remove previous one.
        yield fill(r(0, 2, 4), r(0, 3, 4), 'air')
        yield setblock(r(0, 2, 4), (type + 'copper_door', {'facing': NORTH, 'half': 'lower'}))
        yield setblock(r(0, 3, 4), (type + 'copper_door', {'facing': NORTH, 'half': 'upper'}))

        sign_text = ['', type.replace('_', ' ').title(), 'Copper', '']
        yield Sign.change(r(2, 2, 0), sign_text)

    # Share a score so we only change 'waxness', not oxidization level
    copper_score = room.score('coppers')
    room.loop('unwaxed_coppers', main_clock, score=copper_score).loop(
        copper_loop, ('', 'exposed', 'weathered', 'oxidized'))
    room.loop('waxed_coppers', main_clock, score=copper_score).loop(
        copper_loop, ('waxed', 'waxed_exposed', 'waxed_weathered', 'waxed_oxidized'))
    copper_home = e().tag('coppers_home')
    run_unwaxed = room.function('unwaxed_coppers_run', home=False).add(tag(copper_home).remove('waxed_coppers_home'),
                                                                       tag(copper_home).add('unwaxed_coppers_home'),
                                                                       execute().at(copper_home).run(function(
                                                                           'restworld:materials/unwaxed_coppers_cur')))
    room.function('waxed_coppers_run', home=False).add(tag(copper_home).remove('unwaxed_coppers_home'),
                                                       tag(copper_home).add('waxed_coppers_home'),
                                                       execute().at(copper_home).run(
                                                           function('restworld:materials/waxed_coppers_cur')))
    room.function('coppers_init').add(label(r(2, 2, -2), 'Waxed'), function(run_unwaxed))


def wood_functions(room):
    wood_init = room.function('wood_init').add(
        summon('item_frame', r(2, 3, -3), {
            'Tags': ['wood_boat_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        summon('item_frame', r(3, 3, -3), {
            'Tags': ['wood_sign_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        label(r(-1, 2, 4), 'Chest Boat'))
    wood_init.add(summon('item_frame', r(3, 4, -3), {
        'Tags': ['wood_hanging_sign_frame', room.name], 'Facing': 3, 'Fixed': True,
        'Item': {'id': 'stone', 'Count': 1}}))

    volume = Region(r(-5, 1, -5), r(6, 5, 3))

    def wood_loop(step):
        name = step.elem
        id = to_id(name)
        planks = f'{id}_planks'
        slab = f'{id}_slab'
        stairs = f'{id}_stairs'
        if name in stems:
            log = f'{id}_stem'
            wood = f'{id}_hyphae'
            leaves = 'nether_wart_block' if name == 'Crimson' else f'{id}_wart_block'
            saplings = (f'{id}_roots', f'{id}_fungus', f'{id}_nylium')
        else:
            if 'Mosaic' in name:
                id = 'bamboo'
                planks = 'bamboo_mosaic'
            log = f'{id}_log'
            wood = f'{id}_wood'
            leaves = f'{id}_leaves'
            if 'Bamboo' in name:
                log = 'bamboo_block'
                wood = 'jungle_wood'
                leaves = 'jungle_leaves'
            saplings = (Block(f'{id}_sapling'), Block(f'{id}_sapling', {'stage': 1}), 'grass_block')
            if name == 'Mangrove':
                saplings = (
                    Block('mangrove_propagule', {'age': 1}),
                    Block('mangrove_propagule', {'age': 4}),
                    'grass_block')
            elif 'Bamboo' in name:
                saplings = ('bamboo_sapling', Block('bamboo', {'age': 0, 'leaves': 'small'}), 'grass_block')

        # General replacement
        yield from volume.replace(wood, '#restworld:woodlike')
        yield from volume.replace(leaves, '#restworld:leaflike')
        yield from volume.replace(planks, '#restworld:planks')
        yield from volume.replace_slabs(slab, '#restworld:stepable_slabs')
        yield from volume.replace_stairs(stairs, '#restworld:stepable_stairs')
        yield from volume.replace(f'{id}_fence', '#wooden_fences')
        yield from volume.replace_facing(f'{id}_fence_gate', '#fence_gates')
        yield from volume.replace_buttons(f'{id}_button')
        yield from volume.replace(f'{id}_pressure_plate', '#pressure_plates')
        yield from volume.replace_axes(log, '#restworld:loglike')
        yield from volume.replace_axes(f'stripped_{log}', '#restworld:stripped_loglike')
        yield from volume.replace_axes(f'stripped_{wood}', '#restworld:stripped_woodlike')
        # doors can't be generically replaced, see below for the manual placement
        yield from volume.replace_trapdoors(f'{id}_trapdoor', '#trapdoors')
        yield from volume.replace_facing(
            WallSign((), wood=id).messages((None, f'{name}', 'Wall Sign')).wax(False), '#wall_signs')
        yield from volume.replace_rotation(Sign((), wood=id).messages((None, f'{name} Sign')).wax(False), '#signs')
        yield from volume.replace_facing(
            WallSign((), wood=id, hanging=True).messages((None, f'{name}', 'Hanging', 'Wall Sign')).wax(False),
            '#wall_hanging_signs')
        yield from volume.replace_rotation(
            Sign((), wood=id, hanging=True).messages((None, f'{name}', 'Hanging', 'Sign')).wax(False),
            '#ceiling_hanging_signs')

        yield from volume.replace_facing(
            Block(f'{id}_wall_hanging_sign', nbt=Sign.lines_nbt((name, 'Wall', 'Hanging', 'Sign'))),
            '#wall_hanging_signs')
        for attached in True, False:
            sign_text = Sign.lines_nbt((name, 'Attached', 'Hanging', 'Sign')) if attached else Sign.lines_nbt(
                (name, 'Hanging', 'Sign'))
            yield from volume.replace_rotation(
                Block(f'{id}_hanging_sign', nbt=sign_text),
                '#all_hanging_signs',
                shared_states={'attached': attached})

        # Add special cases
        yield from volume.fill('air', 'vine')  # remove any existing vine
        if name == ('Jungle', 'Mangrove'):
            yield fill(r(-4, 2, -2), r(-4, 4, -2), ('vine', {'north': True}))

        yield setblock(r(-2, 2, -1), saplings[0])
        yield setblock(r(0, 2, -1), saplings[1])
        yield setblock(r(-2, 1, -1), saplings[2])
        yield setblock(r(0, 1, -1), saplings[2])

        workplace = 'air'
        if id == 'dark_oak':
            workplace = Block('cartography_table')
        elif id == 'oak':
            workplace = Block('lectern', {'facing': WEST})
        elif id == 'birch':
            workplace = Block('fletching_table')
        yield setblock(r(4, 2, 0), workplace)

        # The doors won't be set unless we manually remove previous ones.
        yield fill(r(4, 2, -1), r(4, 3, -1), 'air')
        yield fill(r(4, 2, 1), r(4, 3, 2), 'air')
        yield setblock(r(4, 2, -1), (f'{id}_door', {'facing': WEST, 'half': 'lower'}))
        yield setblock(r(4, 3, -1), (f'{id}_door', {'facing': WEST, 'half': 'upper'}))
        yield setblock(r(4, 2, 1), (f'{id}_door', {'facing': WEST, 'half': 'lower', 'hinge': 'right'}))
        yield setblock(r(4, 3, 1), (f'{id}_door', {'facing': WEST, 'half': 'upper', 'hinge': 'right'}))
        yield setblock(r(4, 2, 2), (f'{id}_door', {'facing': WEST, 'half': 'lower'}))
        yield setblock(r(4, 3, 2), (f'{id}_door', {'facing': WEST, 'half': 'upper'}))

        yield execute().as_(e().tag('wood_sign_frame')).run(
            data().merge(s(), ItemFrame(SOUTH).item(f'{id}_sign').named(f'{name} Sign').nbt))
        yield execute().as_(e().tag('wood_hanging_sign_frame')).run(
            data().merge(s(), ItemFrame(SOUTH).item(f'{id}_hanging_sign').named(f'{name} Hanging Sign').nbt))

        yield kill_em(e().tag('wood_boat'))  # remove existing boat
        if 'stem' not in log:
            wood_boat_chest = room.score('wood_boat_chest')
            location = r(-0.5, 1.525, 2)
            boat_state = {'Type': id, 'Tags': ['wood_boat', room.name], 'Rotation': [90, 0], 'CustomName': name,
                          'CustomNameVisible': True}
            boat = Entity('boat', boat_state)
            chest_boat = Entity('chest_boat', boat_state)
            yield execute().if_().score(wood_boat_chest).matches(0).run(summon(boat, location))
            yield execute().if_().score(wood_boat_chest).matches(1).run(summon(chest_boat, location))
            boat_item = f'{id}_boat'
            chest_boat_item = f'{id}_chest_boat'
            if 'bamboo' in log:
                boat_item = 'bamboo_raft'
                chest_boat_item = 'bamboo_chest_raft'
            yield execute().if_().score(wood_boat_chest).matches(0).as_(
                e().tag('wood_boat_frame')).run(
                data().merge(s(), ItemFrame(SOUTH).item(boat_item).named(f'{name} Boat').nbt))
            yield execute().if_().score(wood_boat_chest).matches(1).as_(
                e().tag('wood_boat_frame')).run(
                data().merge(s(), ItemFrame(SOUTH).item(chest_boat_item).named(f'{name} Chest Boat').nbt))
        else:
            yield data().remove(e().tag('wood_boat_frame').limit(1), 'Item')

    i = info.woods.index('Bamboo') + 1
    woods = info.woods[:i] + ('Bamboo Mosaic',) + info.woods[i:]
    room.loop('wood', main_clock).add(kill_em(e().tag('wood_boat'))).loop(wood_loop, woods + stems)


armor_pieces = ('boots', 'leggings', 'chestplate', 'helmet')


def armor_for(stand: Entity, kind: str, nbt: NbtDef = None) -> None:
    if nbt is None:
        nbt = {}
    base_nbt = Nbt({'components': {'trim': {'material': 'redstone', 'pattern': 'coast'}}})
    base_nbt = base_nbt.merge(nbt)
    items = [Item.nbt_for(f'{kind}_{x}', base_nbt)
             for x in armor_pieces]
    stand.merge_nbt({'ArmorItems': items})


def trim_functions(room):
    overall_tag = 'trim_stand'
    base_stand = Entity('armor_stand',
                        {'ShowArms': True,
                         'Pose': {'LeftArm': [-20, 0, -120], 'RightArm': [-20, 0, 20],
                                  'LeftLeg': [-20, 0, 0], 'RightLeg': [20, 0, 0]}}).tag(room.name, overall_tag)

    places = (
        (r(-3, 2, -5), EAST), (r(2, 2, -5), WEST),
        (r(-4, 3, -4), EAST), (r(3, 3, -4), WEST),
        (r(-3, 2, -3), EAST), (r(2, 2, -3), WEST),
        (r(-4, 3, -2), EAST), (r(3, 3, -2), WEST),
        (r(-3, 2, -1), EAST), (r(2, 2, -1), WEST),
        (r(-4, 3, 0), EAST), (r(3, 3, 0), WEST),
        (r(-3, 2, 1), NE), (r(-1, 2, 1), NORTH), (r(0, 2, 1), NORTH), (r(2, 2, 1), NW),
        (r(-2, 3, 2), NORTH), (r(1, 3, 2), NORTH)
    )

    patterns_places = range(len(trim_patterns))
    material_places = (4, 5, 6, 7, 8, 9, 10, 13, 14, 15)
    armors_places = material_places[-6:]

    show = room.score('trim_show')
    change = room.score('trim_change')
    adjust_change = room.score('trim_adjust_change')
    num_categories = room.score_max('TRIMS')
    facing = NORTH

    frame = 'trim_frame'
    trim_nbt = {'components': {'trim': {'pattern': 'sentry', 'material': 'redstone'}}}
    room.function('trim_init').add(kill(e().tag(frame)), ItemFrame(NORTH).item('iron_boots').merge_nbt(
        {'Item': trim_nbt}).tag('materials', frame, f'{frame}_boots').summon(r(1, 5, 2)),
                                   ItemFrame(NORTH).item('iron_leggings').merge_nbt(
                                       {'Item': trim_nbt}).tag('materials', frame, f'{frame}_leggings').summon(
                                       r(0, 5, 2)), ItemFrame(NORTH).item('iron_chestplate').merge_nbt(
            {'Item': trim_nbt}).tag('materials', frame, f'{frame}_chestplate').summon(r(-1, 5, 2)),
                                   ItemFrame(NORTH).item('iron_helmet').merge_nbt(
                                       {'Item': trim_nbt}).tag('materials', frame, f'{frame}_helmet').summon(
                                       r(-2, 5, 2)), WallSign().messages((None, 'Material:')).place(r(0, 6, 2), NORTH),
                                   WallSign().messages((None, 'Armor:', 'Iron')).place(r(-1, 6, 2), NORTH))

    class Trim:
        _num = 0

        def __init__(self, name: str, types, pos, armor_gen, nbt_path):
            self.name = name
            self.types = types
            self.tag = f'trim_{name}'
            self.pos = pos
            self.armor_gen = armor_gen
            self.nbt_path = nbt_path

            self.num = Trim._num
            Trim._num += 1
            self.init = room.function(f'trim_{name}_init').add(self._init())
            self.detect = room.function(f'trim_{name}_detect', home=False).add(self._detect())
            self.loop = room.loop(f'trim_{name}', main_clock).loop(self._loop_func, types)

        def _init(self):
            yield kill_em(e().tag(overall_tag))
            for i, t in enumerate(self.types):
                stand = base_stand.clone().tag(self.tag).merge_nbt({'CustomName': t.title()})
                self.armor_gen(stand, t)
                loc = places[self.pos[i]]
                yield stand.summon(loc[0], {'Rotation': as_facing(loc[1]).rotation})
            yield show.set(self.num)

        def _loop_func(self, step):
            yield execute().as_(e().tag(overall_tag)).run(
                data().modify(s(), f'ArmorItems[].{self.nbt_path}').set().value(step.elem))
            yield execute().as_(e().tag(frame)).run(data().modify(s(), f'Item.{self.nbt_path}').set().value(step.elem))
            yield execute().at(e().tag('trim_change_home')).run(
                Sign.change(r(0, 2, 0), (None, None, None, step.elem.title())))
            yield from self._trim_frame_sign(step)

        def _trim_frame_sign(self, step):
            if 'pattern' in self.nbt_path:
                return
            sign_x = 2 if 'material' in self.nbt_path else 1
            yield execute().at(e().tag(f'{frame}_helmet')).run(
                Sign.change(r(sign_x, 1, 0), (None, None, step.elem.title())))

        def _detect(self):
            for i, t in enumerate(self.types):
                # The path is a.b.c, but we need the last element to be a.b{c:value}, and there is no replace, so...
                path = self._to_path(t)
                sign = WallSign().messages((None, 'Keep', f'{self.name.title().replace("s", "")}:', t.title()))
                yield execute().if_().data(e().tag(overall_tag).limit(1), path).run(sign.place(r(-1, 2, 0), facing))

        def _to_path(self, t):
            return ('ArmorItems[0].' + self.nbt_path)[::-1].replace('.', '{', 1)[::-1] + ':' + t + '}'

    class Armors(Trim):
        def __init__(self, name: str, types, pos, armor_gen):
            super().__init__(name, types, pos, armor_gen, 'id')

        def _loop_func(self, step):
            for i, piece in enumerate(armor_pieces):
                which = f'{step.elem}_{piece}'
                yield execute().as_(e().tag(overall_tag)).run(
                    data().modify(s(), f'ArmorItems[{i}].{self.nbt_path}').set().value(which))
                yield execute().as_(e().tag(f'{frame}_{piece}')).run(
                    data().modify(s(), f'Item.{self.nbt_path}').set().value(which))
            yield execute().at(e().tag('trim_change_home')).run(
                Sign.change(r(0, 2, 0), (None, None, None, step.elem.title())))
            yield from self._trim_frame_sign(step)

        def _to_path(self, t):
            return f'ArmorItems[{{id:"minecraft:{t}_boots"}}]'

    categories = {
        'patterns': Trim('patterns', trim_patterns, patterns_places,
                         lambda stand, type: armor_for(stand, 'iron', {'components': {'trim': {'pattern': type}}}),
                         'components.minecraft:trim.pattern'),
        'materials': Trim('materials', trim_materials, material_places,
                          lambda stand, type: armor_for(stand, 'iron', {'components': {'trim': {'material': type}}}),
                          'components.minecraft:trim.material'),
        'armors': Armors('armors', info.armors, armors_places,
                         lambda stand, type: armor_for(stand, type))}

    # menu: pop the menu up; call other menu's "cleanup" (for 'show', first ensure 'change' value != 'show' value)
    # cleanup: pull the menu down, using variable to define "current"
    # each sign: set "current", then cleanup
    # init: Call 'cleanup'
    #
    # change_home: the armor stand for the current "change" value
    show_menu = room.function('trim_show_menu', home=False)
    show_cleanup = room.function('trim_show_cleanup', home=False)
    show_init = room.function('trim_show_init')
    change_menu = room.function('trim_change_menu', home=False)
    change_cleanup = room.function('trim_change_cleanup', home=False)
    change_init = room.function('trim_change_init')
    room.function('trim_loop_init')
    run_show_cleanup = execute().at(e().tag('trim_show_home')).run(function(show_cleanup))
    run_change_cleanup = execute().at(e().tag('trim_change_home')).run(function(change_cleanup))

    # These labels have to go somewhere...
    change_init.add(label(r(-1, 2, -1), "Leggings"), label(r(1, 2, -1), "Turtle Helmet"), label(r(3, 2, -1), "Labels"))

    show_init.add(show.set(0), run_show_cleanup)
    show_menu.add(
        execute().at(e().tag('trim_change_home')).if_().block(r(0, 3, 0), 'oak_wall_sign').run(run_change_cleanup))
    show_cleanup.add(fill(r(0, 3, 0), r(0, 4, 0), 'air'),
                     execute().store(RESULT).score(adjust_change).if_().score(show).is_(EQ, change),
                     execute().if_().score(adjust_change).matches(True).run(
                         change.add(1),
                         change.operation(MOD, num_categories),
                         run_change_cleanup))
    for i, cat in enumerate(categories.values()):
        lines = (None, 'Show All', cat.name.title())
        show_menu.add(WallSign().messages(lines, commands=(show.set(i), run_show_cleanup)).place(r(0, i, 0), facing))
        show_cleanup.add(execute().if_().score(show).matches(i).run(
            WallSign().messages(
                (None, 'Show All', cat.name.title()), commands=(function(show_menu),)).place(r(0, 2, 0), facing),
            execute().at(e().tag('trim_home')).run(function(cat.init))))

    change_init.add(change.set(1), run_change_cleanup)
    change_menu.add(
        execute().at(e().tag('trim_show_home')).if_().block(r(0, 3, 0), 'oak_wall_sign').run(run_show_cleanup))
    change_cleanup.add(fill(r(0, 3, 0), r(0, 4, 0), 'air'), kill(e().tag('trim_loop_home')),
                       execute().at(e().tag('trim_change_home')).positioned(r(-1, -0.5, 0)).run(
                           function('restworld:materials/trim_loop_home')))
    for i, cat in enumerate(categories.values()):
        sign_num = 0
        for j, jcat in enumerate(categories.values()):
            if i == j:
                continue
            lines = (None, 'Change', jcat.name.title())
            change_menu.add(execute().if_().score(show).matches(i).run(
                WallSign().messages(lines, commands=(change.set(j), run_change_cleanup)).place(
                    r(0, sign_num, 0), facing)))
            sign_num += 1
        change_cleanup.add(execute().if_().score(change).matches(i).at(e().tag('trim_change_home')).run(
            WallSign().messages((None, 'Change', f'{cat.name.title()}:'),
                                commands=(function(change_menu),)).place(r(0, 2, 0), facing),
            tag(e().tag('trim_loop_home')).add(f'trim_{cat.name}_home')))

    trim_sum = room.score('trim_sum')
    keep_detect = room.function('trim_keep_detect', home=False).add(
        scoreboard().players().operation(trim_sum, EQ, show), scoreboard().players().operation(trim_sum, PLUS, change),
        execute().if_().score(trim_sum).matches(1).at(e().tag('trim_change_home')).run(
            function(categories['armors'].detect)),
        execute().if_().score(trim_sum).matches(2).at(e().tag('trim_change_home')).run(
            function(categories['materials'].detect)),
        execute().if_().score(trim_sum).matches(3).at(e().tag('trim_change_home')).run(
            function(categories['patterns'].detect)))
    show_cleanup.add(function(keep_detect))
    change_cleanup.add(function(keep_detect))

    room.function('trim_chestplate_off', home=False).add(execute().as_(e().tag(overall_tag)).run(
        item().replace().entity(s(), 'armor.feet').with_('air'),
        item().replace().entity(s(), 'armor.chest').with_('air')))

    chestplate_on = room.function('trim_chestplate_on', home=False)
    for armor in info.armors:
        chestplate_on.add(
            execute().as_(e().tag(overall_tag).nbt({'ArmorItems': [{'id': f'minecraft:{armor}_leggings'}]})).run(
                item().replace().entity(s(), 'armor.feet').with_(f'{armor}_boots'),
                item().replace().entity(s(), 'armor.chest').with_(f'{armor}_chestplate')))
    chestplate_on.add(execute().as_(e().tag(overall_tag)).run(
        data().modify(s(), 'ArmorItems[0].components.trim').merge().from_(s(), 'ArmorItems[1].components.trim'),
        data().modify(s(), 'ArmorItems[2].components.trim').merge().from_(s(), 'ArmorItems[1].components.trim')))

    room.function('trim_turtle_on', home=False).add(
        execute().as_(e().tag(overall_tag)).run(
            data().modify(s(), 'ArmorItems[3].id').set().value('turtle_helmet')))
    turtle_off = room.function('trim_turtle_off', home=False)
    for armor in info.armors:
        turtle_off.add(
            execute().as_(e().tag(overall_tag).nbt({'ArmorItems': [{'id': f'minecraft:{armor}_leggings'}]})).run(
                data().modify(s(), 'ArmorItems[3].id').set().value(f'{armor}_helmet')))
