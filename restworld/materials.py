from __future__ import annotations

from pyker.commands import mc, r, Block, WEST, entity, EAST, Entity, SOUTH, self
from pyker.simpler import WallSign
from restworld.rooms import Room, label
from restworld.world import restworld, main_clock, kill_em


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
    assert len(blocks) == 2

    fill = (r(0, 1, 0), r(10, 6, 7))

    def all_sand_loop(step):
        i = step.i
        for j in range(0, len(blocks[i])):
            o = 1 - i
            pl_id, sl_id, st_id = blocks[i][j], slabs[i][j], stairs[i][j]
            opl_id, osl_id, ost_id = blocks[o][j], slabs[o][j], stairs[o][j]
            pl, sl, st = Block(pl_id) if pl_id else None, Block(sl_id) if sl_id else None, Block(
                st_id) if st_id else None
            opl, osl, ost = Block(opl_id) if opl_id else None, Block(osl_id) if osl_id else None, Block(
                ost_id) if ost_id else None
            yield mc.fill(*fill, Block(walls[i]).kind).replace(Block(walls[o]).kind)
            yield mc.fill(*fill, pl.kind).replace(opl.kind)

            if sl:
                yield mc.fill(*fill, Block(sl.kind, {'type': 'double'})).replace(Block(osl.kind, {'type': 'double'}))
                for t in ('top', 'bottom'):
                    yield mc.fill(*fill, Block(sl.kind, {'type': t})).replace(Block(osl.kind, {'type': t}))
                if st:
                    for f in ('north', 'east', 'west', 'south'):
                        yield mc.fill(*fill, Block(st.kind, state={'half': t, 'facing': f})).replace(
                            Block(ost.kind, {'half': t, 'facing': f}))
                        for s in ('inner_left', 'inner_right', 'outer_left', 'outer_right'):
                            yield mc.fill(*fill,
                                          Block(st.kind, state={'half': t, 'facing': f, 'shape': s})).replace(
                                Block(ost.kind, {'half': t, 'facing': f, 'shape': s}))

        yield mc.data().merge(r(0, 2, 3), {'Text2': blocks[i][0]})

    room.loop('all_sand', main_clock).loop(all_sand_loop, range(0, 2))

    room.function('arrows_init').add(WallSign(()).place(r(1, 2, 0), EAST))

    def arrows_loop(step):
        yield mc.summon(step.elem, r(0, 3, 0.25), {
            'Tags': ['arrow'], 'NoGravity': True, 'Color': 127, 'CustomPotionColor': 127 if step.i == 2 else ''})
        yield mc.data().merge(r(1, 2, 0), {'Text2': step.elem.display_name})

    room.loop('arrows', main_clock).add(
        mc.kill(entity().tag('arrow'))
    ).loop(arrows_loop, (
        Block('Arrow'),
        Block('Spectral Arrow'),
        Block('arrow', display_name='Tipped Arrow')))

    basic_functions(room)


