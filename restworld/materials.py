from __future__ import annotations

from collections import namedtuple

from pynecraft import info
from pynecraft.base import Arg, EAST, EQ, NE, NORTH, NW, Nbt, NbtDef, RelCoord, SOUTH, WEST, as_facing, r, to_id
from pynecraft.commands import Block, BlockDef, Entity, LONG, MOD, PLUS, RESULT, Score, as_block, data, e, execute, \
    fill, fillbiome, function, item, kill, n, random, s, scoreboard, setblock, summon, tag
from pynecraft.function import BLOCK
from pynecraft.info import armor_equipment, colors, copper_golem_poses, default_skins, must_give_items, operator_menu, \
    stems, \
    trim_materials, trim_patterns, weathering_id, weathering_name, weatherings
from pynecraft.simpler import Item, ItemFrame, PLAINS, Region, SWAMP, Sign, WallSign
from pynecraft.values import COLD_OCEAN, FROZEN_OCEAN, LUKEWARM_OCEAN, MANGROVE_SWAMP, OCEAN, WARM_OCEAN, biomes
from restworld.rooms import Room, erase, kill_em
from restworld.world import fast_clock, main_clock, restworld

water_biomes = (PLAINS, FROZEN_OCEAN, COLD_OCEAN, OCEAN, LUKEWARM_OCEAN, WARM_OCEAN, SWAMP, MANGROVE_SWAMP)


def enchant(score: Score, tag: str):
    for on in (True, False):
        places = tuple(armor_equipment.keys()) + ('saddle', 'mainhand', 'offhand', 'body')
        if on:
            equipment = {}
            enchantment = {'components': {'enchantments': {'mending': 1}}}
            for place in places:
                equipment[place] = enchantment
            commands = [data().merge(s(), {'equipment': equipment, 'Item': enchantment})]
        else:
            commands = [data().remove(s(), 'Item.components.enchantments')]
            for place in places:
                commands.append(data().remove(s(), f'equipment.{place}.components.enchantments'))
        value = int(on)
        yield execute().if_().score(score).matches(value).as_(e().tag(tag)).run(commands)


