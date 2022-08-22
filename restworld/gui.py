from __future__ import annotations

from pynecraft import commands
from pynecraft.base import EAST, NORTH, WEST, r
from pynecraft.commands import BOSSBAR_COLORS, BOSSBAR_STYLES, Block, CREATIVE, EQ, Entity, LEVELS, REPLACE, \
    SURVIVAL, a, \
    bossbar, clone, data, e, execute, fill, function, gamemode, give, item, kill, p, s, schedule, setblock, summon, tag
from pynecraft.info import block_items, blocks, items
from pynecraft.simpler import Item, ItemFrame, WallSign
from restworld import global_
from restworld.rooms import Room, label, named_frame_item
from restworld.world import fast_clock, main_clock, restworld, slow_clock


def room():
    room = Room('gui', restworld, NORTH, ('GUI,', 'gui,', 'Items', 'HUD'))

    room.function('anvil_container_enter').add(setblock(r(0, 2, 0), 'anvil'))

    # These offsets are used inside beacon functions so we can center the calculations under the middle of the pyramid,
    # which is easier to reason about.
    at = execute().positioned(r(0, -4, -5)).run

    def beacon_loop(step):
        depth = step.elem
        start_gold = depth - 1
        end_dirt = 4 - depth - 1
        if end_dirt >= 0:
            yield at(fill(r(4, 2, 4), r(-4, 2 + end_dirt, -4), 'chiseled_quartz_block').replace('gold_block'))
        if start_gold >= 0:
            yield at(fill(r(4, 5, 4), r(-4, 5 - start_gold, -4), 'gold_block').replace('chiseled_quartz_block'))

        if step.i == 4:
            yield at(data().merge(r(0, 6, 0), {'Secondary': -1}))
        elif step.i == 5:
            yield at(data().merge(r(0, 6, 0), {'Secondary': 10}))

    # Can't use bounce because we need to show two things at full strength.
    room.loop('beacon', slow_clock).loop(beacon_loop, (0, 1, 2, 3, 4, 4, 3, 2, 1))
    room.function('beacon_enter').add(
        at(fill(r(0, 1, 0), r(0, 5, 0), 'gold_block')),
        at(clone(r(0, -5, 1), r(0, -5, 1), r(0, 6, 1))))
    room.function('beacon_exit').add(
        at(fill(r(0, 1, 0), r(0, 5, 0), 'chiseled_quartz_block')))

    bossbar_which = room.score('bossbar_which')
    room.function('bossbar_exit').add(bossbar().set('restworld:bossbar').visible(False))
    room.function('bossbar_enter').add(
        execute().at(e().tag('bossbar_run_home')).run(bossbar().set('restworld:bossbar').visible(True)))
    bb_off = room.function('bossbar_off', home=False).add(
        kill(e().tag('bossbar_run_home')),
        bossbar().set('restworld:bossbar').visible(False),
    )
    bb_on = room.function('bossbar_on', home=False).add(
        bossbar().set('restworld:bossbar').players(a()),
        execute().at(e().tag('bossbar_home')).positioned(r(-2, -0.5, 0)).run(
            function('restworld:gui/bossbar_run_home')),
        bossbar().set('restworld:bossbar').visible(True),
    )
    toggle_bossbar = room.score('toggle_bossbar')
    room.function('toggle_bossbar', home=False).add(
        toggle_bossbar.set(1),
        execute().at(e().tag('bossbar_run_home')).run(toggle_bossbar.set(0)),
        execute().if_().score(toggle_bossbar).matches(1).run(function(bb_on.full_name)),
        execute().if_().score(toggle_bossbar).matches(0).run(function(bb_off.full_name)),
    )

    bb_color_init = room.function('bossbar_color_init', home=False).add(
        label(r(-1, 2, -1), 'Color'), WallSign((None, 'Color:', BOSSBAR_COLORS[0].title())).place(r(0, 2, -1), WEST))
    bb_style_init = room.function('bossbar_style_init', home=False).add(
        label(r(-1, 2, 0), 'Style'), WallSign((None, 'Style:', BOSSBAR_STYLES[0])).place(r(0, 2, 0, ), WEST))
    bb_value_init = room.function('bossbar_value_init', home=False).add(
        label(r(-1, 2, 1), 'Value'), WallSign((None, 'Value:', str(50))).place(r(0, 2, 1), WEST))

    def bossbar_color_loop(step):
        yield bossbar().set('restworld:bossbar').color(step.elem.lower())
        yield data().merge(r(0, 2, -1), {'Text3': step.elem.title()})

    def bossbar_style_loop(step):
        yield bossbar().set('restworld:bossbar').style(step.elem)
        yield data().merge(r(0, 2, 0), {'Text3': step.elem})

    def bossbar_value_loop(step):
        yield bossbar().set('restworld:bossbar').value(step.elem)
        yield data().merge(r(0, 2, 1), {'Text3': f'{step.elem}'})

    bb_color = room.loop('bossbar_color', home=False).loop(bossbar_color_loop, BOSSBAR_COLORS)
    bb_style = room.loop('bossbar_style', home=False).loop(bossbar_style_loop, BOSSBAR_STYLES)
    bb_value = room.loop('bossbar_value', home=False).loop(bossbar_value_loop, (50, 75, 100, 0, 25))

    room.function('bossbar_init').add(
        bossbar().add('restworld:bossbar', 'Ornamental Stud'),
        bossbar().set('restworld:bossbar').players(a()),
        function(bb_on.full_name),
        execute().at(e().tag('bossbar_run_home')).run(function(bb_color_init.full_name)),
        execute().at(e().tag('bossbar_run_home')).run(function(bb_style_init.full_name)),
        execute().at(e().tag('bossbar_run_home')).run(function(bb_value_init.full_name)),
        function(bb_off.full_name),
        WallSign((None, 'Boss Bar')).place(r(0, 3, 0, ), WEST),
        label(r(-1, 3, 0), 'Bossbar'),
    )

    room.loop('bossbar_run', main_clock).loop(None, range(0, 1)).add(
        execute().if_().score(bossbar_which).matches(0).run(function(bb_color.full_name)),
        execute().if_().score(bossbar_which).matches(1).run(function(bb_style.full_name)),
        execute().if_().score(bossbar_which).matches(2).run(function(bb_value.full_name)),
        execute().unless().score(bossbar_which).matches(0).run(function(bb_color.full_name + '_cur')),
        execute().unless().score(bossbar_which).matches(1).run(function(bb_style.full_name + '_cur')),
        execute().unless().score(bossbar_which).matches(2).run(function(bb_value.full_name + '_cur')),
    )

    water_potion = Block('potion', nbt={'Potion': 'water'})

    def brewing_loop(step):
        for j in range(0, 3):
            if j in step.elem:
                block = water_potion
            else:
                block = 'air'
            yield item().replace().block(r(0, 2, 0), 'container.%d' % j).with_(block, 1)

    room.function('brewing_init').add(
        function('restworld:gui/switch_brewing_off'),
        label(r(-1, 2, -1), 'Brew'))
    bottle_possibilities = ((), (0,), (1,), (2,), (2, 0), (1, 2), (0, 1), (0, 1, 2))
    room.loop('brewing_rotate', main_clock).add(
        item().replace().block(r(0, 2, 0), 'container.3').with_('air'),
        item().replace().block(r(0, 2, 0), 'container.4').with_('air'),
        data().merge(r(0, 2, 0), {'BrewTime': 0, 'Fuel': 0})).loop(brewing_loop, bottle_possibilities)
    room.function('brewing_run', fast_clock).add(
        item().replace().block(r(0, 2, 0), 'container.0').with_(water_potion),
        item().replace().block(r(0, 2, 0), 'container.1').with_('air'),
        item().replace().block(r(0, 2, 0), 'container.2').with_(water_potion),
        item().replace().block(r(0, 2, 0), 'container.3').with_('nether_wart'),
        item().replace().block(r(0, 2, 0), 'container.4').with_('blaze_powder'),
    )
    room.function('switch_brewing_off', home=False).add(
        item().replace().block(r(0, 2, 0), 'container.3').with_('air'),
        item().replace().block(r(0, 2, 0), 'container.4').with_('air'),
        data().merge(r(0, 2, 0), {'Fuel': 0}),
        kill(e().tag('brewing_run_home'))
    )
    room.function('switch_brewing_on', home=False).add(
        execute().at(e().tag('brewing_home')).run(
            summon('armor_stand', r(0, 0, 0), {'Tags': ['homer', 'brewing_run_home'], 'NoGravity': True})))

    placer = room.mob_placer(r(0, 2, 0), EAST, 3, 0, tags=('carrier',), adults=True,
                             nbt={'ChestedHorse': True, 'Tame': True, 'Variant': 2}, auto_tag=False)
    room.function('carrier_init').add(
        placer.summon('llama', tags=('strength_llama',)),
        placer.summon('donkey'),
    )
    room.loop('strength_llama', main_clock).loop(
        lambda x: execute().as_(e().tag('strength_llama')).run(data().merge(s(), {'Strength': x.elem})), range(1, 6))
    placer = room.mob_placer(r(0, 2, 0), EAST, adults=True, tags=('trades',), auto_tag=False,
                             nbt={'VillagerData': {'profession': 'farmer', 'level': 3}, 'CanPickUpLoot': False})
    room.function('trader_init').add(
        placer.summon('villager'),
        function('restworld:gui/trader_cur'))

    room.function('cookers_init').add(
        setblock(r(0, 2, 0), Block('furnace', {'facing': WEST}, {'CookTime': 0})),
        setblock(r(3, 2, 0), Block('blast_furnace', {'facing': WEST}, {'CookTime': 0})),
        setblock(r(0, 2, 3), Block('smoker', {'facing': WEST}, {'CookTime': 0})),
        label(r(-1, 2, 1), 'Cook'))
    room.function('cookers_run', home=False).add(
        item().replace().block(r(0, 2, 0), 'container.1').with_('minecraft:stick', 64),
        item().replace().block(r(0, 2, 0), 'container.0').with_('minecraft:stone', 64),
        item().replace().block(r(0, 2, 0), 'container.2').with_('air', 1),
        item().replace().block(r(3, 2, 0), 'container.1').with_('minecraft:stick', 64),
        item().replace().block(r(3, 2, 0), 'container.0').with_('minecraft:gold_ore', 64),
        item().replace().block(r(3, 2, 0), 'container.2').with_('air', 1),
        item().replace().block(r(0, 2, 3), 'container.1').with_('minecraft:stick', 64),
        item().replace().block(r(0, 2, 3), 'container.0').with_('minecraft:beef', 64),
        item().replace().block(r(0, 2, 3), 'container.2').with_('air', 1),
    )

    def trade_nbt(*args):
        return {'maxUses': 1000, 'xp': 1, 'uses': args[6],
                'buy': {'id': args[0], 'Count': args[1]},
                'buyB': {'id': args[2], 'Count': args[3]},
                'sell': {'id': args[4], 'Count': args[5]},
                }

    thresholds = (10, 60, 80, 100)
    xp = []
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

    def trader_loop(step):
        yield data().merge(e().tag('trades').limit(1),
                           {'VillagerData': {'level': step.elem[0]}, 'Xp': step.elem[1]}),
        recipes = list(trade_nbt(*t) for t in trades[:(step.elem[0] * 2)])
        yield data().merge(e().tag('trades').limit(1), {'Offers': {'Recipes': recipes}})

    room.loop('trader', main_clock).loop(trader_loop, xp)

    enchanting = room.function('enchanting_enter')
    for i in range(9):
        enchanting.add(
            item().replace().block(r(0, 4, 0), f'container.{i}').with_('book', 64),
            item().replace().block(r(0, 4, 0), f'container.{i + 9}').with_('lapis_lazuli', 64))

    room.function('ingredients_enter').add(
        clone(r(20, -5, 30), r(-15, -5, 1), r(-15, 1, 1)).filtered('chest'))

    placer = room.mob_placer(r(0, 2, -1), EAST, auto_tag=False, adults=True, nbt={'ShowArms': True})
    placer_head = room.mob_placer(r(0, 2.77, -1), EAST, auto_tag=False, adults=True)
    all_src = e().tag('item_src')
    item_src = all_src.limit(1)
    all_ground = e().tag('item_ground')
    item_ground = all_ground.limit(1)
    item_holder = e().tag('item_holder').limit(1)
    item_head = room.function('item_head', home=False).add(
        item().replace().entity(e().tag('item_holder_head').limit(1), 'armor.head').with_(
            ('player_head', dict(SkullOwner='BlueMeanial'))),
    )

    is_empty = room.score('item_is_empty')
    was_empty = room.score('item_was_empty')
    was_in = room.score('item_was_in')
    is_in = room.score('item_is_in')

    recent_item_sign_pos = r(0, 3, -2)
    room.function('item_init').add(
        kill(all_src),
        kill(all_ground),
        placer.summon('armor_stand', tags=('item_holder', 'item_hands')),
        placer_head.summon('armor_stand', tags=('item_holder_head',),
                           nbt=dict(Small=True, NoGravity=True, Invisible=True)),
        # I don't know why I can't do this right away, 1 tick isn't enough, and 1 second is.
        schedule().function(item_head, '1s', REPLACE),
        setblock(r(0, 3, 1), 'barrier'),
        ItemFrame(EAST).item('iron_pickaxe').tag('item_src', 'gui').fixed(False).summon(r(1, 3, 1)),
        is_empty.set(1),
        ItemFrame(EAST, nbt={'Invisible': True}, name='Invisible Frame').item('iron_pickaxe').tag(
            'item_invis_frame', 'gui').fixed(False).summon(r(1, 2, -3)),
        WallSign(
            ('Put item in frame', 'to show in "fixed",', '"ground", and 3rd', 'party hands')).place(r(0, 3, 0), EAST),
        label(r(1, 2, -2), 'On Head'),
        label(r(1, 2, -1), 'All Items'),
        label(r(1, 2, 0), 'All Blocks'),
    )
    invis_frame = e().tag('item_invis_frame').limit(1)
    ground_default_nbt = {'Item': Item.nbt_for('iron_pickaxe'), 'Age': -32768, 'PickupDelay': 2147483647,
                          'Tags': ['item_ground']}
    named_frame_data = named_frame_item(name='Invisible Frame').merge({'ItemRotation': 0})
    item_copy = room.function('item_copy', home=False).add(
        execute().unless().data().entity(item_src, 'Item.id').run(kill(all_ground)),
        execute().if_().data().entity(item_src, 'Item.id').run(
            data().merge(item_src, {'ItemRotation': 0}),
            execute().unless().entity(item_ground).at(e().tag('item_home')).run(
                summon('item', r(0, 3, -3), ground_default_nbt)),
            data().modify(item_ground, 'Item').set().from_(item_src, 'Item'),
            data().merge(item_ground, {'Age': -32768, 'PickupDelay': 2147483647})),
        item().replace().entity(item_holder, 'weapon.mainhand').from_().entity(item_src, 'container.0'),
        item().replace().entity(item_holder, 'weapon.offhand').from_().entity(item_src, 'container.0'),
        execute().if_().score(room.score('item_head')).matches(0).run(
            item().replace().entity(item_holder, 'armor.head').with_('air')),
        execute().if_().score(room.score('item_head')).matches(1).run(
            item().replace().entity(item_holder, 'armor.head').from_().entity(item_src, 'container.0')),
        item().replace().entity(invis_frame, 'container.0').from_().entity(item_src, 'container.0'),
        data().merge(invis_frame, named_frame_data),
        global_.if_clock_running.at(e().tag('all_things_home')).run(
            item().replace().entity(p(), 'weapon.mainhand').from_().entity(item_src, 'container.0'),
            item().replace().entity(p(), 'weapon.offhand').from_().entity(item_src, 'container.0')),
    )
    room.function('item_run', home=False).add(
        was_empty.operation(EQ, is_empty),
        is_empty.set(1),
        execute().if_().data().entity(item_src, 'Item.id').run(is_empty.set(0)),
        execute().unless().score(was_empty).is_(EQ, is_empty).run(function(item_copy.full_name)),
        was_in.operation(EQ, is_in),
        is_in.set(0),
        execute().if_().entity(p().volume((6, 5, 4))).run(is_in.set(1)),
        execute().if_().score(is_in).matches(1).if_().score(was_in).matches(0).run(
            (item().replace().block(r(0, 0, 1), f'container.{i}').from_().entity(p(), f'hotbar.{i}') for i
             in range(0, 9)),
            item().replace().block(r(0, 0, 1), 'container.10').from_().entity(p(), 'weapon.offhand')),
        execute().if_().score(is_in).matches(0).if_().score(was_in).matches(1).run(
            kill(e().tag('all_things_home')),
            (item().replace().entity(p(), f'hotbar.{i}').from_().block(r(0, 0, 1), f'container.{i}') for i in
             range(0, 9)),
            item().replace().entity(p(), 'weapon.offhand').from_().block(r(0, 0, 1), 'container.1'),
        ),
    )
    room.function('item_enter').add(setblock(r(-3, -2, -3), 'redstone_block'))
    room.function('item_exit').add(setblock(r(-1, -2, 0), 'air'))

    def all_funcs(which, things):
        at_home = execute().at(e().tag('item_home')).run

        def all_loop(step):
            yield item().replace().entity(item_src, 'container.0').with_(step.elem)
            yield at_home(data().merge(recent_item_sign_pos, {'Text1': step.elem.name}))

        all_things = things
        room.loop(f'all_{which}', fast_clock).add(is_empty.set(1)).add(
            at_home(data().modify(recent_item_sign_pos, 'Text4').set().from_(recent_item_sign_pos, 'Text3')),
            at_home(data().modify(recent_item_sign_pos, 'Text3').set().from_(recent_item_sign_pos, 'Text2')),
            at_home(data().modify(recent_item_sign_pos, 'Text2').set().from_(recent_item_sign_pos, 'Text1')),
        ).loop(all_loop, all_things)
        room.function(f'all_{which}_home', exists_ok=True).add(tag(e().tag(f'all_{which}_home')).add('all_things_home'))

        other = 'items' if which == 'blocks' else 'blocks'
        start_all = room.score('start_all')
        room.function(f'toggle_all_{which}', home=False).add(
            kill(e().tag(f'all_{other}_home')),
            start_all.set(1),
            execute().at(e().tag(f'all_{which}_home')).run(start_all.set(0)),
            execute().if_().score(start_all).matches(1).at(e().tag('item_home')).positioned(r(2, 0, 0)).run(
                function(f'restworld:gui/all_{which}_home')),
            execute().if_().score(start_all).matches(1).run(
                at_home(WallSign(()).place(recent_item_sign_pos, EAST))),
            execute().if_().score(start_all).matches(0).run(
                kill(e().tag(f'all_{which}_home')),
                item().replace().entity(item_src, 'container.0').with_('air'),
                at_home(setblock(recent_item_sign_pos, 'air'))),
        )

    all_funcs('blocks',
              filter(lambda block: block.name not in block_items and 'Air' not in block.name, blocks.values()))
    all_funcs('items', filter(lambda row: 'Spawn' not in row.name, items.values()))

    non_inventory = list(Entity(i) for i in (
        'Knowledge Book',
        'Debug Stick',
        'Suspicious Stew',
        'Firework Star',
        'Bundle',
        'Jigsaw',
        'Structure Block',
        'Structure Void',
        'Barrier',
        'Light',
        'Dragon Egg',
        'Command Block',
        'Command Block Minecart',
        'Spawner',
    ))
    non_inventory.append(Entity('elytra', nbt={'Damage': 450}, name='Damaged Elytra'))

    only_item_chest_pos = r(-1, -5, -2)

    def only_items_init_func():
        rows = [(0, 5), (0, 5), (0, 5)]
        dx = 2
        dz = 1
        x = -1
        items = list(non_inventory)
        yield kill(e().tag('only_item_frame'))
        index = 0
        while len(items) > 0:
            z, end = rows.pop(0)
            for i in range(0, end):
                t = items.pop(0)
                frame = ItemFrame(NORTH).item(t).named(t.name)
                frame.tag('gui', 'only_item_frame', f'only_item_frame_{t.id}')
                if t.id == 'elytra':
                    frame.merge_nbt({'Item': {'tag': {'Damage': 450}}})
                yield frame.summon(r(x, 2, z - 4), facing=WEST)
                yield item().replace().block(only_item_chest_pos, f'container.{index}').with_(t)
                z += dz
                index += 1
            x += dx

        clone_pos = list(only_item_chest_pos)
        clone_pos[1] = r(1)
        # noinspection PyTypeChecker
        yield clone(only_item_chest_pos, only_item_chest_pos, tuple(clone_pos))
        yield WallSign((None, 'Items Not', 'in Creative', 'Inventory')).place(r(5, 3, -2), WEST)

    giveable = non_inventory[:-1]
    giveable.append(Entity('Elytra', {'Damage': 450}))
    room.function('only_items_give', home=False).add(
        give(p(), 'chain_command_block'),
        give(p(), 'repeating_command_block'),
        (give(p(), x) for x in giveable),
        give(p(), 'firework_rocket'),
    )
    room.function('only_items_init').add(
        label(r(-2, 2, -2), 'Give'),
        setblock(only_item_chest_pos, Block('chest', {'facing': WEST}))
    ).add(list(only_items_init_func()))

    enchant_chest = {'Items': [{'Slot': 0, 'id': 'lapis_lazuli', 'Count': 64}, {'Slot': 1, 'id': 'book', 'Count': 64}]}
    room.loop('survival', main_clock).add(data().merge(r(-6, 6, 0), enchant_chest)).loop(
        lambda step: commands.xp().set(p(), step.elem, LEVELS), (0, 9, 20, 30))
    room.function('survival_init').add(
        gamemode(SURVIVAL, p()),
        function('restworld:gui/survival_cur'))
    room.function('survival_stop', home=False).add(
        gamemode(CREATIVE, p()),
        kill(e().tag('survival_home'))
    )
