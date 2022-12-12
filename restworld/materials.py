from __future__ import annotations

from pynecraft import info
from pynecraft.base import EAST, NORTH, SOUTH, WEST, r, to_id
from pynecraft.commands import Block, BlockDef, Entity, data, e, execute, fill, fillbiome, function, good_block, item, \
    kill, s, \
    setblock, summon, tag
from pynecraft.enums import BiomeId
from pynecraft.info import colors, stems, woods
from pynecraft.simpler import Item, ItemFrame, Region, Sign, WallSign
from restworld.rooms import Room, label
from restworld.world import fast_clock, kill_em, main_clock, restworld


def room():
    room = Room('materials', restworld, WEST, ('Materials', '& Tools,', 'Time, GUI,', 'Redstone, Maps'))

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
        yield data().merge(r(0, 2, 3), {'Text2': blocks[i][0]})

    room.loop('all_sand', main_clock).loop(all_sand_loop, range(0, 2))

    room.function('arrows_init').add(WallSign(()).place(r(1, 2, 0), EAST))

    def arrows_loop(step):
        yield summon(step.elem, r(0, 3, 0.25), {
            'Tags': ['arrow'], 'NoGravity': True, 'Color': 127, 'CustomPotionColor': 127 if step.i == 2 else ''})
        yield data().merge(r(1, 2, 0), {'Text2': step.elem.name})

    room.loop('arrows', main_clock).add(
        kill(e().tag('arrow'))
    ).loop(arrows_loop, (
        Block('Arrow'),
        Block('Spectral Arrow'),
        Block('arrow', name='Tipped Arrow')))

    points = (2, 6, 16, 36, 72, 148, 306, 616, 1236, 2476, 32767)

    def experience_orbs_loop(step):
        i = step.i
        p = points[i]
        f = -32768 if i == 0 else points[i - 1]
        yield summon('experience_orb', r(0, 3, 0), {'Value': p, 'Age': 6000 - 40})
        yield data().merge(r(1, 2, 0), {'Text3': 'Size %d' % (i + 1), 'Text4': '%d - %d' % (f, p)})

    room.loop('experience_orbs', fast_clock).loop(experience_orbs_loop, points)
    room.function('experience_orbs_init').add(WallSign((None, 'Experience Orb')).place(r(1, 2, 0), EAST))
    frame = ItemFrame(SOUTH, nbt={'Tags': [room.name, 'ores_ingot_frame']})
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
        yield data().merge(r(3, 2, 6), {'Text2': ore.name.replace(' Ore', '')})
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
            yield data().merge(r(3, 2, 6), {'Text3': '/ Netherite'})
        if raw:
            if 'Raw' in raw.name:
                yield setblock(r(3, 4, 2), '%s_block' % raw.id)
            yield summon(ItemFrame(SOUTH, nbt={'Tags': [raw_frame, room.name]}).named(raw.name),
                         r(3, 4, 3))
        else:
            yield kill(e().tag(raw_frame))
        yield execute().as_(e().tag('ore_ingot_frame').volume((8, 5, 8))).run(
            data().merge(s(), {'Item': Item.nbt_for(item.id)}))

    room.loop('ores', main_clock).add(
        kill(e().tag(raw_frame)),
        data().merge(r(3, 2, 6), {'Text3': ''}),
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
        yield data().merge(r(0, 2, 0), {'Text4': step.elem.display_name()})

    water_biomes = (
        BiomeId.MEADOW,
        BiomeId.FROZEN_OCEAN,
        BiomeId.COLD_OCEAN,
        BiomeId.OCEAN,
        BiomeId.LUKEWARM_OCEAN,
        BiomeId.WARM_OCEAN,
        BiomeId.SWAMP,
        BiomeId.MANGROVE_SWAMP,
    )
    room.function('water_init').add(
        WallSign((None, 'Flowing Water', 'Biome:')).place(r(0, 2, 0), WEST),
        WallSign((None, 'Flowing Lava')).place(r(0, 2, 6), WEST),
    )
    room.loop('water', main_clock).loop(water_loop, water_biomes)

    basic_functions(room)
    fencelike_functions(room)
    wood_functions(room)


def basic_functions(room):
    stand = Entity('armor_stand', {'Tags': ['basic_stand', 'material_static'], 'ShowArms': True, 'NoGravity': True})
    invis_stand = stand.clone().merge_nbt({'Tags': ['material_static'], 'Invisible': True})
    basic_init = room.function('basic_init').add(
        kill(e().tag('material_static')),
        stand.summon(r(0, 2.0, 0), facing=NORTH, nbt={'CustomNameVisible': True}),
    )
    for i in range(0, 5):
        basic_init.add(
            invis_stand.summon(r(-(0.8 + i * 0.7), 2.0, 0), facing=NORTH,
                               nbt={'Tags': ['material_%d' % (4 + i), 'material_static']}))
        if i < 4:
            basic_init.add(
                invis_stand.summon(r(+(0.6 + i * 0.7), 2.0, 0), facing=NORTH,
                                   nbt={'Tags': ['material_%d' % (3 - i), 'material_static']}))

    basic_init.add(
        fill(r(-3, 2, 2), r(-3, 5, 2), 'stone'),

        kill(e().tag('armor_frame')),
        summon('item_frame', r(-3, 2, 1), {'Facing': 2, 'Tags': ['armor_boots', 'enchantable', 'armor_frame']}),
        summon('item_frame', r(-3, 3, 1),
               {'Facing': 2, 'Tags': ['armor_leggings', 'enchantable', 'armor_frame']}),
        summon('item_frame', r(-3, 4, 1),
               {'Facing': 2, 'Tags': ['armor_chestplate', 'enchantable', 'armor_frame']}),
        summon('item_frame', r(-3, 5, 1), {'Facing': 2, 'Tags': ['armor_helmet', 'enchantable', 'armor_frame']}),
        summon('item_frame', r(3, 2, 1), {'Facing': 2, 'Tags': ['armor_gem', 'armor_frame']}),
        summon('item_frame', r(4, 4, 1),
               {'Facing': 2, 'Tags': ['armor_horse_frame', 'enchantable', 'armor_frame']}),

        label(r(5, 2, -2), 'Saddle'),
        label(r(3, 2, -2), 'Enchanted'),
        label(r(1, 2, -2), 'Turtle Helmet'),
        label(r(-1, 2, -2), 'Elytra'),
    )

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
            value, cmd = 1, lambda path: data().modify(s(), path).merge().value({'Enchantments': [{'id': 'mending'}]})
        else:
            value, cmd = 0, lambda path: data().remove(s(), path)

        yield enchanter(value, 'enchantable', cmd('Item.tag'))
        yield enchanter(value, 'armor_horse', cmd('ArmorItem.tag'))
        yield enchanter(value, 'material_static', cmd('ArmorItem.tag'))

        for a in range(0, 4):
            yield enchanter(value, 'material_static', cmd('ArmorItems[%d].tag' % a))
            if a < 2:
                yield enchanter(value, 'material_static', cmd('HandItems[%d].tag' % a))

    horse_saddle = room.score('horse_saddle')
    turtle_helmet = room.score('turtle_helmet')
    elytra = room.score('elytra')

    def basic_loop(step):
        material, armor, horse_armor, background, gem = step.elem

        yield data().merge(
            e().tag('basic_stand').limit(1), {
                'CustomName': material.capitalize(),
                'ArmorItems': [{'id': '%s_boots' % armor, 'Count': 1}, {'id': '%s_leggings' % armor, 'Count': 1},
                               {'id': '%s_chestplate' % armor, 'Count': 1}, {'id': '%s_helmet' % armor, 'Count': 1}]})

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
                'ArmorItem': {'id': '%s_horse_armor' % armor, 'Count': 1}})
            yield data().merge(e().tag('armor_horse_frame').limit(1),
                               {'Item': {'id': '%s_horse_armor' % armor, 'Count': 1}, 'ItemRotation': 0})
            yield execute().if_().score(horse_saddle).matches(1).run(
                item().replace().entity(e().tag('armor_horse'), 'horse.saddle').with_('saddle'))
            yield execute().if_().score(horse_saddle).matches(0).run(
                item().replace().entity(e().tag('armor_horse'), 'horse.saddle').with_('air'))
        else:
            yield data().merge(e().tag('armor_horse_frame').limit(1), {
                'Item': {'id': 'air', 'Count': 1}})
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
        hands = list({'id': h if h else '', 'Count': 1} for h in hands_row)

        for j in range(0, 4):
            yield data().merge(e().tag('material_%d' % j).limit(1), {'HandItems': [hands[j], {}]})
        for j in range(4, 8):
            yield data().merge(e().tag('material_%d' % j).limit(1), {'HandItems': [{}, hands[j]]})
        yield data().merge(r(-2, 0, 1), {'name': f'restworld:material_{material}', 'mode': 'LOAD'})

    room.loop('basic', main_clock).add(
        fill(r(2, 2, 2), r(-2, 5, 4), 'air'),
        kill_em(e().tag('material_thing'))
    ).loop(basic_loop, materials).add(
        enchant(True),
        enchant(False),
        execute().if_().score(turtle_helmet).matches(1).run(
            data().modify(e().tag('basic_stand').limit(1), 'ArmorItems[3].id').set().value('turtle_helmet')),
        execute().if_().score(turtle_helmet).matches(1).run(
            data().modify(e().tag('armor_helmet').limit(1), 'Item.id').set().value('turtle_helmet')),
        execute().if_().score(elytra).matches(1).run(
            data().modify(e().tag('basic_stand').limit(1), 'ArmorItems[2].id').set().value('elytra')),
        execute().if_().score(elytra).matches(1).run(
            data().modify(e().tag('armor_chestplate').limit(1), 'Item.id').set().value('elytra')),
        fill(r(-2, 2, 2), r(2, 4, 4), 'air'),
        setblock(r(-2, 0, 0), 'redstone_block'),
        execute().positioned(r(-2, 0, 2)).run(kill(e().type('item').volume((5, 3, 4))))
    )

    room.function('basic_update').add(
        execute().at(e().tag('basic_home')).run(function('restworld:materials/basic_cur')),
        execute().at(e().tag('basic_home')).run(function('restworld:materials/basic_finish_main')))


