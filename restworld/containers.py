from __future__ import annotations

from pyker.base import Nbt
from pyker.commands import mc, r, NORTH, entity, WEST, all_, Block, RESULT, VISIBLE, STYLE, VALUE, PLAYERS, COLOR, \
    SOUTH, EAST, self, player, Entity, JsonText, SURVIVAL, LEVELS, CREATIVE
from pyker.simpler import WallSign, Item
from restworld.rooms import Room, label
from restworld.world import restworld, slow_clock, main_clock, fast_clock


def room():
    room = Room('containers', restworld, NORTH, ('GUI,', 'Containers,', 'Items'))

    room.function('anvil_container_enter').add(mc.setblock(r(0, 2, 0), 'anvil'))

    def beacon_loop(step):
        depth = step.elem
        start_gold = depth - 1
        end_dirt = 4 - depth - 1
        if end_dirt >= 0:
            yield mc.fill(r(4, 2, 4), r(-4, 2 + end_dirt, -4), 'chiseled_quartz_block').replace('gold_block')
        if start_gold >= 0:
            yield mc.fill(r(4, 5, 4), r(-4, 5 - start_gold, -4), 'gold_block').replace('chiseled_quartz_block')

        if step.i == 4:
            yield mc.data().merge(r(0, 6, 0), {'Secondary': -1})
        elif step.i == 5:
            yield mc.data().merge(r(0, 6, 0), {'Secondary': 10})

    room.loop('beacon', slow_clock).loop(beacon_loop, (0, 1, 2, 3, 4, 4, 3, 2, 1))
    room.function('beacon_enter').add(
        mc.fill(r(0, 1, 0), r(0, 5, 0), 'gold_block'),
        mc.clone(r(0, -5, 1), r(0, -5, 1), r(0, 6, 1)))
    room.function('beacon_exit').add(
        mc.fill(r(0, 1, 0), r(0, 5, 0), 'chiseled_quartz_block'))

    bossbar_value = room.score('bossbar_value')
    room.function('bossbar_init').add(
        mc.kill(entity().tag('bossbar_current')),
        mc.bossbar().add('restworld:bossbar', "Ornamental Stud"),
        mc.bossbar().set('restworld:bossbar', PLAYERS, all_()),
        mc.bossbar().set('restworld:bossbar', VALUE, 50),
        bossbar_value.set(3),
        mc.function('restworld:containers/bossbar_exit'),
        WallSign('Boss Bar').place(r(0, 3, 0, ), WEST),
        label(r(-3, 2, -100), 'Color'),
        WallSign('Color:').place(r(-2, 2, -1), WEST),
        label(r(-3, 2, 000), 'Style'),
        WallSign('Style:').place(r(-2, 2, 0, ), WEST),
        label(r(-3, 2, 100), 'Style'),
        WallSign('Value:').place(r(-2, 2, 1), WEST),
    )
    room.function('bossbar_exit').add(mc.bossbar().set('restworld:bossbar', VISIBLE, False))
    toggle_bossbar = room.score('toggle_bossbar')
    room.function('toggle_bossbar', home=False).add(
        mc.execute().store(RESULT).score(toggle_bossbar).run().bossbar().get('restworld:bossbar', VISIBLE),
        mc.execute().if_().score(toggle_bossbar).matches(0).run().bossbar().set('restworld:bossbar', VISIBLE, True),
        mc.execute().if_().score(toggle_bossbar).matches(1).run().bossbar().set('restworld:bossbar', VISIBLE, False),
    )

    def bossbar_param(which):
        return (
            mc.kill(entity().tag('bossbar_current')),
            mc.execute().at(entity().tag('bossbar_home')).run().summon(
                'armor_stand', r(-2, 0, -1), {'Tags': ['bossbar_current', 'bossbar_%s_home' % which], 'Small': True}),
            mc.execute().at(entity().tag('bossbar_%s_home' % which)).run().function(
                'restworld:containers/bossbar_%s_cur' % which),
            mc.bossbar().set('restworld:bossbar', VISIBLE, True),
        )

    def bossbar_color_loop(step):
        yield mc.bossbar().set('restworld:bossbar', COLOR, step.elem.lower())
        yield mc.data().merge(r(0, 2, 0), {'Text3': step.elem})

    def bossbar_style_loop(step):
        yield mc.bossbar().set('restworld:bossbar', STYLE, step.elem)
        yield mc.data().merge(r(0, 2, 0), {'Text3': step.elem})

    def bossbar_value_loop(step):
        yield mc.bossbar().set('restworld:bossbar', VALUE, step.elem)
        yield mc.data().merge(r(0, 2, 0), {'Text3': step.elem})

    room.function('bossbar_color_init').add(bossbar_param('color'))
    room.loop('bossbar_color', main_clock).loop(bossbar_color_loop,
                                                ('Blue', 'Green', 'Pink', 'Purple', 'Red', 'White', 'Yellow'))
    room.function('bossbar_style_init').add(bossbar_param('style'))
    room.loop('bossbar_style', main_clock).loop(bossbar_style_loop,
                                                ('progress', 'notched_6', 'notched_10', 'notched_12', 'notched_20'))
    room.function('bossbar_value_init').add(bossbar_param('value'))
    room.loop('bossbar_value', main_clock).loop(bossbar_value_loop, (0, 25, 50, 75, 100))

    water_potion = Block('potion', nbt={'Potion': "water"})

    def brewing_loop(step):
        for j in range(0, 3):
            if j in step.elem:
                block = water_potion
            else:
                block = 'air'
            yield mc.item().replace().block(r(0, 2, 0), 'container.%d' % j).with_(block, 1)

    room.function('brewing_init').add(
        mc.function('restworld:containers/switch_brewing_off'),
        label(r(1, 1, -1), "Brew"))
    room.loop('brewing_rotate', main_clock).add(
        mc.item().replace().block(r(0, 2, 0), 'container.3').with_('air'),
        mc.item().replace().block(r(0, 2, 0), 'container.4').with_('air'),
        mc.data().merge(r(0, 2, 0), {'BrewTime': 0, 'Fuel': 0})).loop(brewing_loop, (
        (), (0,), (1,), (2,), (2, 0), (1, 2), (0, 1), (0, 1, 2)))
    room.function('brewing_run', fast_clock).add(
        mc.item().replace().block(r(0, 2, 0), 'container.0').with_(water_potion),
        mc.item().replace().block(r(0, 2, 0), 'container.1').with_('air'),
        mc.item().replace().block(r(0, 2, 0), 'container.2').with_(water_potion),
        mc.item().replace().block(r(0, 2, 0), 'container.3').with_('nether_wart'),
        mc.item().replace().block(r(0, 2, 0), 'container.4').with_('blaze_powder'),
    )
    room.function('switch_brewing_off', home=False).add(
        mc.item().replace().block(r(0, 2, 0), 'container.3').with_('air'),
        mc.item().replace().block(r(0, 2, 0), 'container.4').with_('air'),
        mc.data().merge(r(0, 2, 0), {'Fuel': 0}),
        mc.kill(entity().tag('brewing_run_home'))
    )
    room.function('switch_brewing_on', home=False).add(
        mc.execute().at(entity().tag('brewing_home')).run().summon(
            'armor_stand', r(0, 0, 0), {'Tags': ['homer', 'brewing_run_home'], 'NoGravity': True}))

    placer = room.mob_placer(r(0, 2, 0), WEST, -3, 0, tags=('carrier',), adults=True,
                             nbt={'ChestedHorse': True, 'Tame': True, 'Variant': 2})
    room.function('carrier_init').add(
        placer.summon('llama', tags=('strength_llama',)),
        placer.summon('donkey'))
    room.loop('strength_llama', main_clock).loop(
        lambda x: mc.execute().as_(entity().tag('strength_llama')).run().data().merge(self(), {'Strength': x.elem}),
        range(1, 6))

    room.function('cookers_init').add(
        mc.setblock(r(0, 2, 0), Block('furnace', {'facing': WEST}, {'CookTime': 0})),
        mc.setblock(r(3, 2, 0), Block('blast_furnace', {'facing': WEST}, {'CookTime': 0})),
        mc.setblock(r(0, 2, 3), Block('smoker', {'facing': WEST}, {'CookTime': 0})),
        label(r(-1, 2, 1), "Cook"))
    room.function('cookers_run', home=False).add(
        mc.item().replace().block(r(0, 2, 0), 'container.1').with_('minecraft:stick', 64),
        mc.item().replace().block(r(0, 2, 0), 'container.0').with_('minecraft:stone', 64),
        mc.item().replace().block(r(0, 2, 0), 'container.2').with_('air', 1),
        mc.item().replace().block(r(3, 2, 0), 'container.1').with_('minecraft:stick', 64),
        mc.item().replace().block(r(3, 2, 0), 'container.0').with_('minecraft:gold_ore', 64),
        mc.item().replace().block(r(3, 2, 0), 'container.2').with_('air', 1),
        mc.item().replace().block(r(0, 2, 3), 'container.1').with_('minecraft:stick', 64),
        mc.item().replace().block(r(0, 2, 3), 'container.0').with_('minecraft:beef', 64),
        mc.item().replace().block(r(0, 2, 3), 'container.2').with_('air', 1),
    )

    trade_nbt = lambda *args: {
        'maxUses': 1000, 'buy': {'id': args[0], 'Count': args[1]}, 'buyB': {'id': args[2], 'Count': args[3]},
        'sell': {'id': args[4], 'Count': args[5]}, 'xp': 1, 'uses': args[6]}

    def experience_loop(step):
        yield mc.data().merge(entity().tag('trades').limit(1),
                              {'VillagerData': {'level': step.elem[0]}, 'Xp': step.elem[1]}),
        recipes = list(trade_nbt(*t) for t in trades[:(step.elem[0] * 2)])
        yield mc.data().merge(entity().tag('trades').limit(1), {'Offers': {'Recipes': recipes}})

    placer = room.mob_placer(r(0, 2, 0), SOUTH, adults=True, tags=('trades',),
                             nbt={'VillagerData': {'profession': 'farmer', 'level': 3}, 'CanPickUpLoot': False})
    room.function('experience_init').add(
        placer.summon('villager'),
        mc.function('restworld:containers/experience_cur'))

    thresholds = (10, 60, 80, 100)
    xp = []
    x = 0
    level_x = 0
    for i in range(0, len(thresholds)):
        for j in range(0, 3):
            x = level_x
            if j == 1:
                x = level_x + thresholds[i] / 2
            elif j == 2:
                x = level_x + thresholds[i] - 1
            xp += ((i + 1, int(x)),)
        level_x += thresholds[i]
    xp += ((5, 250),)
    trades = (
        ('carrot', 6, 'iron_hoe', 1, 'emerald', 2, 0),
        ('emerald', 1, 'air', 20, 'bread', 6, 1001),
        ('pumpkin', 6, 'air', 1, 'emerald', 1, 0),
        ('emerald', 1, 'air', 1, 'pumpkin_pie', 1, 0),
        ('melon', 4, 'air', 1, 'emerald', 1, 1001),
        ('emerald', 1, 'cocoa_beans', 1, 'cookie', 18, 0),
        ('emerald', 1, 'air', 1, 'cake', 1, 0),
        ('emerald', 1, 'air', 1, 'suspicious_stew', 1, 0),
        ('emerald', 1, 'air', 1, 'golden_carrot', 3, 1001),
        ('emerald', 1, 'melon', 1, 'glistering_melon_slice', 3, 0),
    )
    room.loop('experience', main_clock).loop(experience_loop, xp)
    room.function('enchanting_enter').add(
        mc.data().merge(r(0, 4, 0), {'Items': [','.join(
            '{Slot:%d,id:book,Count:64},{Slot:%d,id:lapis_lazuli,Count:64}' % (i, i + 9) for i in range(0, 9))]}))

    room.function('ingredients_enter', home=False).add(
        mc.clone(r(20, -5, 27), r(-15, -5, 1), r(-15, 1, 1)).filtered('chest'))
    room.function('item_enter').add(
        mc.setblock(r(-1, -2, 0), 'redstone_torch'),
        mc.function('restworld:containers/item_update'))
    room.function('item_exit').add(mc.setblock(r(-1, -2, 0), 'air'))

    placer = room.mob_placer(r(0, 2, -1), EAST, tags=('item_holder', 'item_hands'), adults=True, nbt={'ShowArms': True})
    room.function('item_init').add(
        placer.summon('armor_stand'),
        mc.setblock(r(0, 2, 1), 'barrier'),
        mc.summon('item_frame', r(1, 2, 1),
                  {'Facing': 5, 'Tags': ['containers', 'item_holder', 'item_src'], 'Item': Item.nbt('iron_pickaxe')}),
        mc.summon('item_frame', r(1, -1, 1), {'Facing': 5, 'Tags': ['containers', 'item_holder', 'item_dst']}),

        mc.setblock(r(-1, 2, 0), 'air'),
        WallSign(('Item put in frame', 'shown in "fixed",', '"ground", and 3rd', 'party hands')).place(r(-1, 2, 0),
                                                                                                       EAST),
        label(r(1, 2, -1), "On Head"),
    )
    item_new = room.score('item_new')
    room.function('item_run').add(
        mc.execute().store(RESULT).score(item_new).run().data().modify(
            entity().tag('item_dst').limit(1), 'Item').set().from_(entity().tag('item_src').limit(1), 'Item'),
        mc.execute().if_().score(item_new).matches(1).at(entity().tag('item_home')).run().function(
            'restworld:containers/item_update'),
        mc.execute().as_(entity().tag('item_holder')).run().data().modify(self(), 'ItemRotation').set().value(0),
    )
    room.function('item_update').add(
        mc.execute().unless().entity(entity().tag('item_ground')).at(entity().tag('item_home')).run().summon(
            'item', r(0, 3, 1),
            {'Item': Item.nbt('iron_pickaxe'), 'Age': -32768, 'PickupDelay': 2147483647, 'Tags': ['item_ground']}),
        mc.data().modify(entity().tag('item_ground').limit(1), 'Item').set().from_(entity().tag('item_src').limit(1),
                                                                                   'Item'),
        mc.data().merge(entity().tag('item_ground').limit(1), {'Age': -32768, 'PickupDelay': 2147483647}),
        mc.data().modify(entity().tag('item_hands').limit(1), 'HandItems[0]').set().from_(
            entity().tag('item_src').limit(1), 'Item'),
        mc.data().modify(entity().tag('item_hands').limit(1), 'HandItems[1]').set().from_(
            entity().tag('item_src').limit(1), 'Item'),
        mc.data().remove(entity().tag('item_hands').limit(1), 'ArmorItems[3]'),
        mc.execute().if_().score(room.score('item_head')).matches(1).run().data().modify(
            entity().tag('item_hands').limit(1), 'ArmorItems[3]').set().from_(entity().tag('item_src').limit(1), 'Item')
    )

    non_inventory = list(Block(s) for s in (
        "Knowledge Book",
        "Debug Stick",
        "Suspicious Stew",
        "Firework Star",
        "Bundle",
        "Jigsaw",
        "Structure Block",
        "Structure Void",
        "Barrier",
        "Light",
        "Dragon Egg",
        "Command Block",
        "Command Block Minecart",
        "Spawner",
    ))
    non_inventory.append(Entity("elytra", nbt={'Damage': 450}, display_name='Damaged Elytra'))

    def only_items_init_func():
        rows = [(0, 5), (0, 5), (0, 5)]
        dx = 2
        dz = 1
        x = 0
        items = list(non_inventory)
        yield mc.kill(entity().tag('only_item_frame'))
        while len(items) > 0:
            z, end = rows.pop(0)
            for i in range(0, end):
                t = items.pop(0)
                yield mc.summon('item_frame', r(x, 2, 5 - z),
                                {'Facing': 2, 'Tags': ['containers', 'only_item_frame', 'only_item_frame_%s' % t.kind]})
                z += dz
            x += dx

        for i, t in enumerate(non_inventory):
            tag_nbt = Nbt({'tag': {'display': JsonText.text(t.display_name)}})
            if t.kind == 'elytra':
                tag_nbt = tag_nbt.merge({'Damage': 450})
            nbt = {'Fixed': True, 'Item': Item.nbt(t.kind).merge({'tag': tag_nbt})}
            yield mc.data().merge(entity().tag('only_item_frame_%s' % t.kind).limit(1), nbt)
            yield mc.item().replace().block(r(1, -5, -1), 'container.%d' % i).with_(t)
        yield mc.clone(r(1, -5, -1), r(1, -5, -1), r(1, 1, -1))

        yield WallSign(('Items Not', 'in Creative', 'Iventory')).place(r(2, 2, -1, ), NORTH)

    giveable = non_inventory[:-1]
    giveable.append(Entity('Elytra', {'Damage': 450}))
    room.function('only_items_give').add(
        mc.give(player(), 'chain_command_block'),
        mc.give(player(), 'repeating_command_block'),
        (mc.give(player(), x) for x in giveable),
        mc.give(player(), 'firework_rocket'),
    )
    room.function('only_items_init').add(
        label(r(3, 2, -1), "Give"),
        mc.setblock(r(1, -5, -1), Block('chest', {'facing': EAST}))
    ).add(list(only_items_init_func()))

    enchant_chest = {'Items': [{'Slot': 0, 'id': 'lapis_lazuli', 'Count': 64}, {'Slot': 1, 'id': 'book', 'Count': 64}]}
    room.loop('survival', main_clock).add(mc.data().merge(r(-6, 6, 0), enchant_chest)).loop(
        lambda step: mc.xp().set(player(), step.elem, LEVELS), (0, 9, 20, 30))
    room.function('survival_init').add(
        mc.gamemode(SURVIVAL, player()),
        mc.function("restworld:containers/survival_cur"))
    room.function('survival_stop', home=False).add(
        mc.gamemode(CREATIVE, player()),
        mc.kill(entity().tag('survival_home'))
    )