from __future__ import annotations

import math

from pynecraft import commands
from pynecraft.base import EAST, NORTH, Nbt, TEXT_COLORS, WEST, as_facing, r, to_name
from pynecraft.commands import BOSSBAR_COLORS, BOSSBAR_STYLES, Block, CREATIVE, Entity, LEVELS, REPLACE, \
    RESET, SURVIVAL, Text, a, bossbar, clone, data, dialog, e, effect, execute, fill, forceload, function, gamemode, \
    gamerule, item, kill, n, p, return_, s, schedule, setblock, summon, tag, waypoint
from pynecraft.simpler import Item, ItemFrame, Sign, WallSign
from pynecraft.values import LOCATOR_BAR
from restworld.rooms import Room, kill_em
from restworld.world import fast_clock, main_clock, restworld, slow_clock


def room():
    room = Room('gui', restworld, NORTH, ('GUI,', 'HUD,', 'Items'))
    room.reset_at((0, 13))

    room.function('anvil_container_enter').add(setblock(r(0, 2, 0), 'anvil'))

    # These offsets are used inside beacon functions so we can center the calculations under the middle of the pyramid,
    # which is easier to reason about.
    at = execute().at(e().tag('beacon_home')).positioned(r(0, -4, -5)).run
    primary = (-1, 3, 8, 5, 5)

    crafter_clean = room.function('crafter_ui_clean', home=False).add(
        execute().at(e().tag('crafter_gui_home')).run(kill(e().type('item').distance((None, 10)))))

    def crafter_loop(step):
        if step.i == 0:
            yield setblock(r(0, 2, 1), 'air')
        else:
            yield item().replace().block(r(0, 2, 2), 'container.4').with_('oak_log')
            yield setblock(r(0, 2, 1), 'redstone_torch')
            yield schedule().function(crafter_clean, 5, REPLACE)

    room.loop('crafter_gui', main_clock).loop(crafter_loop, range(0, 2))

    beacon_on = room.score('beacon_on')

    def beacon_loop(step):
        depth = step.elem
        start_gold = depth - 1
        end_dirt = 4 - depth - 1
        if end_dirt >= 0:
            yield at(fill(r(4, 2, 4), r(-4, 2 + end_dirt, -4), 'chiseled_quartz_block').replace('gold_block'))
        if start_gold >= 0:
            yield at(fill(r(4, 5, 4), r(-4, 5 - start_gold, -4), 'gold_block').replace('chiseled_quartz_block'))

        secondary = 10 if step.i == 5 else -1

        yield at(data().merge(r(0, 6, 0), {'Primary': primary[step.elem], 'Secondary': secondary}))
        yield at(WallSign.change(r(-1, 6, 0), (None, f'Pyramid Height: {step.elem}')))

    # Can't use bounce because we need to show two things at full strength.
    room.loop('beacon', slow_clock).add(
        execute().if_().score(beacon_on).matches(0).run(return_())
    ).loop(
        beacon_loop, (0, 1, 2, 3, 4, 4, 3, 2, 1))
    beacon_start = room.function('beacon_start', home=False).add(
        beacon_on.set(1),
        at(fill(r(0, 1, 0), r(0, 5, 0), 'gold_block')),
        at(clone(r(0, -5, 1), r(0, -5, 1), r(0, 6, 1))))
    beacon_stop = room.function('beacon_stop', home=False).add(
        beacon_on.set(0),
        at(fill(r(0, 1, 0), r(0, 5, 0), 'chiseled_quartz_block')),
        effect().clear(p()))
    room.function('beacon_enter').add(function(beacon_start))
    room.function('beacon_exit').add(function(beacon_stop))
    room.function('beacon_init').add(
        beacon_on.set(0),
        at(WallSign((None, 'Pyramid Height: 0')).place(r(-1, 6, 0), WEST)),
        room.label(r(-3, 2, -5), 'Beacon', WEST),
    )
    room.function('beacon_home', exists_ok=True).add(tag(e().tag('beacon_home')).add('beacon_homer'))
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
        execute().at(e().tag('bossbar_home')).positioned(r(2, -0.5, 0)).run(
            function('restworld:gui/bossbar_run_home')),
        bossbar().set('restworld:bossbar').visible(True),
    )
    toggle_bossbar = room.score('toggle_bossbar')
    room.function('toggle_bossbar', home=False).add(
        toggle_bossbar.set(1),
        execute().at(e().tag('bossbar_run_home')).run(toggle_bossbar.set(0)),
        execute().if_().score(toggle_bossbar).matches(1).run(function(bb_on)),
        execute().if_().score(toggle_bossbar).matches(0).run(function(bb_off)),
    )

    bb_color_init = room.function('bossbar_color_init', home=False).add(room.label(r(1, 2, 1), 'Color', EAST))
    bb_style_init = room.function('bossbar_style_init', home=False).add(room.label(r(1, 2, 0), 'Style', EAST))
    bb_value_init = room.function('bossbar_value_init', home=False).add(room.label(r(1, 2, -1), 'Value', EAST))

    def bossbar_color_loop(step):
        yield bossbar().set('restworld:bossbar').color(step.elem.lower())
        yield Sign.change(r(0, 2, 0), (f'Color: {step.elem.title()}',))

    def bossbar_style_loop(step):
        yield bossbar().set('restworld:bossbar').style(step.elem)
        yield Sign.change(r(0, 2, 0), (None, None, step.elem))

    def bossbar_value_loop(step):
        yield bossbar().set('restworld:bossbar').value(step.elem)
        yield Sign.change(r(0, 2, 0), (None, None, None, f'Value: {step.elem}'))

    bb_color = room.loop('bossbar_color', home=False).loop(bossbar_color_loop, BOSSBAR_COLORS)
    bb_style = room.loop('bossbar_style', home=False).loop(bossbar_style_loop, BOSSBAR_STYLES)
    bb_value = room.loop('bossbar_value', home=False).loop(bossbar_value_loop, (50, 75, 100, 0, 25))

    room.function('bossbar_init').add(
        WallSign((f'Color: {BOSSBAR_COLORS[0].title()}', 'Style:', BOSSBAR_STYLES[0], 'Value: 50')).place(r(2, 2, 0),
                                                                                                          EAST),
        bossbar().add('restworld:bossbar', 'Ornamental Stud'),
        bossbar().set('restworld:bossbar').players(a()),
        function(bb_on),
        execute().at(e().tag('bossbar_run_home')).run(function(bb_color_init)),
        execute().at(e().tag('bossbar_run_home')).run(function(bb_style_init)),
        execute().at(e().tag('bossbar_run_home')).run(function(bb_value_init)),
        function(bb_off),
        WallSign((None, 'Boss Bar')).place(r(0, 4, 0, ), WEST),
    )

    room.loop('bossbar_run', main_clock).loop(None, range(0, 1)).add(
        execute().if_().score(bossbar_which).matches(0).run(function(bb_color)),
        execute().if_().score(bossbar_which).matches(1).run(function(bb_style)),
        execute().if_().score(bossbar_which).matches(2).run(function(bb_value)),
        execute().unless().score(bossbar_which).matches(0).run(function(bb_color.full_name + '_cur')),
        execute().unless().score(bossbar_which).matches(1).run(function(bb_style.full_name + '_cur')),
        execute().unless().score(bossbar_which).matches(2).run(function(bb_value.full_name + '_cur')),
    )

    water_potion = Item('potion', components={'potion_contents': {'potion': 'water'}})

    def brewing_loop(step):
        for j in range(0, 3):
            if j in step.elem:
                block = water_potion
            else:
                block = 'air'
            yield item().replace().block(r(0, 2, 0), 'container.%d' % j).with_(block)

    room.function('brewing_init').add(
        function('restworld:gui/switch_brewing_off'),
        room.label(r(-1, 2, -1), 'Brew', WEST))
    bottle_possibilities = ((), (0,), (1,), (2,), (2, 0), (1, 2), (0, 1), (0, 1, 2))
    room.loop('brewing_rotate', main_clock).add(
        item().replace().block(r(0, 2, 0), 'container.3').with_('air'),
        item().replace().block(r(0, 2, 0), 'container.4').with_('air'),
        data().merge(r(0, 2, 0), {'BrewTime': 0, 'Fuel': 0})).loop(brewing_loop, bottle_possibilities)
    room.function('brewing_run', fast_clock).add(
        (execute().if_().items(r(0, 2, 0), f'container.{i}',
                               str(Item('potion', components={'potion_contents': 'awkward'}))).run(
            item().replace().block(r(0, 2, 0), f'container.{i}').with_(water_potion)) for i in range(3)),
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
            summon('armor_stand', r(0, 0, 0), {'Tags': ['homer', 'brewing_run_home'], 'NoGravity': True}),
            item().replace().block(r(0, 2, 0), 'container.0').with_(water_potion),
            item().replace().block(r(0, 2, 0), 'container.1').with_('air'),
            item().replace().block(r(0, 2, 0), 'container.2').with_(water_potion),
        ))

    placer = room.mob_placer(r(0, 2, 0), NORTH, 2, 0, adults=True,
                             nbt={'ChestedHorse': True, 'Tame': True, 'Variant': 2})

    def carrier_llama_loop(step):
        yield data().merge(e().tag('carrier_llama').limit(1), {'Strength': step.elem})
        yield Sign.change(r(0, 2, -1), (None, None, f'Strength: {step.elem}'))

    room.function('carrier_llama_init').add(
        placer.summon('llama', tags=('carrier_llama', 'waypointable'), auto_tag=False),
        WallSign((None, 'Llama')).place(r(0, 2, -1), NORTH)
    )
    room.loop('carrier_llama', main_clock).loop(carrier_llama_loop, range(1, 6))

    def carrier_loop(step):
        placer = room.mob_placer(
            r(0, 2, 0.3), NORTH, 2, 0, adults=True, nbt={'ChestedHorse': True, 'Tame': True}, tags=('carrier',))
        yield placer.summon(step.elem)
        yield Sign.change(r(0, 2, -1), (None, None, step.elem.title()))

    room.loop('carrier', main_clock).add(kill_em(e().tag('carrier'))).loop(carrier_loop, ('camel', 'donkey'))
    room.function('carrier_init').add(WallSign((None, 'Saddlable')).place(r(0, 2, -1), NORTH))

    placer = room.mob_placer(r(0, 2, 0), NORTH, adults=True, tags=('trades',), auto_tag=False,
                             nbt={'VillagerData': {'profession': 'mason', 'level': 3}, 'CanPickUpLoot': False})
    room.function('trader_init').add(
        placer.summon('villager', tags=('waypointable',)),
        WallSign(()).place(r(0, 2, -1), NORTH),
        WallSign(('To see villager', 'GUI mid-trade,', 'offer to', 'buy something')).place(r(1, 2, -1), NORTH),
        function('restworld:gui/trader_cur'))

    room.function('cookers_init').add(
        setblock(r(0, 2, 0), Block('furnace', {'facing': WEST}, {'CookTime': 0})),
        setblock(r(3, 2, 0), Block('blast_furnace', {'facing': WEST}, {'CookTime': 0})),
        setblock(r(0, 2, 3), Block('smoker', {'facing': WEST}, {'CookTime': 0})),
        room.label(r(-1, 2, 1), 'Cook', WEST))

    room.function('cookers_run', home=False).add(
        item().replace().block(r(0, 2, 0), 'container.1').with_('stick', 64),
        item().replace().block(r(0, 2, 0), 'container.0').with_('stone', 64),
        item().replace().block(r(0, 2, 0), 'container.2').with_('air', 1),
        item().replace().block(r(3, 2, 0), 'container.1').with_('stick', 64),
        item().replace().block(r(3, 2, 0), 'container.0').with_('gold_ore', 64),
        item().replace().block(r(3, 2, 0), 'container.2').with_('air', 1),
        item().replace().block(r(0, 2, 3), 'container.1').with_('stick', 64),
        item().replace().block(r(0, 2, 3), 'container.0').with_('beef', 64),
        item().replace().block(r(0, 2, 3), 'container.2').with_('air', 1),
    )

    def trade_nbt(*args):
        return {
            'maxUses': 1000, 'xp': 1, 'uses': args[6],
            'buy': {'id': args[0], 'Count': args[1]},
            'buyB': {'id': args[2], 'Count': args[3]},
            'sell': {'id': args[4], 'Count': args[5]},
        }

    thresholds = (10, 60, 80, 100)
    # "Intermediate" is "Journeyman" in vanilla; removing sexism where possible.
    levels = ('Novice', 'Apprentice', 'Intermediate', 'Expert', 'Master')
    stages = ('Start', 'Middle', 'End')
    xp = []
    level_x = 0
    for i, threshold in enumerate(thresholds):
        for j, stage in enumerate(stages):
            x = level_x
            if j == 1:
                x = level_x + threshold / 2
            elif j == 2:
                x = level_x + threshold - 1
            xp.append((i + 1, int(x), stage))
        level_x += threshold
    xp += ((5, 250, None),)
    trades = (
        ('carrot', 6, 'iron_hoe', 1, 'emerald', 1, 1001),
        ('emerald', 1, 'air', 0, 'bread', 1, 2),
        ('pumpkin', 6, 'air', 1, 'emerald', 1, 0),
        ('emerald', 1, 'air', 1, 'pumpkin_pie', 1, 1001),
        ('melon', 4, 'air', 1, 'emerald', 1, 0),
        ('emerald', 1, 'cocoa_beans', 1, 'cookie', 18, 0),
        ('emerald', 1, 'air', 1, 'cake', 1, 0),
        ('emerald', 1, 'air', 1, 'suspicious_stew', 1, 0),
        ('emerald', 1, 'air', 1, 'golden_carrot', 3, 1001),
        ('emerald', 1, 'melon', 1, 'glistering_melon_slice', 3, 0),
    )

    def trader_loop(step):
        if step.elem[2]:
            stage = f'{step.elem[2]} of Range'
        else:
            stage = ''
        yield Sign.change(r(0, 2, -1), (None, 'Level:', f'{levels[step.elem[0] - 1]}', stage))
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

    room.function('bundle_init').add(
        ItemFrame(EAST, nbt={'Tags': ['gui', 'bundle']}).item('bundle').summon(r(0, 3, 0)),
        WallSign((None, None, 'Bundle')).place(r(0, 4, 0), EAST),
    )

    enchant_chest = {
        'Items': [{'Slot': 0, 'id': 'lapis_lazuli', 'Count': 64}, {'Slot': 1, 'id': 'book', 'Count': 64}]}
    room.loop('survival', main_clock).add(data().merge(r(-6, 6, 0), enchant_chest)).loop(
        lambda step: commands.xp().set(p(), step.elem, LEVELS), (0, 9, 20, 30))
    room.function('survival_init').add(
        gamemode(SURVIVAL, p()),
        execute().at(e().tag('enchanting_home')).positioned(r(0, -0.5, 1)).run(
            function('restworld:gui/survival_home')),
        function('restworld:gui/survival_cur'))
    room.function('survival_stop', home=False).add(
        gamemode(CREATIVE, p()),
        kill(e().tag('survival_home'))
    )

    room.function('powder_snow_init').add(
        setblock(r(-1, 2, 0), 'powder_snow'),
        WallSign((None, 'Freezing', '(step inside)')).place(r(-1, 3, 0), NORTH),
        setblock(r(-3, 2, 0), 'fire'),
        WallSign((None, 'On Fire', '(step inside)')).place(r(-3, 3, 0), NORTH),
    )
    saver_name = 'blur_saver'
    saver = n().tag(saver_name)
    room.function('pumpkin_blur_init').add(
        room.mob_placer(r(0, -2, 1), NORTH, kids=True, auto_tag=False).summon(
            Entity('armor_stand', Nbt(NoGravity=True), name=saver_name).tag(saver_name)),
        WallSign((None, 'Pumpkin Blur', '(step on plate)')).place(r(1, 3, 0), NORTH))
    room.function('pumpkin_blur_on', home=False).add(
        item().replace().entity(saver, 'armor.head').from_().entity(p(), 'armor.head'),
        item().replace().entity(p(), 'armor.head').with_(Item('carved_pumpkin')))
    room.function('pumpkin_blur_off', home=False).add(
        item().replace().entity(p(), 'armor.head').from_().entity(saver, 'armor.head'))

    room.function('waypoints_base_init')
    waypoint_sign_pos = r(0, 2, 0)
    room.function('waypoints_init', home=False).add(
        room.label(r(1, 2, 0), 'Waypoints', EAST),
        WallSign((None, 'Waypoint Style:')).place(waypoint_sign_pos, EAST),
    )

    waypoints_setup = room.function('waypoints_setup', home=False).add()
    radii = [(3, 'Here'), (205, 'Near'), (255, 'Far'), (320, 'Very Far')]
    for i, color in enumerate(TEXT_COLORS):
        my_tag = f'waypoint_{color}'
        angle = 360 * i / len(TEXT_COLORS)
        angle_rad = math.radians(angle)
        radius, radius_name = radii[i % len(radii)]
        x, z = math.cos(angle_rad) * radius, math.sin(angle_rad) * radius
        tx, tz = math.cos(angle_rad) * 3.5, math.sin(angle_rad) * 3.5
        x += 1
        tx += 1
        color_name = to_name(color)
        stand = Entity('armor_stand', {'Rotation': [angle + 90, 0], 'PersistenceRequired': True, 'NoGravity': True,
                                       'attributes': [{'id': "minecraft:waypoint_transmit_range", 'base': 100000}]},
                       name=color_name).custom_name_visible(
            True).tag(room.name, 'waypoint', my_tag)
        waypoints_setup.add(
            forceload().add(r(x, z)),
            execute().at(e().tag('waypoints_home')).run(
                stand.summon(r(x, 2, z)),
                waypoint().modify(n().tag(my_tag)).color(color)),
        )
        if radius != radii[0][0]:
            blob = Text.text("█").color(color)
            text = [f'{color_name}\\n{radius_name}\\n', blob, Text('⇧').bold(), blob]
            waypoints_setup.add(
                room.label(r(tx, 2, tz), text, as_facing((angle + 90) % 360), tags=('waypoint',)))

    def waypoints_loop(step):
        yield execute().as_(e().tag('waypoint')).run(waypoint().modify(s()).style(step.elem))
        name = 'Default' if step.elem == RESET else step.elem
        yield Sign.change(waypoint_sign_pos, (name,), start=2)

    room.loop('waypoints', main_clock, home=False).loop(waypoints_loop, (RESET, 'bowtie'))

    room.function('waypoints_on', home=False).add(
        gamerule(LOCATOR_BAR, True),
        tag(e().tag('waypoints_base_home')).add('waypoints_home'),
        execute().at(e().tag('waypoints_home')).run(function(waypoints_setup)),
    )
    room.function('waypoints_off', home=False).add(
        forceload().remove_all(),
        gamerule(LOCATOR_BAR, False),
        tag(e().tag('waypoints_base_home')).remove('waypoints_home'),
        kill(e().tag('waypoint')),
    )

    dialogs_init = room.function('dialogs_init').add(
        WallSign((None, Text('Custom Dialogs').bold())).place(r(0, 4, 1), EAST))
    for i, d in enumerate(restworld.registry('dialog')):
        sign = WallSign((None, to_name(d)), dialog().show(a(), f'restworld:{d}'))
        z = 2 - i % 3
        if i >= 3:
            z -= 1
        dialogs_init.add(sign.place(r(0, 3 - int(i / 3), z), EAST))