def fencelike_functions(room):
    volume = Region(r(8, 3, 6), r(0, 2, 0))

    room.function('fencelike_init').add(
        WallSign(()).place(r(6, 2, 0), NORTH),
        label(r(6, 2, -1), 'Change Height'),
        label(r(4, 2, -1), 'Glass Panes'),
        label(r(3, 2, -1), 'Walls'),
        label(r(2, 2, -1), 'Fences'),
    )

    def fencelike(block: BlockDef):
        block = good_block(block)
        yield volume.replace(block, '#restworld:fencelike')
        yield execute().at(e().tag('fencelike_home')).run(data().merge(r(6, 2, 0), block.sign_nbt))

    def switch_to_fencelike(which):
        room.function(f'switch_to_{which}', home=False).add(
            kill(e().tag('which_fencelike_home')),
            execute().at(e().tag('fencelike_home')).positioned(r(1, -0.5, 0)).run(
                function('restworld:materials/%s_home' % which)),
            tag(e().tag('%s_home' % which)).add('which_fencelike_home'),
            execute().at(e().tag('%s_home' % which)).run(function('restworld:materials/%s_cur' % which)))

    def fence_loop(step):
        yield from fencelike(step.elem)
        if step.elem[:-len(' Fence')] in woods + stems:
            yield volume.replace_facing(step.elem + ' Gate', '#fence_gates')

    room.loop('panes', main_clock).loop(lambda step: fencelike(step.elem),
                                        tuple(f'{x.name} Stained Glass Pane' for x in colors) + ('Glass Pane',))
    switch_to_fencelike('panes')
    room.loop('fences', main_clock).loop(fence_loop,
                                         tuple(f'{x} Fence' for x in woods + stems + ('Nether Brick',)) + (
                                             'Iron Bars',))
    switch_to_fencelike('fences')
    room.loop('walls', main_clock).loop(lambda step: fencelike(step.elem), (x + ' Wall' for x in (
        'Cobblestone', 'Mossy|Cobblestone', 'Sandstone', 'Red Sandstone', 'Brick', 'Mud|Brick', 'Stone|Brick',
        'Mossy Stone|Brick', 'Nether|Brick', 'Red Nether|Brick', 'End Stone|Brick', 'Polished|Blackstone|Brick',
        'Polished|Blackstone', 'Blackstone', 'Andesite', 'Granite', 'Diorite', 'Deepslate|Brick', 'Deepslate|Tile',
        'Cobbled|Deepslate', 'Polished|Deepslate', 'Prismarine',
    )))
    switch_to_fencelike('walls')


