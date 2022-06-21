from __future__ import annotations

from typing import Iterable

from pyker.commands import EAST, r, mc, entity, Entity, facing_info, good_block, Block, NORTH, SOUTH, WEST, self, MOVE
from pyker.info import colors, Color
from pyker.simpler import Sign, Item, WallSign
from restworld.rooms import Room, label, woods, stems
from restworld.world import restworld, main_clock, kill_em


def room():
    room = Room('blocks', restworld, EAST, ('Blocks,', 'Paintings,', 'Banners,', 'DIY'))

    block_list_score = room.score('block_list')

    name_stand = Entity('armor_stand', nbt={'Invisible': True, 'NoGravity': True, 'CustomNameVisible': True})
    name_stand.tag('block_list')
    all_names = room.function('all_names', needs_home=False)

    def blocks(name, facing, block_lists: Iterable[Block, str] | Iterable[Iterable[Block, str]], dx=0, dz=0, size=0,
               labels=None):
        facing_data = facing_info(facing)

        if not isinstance(block_lists, list):
            block_lists = list(block_lists)
        if not isinstance(block_lists[0], Iterable) or isinstance(block_lists[0], str):
            block_lists = [block_lists, ]
        for i, sublist in enumerate(block_lists):
            nsublist = []
            for block in sublist:
                nsublist.append(good_block(block))
            block_lists[i] = nsublist
        show_list = len(set(x.kind for x in block_lists[0])) > 1

        block_loop = room.loop(name, main_clock)
        block_init = room.function(name + '_init', exists_ok=True).add(
            Sign(()).place(r(facing_data[0], 2, facing_data[1]), facing)
        )
        if show_list:
            block_init.add(
                mc.execute().if_().score(block_list_score).matches(0).run().kill(entity().tag('block_list_%s' % name))
            )
            names = room.function(name + '_names', needs_home=False)
            all_names.add(mc.function(names.full_name))

        def blocks_loop_body(step):
            i = step.i
            x = z = 0
            x_size = 0

            for block_list in block_lists:
                block = block_list[i]
                signage = labels[i] if labels else block.sign_text
                if len(signage) < 4:
                    signage = ('', *signage)
                    signage = signage + ('',) * (4 - len(signage))

                yield mc.setblock(r(x, 3, z), block)
                yield mc.data().merge(r(x + facing_data[0], 2, z + facing_data[1]), Sign.lines_nbt(signage))

                if show_list:
                    stand = name_stand.clone()
                    block_list_name = 'block_list_%s_%d_%d' % (name, x, z)
                    block_list_block_name = 'block_list_%s_%d_%d_%d' % (name, x, z, i)
                    stand.tag('block_list_%s' % name, block_list_name, block_list_block_name)
                    stand.merge_nbt({'CustomName': block.display_name})
                    stand_y = 2.5 + i * 0.24
                    names.add(
                        stand.summon(r(x, stand_y, z))
                    )

                x += dx
                x_size += 1
                if size == 0:
                    z += dz
                elif x_size >= size:
                    x = 0
                    z += dz
                    x_size = 0

        block_loop.loop(blocks_loop_body, range(0, len(block_lists[0])))

        return block_init, block_loop

    def job_sites(name, facing, sites, stages=None):
        if stages is None:
            stages = {}
        all = []
        for b in sites:
            if b in stages:
                all.extend(Block(b, s) for s in stages[b])
            else:
                all.append(Block(b))
        blocks(name, facing, all)

    def amethyst_loop(step):
        block = good_block(step.elem)
        if step.elem == amethyst_phases[0]:
            yield mc.setblock(r(0, 4, 0), block.kind)
        else:
            yield mc.setblock(r(0, 4, 0), 'budding_amethyst')
            if ' Bud' in block.display_name or 'Cluster' in block.display_name:
                yield mc.setblock(r(0, 3, 0), block.clone().merge_state({'facing': 'down'}))
                yield mc.setblock(r(0, 5, 0), block.clone().merge_state({'facing': 'up'}))
                for offset in (NORTH, EAST, WEST, SOUTH):
                    face = facing_info(offset)
                    yield mc.setblock(r(face[0], 4, face[1]), block.clone().merge_state({'facing': offset}))
        mc.data().merge(r(0, 2, -1), block.sign_nbt())

    room.functions['blocks_room_init'].add(
        label(r(-16, 2, 3), 'List Blocks'),
        label(r(-16, 2, -3), 'List Blocks'),
        label(r(-43, 2, 3), 'List Blocks'),
        label(r(-43, 2, -3), 'List Blocks'),
        mc.kill(entity().tag('block_list'))
    )

    room.function('blocks_sign_init').add(
        mc.execute().at(entity().tag('blocks_home', '!no_expansion')).run().data().merge(r(0, 2, -1), {
            'Text1': 'function restworld:blocks/toggle_expand'}),
        mc.execute().at(entity().tag('blocks_home', '!no_expansion')).run().data().merge(r(0, 2, 1), {
            'Text1': 'function restworld:blocks/toggle_expand'}),

        mc.execute().at(entity().tag('blocks_home', 'no_expansion')).run().data().merge(r(0, 2, -1), {
            'Text1': 'say Sorry, cannot expand this block'}),
        mc.execute().at(entity().tag('blocks_home', 'no_expansion')).run().data().merge(r(0, 2, 1), {
            'Text1': 'say Sorry, cannot expand this block'}),
        mc.tag(entity().tag('block_sign_home')).add('no_expansion'),
    )

    room.function('anvil_init', exists_ok=True).add(Sign((None, 'Anvil')).place(r(0, 2, -1), NORTH))
    blocks('anvil', NORTH, list(Block(b, state={'facing': WEST}) for b in ('Anvil', 'Chipped Anvil', 'Damaged Anvil')))

    bee_nests = [[], []]
    for i in range(0, 6):
        state = {'facing': SOUTH, 'honey_level': i}
        bee_nests[0].append(Block('Beehive', state=state))
        bee_nests[1].append(Block('Bee Nest', state=state))
    blocks('bee_nest', SOUTH, bee_nests, dx=-3)
    blocks('bricks', NORTH, (
        'Bricks', 'Quartz Bricks', 'Mud Bricks', 'Deepslate|Bricks', 'Cracked|Deepslate|Bricks', 'Deepslate|Tiles',
        'Cracked|Deepslate|Tiles', 'Prismarine Bricks', 'Nether Bricks', 'Cracked|Nether Bricks',
        'Chiseled|Nether Bricks', 'Red|Nether Bricks'))
    blocks('campfire', NORTH, (
        Block('Campfire', {'lit': True}),
        Block('campfire', {'lit': False}, display_name='Campfire|Unlit'),
        Block('Soul Campfire', {'lit': True}),
        Block('soul_campfire', {'lit': False}, display_name='Soul Campfire|Unlit'),
    ))
    room.function('campfire_enter').add(mc.function('restworld:/blocks/campfire_cur'))
    room.function('campfire_exit').add(mc.setblock(r(0, 3, 0), Block('campfire', {'lit': False})))
    blocks('clay', SOUTH, ('Clay', 'Mud', 'Muddy|Mangrove Roots', 'Packed Mud'))
    blocks('cobble', NORTH, ('Cobblestone', 'Mossy|Cobblestone', 'Cobbled|Deepslate'))

    # types = ("Copper Block", "Exposed Copper", "Weathered|Copper", "Oxidized Copper")
    # block = list(x.replace('Copper', 'Cut Copper').replace(' Block', '').replace(' Cut', '|Cut') for x in types)
    # waxed_types = tuple("Waxed|%s" % x for x in types)
    # waxed_block = tuple("Waxed|%s" % x for x in block)
    # prefs=('execute if score waxed_copper funcs matches 0 run', 'execute if score waxed_copper funcs matches 1 run')
    # blocks(types, waxed_types, block, waxed_block, dx=-3, prefixes=(prefs, prefs))

    woodlike = woods + stems
    leaves = ['%s Leaves' % x for x in woods] + ['Warped Wart Block', 'Nether Wart Block']
    logs = ['%s Log' % x for x in woods] + [('%s Stem' % x) for x in stems]
    wood = ['%s Wood' % x for x in woods] + [('%s Hyphae' % x) for x in stems]
    stripped_logs = ['Stripped|%s Log' % x for x in woods] + [('Stripped|%s Stem' % x) for x in stems]
    stripped_woods = ['Stripped|%s Wood' % x for x in woods] + [('Stripped|%s Hyphae' % x) for x in stems]
    blocks('wood_blocks', SOUTH, (tuple('%s Planks' % f for f in woodlike),
                                  stripped_logs,
                                  logs,
                                  wood,
                                  leaves,
                                  stripped_woods), dx=-3, dz=-3, size=2)

    sites = (
        'Cauldron',
        'Water Cauldron',
        'Lava Cauldron',
        'Powder Snow Cauldron',
    )
    stages = {
        'Water Cauldron': list({'level': t} for t in range(1, 4)),
        'Powder Snow Cauldron': list({'level': t} for t in range(3, 0, -1)),
    }
    job_sites('cauldron', NORTH, sites, stages)
    job_sites('composter', NORTH, ('Composter',), {'Composter': tuple({'level': t} for t in range(0, 9))})

    for f in ('amethyst',):
        room.function(f + '_init').add(mc.tag(entity().tag(f + '_home')).add('no_expansion'))
    amethyst_phases = (
        'Amethyst Block', 'Budding Amethyst', 'Small Amethyst|Bud', 'Medium Amethyst|Bud', 'Large Amethyst|Bud',
        'Amethyst Cluster')

    room.loop('amethyst', main_clock).add(
        mc.fill(r(-1, 3, -1), r(1, 5, 1), 'air')
    ).loop(
        amethyst_loop, amethyst_phases, bounce=True
    ).add(
        mc.kill(entity().type('item').nbt({'Item': Item.nbt('amethyst_shard')}))
    )

    def bell_loop(step):
        if step.i == 0:
            yield mc.setblock(r(-1, 3, 0), 'air')
            yield mc.setblock(r(1, 3, 0), 'air')
            yield mc.setblock(r(0, 4, 0), 'stone_slab')
        elif step.i == 1:
            yield mc.setblock(r(-1, 3, 0), Block('stone_stairs', state={'facing': EAST}))
            yield mc.setblock(r(1, 3, 0), 'air')
            yield mc.setblock(r(0, 4, 0), 'air')
        elif step.i == 2:
            yield mc.setblock(r(-1, 3, 0), 'air')
            yield mc.setblock(r(1, 3, 0), 'air')
            yield mc.setblock(r(0, 4, 0), 'air')
        else:
            yield mc.setblock(r(-1, 3, 0), Block('stone_stairs', {'facing': EAST}))
            yield mc.setblock(r(1, 3, 0), Block('stone_stairs', {'facing': WEST}))
            yield mc.setblock(r(0, 4, 0), 'air')
        yield mc.setblock(r(0, 3, 0), Block('bell', state={'attachment': step.elem, 'facing': facing[step.i]}))

    attachments = ('ceiling', 'single_wall', 'floor', 'double_wall')
    facing = (NORTH, WEST, NORTH, WEST)
    room.loop('bell', main_clock).add(mc.setblock(r(0, 3, 0), 'air')).loop(bell_loop, attachments)

    room.function('brewing_stand_init').add(mc.function('restworld:containers/brewing_init'))
    room.function('brewing_stand', main_clock).add(
        mc.execute().positioned(r(0, 1, 0)).run().function('restworld:containers/brewing_main'))

    def cake_loop(step):
        yield mc.setblock(r(0, 3, 0), Block('cake', {'bites': step.elem}))
        yield mc.data().merge(r(0, 2, -1), {'Text3': 'Bites: %d' % step.elem})

    room.function('cake_init').add(mc.data().merge(r(0, 2, -1), {'Text2': 'Cake'}))
    room.loop('cake', main_clock).loop(cake_loop, range(0, 7), bounce=True)

    def chest_loop(step):
        step.elem.merge_state({'facing': NORTH})
        yield mc.setblock(r(0, 3, 0), step.elem)
        txt = {'Text2': 'Trapped' if 'T' in step.elem.display_name else '',
               'Text3': 'Double Chest' if 'type' in step.elem.state else 'Chest'}
        yield mc.data().merge(r(0, 2, -1), txt)
        if 'type' in step.elem.state:
            step.elem.state['type'] = 'left'
            yield mc.setblock(r(-1, 3, 0), step.elem)
        else:
            yield mc.setblock(r(-1, 3, 0), 'air')

    types = (
        Block('Chest'),
        Block('Ender Chest'),
        Block('Trapped Chest'),
        Block('Chest', state={'type': 'right'}),
        Block('Trapped Chest', state={'type': 'right'}),
    )
    room.loop('chest', main_clock).loop(chest_loop, types)

    coloring_coords = (r(1, 4, 6), r(-13, 2, -1))
    lit_candles = room.score('lit_candles')

    def command_block_loop(step):
        block = Block(step.elem[0], {'facing': WEST, 'conditional': str(step.elem[1]).lower()})
        yield mc.setblock(r(0, 3, 0), block)
        words = step.elem[0].split(' ')
        modifier = '' if len(words) == 2 else words[0]
        yield mc.data().merge(r(0, 2, 1),
                              Sign.lines_nbt((None, modifier, None, '(Conditional)' if step.elem[1] else '')))

    room.function('command_blocks_init').add(WallSign((None, None, 'Command Block', None)).place(r(0, 2, 1), SOUTH))
    room.loop('command_blocks', main_clock).loop(command_block_loop, (
        ("Command Block", True), ("Command Block", False),
        ("Chain Command Block", False), ("Chain Command Block", True),
        ("Repeating Command Block", True), ("Repeating Command Block", False),
        ("Command Block", False), ("Command Block", True),
        ("Chain Command Block", True), ("Chain Command Block", False),
        ("Repeating Command Block", False), ("Repeating Command Block", True),
    ))

    room.function('contract_all').add(
        mc.execute().as_(entity().tag('blocks_home', '!no_expansion', 'expander')).run().execute().at(
            self()).run().function("restworld:blocks/toggle_expand_at"))
    room.function('contract_dripstone').add(
        # Erase the front and back lines
        mc.fill(r(1, 12, 1), r(-1, 3, 1), 'air'),
        mc.fill(r(1, 12, -1), r(-1, 3, -1), 'air'),

        ## Erase either side
        mc.fill(r(1, 12, 0), r(1, 3, 0), 'air'),
        mc.fill(r(-1, 12, 0), r(-1, 3, 0), 'air'),
    )
    room.function('contract_fire').add(
        mc.fill(r(1, 5, 1), r(-1, 3, -1), 'air'),
        mc.function('restworld:blocks/fire_cur'))
    room.function('contract_gen4ric').add(
        mc.clone(r(0, 5, 0), r(0, 6, 0), r(0, -10, 0)),
        mc.fill(r(-1, 3, -1), r(1, 6, 1), 'air'),
        mc.clone(r(0, -9, 0), r(0, -10, 0), r(0, 3, 0)).replace(MOVE),
        mc.setblock(r(0, 2, 0), 'stone'),
        mc.fill(r(-1, 2, -1), r(1, 2, 1), 'air').replace('barrier'),
        mc.setblock(r(0, 2, 0), 'barrier')
    )


    def colorings(is_plain, color):
        fills = (
            'stained_glass', 'stained_glass_pane', 'wool', 'banner', 'shulker_box', 'carpet', 'concrete',
            'concrete_powder',
            'terracotta')
        plain_fills = tuple(
            Block(x) for x in ('glass', 'glass_pane', 'air', 'air', 'shulker_box', 'air', 'air', 'air', 'terracotta'))
        candles = [Block('candle' if is_plain else color.name + '_candle', {'candles': x, 'lit': True}) for x in
                   range(1, 5)]
        candles.append(Block('candle_cake', {'lit': True}))

        for i, which in enumerate(fills):
            state = {'rotation': 2} if which == 'banner' else {}
            if is_plain:
                filler = plain_fills[i]
            else:
                filler = Block('%s_%s' % (color.id, which), state)
            yield mc.fill(*coloring_coords, filler).replace('#restworld:' + which)

        for candle in candles:
            candle = Block('candle' if is_plain else color.name + '_candle', {'lit': True})
            for count in range(1, 6):
                if count < 5:
                    candle.merge_state({'candles': count})
                    filter = '#restworld:candle[candles=%d]' % count
                else:
                    candle = Block(candle.kind + '_cake', {'lit': True})
                    filter = '#restworld:candle_cake'
                yield mc.execute().if_().score(lit_candles).matches(0).run().fill(*coloring_coords, candle).replace(filter)
                candle.merge_state({'lit': False})
                yield mc.execute().unless().score(lit_candles).matches(0).run().fill(*coloring_coords, candle).replace(filter)

        yield mc.data().merge(r(-7, 0, 3), {'name': 'restworld:%s_terra' % color.id, 'showboundingbox': False})

        if is_plain:
            mc.fill(r(-9, 2, 2), r(-9, 2, 3), 'air')
            mc.fill(*coloring_coords, 'air').replace('#standing_signs')
            mc.data().merge(entity().tag('colorings_item_frame').limit(1), {'Item': {'Count': 0}})
        else:
            mc.setblock(r(-9, 2, 2), Block('%s_bed' % color.id, {'facing': NORTH, 'part': 'head'}))
            mc.setblock(r(-9, 2, 3), Block('%s_bed' % color.id, {'facing': NORTH, 'part': 'foot'}))
            frame_nbt = {'Item': Item.nbt('%s_dye' % color.id)}
            frame_nbt['ItemRotation'] = 0
            mc.data().merge(entity().tag('colorings_item_frame').limit(1), frame_nbt)

        if is_plain:
            leather_color = {}
            horse_leather_color = {}
            llama_decor = {'Count': 0}
            sheep_nbt = {'Sheared': True}
        else:
            leather_color = {'tag': {'Variant': 2, 'display': {'color': color.leather}}}
            horse_leather_color = {'tag': {'display': {'color': color.leather}}}
            llama_decor = {'id': color.id + '_carpet', 'Count': 1}
            sheep_nbt = {'Color': color.num, 'Sheared': False}

        if is_plain:
            yield kill_em(entity().tag('colorings_horse'))
            horse = Entity('horse', nbt=
            {'Variant': 5, 'ArmorItem': {'id': 'leather_horse_armor', 'Count': 1}, 'Rotation': [0, 0],
             'Tame': True, 'NoAI': True, 'Silent': True}).tag('colorings_horse', 'colorings_item',
                                                              'colorings_names')
            yield horse.summon(r(0.2, 2, 4.4))

        yield mc.data().merge(entity().tag('colorings_armor_stand').limit(1), {
            'ArmorItems': [Item.nbt('leather_boots', nbt=leather_color), Item.nbt('leather_leggins', nbt=leather_color),
                           Item.nbt('leather_chestplate', nbt=leather_color),
                           Item.nbt('leather_helmet', nbt=leather_color)]})
        yield mc.data().merge(entity().tag('colorings_horse').limit(1),
                              {'ArmorItem': Item.nbt('leather_horse_armor', nbt=horse_leather_color)})
        yield mc.data().merge(entity().tag('colorings_llama').limit(1), {'DecorItem': llama_decor})
        yield mc.data().merge(entity().tag('colorings_sheep').limit(1), sheep_nbt)

        yield mc.data().merge(r(-4, 2, 4), {'Text2': color.name})
        yield mc.execute().as_(entity().tag('colorings_names')).run().data().merge(self(), {'CustomName': color.name})

        yield mc.data().merge(r(0, 0, -1), {'name': 'restworld:%s_terra' % 'plain' if is_plain else color.id})
        yield mc.data().merge(r(1, 2, -0), {'Text1': color.name})

    def colored_signs(color, render):
        signables = woods + stems
        for w in range(0, len(signables)):
            wood = signables[w]
            row_len = 4 if w < 4 else 3 if w < 7 else 2
            x = w % row_len - 12
            y = (4 - row_len) + 2
            z = -(w % row_len) + 3
            yield from render(x, y, z, color, Block(wood))

    def render_signs_glow(x, y, z, _, _2):
        lit_signs = room.score('lit_signs')
        yield mc.execute().if_().score(lit_signs).matches(0).run().data().merge(r(x, y, z),
                                                                                {'GlowingText': False, 'Text4': 'Text'})
        yield mc.execute().if_().score(lit_signs).matches(1).run().data().merge(r(x, y, z),
                                                                                {'GlowingText': True, 'Text4': 'Text'})

    def render_signs(x, y, z, color, _):
        yield mc.data().merge(r(x, y, z), {'Color': color.id, 'Text3': color.name})

    def colorings_loop(step):
        yield from colorings(False, step.elem)
        yield from colored_signs(step.elem, render_signs)

    room.function('colorings_init').add(
        mc.kill(entity().tag('colorings_item')),

        Entity('item_frame', {
            'Facing': 3, 'Tags': ['colorings_item_frame', 'colorings_item'], 'Item': Item.nbt('stone'),
            'Fixed': True}).summon(r(-4.5, 4, 0.5)),
        Entity('horse', {
            'Variant': 5, 'Tags': ['colorings_horse', 'colorings_item', 'colorings_names'],
            'ArmorItem': Item.nbt('leather_horse_armor'), 'Rotation': [0, 0], 'Tame': True, 'NoAI': True,
            'Silent': True}).summon(r(0.2, 2, 4.4)),
        Entity('armor_stand', {
            'Tags': ['colorings_armor_stand', 'colorings_item'], 'Rotation': [30, 0]}).summon(r(-1.1, 2, 3)),
        Entity('llama', {
            'Tags': ['colorings_llama', 'colorings_item', 'colorings_names'], 'Variant': 1, 'Tame': True, 'NoAI': True,
            'Silent': True, 'Rotation': [0, 0], 'Leashed': True}).summon(r(-11, 2, 5.8)),
        Entity('sheep', {
            'Tags': ['colorings_sheep', 'colorings_item'], 'Variant': 1, 'NoAI': True, 'Silent': True,
            'Rotation': [-35, 0], 'Leashed': True}).summon(r(-9.0, 2, 5.0)),

        mc.execute().as_(entity().tag('colorings_names')).run().data().merge(self(), {'CustomNameVisible': True}),

        WallSign((None, 'Terracotta')).place(r(-1, 3, 1), SOUTH),
        WallSign((None, 'Shulker Box')).place(r(-3, 3, 1), SOUTH),
        WallSign((None, 'Dye')).place(r(-4, 3, 1, ), SOUTH),
        WallSign((None, 'Concrete')).place(r(-5, 3, 1), SOUTH),
        WallSign((None, 'Glass')).place(r(-7, 3, 1), SOUTH),

        colored_signs(None,
                      lambda x, y, z, _, wood: Sign((wood.kind, 'Sign With', 'Default', 'Text')).place(r(x, y, z), 14)),
        WallSign([]).place(r(-4, 2, 4, ), SOUTH),

        mc.kill(entity().type('item')),

        label(r(-1, 2, 7), 'Lit Candles'),
        label(r(-7, 2, 7), 'Plain'),
        label(r(-11, 2, 3), 'Glowing'),
    ),
    room.loop('colorings', main_clock).add(
        mc.fill(r(-9, 2, 2), r(-9, 2, 3), 'air')
    ).loop(colorings_loop, colors).add(
        colored_signs(None, render_signs_glow),
        mc.setblock(r(-7, -1, 3), 'redstone_block'),
        mc.setblock(r(-7, -1, 3), 'air'),
    )
    room.function('colorings_plain_off').add(
        mc.clone((coloring_coords[0][0], coloring_coords[0][1] - coloring_coords[1][1] + 1, coloring_coords[0][2]),
                 (coloring_coords[1][0], 0, coloring_coords[1][2]),
                 (coloring_coords[1][0], coloring_coords[1][1] - 1, coloring_coords[1][2])),

        mc.tag(entity().tag('colorings_base_home')).add('colorings_home'),
        mc.execute().at(entity().tag('colorings_home')).run().function('restworld:/blocks/colorings_cur'),
        mc.kill(entity().type('item').distance((None, 20))),
    )
    room.function('colorings_plain_on').add(
        mc.tag(entity().tag('colorings_base_home')).remove('colorings_home'),
        mc.clone((coloring_coords[0][0], coloring_coords[0][1], coloring_coords[0][2]),
                 (coloring_coords[1][0], coloring_coords[1][1] - 1, coloring_coords[1][2]),
                 (coloring_coords[0][0], 0, coloring_coords[0][2])),
        colorings(True, Color('Plain', 0x0)),
        mc.setblock(r(-7, -1, 3), 'redstone_torch'),
        mc.setblock(r(-7, -1, 3), 'air'),
        mc.kill(entity().type('item').distance((None, 20))),
    )
    room.functions['colorings_home'].add(mc.tag(entity().tag('colorings_home')).add('colorings_base_home'))
    room.function('colorings_enter').add(
        mc.execute().as_(entity().tag('colorings_names')).run().data().merge(self(), {'CustomNameVisible': True}))
    room.function('colorings_exit').add(
        mc.execute().as_(entity().tag('colorings_names')).run().data().merge(self(), {'CustomNameVisible': False}))
    room.function('colored_beam_enter').add(mc.setblock(r(0, 1, 0), 'iron_block'))
    room.function('colored_beam_exit').add(mc.setblock(r(0, 1, 0), 'white_concrete'))

    for b in (
            'amethyst', 'anvil', 'bell', 'brewing_stand', 'cake', 'campfire', 'cauldron', 'chest', 'colored_beam',
            'colorings', 'composter'):
        room.function(b + '_init', exists_ok=True).add(mc.tag(entity().tag(b + '_home')).add('no_expansion'))

    room.function('contracter').add(
        mc.execute().if_().entity(entity().tag('fire_home').distance((None, 1))).run().function(
            "restworld:blocks/contract_fire"),
        mc.execute().if_().entity(entity().tag('dripstone_home').distance((None, 1))).run().function(
            "restworld:blocks/contract_dripstone"),
        mc.execute().unless().entity(entity().tag('fire_home').distance((None, 1))).unless().entity(
            entity().tag('dripstone_home').distance((None, 1))).run().function("restworld:blocks/contract_generic"),
    )