def room():
    room = Room('materials', restworld, WEST, ('Materials', '& Tools,', 'Time, GUI,', 'Redstone, Maps'))
    room.reset_at((18, 0))

    enchanted = room.score('enchanted')

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

    room.function('arrows_init').add(WallSign(()).place(r(1, 2, 0), WEST), room.label(r(0, 2, -1), 'Fire', EAST))

    fire_arrow = room.score('fire_arrow')

    def arrows_loop(step):
        nbt = {'Tags': ['arrow'], 'NoGravity': True}
        yield summon(step.elem, r(0, 3, 0.25), nbt)
        if step.i == 2:
            # Choose a random color
            yield execute().store(RESULT).entity(e().tag('arrow').limit(1),
                                                 'item.components.potion_contents.custom_color', LONG).run(
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

    wolf_sign_pos = r(0, 2, -1)

    def wolf_armor_color_loop(step):
        color = step.elem
        if color:
            yield data().modify(n().tag('wolf_armor_damage'),
                                'equipment.body.components.dyed_color').set().value(color.leather)
            yield Sign.change(wolf_sign_pos, (None, None, None, f'Color: {step.elem.name}'))
        else:
            yield data().remove(n().tag('wolf_armor_damage'), 'equipment.body.components.dyed_color')
            yield Sign.change(wolf_sign_pos, (None, None, None, 'Color: None'))
        yield enchant(enchanted, 'wolf_armor_damage')

    def wolf_armor_damage_loop(step):
        if step.elem:
            yield data().modify(n().tag('wolf_armor_damage'),
                                'equipment.body.components.damage').set().value(step.elem)
        else:
            yield data().remove(n().tag('wolf_armor_damage'), 'equipment.body.components.damage')
        yield enchant(enchanted, 'wolf_armor_damage')
        yield Sign.change(
            wolf_sign_pos, (None, None, f'Damage: {step.elem}'))

    room.loop('wolf_armor_color', main_clock, home=False).loop(wolf_armor_color_loop, colors + (None,))
    room.loop('wolf_armor_damage', main_clock, home=False).loop(wolf_armor_damage_loop, (None, 19, 40, 60), bounce=True)
    room.function('wolf_armor_init').add(
        room.mob_placer(r(0, 3, 0), NORTH, adults=True).summon(
            Entity('wolf', name='Wolf Armor'), tags=('wolf_armor_damage',),
            nbt={'Owner': 'dummy', 'equipment': {'body': Item.nbt_for('wolf_armor')}}),
        WallSign((None, 'Wolf Armor', 'Damage: None', 'Color: None')).place(wolf_sign_pos, NORTH),
        room.label(r(0, 2, -2), 'Color', NORTH))
    room.function('wolf_armor_home', exists_ok=True).add(tag(e().tag('wolf_armor_home')).add('wolf_armor_damage_home'))
    room.function('wolf_damage', home=False).add(
        tag(e().tag('wolf_armor_home')).remove('wolf_armor_color_home'),
        tag(e().tag('wolf_armor_home')).add('wolf_armor_damage_home'))
    room.function('wolf_color', home=False).add(
        tag(e().tag('wolf_armor_home')).remove('wolf_armor_damage_home'),
        tag(e().tag('wolf_armor_home')).add('wolf_armor_color_home'))

    points = (2, 6, 16, 36, 72, 148, 306, 616, 1236, 2476, 32767)

    def experience_orbs_loop(step):
        i = step.i
        p = points[i]
        f = -32768 if i == 0 else points[i - 1]
        yield summon('experience_orb', r(0, 3, 0), {'Value': p, 'Age': 6000 - 40})
        yield Sign.change(r(1, 2, 0), (None, None, f'Size {i + 1}', f'{f} - {p}'))

    room.loop('experience_orbs', fast_clock).loop(experience_orbs_loop, points)
    room.function('experience_orbs_init').add(WallSign((None, 'Experience Orb')).place(r(1, 2, 0), EAST))

    non_inventory = list(filter(lambda x: x.name not in operator_menu, must_give_items.values()))
    non_inventory.append(Entity('elytra', name='Damaged Elytra', nbt={'components': {'damage': 450}}))

    def only_items_init_func():
        rows = [(-1, len(non_inventory))]
        delta = 1
        x = 1
        items = list(non_inventory)
        yield kill(e().tag('only_item_frame'))
        index = 0
        while len(items) > 0:
            z, end = rows.pop(0)
            for i in range(0, end):
                t = items.pop(0)
                frame = ItemFrame(EAST).item(t).named(t.name)
                frame.tag('materials', 'only_item_frame', f'only_item_frame_{t.id}')
                if t.id == 'elytra':
                    frame.merge_nbt({'Item': {'components': {'damage': 450}}})
                yield frame.summon(r(x, 2, z), facing=EAST)
                z += delta
                index += 1
            x += delta
        yield WallSign((None, 'Items Not', 'In Creative', 'Inventory')).place(r(0, 3, -1), EAST)

    room.function('only_items_init').add(
        only_items_init_func())

    volume = Region(r(0, 1, 0), r(4, 5, 8))
    sign_pos = r(4, 2, 7)
    room.function('sand_init').add(
        WallSign((None, 'Sand &', 'Sandstone')).place(sign_pos, NORTH))

    def sand_loop(step):
        next, prev = [('sand', 'red_sand'), ('red_sand', 'sand')][step.i]
        name = f'{step.elem} Sand &'.strip().title()
        yield Sign.change(
            sign_pos, (None, name))
        for x in ('sand', 'sandstone', 'smooth_sandstone', 'cut_sandstone', 'sandstone_wall', 'chiseled_sandstone'):
            yield volume.replace(x.replace('sand', next), x.replace('sand', prev))
        for x in ('sandstone', 'smooth_sandstone', 'cut_sandstone'):
            yield volume.replace_slabs(x.replace('sand', next) + '_slab', x.replace('sand', prev) + '_slab')
        for x in ('sandstone', 'smooth_sandstone'):
            yield volume.replace_stairs(x.replace('sand', next) + '_stairs', x.replace('sand', prev) + '_stairs')
        yield setblock(r(2, 2, 3), 'suspicious_sand' if next == 'sand' else 'air')

    room.loop('sand', main_clock).loop(sand_loop, ('', 'red'))

    ingot_frame = 'ores_ingot_frame'
    frame = ItemFrame(SOUTH, nbt={'Tags': [room.name, ingot_frame]})
    room.function('ores_init').add(
        summon(frame, r(3, 3, 3)),
        summon(frame.merge_nbt({'Invisible': True}), r(4, 3, 3)),
        room.label(r(3, 2, 7), 'Deepslate', SOUTH))

    raw_frame = 'ore_raw_frame'
    volume = Region(r(8, 5, 6), r(0, 2, -1))
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
                yield setblock(r(3, 4, 2), f'{raw.id}_block')
                yield summon(ItemFrame(SOUTH,
                                       nbt={'Tags': [raw_frame, room.name, 'nugget_frame'],
                                            'Item': Item.nbt_for(raw.name[4:] + ' Nugget')}).named(raw.name),
                             r(3, 5, 3))
            yield summon(ItemFrame(SOUTH, nbt={'Tags': [raw_frame, room.name]}).named(raw.name),
                         r(3, 4, 3))
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

    room.function('water_init').add(
        WallSign((None, 'Flowing Water', 'Biome:')).place(r(0, 2, 0), WEST),
        WallSign((None, 'Flowing Lava')).place(r(0, 2, 6), WEST),
    )
    room.loop('water', main_clock).loop(water_loop, water_biomes)

    def saddles_loop(step):
        mob, pos = step.elem
        yield kill_em(e().tag('saddlable'))
        if isinstance(pos, (float, int)):
            pos = r(0, 2 + pos, 0)
        else:
            pos = RelCoord.add(pos, r(0, 2, 0))
        nbt = {'NoAI': True, 'equipment': {'saddle': Item.nbt_for('saddle')}}
        yield Entity(mob, nbt).tag(
            'materials', 'saddlable').summon(pos, facing=NORTH)
        yield enchant(enchanted, 'saddlable')

    room.loop('saddles', main_clock).loop(
        saddles_loop,
        (('horse', 0), ('zombie_horse', 0.15), ('skeleton_horse', r(0, 0.15, -0.05)), ('mule', 0.23), ('donkey', 0.29),
         ('pig', 0.53), ('strider', -0.32), ('nautilus', 0.3), ('camel', -0.56)))
    room.function('saddles_init').add(
        WallSign((None, 'Saddles')).place(r(0, 2, -2), NORTH))

    basic_functions(room, enchanted)
    fencelike_functions(room)
    wood_functions(room)
    copper_functions(room)
    trim_functions(room)


def basic_functions(room, enchanted):
    invis_stand = Entity('armor_stand',
                         {'Tags': ['basic_stand', 'material_static', 'enchantable'], 'ShowArms': True,
                          'NoGravity': True}).clone().merge_nbt({'Tags': ['material_static'], 'Invisible': True})
    mannequin = Entity('mannequin',
                       {'Tags': ['basic_stand', 'material_static', 'enchantable'], 'immovable': True,
                        'hide_description': True})
    basic_init = room.function('basic_init').add(
        kill(e().tag('material_static')),
        mannequin.summon(r(0, 2.0, 0), facing=NORTH, nbt={'CustomNameVisible': True}))
    for i in range(0, 5):
        basic_init.add(invis_stand.summon(
            r(-(0.8 + i * 0.7), 2.0, 0), facing=NORTH,
            nbt={'LeftHanded': True, 'Tags': ['enchantable', 'material_%d' % (4 + i), 'material_static']}))
        if i < 4:
            basic_init.add(invis_stand.summon(
                r(+(0.6 + i * 0.7), 2.0, 0), facing=NORTH,
                nbt={'Tags': ['enchantable', 'material_%d' % (3 - i), 'material_static']}))

    basic_init.add(fill(r(-3, 2, 2), r(-3, 5, 2), 'stone'), kill(e().tag('armor_frame')),
                   ItemFrame(NORTH).tag('armor_boots', 'enchantable', 'armor_frame').summon(r(-3, 2, 1)),
                   ItemFrame(NORTH).tag('armor_leggings', 'enchantable', 'armor_frame').summon(r(-3, 3, 1)),
                   ItemFrame(NORTH).tag('armor_chestplate', 'enchantable', 'armor_frame').summon(r(-3, 4, 1)),
                   ItemFrame(NORTH).tag('armor_helmet', 'enchantable', 'armor_frame').summon(r(-3, 5, 1)),
                   ItemFrame(NORTH).tag('armor_gem', 'armor_frame').summon(r(3, 2, 3)),
                   ItemFrame(NORTH).tag('armor_horse_frame', 'enchantable', 'armor_frame').summon(r(4, 4, 1)),
                   ItemFrame(NORTH).tag('armor_nautilus_frame', 'enchantable', 'armor_frame').summon(r(4, 3, 1)),
                   room.label(r(5, 2, -2), 'Saddle', NORTH),
                   room.label(r(3, 2, -2), 'Enchanted', NORTH),
                   room.label(r(1, 2, -2), 'Turtle Helmet', NORTH),
                   room.label(r(-1, 2, -2), 'Elytra & Leggings', NORTH))

    Material = namedtuple('Material', ('material', 'armor', 'horse_armor', 'nautilus_armor', 'background', 'gem'))
    materials = (
        Material('stone', 'chainmail', False, False, Block('stone'), 'stone'),
        Material('wooden', 'leather', True, False, Block('oak_planks'), 'oak_sign'),
        Material('copper', 'copper', True, True, Block('copper_block'), 'copper_ingot'),
        Material('iron', 'iron', True, True, Block('iron_block'), 'iron_ingot'),
        Material('golden', 'golden', True, True, Block('gold_block'), 'gold_ingot'),
        Material('diamond', 'diamond', True, True, Block('diamond_block'), 'diamond'),
        Material('netherite', 'netherite', False, True, Block('netherite_block'), 'netherite_ingot'),
    )

    turtle_helmet = room.score('turtle_helmet')
    elytra = room.score('elytra')

    def mannequin_loop(step):
        yield data().modify(n().tag('basic_stand'), 'profile.texture').set().value(f'entity/player/wide/{step.elem}')

    switch_mannequin = room.loop('switch_mannequin', home=False).loop(mannequin_loop, default_skins)

    def basic_loop(step):
        material, armor, horse_armor, nautilus_armor, background, gem = step.elem

        if step.i == 0:
            yield function(switch_mannequin)
        yield data().merge(
            e().tag('basic_stand').limit(1), {
                'CustomName': material.capitalize(),
                'equipment': {
                    'feet': Item.nbt_for('%s_boots' % armor), 'legs': Item.nbt_for('%s_leggings' % armor),
                    'chest': Item.nbt_for('%s_chestplate' % armor), 'head': Item.nbt_for('%s_helmet' % armor)}})

        yield fill(r(-3, 2, 2), r(-3, 5, 2), background.id)
        yield setblock(r(3, 2, 4), background.id)
        yield fill(r(4, 3, 2), r(4, 4, 2), background.id)

        yield data().merge(e().tag('armor_boots').limit(1), {'Item': {'id': '%s_boots' % armor}, 'ItemRotation': 0})
        yield data().merge(e().tag('armor_leggings').limit(1),
                           {'Item': {'id': '%s_leggings' % armor}, 'ItemRotation': 0})
        yield data().merge(e().tag('armor_chestplate').limit(1),
                           {'Item': {'id': '%s_chestplate' % armor}, 'ItemRotation': 0})
        yield data().merge(e().tag('armor_helmet').limit(1), {'Item': {'id': '%s_helmet' % armor}, 'ItemRotation': 0})
        yield data().merge(e().tag('armor_gem').limit(1), {'Item': {'id': gem, 'Count': 1}, 'ItemRotation': 0})

        yield from armored_mob(armor, 'horse', horse_armor, r(5, 2, 0.5), NORTH)
        yield from armored_mob(armor, 'nautilus', nautilus_armor, r(3, 2, 0.75), EAST)

        yield data().merge(e().tag('basic_stand').limit(1),
                           {'equipment': {'mainhand': Item.nbt_for('%s_sword' % material),
                                          'offhand': Item.nbt_for('shield')}})

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
        for j in range(0, 8):
            hand = 'mainhand' if j < 4 else 'offhand'
            who = e().tag('material_%d' % j).limit(1)
            thing = hands_row[j]
            if thing:
                yield data().merge(who, {'equipment': {hand: Item.nbt_for(thing)}})
            else:
                yield data().remove(who, f'equipment.{hand}')
        yield data().merge(r(-2, 0, 1), {'name': f'restworld:material_{material}', 'mode': 'LOAD'})

    def armored_mob(armor, mob, has_armor, pos, dir):
        if has_armor:
            has_saddle = room.score(f'{mob}_saddle')
            yield execute().unless().entity(e().tag(f'armor_{mob}').distance((None, 10))).run(
                room.mob_placer(pos, dir, adults=True).summon(
                    mob,
                    nbt={'Variant': 1, 'Tame': True, 'Tags': [f'armor_{mob}', 'enchantable', 'material_static']}))
            yield data().merge(n().tag(f'armor_{mob}').limit(1),
                               {'equipment': {'body': Item.nbt_for(f'{armor}_{mob}_armor')}})
            yield data().merge(e().tag(f'armor_{mob}_frame').limit(1),
                               {'Item': Item.nbt_for(f'{armor}_{mob}_armor'), 'ItemRotation': 0})
            yield execute().if_().score(has_saddle).matches(1).run(
                item().replace().entity(e().tag(f'armor_{mob}'), 'saddle').with_('saddle'))
            yield execute().if_().score(has_saddle).matches(0).run(
                data().remove(e().tag(f'armor_{mob}').limit(1), 'equipment.saddle'))
        else:
            yield data().remove(e().tag(f'armor_{mob}_frame').limit(1), 'Item')
            yield execute().if_().entity(e().tag(f'armor_{mob}').distance((None, 10))).run(
                kill_em(e().tag(f'armor_{mob}')))

    which_elytra = room.score('which_elytra')
    basic_init.add(which_elytra.set(0))
    basic = room.loop('basic', main_clock)
    basic.add(
        erase(r(2, 2, 2), r(-2, 5, 4)),
        kill_em(e().tag('material_thing'))
    ).loop(basic_loop, materials).add(
        execute().if_().score(turtle_helmet).matches(1).run(
            data().modify(n().tag('basic_stand'), 'equipment.head.id').set().value('turtle_helmet'),
            data().modify(n().tag('armor_helmet'), 'Item.id').set().value('turtle_helmet')),
        execute().if_().score(elytra).matches(1).run(
            data().modify(n().tag('basic_stand'), 'equipment.chest.id').set().value('elytra'),
            data().modify(n().tag('armor_chestplate'), 'Item.id').set().value('elytra'),
            which_elytra.add(1),
            execute().if_().score(which_elytra).matches((2, None)).run(which_elytra.set(0)),
            execute().if_().score(which_elytra).matches(1).run(
                data().modify(n().tag('basic_stand'), 'equipment.chest.components.damage').set().value(450),
                data().modify(n().tag('armor_chestplate'), 'Item.components.damage').set().value(450)
            ),
            execute().unless().score(which_elytra).matches(1).run(
                data().modify(n().tag('basic_stand'), 'equipment.chest.components.damage').set().value(0),
                data().modify(n().tag('armor_chestplate'), 'Item.components.damage').set().value(0)
            )
        ),
        enchant(enchanted, 'enchantable'),
        fill(r(-2, 2, 2), r(2, 4, 4), 'air'),
        setblock(r(-2, 0, 0), 'redstone_block'),
        execute().positioned(r(-2, 0, 2)).run(kill(e().type('item').volume((5, 3, 4)))))

    room.function('basic_update').add(
        execute().at(e().tag('basic_home')).run(function('restworld:materials/basic_cur')),
        execute().at(e().tag('basic_home')).run(function('restworld:materials/basic_finish_main')),
        execute().at(e().tag('wolf_armor_home')).run(function('restworld:materials/wolf_armor_color_cur')),
        execute().at(e().tag('wolf_armor_home')).run(function('restworld:materials/wolf_armor_damage_cur')),
        execute().at(e().tag('saddles_home')).run(function('restworld:materials/saddles_cur')),
    )


def fencelike_functions(room):
    volume = Region(r(4, 3, 6), r(0, 2, -1))

    fencelike_sign_pos = r(5, 2, -1)
    room.function('fencelike_init').add(
        WallSign(()).place(fencelike_sign_pos, NORTH),
        room.label(r(6, 2, -2), 'Height', NORTH), room.label(r(4, 2, -2), 'Glass Panes', NORTH),
        room.label(r(3, 2, -2), 'Walls', NORTH), room.label(r(2, 2, -2), 'Fences', NORTH),
        room.label(r(1, 2, -2), 'Bars', NORTH)
    )

    def fencelike(block: BlockDef):
        block = as_block(block)
        yield volume.replace(block, '#restworld:fencelike')
        yield execute().at(e().tag('fencelike_home')).run(data().merge(fencelike_sign_pos, block.sign_nbt(front=None)))

    def switch_to_fencelike(which):
        room.function(f'switch_to_{which}', home=False).add(
            kill(e().tag('which_fencelike_home')),
            execute().at(e().tag('fencelike_home')).positioned(r(1, -0.5, 0)).run(
                function('restworld:materials/%s_home' % which)),
            tag(e().tag('%s_home' % which)).add('which_fencelike_home'),
            execute().at(e().tag('%s_home' % which)).run(
                function('restworld:materials/%s_cur' % which)))

    def fence_loop(step):
        yield from fencelike(step.elem)
        if step.elem[:-len(' Fence')] in info.woods + stems:
            yield volume.replace_facing(step.elem + ' Gate', '#fence_gates')

    room.loop('panes', main_clock).loop(lambda step: fencelike(step.elem),
                                        tuple(f'{x.name}|Stained Glass|Pane' for x in colors) + ('Glass Pane',))
    switch_to_fencelike('panes')
    room.loop('fences', main_clock).loop(fence_loop,
                                         tuple(f'{x} Fence' for x in info.woods + stems + ('Nether Brick',)))
    switch_to_fencelike('fences')
    room.loop('walls', main_clock).loop(lambda step: fencelike(step.elem), (x + ' Wall' for x in (
        'Cobblestone', 'Mossy|Cobblestone', 'Sandstone', 'Red|Sandstone', 'Brick', 'Mud|Brick', 'Stone|Brick',
        'Mossy Stone|Brick', 'Resin Brick', 'Nether|Brick', 'Red Nether|Brick', 'End Stone|Brick',
        'Polished|Blackstone|Brick', 'Polished|Blackstone', 'Blackstone', 'Andesite', 'Granite', 'Diorite',
        'Deepslate|Brick', 'Deepslate|Tile', 'Cobbled|Deepslate', 'Polished|Deepslate', 'Prismarine'
    )))
    switch_to_fencelike('walls')
    waxed_ = tuple(f'{x} Bars' for x in
                   ('Iron', *tuple(w + weathering_name(x, join='|') for x in weatherings for w in ('', 'Waxed|'))))
    room.loop('bars', main_clock).loop(lambda step: fencelike(step.elem), waxed_)
    switch_to_fencelike('bars')


def copper_functions(room):
    tags = restworld.tags(BLOCK)

    copper_sign_pos = r(4, 2, -1)

    def copper_tags(type) -> None:
        blocks = list(weathering_id(x, base=type) for x in weatherings)
        if blocks[0] == 'copper':
            blocks[0] += '_block'
        tag_name = type
        if tag_name[-1] != 's':
            tag_name += 's'
        blocks.extend(list('waxed_' + b for b in blocks))
        tags[tag_name] = {'values': blocks}

    volume = Region(r(0, 1, 0), r(5, 5, 6))
    copper_tags('copper')
    copper_tags('cut_copper')
    copper_tags('chiseled_copper')
    copper_tags('copper_grate')
    copper_tags('copper_bulb')
    copper_tags('cut_copper_stairs')
    copper_tags('cut_copper_slab')
    copper_tags('copper_door')
    copper_tags('copper_trapdoor')
    copper_tags('copper_chest')
    copper_tags('copper_golem_statue')

    def copper_loop(step):
        type: str = step.elem.lower()
        basic = 'copper'
        if type in ('', 'waxed'):
            basic += '_block'
        if len(type) > 0:
            type += '_'
        yield Sign.change(copper_sign_pos, (None, type.replace('_', ' ').title()))
        yield from volume.replace(type + basic, '#restworld:coppers')
        yield from volume.replace(type + 'lightning_rod', '#lightning_rods')
        yield from volume.replace(type + 'cut_copper', '#restworld:cut_coppers')
        yield from volume.replace(type + 'chiseled_copper', '#restworld:chiseled_coppers')
        yield from volume.replace(type + 'copper_grate', '#restworld:copper_grates')
        yield from volume.replace(type + 'copper_bulb', '#restworld:copper_bulbs', {'lit': True})
        yield from volume.replace(type + 'copper_bulb', '#restworld:copper_bulbs', {'lit': False})
        yield from volume.replace(type + 'copper_bars', '#bars')
        yield from volume.replace(type + 'copper_lantern', '#lanterns')
        yield from volume.replace_axes(type + 'copper_chain', '#chains')
        yield from volume.replace_stairs(type + 'cut_copper_stairs', '#stairs')
        yield from volume.replace_slabs(type + 'cut_copper_slab', '#restworld:cut_copper_slabs')
        # doors can't be generically replaced, see below for the manual placement
        yield from volume.replace_trapdoors(type + 'copper_trapdoor', '#restworld:copper_trapdoors')
        yield from volume.replace_facing(type + 'copper_chest', '#copper_chests')
        # yield from volume.replace_facing(type + 'copper_chest', '#copper_chests', shared_states={'type': 'left'})
        # yield from volume.replace_facing(type + 'copper_chest', '#copper_chests', shared_states={'type': 'right'})
        yield from (
            volume.replace_facing(type + 'copper_golem_statue', '#restworld:copper_golem_statues',
                                  shared_states={'copper_golem_pose': x})
            for x in copper_golem_poses)

        # The door won't be set unless we manually remove previous one.
        yield erase(r(0, 2, 4), r(0, 3, 4))
        yield setblock(r(0, 2, 4), (type + 'copper_door', {'facing': NORTH, 'half': 'lower'})).replace()
        yield setblock(r(0, 3, 4), (type + 'copper_door', {'facing': NORTH, 'half': 'upper'})).replace()
        yield fill(r(1, 2, 3), r(0, 2, 3), 'air')  # currently needed, or the setblocks are ignored, even with replace
        yield setblock(r(1, 2, 3), (type + 'copper_chest', {'type': 'right'}))
        yield setblock(r(0, 2, 3), (type + 'copper_chest', {'type': 'left'}))

        yield item().replace().entity(n().tag('copper_door_frame'), 'container.0').with_(Item(type + 'copper_door'))

        sign_text = ['', type.replace('_', ' ').title(), 'Copper', '']
        yield Sign.change(r(2, 2, 0), sign_text)

    # Share a score so we only change 'waxness', not oxidization level
    copper_score = room.score('coppers')
    room.loop('unwaxed_coppers', main_clock, score=copper_score).loop(copper_loop, weatherings)
    room.loop('waxed_coppers', main_clock, score=copper_score).loop(
        copper_loop, (f'waxed_{x}'.strip('_') for x in weatherings))
    copper_home = e().tag('coppers_home')
    run_unwaxed = room.function('unwaxed_coppers_run', home=False).add(
        tag(copper_home).remove('waxed_coppers_home'),
        tag(copper_home).add('unwaxed_coppers_home'),
        execute().at(copper_home).run(function('restworld:materials/unwaxed_coppers_cur')))
    room.function('waxed_coppers_run', home=False).add(
        tag(copper_home).remove('unwaxed_coppers_home'),
        tag(copper_home).add('waxed_coppers_home'),
        execute().at(copper_home).run(function('restworld:materials/waxed_coppers_cur')))
    room.function('coppers_init').add(
        room.label(r(3, 2, -2), 'Waxed', NORTH),
        function(run_unwaxed),
        ItemFrame(NORTH).tag('materials', 'copper_door_frame').summon(r(0, 4, 4)),
        WallSign((None, None, 'Copper')).place(copper_sign_pos, NORTH))


def wood_functions(room):
    room.function('wood_init').add(
        summon('item_frame', r(2, 3, -3), {
            'Tags': ['wood_boat_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        summon('item_frame', r(2, 4, -3), {
            'Tags': ['wood_door_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        summon('item_frame', r(3, 3, -3), {
            'Tags': ['wood_sign_frame', room.name], 'Facing': 3, 'Fixed': True, 'Item': {'id': 'stone', 'Count': 1}}),
        summon('item_frame', r(3, 4, -3), {
            'Tags': ['wood_hanging_sign_frame', room.name], 'Facing': 3, 'Fixed': True,
            'Item': {'id': 'stone', 'Count': 1}}),
        room.label(r(-1, 2, 4), 'Chest Boat', SOUTH),
    )

    volume = Region(r(-5, 1, -4), r(4, 5, 3))

    def wood_loop(step):
        def sign_messages(nbt):
            return Nbt({'front_text': nbt, 'back_text': nbt})

        name = step.elem
        root_name = name.replace(' Mosaic', '')
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
        yield from volume.replace_facing(f'{id}_shelf', '#wooden_shelves')
        yield from volume.replace_buttons(f'{id}_button')
        yield from volume.replace(f'{id}_pressure_plate', '#pressure_plates')
        yield from volume.replace_axes(log, '#restworld:loglike')
        yield from volume.replace_axes(f'stripped_{log}', '#restworld:stripped_loglike')
        yield from volume.replace_axes(f'stripped_{wood}', '#restworld:stripped_woodlike')
        # doors can't be generically replaced, see below for the manual placement
        yield from volume.replace_trapdoors(f'{id}_trapdoor', '#trapdoors')
        text_color = 'white' if id in {'mangrove', 'dark_oak', 'crimson'} else 'black'
        yield from volume.replace_facing(
            WallSign((), wood=id).messages((None, root_name, 'Wall Sign')).wax(False).color(text_color), '#wall_signs')
        yield from volume.replace_rotation(
            Sign((), wood=id).messages((None, f'{root_name} Sign')).wax(False).color(text_color), '#signs')

        yield from volume.replace_facing(
            Block(f'{id}_wall_hanging_sign', nbt=sign_messages(
                Sign.lines_nbt((root_name, 'Wall', 'Hanging', 'Sign')).merge({'color': text_color}))),
            '#wall_hanging_signs')
        for attached in True, False:
            sign_text = (Sign.lines_nbt((root_name, 'Attached', 'Hanging', 'Sign')) if attached else Sign.lines_nbt(
                (root_name, 'Hanging', 'Sign'))).merge({'color': text_color})
            yield from volume.replace_rotation(
                Block(f'{id}_hanging_sign', nbt=sign_messages(sign_text)),
                '#all_hanging_signs',
                shared_states={'attached': attached})

        # Add special cases
        yield from volume.fill('air', 'vine')  # remove any existing vine
        if name in ('Jungle', 'Mangrove'):
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
        yield erase(r(4, 2, -1), r(4, 3, -1))
        yield erase(r(4, 2, 1), r(4, 3, 2))
        yield setblock(r(4, 2, -1), (f'{id}_door', {'facing': WEST, 'half': 'lower'}))
        yield setblock(r(4, 3, -1), (f'{id}_door', {'facing': WEST, 'half': 'upper'}))
        yield setblock(r(4, 2, 1), (f'{id}_door', {'facing': WEST, 'half': 'lower', 'hinge': 'right'}))
        yield setblock(r(4, 3, 1), (f'{id}_door', {'facing': WEST, 'half': 'upper', 'hinge': 'right'}))
        yield setblock(r(4, 2, 2), (f'{id}_door', {'facing': WEST, 'half': 'lower'}))
        yield setblock(r(4, 3, 2), (f'{id}_door', {'facing': WEST, 'half': 'upper'}))

        yield execute().as_(e().tag('wood_sign_frame')).run(
            data().merge(s(), ItemFrame(SOUTH).item(f'{id}_sign').named(f'{root_name} Sign').nbt))
        yield execute().as_(e().tag('wood_hanging_sign_frame')).run(
            data().merge(s(), ItemFrame(SOUTH).item(f'{id}_hanging_sign').named(f'{root_name} Hanging Sign').nbt))
        yield execute().as_(e().tag('wood_door_frame')).run(
            data().merge(s(), ItemFrame(SOUTH).item(f'{id}_door').named(f'{root_name} Door').nbt))

        yield kill_em(e().tag('wood_boat'))  # remove existing boat
        boat_state = Nbt({'Type': id, 'Tags': ['wood_boat', room.name], 'CustomName': name,
                          'CustomNameVisible': True})
        location = r(-0.5, 1.525, 2)
        if 'stem' not in log:
            wood_boat_chest = room.score('wood_boat_chest')
            boat_item = f'{id}_boat'
            chest_boat_item = f'{id}_chest_boat'
            if 'bamboo' in log:
                boat_item = 'bamboo_raft'
                chest_boat_item = 'bamboo_chest_raft'
            boat = Entity(boat_item, boat_state)
            chest_boat = Entity(chest_boat_item, boat_state)
            yield execute().if_().score(wood_boat_chest).matches(0).run(summon(boat, location))
            yield execute().if_().score(wood_boat_chest).matches(1).run(summon(chest_boat, location))
            yield execute().if_().score(wood_boat_chest).matches(0).as_(
                e().tag('wood_boat_frame')).run(
                data().merge(s(), ItemFrame(SOUTH).item(boat_item).named(f'{root_name} Boat').nbt))
            yield execute().if_().score(wood_boat_chest).matches(1).as_(
                e().tag('wood_boat_frame')).run(
                data().merge(s(), ItemFrame(SOUTH).item(chest_boat_item).named(f'{root_name} Chest Boat').nbt))
        else:
            location = list(location)
            location[1] -= 0.43
            boat_state = boat_state.merge({'Small': True, 'NoGravity': True, 'Invisible': True})
            yield summon(Entity('armor_stand', boat_state), location)
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
    items = {}
    for place, piece in armor_equipment.items():
        items[place] = Item.nbt_for(f'{kind}_{piece}', base_nbt)
    stand.merge_nbt({'equipment': items})


def trim_functions(room):
    overall_tag = 'trim_stand'
    base_stand = Entity('armor_stand',
                        {'ShowArms': True,
                         'Pose': {'LeftArm': [-20, 0, -140], 'RightArm': [-20, 0, 20],
                                  'LeftLeg': [-20, 0, 0], 'RightLeg': [20, 0, 0]}}).tag(room.name, overall_tag)
    places = [None, None]
    places[0] = [
        (r(2, 2, -5), WEST),
        (r(3, 3, -4), WEST),
        (r(2, 2, -3), WEST),
        (r(3, 3, -2), WEST),
        (r(2, 2, -1), WEST),
        (r(3, 3, 0), WEST),

        (r(2, 2, 1), NW),
        (r(1, 3, 2), NORTH),
        (r(0, 2, 1), NORTH),
        (r(-1, 2, 1), NORTH),
        (r(-2, 3, 2), NORTH),
        (r(-3, 2, 1), NE),

        (r(-4, 3, 0), EAST),
        (r(-3, 2, -1), EAST),
        (r(-4, 3, -2), EAST),
        (r(-3, 2, -3), EAST),
        (r(-4, 3, -4), EAST),
        (r(-3, 2, -5), EAST),
    ]
    mid = int(len(places[0]) / 2)
    places[1] = places[0][:mid] + [(r(-0.5, 3, 2), NORTH)] + places[0][mid:]

    show = room.score('trim_show')
    change = room.score('trim_change')
    adjust_change = room.score('trim_adjust_change')
    num_categories = room.score_max('TRIMS')
    facing = NORTH

    frame = 'trim_frame'
    trim_nbt = {'components': {'trim': {'pattern': 'sentry', 'material': 'redstone'}}}
    room.function('trim_init').add(
        kill(e().tag(frame)),
        ItemFrame(NORTH).item('iron_boots').merge_nbt(
            {'Item': trim_nbt}).tag('materials', frame, f'{frame}_boots').summon(r(1, 5, 2)),
        ItemFrame(NORTH).item('iron_leggings').merge_nbt(
            {'Item': trim_nbt}).tag('materials', frame, f'{frame}_leggings').summon(r(0, 5, 2)),
        ItemFrame(NORTH).item('iron_chestplate').merge_nbt(
            {'Item': trim_nbt}).tag('materials', frame, f'{frame}_chestplate').summon(r(-1, 5, 2)),
        ItemFrame(NORTH).item('iron_helmet').merge_nbt(
            {'Item': trim_nbt}).tag('materials', frame, f'{frame}_helmet').summon(r(-2, 5, 2)),
        WallSign().messages((None, 'Material:')).place(r(0, 6, 2), NORTH),
        WallSign().messages((None, 'Armor:', 'Iron')).place(r(-1, 6, 2), NORTH))

    class Trim:
        _num = 0

        def __init__(self, name: str, types, armor_gen, nbt_path):
            self.name = name
            self.types = types
            self.tag = f'trim_{name}'
            self.armor_gen = armor_gen
            self.nbt_path = nbt_path

            self.num = Trim._num
            Trim._num += 1
            self.init = room.function(f'trim_{name}_init').add(self._init())
            self.detect = room.function(f'trim_{name}_detect', home=False).add(self._detect())
            self.loop = room.loop(f'trim_{name}', main_clock).loop(self._loop_func, types)

        def _init(self):
            yield kill(e().tag(overall_tag))
            which_places = len(self.types) % 2
            places_used = places[which_places]
            stand_start = int((len(places_used) - len(self.types)) / 2)
            for i, t in enumerate(self.types):
                stand = base_stand.clone().tag(self.tag).merge_nbt({'CustomName': t.title()})
                self.armor_gen(stand, t)
                loc = places_used[stand_start + i]
                yield stand.summon(loc[0], {'Rotation': as_facing(loc[1]).rotation})
            yield show.set(self.num)

        def _loop_func(self, step):
            for place in armor_equipment.keys():
                yield execute().as_(e().tag(overall_tag)).run(
                    data().modify(s(), f'equipment.{place}.{self.nbt_path}').set().value(step.elem))
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
            return ('equipment.feet.' + self.nbt_path)[::-1].replace('.', '{', 1)[::-1] + ':' + f'"minecraft:{t}"' + '}'

    class Armors(Trim):
        def __init__(self, name: str, types, armor_gen):
            super().__init__(name, types, armor_gen, 'id')

        def _loop_func(self, step):
            for place, piece in armor_equipment.items():
                which = f'{step.elem}_{piece}'
                yield execute().as_(e().tag(overall_tag)).run(
                    data().modify(s(), f'equipment.{place}.{self.nbt_path}').set().value(which))
                yield execute().as_(e().tag(f'{frame}_{piece}')).run(
                    data().modify(s(), f'Item.{self.nbt_path}').set().value(which))
            yield execute().at(e().tag('trim_change_home')).run(
                Sign.change(r(0, 2, 0), (None, None, None, step.elem.title())))
            yield from self._trim_frame_sign(step)

        def _to_path(self, t):
            return f'equipment.feet{{id:"minecraft:{t}_boots"}}'

    categories = {
        'patterns': Trim('patterns', trim_patterns,
                         lambda stand, type: armor_for(stand, 'iron', {'components': {'trim': {'pattern': type}}}),
                         'components.minecraft:trim.pattern'),
        'materials': Trim('materials', trim_materials,
                          lambda stand, type: armor_for(stand, 'iron', {'components': {'trim': {'material': type}}}),
                          'components.minecraft:trim.material'),
        'armors': Armors('armors', info.armors, lambda stand, type: armor_for(stand, type))}

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
    change_init.add(
        room.label(r(-1, 2, -1), 'Leggings', NORTH), room.label(r(1, 2, -1), 'Turtle Helmet', NORTH),
        room.label(r(3, 2, -1), 'Labels', NORTH))

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
        lines = (None, 'Show All:', cat.name.title())
        show_menu.add(WallSign().messages(lines, commands=(show.set(i), run_show_cleanup)).place(r(0, i, 0), facing))
        show_cleanup.add(execute().if_().score(show).matches(i).run(
            WallSign().messages(lines, commands=(function(show_menu),)).place(r(0, 2, 0), facing),
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
                WallSign().messages(lines, commands=(change.set(j), run_change_cleanup)).place(r(0, sign_num, 0),
                                                                                               facing)))
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

    room.function('trim_chestplate_off', home=False).add(
        execute().as_(e().tag(overall_tag)).run(data().remove(s(), 'equipment.feet'),
                                                data().remove(s(), 'equipment.chest')))

    chestplate_on = room.function('trim_chestplate_on', home=False)
    for armor in info.armors:
        chestplate_on.add(
            execute().as_(e().tag(overall_tag).nbt({'equipment': {'legs': {'id': f'minecraft:{armor}_leggings'}}})).run(
                item().replace().entity(s(), 'armor.feet').with_(f'{armor}_boots'),
                item().replace().entity(s(), 'armor.chest').with_(f'{armor}_chestplate')))
    chestplate_on.add(execute().as_(e().tag(overall_tag)).run(
        data().modify(s(), 'equipment.feet.components.trim').merge().from_(s(),
                                                                           'equipment.legs.components.trim'),
        data().modify(s(), 'equipment.chest.components.trim').merge().from_(s(),
                                                                            'equipment.legs.components.trim')))

    room.function('trim_turtle_on', home=False).add(
        execute().as_(e().tag(overall_tag)).run(
            data().modify(s(), 'equipment.head.id').set().value('turtle_helmet')))
    turtle_off = room.function('trim_turtle_off', home=False)
    for armor in info.armors:
        turtle_off.add(
            execute().as_(e().tag(overall_tag).nbt({'equipment': {'legs': {'id': f'minecraft:{armor}_leggings'}}})).run(
                data().modify(s(), 'equipment.head.id').set().value(f'{armor}_helmet')))