def basic_functions(room):
    stand = Entity('armor_stand', {'Tags': ['basic_stand', 'material_static'], 'ShowArms': True, 'NoGravity': True})
    invis_stand = stand.clone().merge_nbt({'Tags': ['material_static'], 'Invisible': True})
    basic_init = room.function('basic_init').add(
        mc.kill(entity().tag('material_static')),
        stand.summon(r(0, 2.0, 0), facing=SOUTH, nbt={'CustomNameVisible': True}),
    )
    for i in range(0, 5):
        basic_init.add(
            invis_stand.summon(r(-(0.8 + i * 0.7), 2.0, 0), facing=SOUTH, nbt={'Tags': ['material_%d' % (4 + i), 'material_static']}))
        if i < 4:
            basic_init.add(
                invis_stand.summon(r(+(0.6 + i * 0.7), 2.0, 0), facing=SOUTH, nbt={'Tags': ['material_%d' % (3 - i), 'material_static']}))

    basic_init.add(
        mc.fill(r(-3, 2, 2), r(-3, 5, 2), 'stone'),

        mc.kill(entity().tag('armor_frame')),
        mc.summon('item_frame', r(-3, 2, 1), {'Facing': 2, 'Tags': ['armor_boots', 'enchantable', 'armor_frame']}),
        mc.summon('item_frame', r(-3, 3, 1),
                  {'Facing': 2, 'Tags': ['armor_leggings', 'enchantable', 'armor_frame']}),
        mc.summon('item_frame', r(-3, 4, 1),
                  {'Facing': 2, 'Tags': ['armor_chestplate', 'enchantable', 'armor_frame']}),
        mc.summon('item_frame', r(-3, 5, 1), {'Facing': 2, 'Tags': ['armor_helmet', 'enchantable', 'armor_frame']}),
        mc.summon('item_frame', r(3, 2, 1), {'Facing': 2, 'Tags': ['armor_gem', 'armor_frame']}),
        mc.summon('item_frame', r(4, 4, 1),
                  {'Facing': 2, 'Tags': ['armor_horse_frame', 'enchantable', 'armor_frame']}),

        label((5, 2, -2), 'Saddle'),
        label((3, 2, -2), 'Enchanted'),
        label((1, 2, -2), 'Turtle Helmet'),
        label((-1, 2, -2), 'Elytra'),
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
        return mc.execute().if_().score(enchanted).matches(to_match).as_(entity().tag(tag)).run().data()

    def enchant(on):
        if on:
            value, act, arg = 1, lambda prefix, path: prefix.modify(self(), path), lambda prefix: prefix.merge().value(
                {'Enchantments': [{'id': 'mending'}]})
        else:
            value, act, arg = 0, lambda prefix, path: prefix.remove(self(), path), lambda prefix: prefix

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
            entity().tag('basic_stand').limit(1), {
                'CustomName': material.capitalize(),
                'ArmorItems': [{'id': '%s_boots' % armor, 'Count': 1}, {'id': '%s_leggings' % armor, 'Count': 1},
                               {'id': '%s_chestplate' % armor, 'Count': 1}, {'id': '%s_helmet' % armor, 'Count': 1}]})

        yield mc.fill(r(-3, 2, 2), r(-3, 5, 2), background.kind)
        yield mc.setblock(r(3, 2, 2), background.kind)
        yield mc.setblock(r(4, 4, 2), background.kind)

        yield mc.data().merge(entity().tag('armor_boots').limit(1), {
            'Item': {'id': '%s_boots' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield mc.data().merge(entity().tag('armor_leggings').limit(1), {
            'Item': {'id': '%s_leggings' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield mc.data().merge(entity().tag('armor_chestplate').limit(1), {
            'Item': {'id': '%s_chestplate' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield mc.data().merge(entity().tag('armor_helmet').limit(1), {
            'Item': {'id': '%s_helmet' % armor, 'Count': 1}, 'ItemRotation': 0})
        yield mc.data().merge(entity().tag('armor_gem').limit(1), {
            'Item': {'id': gem, 'Count': 1}, 'ItemRotation': 0})

        if horse_armor:
            yield mc.execute().unless().entity(entity().tag('armor_horse').distance((None, 10))).run(
                room.mob_placer(r(4.5, 2, 0.5), SOUTH, adults=True).summon(
                    'horse', nbt={'Variant': 1, 'Tame': True, 'Tags': ['armor_horse', 'material_static']}))
            yield mc.data().merge(entity().tag('armor_horse').limit(1).sort('nearest'), {
                'ArmorItem': {'id': '%s_horse_armor' % armor, 'Count': 1}})
            yield mc.data().merge(entity().tag('armor_horse_frame').limit(1),
                                  {'Item': {'id': '%s_horse_armor' % armor, 'Count': 1}, 'ItemRotation': 0})
            yield mc.execute().if_().score(horse_saddle).matches(1).run().item().replace().entity(
                entity().tag('armor_horse'), 'horse.saddle').with_('saddle')
            yield mc.execute().if_().score(horse_saddle).matches(0).run().item().replace().entity(
                entity().tag('armor_horse'), 'horse.saddle').with_('air')
        else:
            yield mc.data().merge(entity().tag('armor_horse_frame').limit(1), {
                'Item': {'id': 'air', 'Count': 1}})
            yield mc.execute().if_().entity(entity().tag('armor_horse').distance((None, 10))).run(
                kill_em(entity().tag('armor_horse')))

        yield mc.data().merge(entity().tag('basic_stand').limit(1), {
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
            yield mc.data().merge(entity().tag('material_%d' % j).limit(1), {'HandItems': [hands[j], {}]})
        for j in range(4, 8):
            yield mc.data().merge(entity().tag('material_%d' % j).limit(1), {'HandItems': [{}, hands[j]]})
        yield mc.data().merge(r(-2, 0, 1), {'name': 'restworld:material_%s' % material, 'mode': 'LOAD'})

    room.loop('basic', main_clock).add(
        mc.fill(r(2, 2, 2), r(-2, 5, 4), 'air'),
        kill_em(entity().tag('material_thing'))
    ).loop(basic_loop, materials).add(
        enchant(True),
        enchant(False),
        mc.execute().if_().score(turtle_helmet).matches(1).run().data().modify(
            entity().tag('basic_stand').limit(1), 'ArmorItems[3].id').set().value('turtle_helmet'),
        mc.execute().if_().score(turtle_helmet).matches(1).run().data().modify(
            entity().tag('armor_helmet').limit(1), 'Item.id').set().value('turtle_helmet'),
        mc.execute().if_().score(elytra).matches(1).run().data().modify(
            entity().tag('basic_stand').limit(1), 'ArmorItems[2].id').set().value('elytra'),
        mc.execute().if_().score(elytra).matches(1).run().data().modify(
            entity().tag('armor_chestplate').limit(1), 'Item.id').set().value('elytra'),
        mc.fill(r(-2, 2, 2), r(2, 4, 4), 'air'),
        mc.setblock(r(-2, 0, 0), 'redstone_block'),
        mc.execute().positioned(r(-2, 0, 2)).run().kill(entity().type('item').delta((5, 3, 4)))
    )

    room.function('basic_update').add(
        mc.execute().at(entity().tag('basic_home')).run().function('restworld:materials/basic_cur'),
        mc.execute().at(entity().tag('basic_home')).run().function('restworld:materials/basic_finish_main'))