def wood_functions(room):
    room.function('wood_init').add(
        summon('item_frame', r(2, 3, -3), {
            'Tags': ['wood_boat_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        summon('item_frame', r(3, 3, -3), {
            'Tags': ['wood_sign_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        summon('item_frame', r(3, 4, -3), {
            'Tags': ['wood_hanging_sign_frame', room.name], 'Facing': 3, 'Fixed': True,
            'Item': {'id': 'stone', 'Count': 1}}),
        label(r(-1, 2, 4), 'Chest Boat'))

    volume = Region(r(-5, 1, -5), r(6, 5, 3))

    def wood_loop(step):
        name = step.elem
        id = to_id(name)
        if name in stems:
            log = f'{id}_stem'
            wood = f'{id}_hyphae'
            leaves = 'nether_wart_block' if name == 'Crimson' else f'{id}_wart_block'
            saplings = (f'{id}_roots', f'{id}_fungus', f'{id}_nylium')
        else:
            log = f'{id}_log'
            wood = f'{id}_wood'
            leaves = f'{id}_leaves'
            if name == 'Bamboo':
                log = 'bamboo_block'
                wood = 'jungle_wood'
                leaves = 'jungle_leaves'
            saplings = (Block(f'{id}_sapling'), Block(f'{id}_sapling', {'stage': 0}), 'grass_block')
            if name == 'Mangrove':
                saplings = (
                    Block('mangrove_propagule', {'age': 1}),
                    Block('mangrove_propagule', {'age': 4}),
                    'grass_block')
            elif name == 'Bamboo':
                saplings = ('bamboo_sapling', Block('bamboo', {'age': 0, 'leaves': 'small'}), 'grass_block')

        # Remove special cases
        yield from volume.fill('air', 'vine')
        yield kill_em(e().tag('wood_boat'))
        yield fill(r(4, 2, -1), r(3, 2, -1), 'air')
        yield fill(r(4, 2, 1), r(4, 3, 2), 'air')

        # General replacement
        yield from volume.replace(wood, '#restworld:woodlike')
        yield from volume.replace(leaves, '#restworld:leaflike')
        yield from volume.replace(f'{id}_planks', '#planks')
        yield from volume.replace_slabs(f'{id}_slab', '#slabs')
        yield from volume.replace_stairs(f'{id}_stairs', '#stairs')
        yield from volume.replace(f'{id}_fence', '#wooden_fences')
        yield from volume.replace_facing(f'{id}_fence_gate', '#fence_gates')
        yield from volume.replace_buttons(f'{id}_button')
        yield from volume.replace(f'{id}_pressure_plate', '#pressure_plates')
        yield from volume.replace_axes(log, '#restworld:loglike')
        yield from volume.replace_axes(f'stripped_{log}', '#restworld:stripped_loglike')
        yield from volume.replace_axes(f'stripped_{wood}', '#restworld:stripped_woodlike')
        yield from volume.replace_doors(f'{id}_door', '#doors')
        yield from volume.replace_trapdoors(f'{id}_trapdoor', '#trapdoors')
        yield from volume.replace_facing(Block(f'{id}_wall_sign', nbt={'Text2': f'{name} Wall Sign'}),
                                         '#wall_signs')
        yield from volume.replace_rotation(Block(f'{id}_sign', nbt={'Text2': f'{name} Sign'}), '#signs')

        hanging_sign_text = Sign.lines_nbt((name, 'Hanging', 'Sign'))
        yield from volume.replace_facing(Block(f'{id}_wall_hanging_sign', nbt=hanging_sign_text), '#wall_hanging_signs')
        for attached in True, False:
            yield from volume.replace_rotation(
                Block(f'{id}_hanging_sign', nbt=hanging_sign_text),
                '#all_hanging_signs',
                shared_states={'attached': attached})

        # Add special cases
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
            yield data().remove(e().tag('wood_boat_frame').limit(1), 'Item.id')

    room.loop('wood', main_clock).add(kill_em(e().tag('wood_boat'))).loop(wood_loop, info.woods + stems)
