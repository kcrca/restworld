from __future__ import annotations

import math

from pyker.commands import mc, r, Block, WEST, e, EAST, Entity, SOUTH, s, NORTH, BlockDef, good_block
from pyker.info import woods, stems, colors
from pyker.simpler import WallSign, Volume, ItemFrame, Item
from restworld.friendlies import _to_id
from restworld.rooms import Room, label
from restworld.world import restworld, main_clock, kill_em, fast_clock


def room():
    room = Room('materials', restworld, WEST, ('Materials', '& Tools,', 'Time, GUI,', 'Redstone'))

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

    volume = Volume(r(0, 1, 0), r(10, 6, 7))
    fill = (r(0, 1, 0), r(10, 6, 7))

    def all_sand_loop(step):
        i = step.i
        o = 1 - i
        for j in range(0, len(blocks[i])):
            yield from volume.replace(walls[i], walls[o])
            yield from volume.replace(blocks[i][j], blocks[o][j])
            if slabs[i][j]:
                yield from volume.replace_slabs(slabs[i][j], slabs[o][j])
            if stairs[i][j]:
                yield from volume.replace_stairs(stairs[i][j], stairs[o][j])
        yield mc.data().merge(r(0, 2, 3), {'Text2': blocks[i][0]})

    room.loop('all_sand', main_clock).loop(all_sand_loop, range(0, 2))

    room.function('arrows_init').add(WallSign(()).place(r(1, 2, 0), EAST))

    def arrows_loop(step):
        yield mc.summon(step.elem, r(0, 3, 0.25), {
            'Tags': ['arrow'], 'NoGravity': True, 'Color': 127, 'CustomPotionColor': 127 if step.i == 2 else ''})
        yield mc.data().merge(r(1, 2, 0), {'Text2': step.elem.display_name})

    room.loop('arrows', main_clock).add(
        mc.kill(e().tag('arrow'))
    ).loop(arrows_loop, (
        Block('Arrow'),
        Block('Spectral Arrow'),
        Block('arrow', display_name='Tipped Arrow')))

    points = (2, 6, 16, 36, 72, 148, 306, 616, 1236, 2476, 32767)
    each = 2 * math.pi / len(points)
    radius = 4

    def experience_orbs_loop(step):
        i = step.i
        p = points[i]
        angle = i * each
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        f = -32768 if i == 0 else points[i - 1]
        yield mc.summon('experience_orb', r(0, 3, 0), {'Value': p, 'Age': 6000 - 40})
        yield mc.data().merge(r(1, 2, 0), {'Text3': 'Size %d' % (i + 1), 'Text4': '%d - %d' % (f, p)})

    room.loop('experience_orbs', fast_clock).loop(experience_orbs_loop, points)
    room.function('experience_orbs_init').add(WallSign((None, 'Experience Orb')).place(r(1, 2, 0), EAST))
    frame = ItemFrame(SOUTH, {'Tags': [room.name, 'ore_ingot_frame']})
    room.function('ores_init').add(
        mc.summon(frame, r(3, 3, 3)),
        mc.summon(frame.merge_nbt({'Invisible': True}), r(4, 3, 3)),
        label(r(3, 2, 7), 'Deepslate'))

    raw_frame = 'ore_raw_frame'
    volume = Volume(r(7, 5, 6), r(0, 2, 0))
    deepslate_materials = room.score('deepslate_materials')

    def ore_loop(step):
        ore, block, item, raw = (Block(s) if s else None for s in step.elem)
        yield from volume.replace(block.id, '#restworld:ore_blocks')
        yield mc.data().merge(r(3, 2, 6), {'Text2': ore.display_name.replace(' Ore', '')})
        if 'Nether' in ore.display_name or 'Ancient' in ore.display_name:
            yield volume.replace(ore.id, '#restworld:ores')
            yield volume.replace('netherrack', '#restworld:ore_background')
            yield volume.replace('soul_sand', 'dirt')
            yield volume.replace('soul_soil', 'andesite')
            yield volume.replace('blackstone', 'diorite')
            yield volume.replace('basalt', 'granite')
        else:
            yield mc.execute().if_().score(deepslate_materials).matches(0).run(
                volume.replace(ore.id, '#restworld:ores'))
            yield mc.execute().if_().score(deepslate_materials).matches(0).run(
                volume.replace('stone', '#restworld:ore_background'))
            yield mc.execute().if_().score(deepslate_materials).matches(1).run(
                volume.replace('deepslate_%s' % ore.id, '#restworld:ores'))
            yield mc.execute().if_().score(deepslate_materials).matches(1).run(
                volume.replace('deepslate', '#restworld:ore_background'))
            yield volume.replace('dirt', 'soul_sand')
            yield volume.replace('andesite', 'soul_soil')
            yield volume.replace('diorite', 'blackstone')
            yield volume.replace('granite', 'basalt')

        if 'Netherite' in item.display_name:
            yield mc.data().merge(r(3, 2, 6), {'Text3': '/ Netherite'})
        if raw:
            if 'Raw' in raw.display_name:
                yield mc.setblock(r(3, 4, 2), '%s_block' % raw.id)
            yield mc.summon(ItemFrame(SOUTH, {'Tags': ['raw_frame', room.name]}).show_item_name(raw.display_name),
                            r(3, 4, 3))
        yield mc.execute().as_(e().tag('ore_ingot_frame').volume((8, 5, 8))).run().data().merge(s(), {
            'Item': Item.nbt_for(item.id)})

    room.loop('ores', main_clock).add(
        mc.kill(e().tag(raw_frame)),
        mc.data().merge(r(3, 2, 6), {'Text3': ''}),
        mc.setblock(r(3, 4, 2), 'air')
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

    basic_functions(room)
    fencelike_functions(room)
    wood_functions(room)


def basic_functions(room):
    stand = Entity('armor_stand', {'Tags': ['basic_stand', 'material_static'], 'ShowArms': True, 'NoGravity': True})
    invis_stand = stand.clone().merge_nbt({'Tags': ['material_static'], 'Invisible': True})
    basic_init = room.function('basic_init').add(
        mc.kill(e().tag('material_static')),
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
        mc.fill(r(-3, 2, 2), r(-3, 5, 2), 'stone'),

        mc.kill(e().tag('armor_frame')),
        mc.summon('item_frame', r(-3, 2, 1), {'Facing': 2, 'Tags': ['armor_boots', 'enchantable', 'armor_frame']}),
        mc.summon('item_frame', r(-3, 3, 1),
                  {'Facing': 2, 'Tags': ['armor_leggings', 'enchantable', 'armor_frame']}),
        mc.summon('item_frame', r(-3, 4, 1),
                  {'Facing': 2, 'Tags': ['armor_chestplate', 'enchantable', 'armor_frame']}),
        mc.summon('item_frame', r(-3, 5, 1), {'Facing': 2, 'Tags': ['armor_helmet', 'enchantable', 'armor_frame']}),
        mc.summon('item_frame', r(3, 2, 1), {'Facing': 2, 'Tags': ['armor_gem', 'armor_frame']}),
        mc.summon('item_frame', r(4, 4, 1),
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

    def do_enchant(to_match, tag):
        return mc.execute().if_().score(enchanted).matches(to_match).as_(e().tag(tag)).run().data()

    def enchant(on):
        if on:
            value, act, arg = 1, lambda prefix, path: prefix.modify(s(), path), lambda prefix: prefix.merge().value(
                {'Enchantments': [{'id': 'mending'}]})
        else:
            value, act, arg = 0, lambda prefix, path: prefix.remove(s(), path), lambda prefix: prefix

        yield arg(act(do_enchant(value, 'enchantable'), 'Item.tag')),
        yield arg(act(do_enchant(value, 'armor_horse'), 'ArmorItem.tag')),
        yield arg(act(do_enchant(value, 'material_static'), 'ArmorItem.tag'))

        for a in range(0, 4):
            yield arg(act(do_enchant(value, 'material_static'), 'ArmorItems[%d].tag' % a))
            if a < 2:
                yield arg(act(do_enchant(value, 'material_static'), 'HandItems[%d].tag' % a))

    horse_saddle = room.score('horse_saddle')
    turtle_helmet = room.score('turtle_helmet')
    elytra = room.score('elytra')

    def basic_loop(step):
        material, armor, horse_armor, background, gem = step.elem

        yield mc.data().merge(
            e().tag('basic_stand').limit(1), {
                'CustomName': material.capitalize(),
                'ArmorItems': [{'id': '%s_boots' % armor, 'Count': 1}, {'id': '%s_leggings' % armor, 'Count': 1},
                               {'id': '%s_chestplate' % armor, 'Count': 1}, {'id': '%s_helmet' % armor, 'Count': 1}]})

        yield mc.fill(r(-3, 2, 2), r(-3, 5, 2), background.id)
        yield mc.setblock(r(3, 2, 2), background.id)
        yield mc.setblock(r(4, 4, 2), background.id)

        yield mc.data().merge(e().tag('armor_boots').limit(1), {
            'Item': {'id': '%s_boots' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield mc.data().merge(e().tag('armor_leggings').limit(1), {
            'Item': {'id': '%s_leggings' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield mc.data().merge(e().tag('armor_chestplate').limit(1), {
            'Item': {'id': '%s_chestplate' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield mc.data().merge(e().tag('armor_helmet').limit(1), {
            'Item': {'id': '%s_helmet' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield mc.data().merge(e().tag('armor_gem').limit(1), {
            'Item': {'id': gem, 'Count': 1}, 'ItemRotation': 0})

        if horse_armor:
            yield mc.execute().unless().entity(e().tag('armor_horse').distance((None, 10))).run(
                room.mob_placer(r(4.5, 2, 0.5), NORTH, adults=True).summon(
                    'horse', nbt={'Variant': 1, 'Tame': True, 'Tags': ['armor_horse', 'material_static']}))
            yield mc.data().merge(e().tag('armor_horse').limit(1).sort('nearest'), {
                'ArmorItem': {'id': '%s_horse_armor' % armor, 'Count': 1}})
            yield mc.data().merge(e().tag('armor_horse_frame').limit(1),
                                  {'Item': {'id': '%s_horse_armor' % armor, 'Count': 1}, 'ItemRotation': 0})
            yield mc.execute().if_().score(horse_saddle).matches(1).run().item().replace().entity(
                e().tag('armor_horse'), 'horse.saddle').with_('saddle')
            yield mc.execute().if_().score(horse_saddle).matches(0).run().item().replace().entity(
                e().tag('armor_horse'), 'horse.saddle').with_('air')
        else:
            yield mc.data().merge(e().tag('armor_horse_frame').limit(1), {
                'Item': {'id': 'air', 'Count': 1}})
            yield mc.execute().if_().entity(e().tag('armor_horse').distance((None, 10))).run(
                kill_em(e().tag('armor_horse')))

        yield mc.data().merge(e().tag('basic_stand').limit(1), {
            'HandItems': [{'id': '%s_sword' % material, 'Count': 1}, {'id': 'shield', 'Count': 1}]})

        hands_row = [None, None, '%s_shovel' % material, '%s_pickaxe' % material, '%s_hoe' % material,
                     '%s_axe' % material, None, None]
        if material == 'wooden':
            hands_row[0] = 'stick'
            hands_row[1] = 'bow'
            hands_row[6] = 'crossbow'
            hands_row[7] = 'fishing_rod'
        elif material == 'iron':
            hands_row[1] = 'flint_and_steel'
            hands_row[6] = 'shears'
            hands_row[7] = 'compass'
        elif material == 'golden':
            hands_row[6] = 'clock'
        hands = list({'id': h if h else '', 'Count': 1} for h in hands_row)

        for j in range(0, 4):
            yield mc.data().merge(e().tag('material_%d' % j).limit(1), {'HandItems': [hands[j], {}]})
        for j in range(4, 8):
            yield mc.data().merge(e().tag('material_%d' % j).limit(1), {'HandItems': [{}, hands[j]]})
        yield mc.data().merge(r(-2, 0, 1), {'name': 'restworld:material_%s' % material, 'mode': 'LOAD'})

    room.loop('basic', main_clock).add(
        mc.fill(r(2, 2, 2), r(-2, 5, 4), 'air'),
        kill_em(e().tag('material_thing'))
    ).loop(basic_loop, materials).add(
        enchant(True),
        enchant(False),
        mc.execute().if_().score(turtle_helmet).matches(1).run().data().modify(
            e().tag('basic_stand').limit(1), 'ArmorItems[3].id').set().value('turtle_helmet'),
        mc.execute().if_().score(turtle_helmet).matches(1).run().data().modify(
            e().tag('armor_helmet').limit(1), 'Item.id').set().value('turtle_helmet'),
        mc.execute().if_().score(elytra).matches(1).run().data().modify(
            e().tag('basic_stand').limit(1), 'ArmorItems[2].id').set().value('elytra'),
        mc.execute().if_().score(elytra).matches(1).run().data().modify(
            e().tag('armor_chestplate').limit(1), 'Item.id').set().value('elytra'),
        mc.fill(r(-2, 2, 2), r(2, 4, 4), 'air'),
        mc.setblock(r(-2, 0, 0), 'redstone_block'),
        mc.execute().positioned(r(-2, 0, 2)).run().kill(e().type('item').volume((5, 3, 4)))
    )

    room.function('basic_update').add(
        mc.execute().at(e().tag('basic_home')).run().function('restworld:materials/basic_cur'),
        mc.execute().at(e().tag('basic_home')).run().function('restworld:materials/basic_finish_main'))


def fencelike_functions(room):
    volume = Volume(r(8, 3, 6), r(0, 2, 0))

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
        yield mc.execute().at(e().tag('fencelike_home')).run().data().merge(r(6, 2, 0), block.sign_nbt)

    def switch_to_fencelike(which):
        room.function('switch_to_%s' % which, home=False).add(
            mc.kill(e().tag('which_fencelike_home')),
            mc.execute().at(e().tag('fencelike_home')).positioned(r(1, -0.5, 0)).run().function(
                'restworld:materials/%s_home' % which),
            mc.tag(e().tag('%s_home' % which)).add('which_fencelike_home'),
            mc.execute().at(e().tag('%s_home' % which)).run().function('restworld:materials/%s_cur' % which))

    def fence_loop(step):
        yield from fencelike(step.elem)
        if step.elem[:-len(' Fence')] in woods + stems:
            yield volume.replace_facing(step.elem + ' Gate', '#restworld:gatelike')

    room.loop('panes', main_clock).loop(lambda step: fencelike(step.elem),
                                        tuple('%s Stained Glass Pane' % x.name for x in colors) + ('Glass Pane',))
    switch_to_fencelike('panes')
    room.loop('fences', main_clock).loop(fence_loop,
                                         tuple('%s Fence' % x for x in woods + stems + ('Nether Brick',)) + (
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
        mc.summon('item_frame', r(2, 3, -3), {
            'Tags': ['wood_boat_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        mc.summon('item_frame', r(3, 3, -3), {
            'Tags': ['wood_sign_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        label(r(-1, 2, 4), 'Chest Boat'))

    volume = Volume(r(-5, 1, -5), r(6, 5, 3))

    def wood_loop(step):
        name = step.elem
        id = _to_id(name)
        if name in stems:
            log = 'stem'
            wood = 'hyphae'
            leaves = 'nether_wart_block' if name == 'Crimson' else '%s_wart_block' % id
            saplings = ('%s_roots' % id, '%s_fungus' % id, '%s_nylium' % id)
        else:
            log = 'log'
            wood = 'wood'
            leaves = '%s_leaves' % id
            saplings = (Block('%s_sapling' % id), Block('%s_sapling' % id, {'stage': 0}), 'grass_block')
            if step.elem == 'Mangrove':
                saplings = (
                    Block('mangrove_propagule', {'age': 1}), Block('mangrove_propagule', {'age': 4}), 'grass_block')

        # Remove special cases
        yield from volume.fill('air', 'vine')
        yield kill_em(e().tag('wood_boat'))
        yield mc.fill(r(4, 2, -1), r(3, 2, -1), 'air')
        yield mc.fill(r(4, 2, 1), r(4, 3, 2), 'air')

        # General replacement
        yield from volume.replace('%s_%s' % (id, wood), '#restworld:woodlike')
        yield from volume.replace(leaves, '#restworld:leaflike')
        yield from volume.replace('%s_planks' % (id), '#planks')
        yield from volume.replace_slabs('%s_slab' % (id), '#slabs')
        yield from volume.replace_stairs('%s_stairs' % (id), '#stairs')
        yield from volume.replace('%s_fence' % id, '#wooden_fences')
        yield from volume.replace_facing('%s_fence_gate' % id, '#restworld:gatelike')
        yield from volume.replace_buttons('%s_button' % (id))
        yield from volume.replace('%s_pressure_plate' % (id), '#pressure_plates')
        yield from volume.replace_axes('%s_%s' % (id, log), '#restworld:loglike')
        yield from volume.replace_axes('stripped_%s_%s' % (id, log), '#restworld:stripped_loglike')
        yield from volume.replace_axes('stripped_%s_%s' % (id, wood), '#restworld:stripped_woodlike')
        yield from volume.replace_doors('%s_door' % (id), '#doors')
        yield from volume.replace_trapdoors('%s_trapdoor' % (id), '#trapdoors')
        yield from volume.replace_facing(Block('%s_wall_sign' % id, nbt={'Text2': '%s Wall Sign' % name}),
                                         '#wall_signs')
        yield from volume.replace(Block('%s_sign' % id, nbt={'Text2': '%s Sign' % name}), '#signs',
                                  added_states=({'rotation': x} for x in range(0, 16, 4)))

        # Add special cases
        if name == ('Jungle', 'Mangrove'):
            yield mc.fill(r(-4, 2, -2), r(-4, 4, -2), ('vine', {'north': True}))

        yield mc.setblock(r(-2, 2, -1), saplings[0])
        yield mc.setblock(r(0, 2, -1), saplings[1])
        yield mc.setblock(r(-2, 1, -1), saplings[2])
        yield mc.setblock(r(0, 1, -1), saplings[2])

        workplace = 'air'
        if id == 'dark_oak':
            workplace = Block('cartography_table')
        elif id == 'oak':
            workplace = Block('lectern', {'facing': WEST})
        elif id == 'birch':
            workplace = Block('fletching_table')
        yield mc.setblock(r(4, 2, 0), workplace)

        yield mc.setblock(r(4, 2, -1), ('%s_door' % id, {'facing': WEST, 'half': 'lower'}))
        yield mc.setblock(r(4, 3, -1), ('%s_door' % id, {'facing': WEST, 'half': 'upper'}))
        yield mc.setblock(r(4, 2, 1), ('%s_door' % id, {'facing': WEST, 'half': 'lower', 'hinge': 'right'}))
        yield mc.setblock(r(4, 3, 1), ('%s_door' % id, {'facing': WEST, 'half': 'upper', 'hinge': 'right'}))
        yield mc.setblock(r(4, 2, 2), ('%s_door' % id, {'facing': WEST, 'half': 'lower'}))
        yield mc.setblock(r(4, 3, 2), ('%s_door' % id, {'facing': WEST, 'half': 'upper'}))

        yield mc.execute().as_(e().tag('wood_sign_frame')).run().data().merge(s(), ItemFrame(NORTH).framed_item(
            '%s_sign' % id).show_item_name('%s Sign' % name).nbt)

        if log == 'log':
            wood_boat_chest = room.score('wood_boat_chest')
            location = r(-0.5, 1.525, 2)
            boat_state = {'Type': id, 'Tags': ['wood_boat', room.name], 'Rotation': [90, 0], 'CustomName': name,
                          'CustomNameVisible': True}
            boat = Entity('boat', boat_state)
            chest_boat = Entity('chest_boat', boat_state)
            yield mc.execute().if_().score(wood_boat_chest).matches(0).run().summon(boat, location)
            yield mc.execute().if_().score(wood_boat_chest).matches(1).run().summon(chest_boat, location)
            yield mc.execute().if_().score(wood_boat_chest).matches(0).as_(
                e().tag('wood_boat_frame')).run().data().merge(s(), ItemFrame(NORTH).framed_item(
                '%s_boat' % id).show_item_name('%s Boat' % name).nbt)
            yield mc.execute().if_().score(wood_boat_chest).matches(1).as_(
                e().tag('wood_boat_frame')).run().data().merge(s(), ItemFrame(NORTH).framed_item(
                '%s_chest_boat' % id).show_item_name('%s Chest Boat' % name).nbt)
        else:
            yield mc.data().remove(e().tag('wood_boat_frame').limit(1), 'Item.id')

    room.loop('wood', main_clock).add(kill_em(e().tag('wood_boat'))).loop(wood_loop, woods + stems)
