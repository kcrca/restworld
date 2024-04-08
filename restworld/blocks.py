from __future__ import annotations

import re
from typing import Iterable, Union

from pynecraft import info
from pynecraft.base import DOWN, EAST, EQ, NORTH, Nbt, RelCoord, SOUTH, WEST, as_facing, r, to_id, to_name
from pynecraft.commands import Block, Commands, Entity, MOD, MOVE, as_block, clone, data, e, execute, fill, function, \
    item, kill, s, say, setblock, summon, tag
from pynecraft.function import Loop
from pynecraft.info import Color, colors, sherds, stems
from pynecraft.simpler import Item, ItemFrame, Region, Sign, TextDisplay, WallSign
from restworld.rooms import Room
from restworld.world import fast_clock, kill_em, main_clock, restworld


def room():
    room = Room('blocks', restworld, EAST, ('Blocks,', 'Paintings,', 'Banners,', 'DIY, Models'))

    block_list_score = room.score('block_list')

    list_scale = 0.6

    def blocks(name, facing, block_lists: Iterable[Union[Block, str]] | Iterable[Iterable[Union[Block, str]]], dx=0,
               dz=0, size=0, labels=None, clock=main_clock, score=None, air=False):
        facing = as_facing(facing)

        if not isinstance(block_lists, list):
            block_lists = list(block_lists)
        if not isinstance(block_lists[0], Iterable) or isinstance(block_lists[0], str):
            block_lists = [block_lists, ]
        for i, sublist in enumerate(block_lists):
            nsublist = []
            for block in sublist:
                # noinspection PyTypeChecker
                if block == '':
                    block = Block(id='structure_void', name='')
                nsublist.append(as_block(block))
            block_lists[i] = nsublist
        # noinspection PyUnresolvedReferences
        show_list = len(set(x.id for x in block_lists[0])) > 1

        block_loop = room.loop(name, clock, score=score)
        block_init = room.function(name + '_init', exists_ok=True).add(
            WallSign(()).place(r(facing.dx, 2, facing.dz), facing)
        )
        if show_list:
            block_init.add(execute().if_().score(block_list_score).matches(0).run(kill(e().tag(f'block_list_{name}'))))
            names = room.function(name + '_names', home=False)
            block_init.add(function(names.full_name))

        def blocks_loop_body(step):
            i = step.i
            x = z = 0
            x_size = 0

            for block_list in block_lists:
                block = block_list[i]
                signage = labels[i] if labels else block.sign_text
                if signage == ('Structure Void',):
                    signage = ()
                if len(signage) < 3:
                    signage = signage + ('',) * (3 - len(signage))

                if air:
                    yield setblock(r(x, 3, z), 'air')
                yield setblock(r(x, 3, z), block)
                # Preserve the 'expand' response
                yield Sign.change(r(x + facing.dx, 2, z + facing.dz), signage, start=1)

                if show_list:
                    block_list_name = f'block_list_{name}_{x}_{z}'
                    block_list_block_name = f'block_list_{name}_{x}_{z}_{i}'
                    # The opacity of 25 means "invisible" so it starts out that way
                    holder = TextDisplay(
                        block.name,
                        nbt={'Rotation': [180.0, 0.0], 'text_opacity': 25, 'background': 0,
                             'billboard': 'vertical', 'shadow_radius': 0}).scale(list_scale).tag(
                        'blocks', 'block_list', f'block_list_{name}', block_list_name, block_list_block_name)
                    names.add(holder.summon(r(x, 4.25 + i * (list_scale / 4), z)))

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
                id = Block(b).id
                for s in stages[b]:
                    n = b
                    for i, (k, v) in enumerate(s.items()):
                        if k != 'facing':
                            n += f'|{to_name(k)}: {to_name(str(v))}'
                    all.append(Block(id, s, name=n))
            else:
                all.append(Block(b))
        blocks(name, facing, all)

    room_init_functions(room, block_list_score)

    room.function('anvil_init', exists_ok=True).add(WallSign((None, 'Anvil')).place(r(0, 2, -1), NORTH))
    blocks('anvil', NORTH, list(Block(b, state={'facing': WEST}) for b in ('Anvil', 'Chipped Anvil', 'Damaged Anvil')))

    bee_nests = [[], []]
    for i in range(0, 6):
        state = {'facing': SOUTH, 'honey_level': i}
        bee_nests[0].append(Block('beehive', state=state, name=f'Beehive|Honey Level: {i}'))
        bee_nests[1].append(Block('bee_nest', state=state, name=f'Bee Nest|Honey Level: {i}'))
    blocks('bee_nest', SOUTH, bee_nests, dx=-3)
    bookshelves = ['Bookshelf']
    bookshelves.extend((
        Block('chiseled_bookshelf', {'facing': SOUTH, }, name='Empty|Chiseled|Bookshelf'),
        Block('chiseled_bookshelf',
              {'facing': SOUTH, 'slot_0_occupied': True, 'slot_4_occupied': True, 'slot_5_occupied': True, },
              name='Partly Filled|Chiseled|Bookshelf'),
        Block('chiseled_bookshelf',
              {'facing': SOUTH,
               'slot_0_occupied': True, 'slot_1_occupied': True, 'slot_2_occupied': True,
               'slot_3_occupied': True, 'slot_4_occupied': True, 'slot_5_occupied': True, },
              name='Full|Chiseled|Bookshelf')))
    blocks('bookshelves', SOUTH, bookshelves)
    blocks('bricks', NORTH, (
        'Bricks', 'Quartz Bricks', 'Mud Bricks', 'Deepslate|Bricks', 'Cracked|Deepslate|Bricks', 'Deepslate|Tiles',
        'Cracked|Deepslate|Tiles', 'Prismarine Bricks', 'Tuff Bricks', 'Chiseled Tuff|Bricks', 'Nether Bricks',
        'Cracked|Nether Bricks', 'Chiseled|Nether Bricks', 'Red|Nether Bricks'))
    blocks('stone_bricks', NORTH, (
        'Stone Bricks', 'Mossy|Stone Bricks', 'Cracked|Stone Bricks', 'Chiseled|Stone Bricks',
        'Polished|Blackstone Bricks', 'Cracked Polished|Blackstone Bricks', 'End Stone|Bricks'))
    blocks('chiseled', NORTH,
           ('Chiseled|Deepslate', 'Chiseled|Polished|Blackstone', 'Chiseled|Quartz Block', 'Chiseled|Tuff'))
    campfire_food = room.score('campfire_food')
    campfire_init, campfire_main = blocks('campfire', NORTH, (
        Block('Campfire', {'lit': True}),
        Block('campfire', {'lit': False}, name='Campfire|Unlit'),
        Block('Soul Campfire', {'lit': True}),
        Block('soul_campfire', {'lit': False}, name='Soul Campfire|Unlit'),
    ))
    campfire_init.add(room.label(r(-1, 2, 0), 'Cook', SOUTH))
    campfire_main.add(
        execute().if_().score(campfire_food).matches(0).run(data().remove(r(0, 3, 0), 'Items')),
        # For some reason the Count is required here
        execute().if_().score(campfire_food).matches(1).run(data().merge(
            r(0, 3, 0),
            {'Items':
                 [Item.nbt_for('porkchop', {'Slot': 0, 'Count': 1}), Item.nbt_for('beef', {'Slot': 1, 'Count': 1}),
                  Item.nbt_for('chicken', {'Slot': 2, 'Count': 1}), Item.nbt_for('mutton', {'Slot': 3, 'Count': 1})],
             'CookingTotalTimes': Nbt.TypedArray('i', (0x7fffffff, 0x7fffffff, 0x7fffffff, 0x7fffffff))}))
    )
    room.function('campfire_enter').add(function('restworld:/blocks/campfire_cur'))
    room.function('campfire_exit').add(setblock(r(0, 3, 0), Block('campfire', {'lit': False})))
    blocks('clay', SOUTH, ('Clay', 'Mud', 'Muddy|Mangrove Roots', 'Packed Mud'))
    blocks('cobble', NORTH, ('Cobblestone', 'Mossy|Cobblestone', 'Cobbled|Deepslate'))
    blocks('deepslate', NORTH, (
        'Deepslate', 'Chiseled|Deepslate', 'Polished|Deepslate', 'Cracked|Deepslate|Bricks', 'Cracked|Deepslate|Tiles',
        'Deepslate|Bricks', 'Deepslate|Tiles', 'Cobbled|Deepslate', 'Reinforced|Deepslate'))
    # Have to replace it with air first, so air=True ... https://bugs.mojang.com/browse/MC-260399
    # Also, the order for sides is weird, https://bugs.mojang.com/browse/MC-260399
    sherd_names = tuple(sherd.replace('_pottery_sherd', '').title() for sherd in sherds)
    usable_sherds = sherds + sherds
    _, pot_loop = blocks(
        'decorated_pot', NORTH, ('decorated_pot',) + tuple(
            Block('decorated_pot',
                  nbt={'sherds': [usable_sherds[i], usable_sherds[i + 1], usable_sherds[i + 2]]},
                  name=f'Decorated Pot|{sherd_names[i]}') for i in range(len(sherds))), air=True, clock=fast_clock)

    blocks('dirt', SOUTH, ('Dirt', 'Coarse Dirt', 'Rooted Dirt', 'Farmland'))
    blocks('end', NORTH, ('End Stone', 'End Stone|Bricks'))
    blocks('frosted_ice', SOUTH,
           list(Block('frosted_ice', {'age': i}, name=f'Frosted Ice|Age: {i}') for i in range(0, 4)))
    blocks('glass', SOUTH, ('Glass', 'Tinted Glass'))
    blocks('lighting', SOUTH, (
        'Glowstone', 'Sea Lantern', 'Shroomlight', 'Ochre|Froglight', 'Pearlescent|Froglight', 'Verdant|Froglight',
        'End Rod'))
    room.function('ladder_init').add(setblock(r(0, 3, 0), 'ladder'))
    blocks('music', SOUTH, (
        Block('Note Block'), Block('Jukebox'),
        Block('jukebox', {'has_record': True}, {'IsPlaying': True, 'RecordItem': {'id': 'music_disc_pigstep'}},
              name='Jukebox|Playing')))
    blocks('netherrack', NORTH, ('Netherrack', 'Warped Nylium', 'Crimson Nylium'))
    blocks('obsidian', SOUTH, ('Obsidian', 'Crying Obsidian'))
    blocks('prismarine', SOUTH, ('Prismarine', 'Prismarine Bricks', 'Dark Prismarine'))
    blocks('pumpkin', SOUTH, (
        'Pumpkin', Block('Carved Pumpkin', {'facing': SOUTH}), Block('Jack O Lantern', {'facing': SOUTH})))
    blocks('purpur', NORTH, ('Purpur Block', 'Purpur Pillar'))
    blocks('quartz', NORTH, (
        'Quartz Block', 'Smooth Quartz', 'Quartz Pillar', 'Chiseled Quartz Block', 'Quartz Bricks'))
    blocks('raw_metal', NORTH, ('Raw Iron|Block', 'Raw Copper|Block', 'Raw Gold|Block'))
    blocks('respawn_anchor', NORTH, (Block('Respawn Anchor', {'charges': x}) for x in range(0, 5)),
           labels=tuple(('Respawn Anchor', f'Charges: {x:d}') for x in range(0, 5)))

    suspicious_data = {'item': {'id': 'emerald'}}

    def suspicious(which):
        return (which,) + tuple(
            Block(f'suspicious_{which}', state={'dusted': s}, nbt=suspicious_data,
                  name=f'Suspicious {which.title()}|Dusted: {s}') for s in range(4))

    sands = suspicious('sand')
    gravels = suspicious('gravel')
    blocks('suspicious', SOUTH, (sands, gravels), dx=3, size=2)

    red_sandstone = ('Red Sandstone', 'Smooth|Red Sandstone', 'Cut|Red Sandstone', 'Chiseled|Red Sandstone')
    blocks('sandstone', SOUTH, (red_sandstone, tuple(re.sub(' *Red *', '', f) for f in red_sandstone)), dx=3)
    blocks('slabs', NORTH, ('Smooth Stone|Slab', 'Petrified Oak|Slab'))
    blocks('snow_blocks', SOUTH, ('Powder Snow', 'Snow Block'))
    _, loop = blocks('soil', SOUTH, ('Grass Block', 'Podzol', 'Mycelium', 'Dirt Path'))
    # Make sure the block above is air so it doesn't turn dirt path to dirt instantly.
    loop.add(setblock(r(0, 4, 0), 'air'))
    blocks('soul_stuff', NORTH, ('Soul Sand', 'Soul Soil'))
    blocks('sponge', SOUTH, ('Sponge', 'Wet Sponge'))
    blocks('sticky', SOUTH, ('Slime Block', 'Honey block', 'Honeycomb Block'))

    stone_types = ('Basalt', 'Stone', 'Deepslate', 'Andesite', 'Diorite', 'Granite', 'Tuff', 'Blackstone', 'Basalt')
    polished_types = ('Smooth Basalt', 'Smooth Stone') + tuple(f'Polished|{t}' for t in stone_types[2:])
    blocks('stone', NORTH, (stone_types, polished_types), dz=3)

    copper_blocks = (
        'Copper Block', 'Cut Copper', 'Chiseled Copper', 'Copper Grate', 'Copper Bulb', 'Copper Trapdoor')

    def coppers(oxidation, waxed=False):
        prefix = 'Waxed ' if waxed else ''
        return tuple(f'{prefix}{oxidation}|{f}'.replace(' Block', '') for f in copper_blocks)

    _, copper_loop = blocks('unwaxed_copper_blocks', NORTH,
                            (copper_blocks, coppers('Exposed'), coppers('Weathered'), coppers('Oxidized')),
                            dx=-3, dz=3, size=2)
    blocks('waxed_copper_blocks', NORTH,
           (list(f'Waxed {b}' for b in copper_blocks), coppers('Waxed Exposed'), coppers('Waxed Weathered'),
            coppers('Waxed Oxidized')),
           score=copper_loop.score, dx=-3, dz=3, size=2)

    copper_home = e().tag('copper_blocks_home')
    run_unwaxed = room.function('unwaxed_copper_blocks_run', home=False).add(
        tag(copper_home).remove('waxed_copper_blocks_home'),
        tag(copper_home).add('unwaxed_copper_blocks_home'),
        execute().at(copper_home).run(function('restworld:blocks/unwaxed_copper_blocks_cur')),
    )
    room.function('waxed_copper_blocks_run', home=False).add(
        tag(copper_home).remove('unwaxed_copper_blocks_home'),
        tag(copper_home).add('waxed_copper_blocks_home'),
        execute().at(copper_home).run(function('restworld:blocks/waxed_copper_blocks_cur')),
    )
    room.function('copper_blocks_init').add(
        room.label(r(-2, 2, -1), 'Waxed', looking=SOUTH),
        function(run_unwaxed)
    )

    woods = info.woods  # Read the current state of info.woods, which the version can change
    woodlike = woods + stems
    leaves = [f'{x} Leaves' for x in woods] + ['Warped Wart Block', 'Nether Wart Block']
    logs = [f'{x} Log' for x in woods] + [f'{x} Stem' for x in stems]
    wood = [f'{x} Wood' for x in woods] + [f'{x} Hyphae' for x in stems]
    logs[logs.index('Bamboo Log')] = 'Bamboo Block'
    wood[wood.index('Bamboo Wood')] = 'Bamboo Mosaic'
    leaves[leaves.index('Bamboo Leaves')] = ''
    stripped_logs = ['Stripped|' + x for x in logs]
    stripped_woods = map(lambda x: '' if x == 'Stripped|Bamboo Mosaic' else x, ['Stripped|' + x for x in wood])
    blocks('wood_blocks', SOUTH, (tuple(f'{f} Planks' for f in woodlike),
                                  stripped_logs, logs, wood, leaves, stripped_woods), dx=-3, dz=-3, size=2)

    sites = ('Cauldron', 'Water Cauldron', 'Lava Cauldron', 'Powder Snow|Cauldron')
    stages = {'Water Cauldron': list({'level': t} for t in range(1, 4)),
              'Powder Snow|Cauldron': list({'level': t} for t in range(3, 0, -1)), }
    job_sites('cauldron', NORTH, sites, stages)
    job_sites('composter', NORTH, ('Composter',), {'Composter': tuple({'level': t} for t in range(0, 9))})
    job_sites('grindstone', NORTH, ('Grindstone',),
              {'Grindstone': list({'face': f} for f in ('floor', 'wall', 'ceiling'))})
    job_sites('job_sites_1', NORTH,
              ('Crafting Table', 'Crafter', 'Cartography Table', 'Fletching Table', 'Smithing Table', 'Loom',
               'Stonecutter'))
    job_sites('job_sites_2', NORTH, ('Blast Furnace', 'Smoker', 'Barrel', 'Lectern'),
              {'Blast Furnace': ({'lit': False}, {'lit': True}),
               'Smoker': ({'lit': False}, {'lit': True}),
               'Barrel': ({'facing': NORTH, 'open': True}, {'facing': NORTH, 'open': False}),
               'Lectern': ({'has_book': False}, {'has_book': True})})

    amethyst_phases = (
        'Amethyst Block', 'Budding Amethyst', 'Small Amethyst|Bud', 'Medium Amethyst|Bud', 'Large Amethyst|Bud',
        'Amethyst Cluster')

    def amethyst_loop(step):
        block = as_block(step.elem)
        if step.elem == amethyst_phases[0]:
            yield setblock(r(0, 4, 0), block.id)
        else:
            yield setblock(r(0, 4, 0), 'budding_amethyst')
            if ' Bud' in block.name or 'Cluster' in block.name:
                yield setblock(r(0, 3, 0), block.clone().merge_state({'facing': 'down'}))
                yield setblock(r(0, 5, 0), block.clone().merge_state({'facing': 'up'}))
                for offset in (NORTH, EAST, WEST, SOUTH):
                    facing = as_facing(offset)
                    yield setblock(r(facing.dx, 4, facing.dz), block.clone().merge_state({'facing': offset}))
        yield data().merge(r(0, 2, -1), block.sign_nbt())

    room.loop('amethyst', main_clock).add(
        fill(r(-1, 3, -1), r(1, 5, 1), 'air')
    ).loop(
        amethyst_loop, amethyst_phases, bounce=True
    ).add(kill(e().type('item').nbt({'Item': {'id': 'minecraft:amethyst_shard'}})))

    def bell_loop(step):
        facing = EAST
        if step.elem == 'ceiling':
            yield setblock(r(-1, 3, 0), 'air')
            yield setblock(r(1, 3, 0), 'air')
            yield setblock(r(0, 4, 0), 'stone_slab')
        elif step.elem == 'single_wall':
            yield setblock(r(-1, 3, 0), Block('stone_stairs', state={'facing': EAST}))
            yield setblock(r(1, 3, 0), 'air')
            yield setblock(r(0, 4, 0), 'air')
        elif step.elem == 'double_wall':
            yield setblock(r(-1, 3, 0), Block('stone_stairs', {'facing': EAST}))
            yield setblock(r(1, 3, 0), Block('stone_stairs', {'facing': WEST}))
            yield setblock(r(0, 4, 0), 'air')
        else:
            yield setblock(r(-1, 3, 0), 'air')
            yield setblock(r(1, 3, 0), 'air')
            yield setblock(r(0, 4, 0), 'air')
            facing = NORTH
        yield setblock(r(0, 3, 0), Block('bell', state={'attachment': step.elem, 'facing': facing}))

    attachments = ('ceiling', 'single_wall', 'double_wall', 'floor')
    room.loop('bell', main_clock).add(setblock(r(0, 3, 0), 'air')).loop(bell_loop, attachments)

    def armor_stand_loop(step):
        if step.elem is None:
            nbt = Nbt(ShowArms=False)
        else:
            h, b, la, ra, ll, rl = step.elem
            nbt = Nbt(ShowArms=True,
                      Pose={'Head': h, 'Body': b, 'LeftArm': la, 'RightArm': ra, 'LeftLeg': ll, 'RightLeg': rl})
        yield data().merge(e().tag('pose_stand').limit(1), nbt)

    room.function('armor_stand_init').add(
        room.mob_placer(r(0, 3, 0), NORTH, adults=True).summon('armor_stand', tags=('pose_stand',)),
        room.label(r(-1, 2, 0), "Get Small", SOUTH))
    room.loop('armor_stand', main_clock).loop(
        armor_stand_loop,
        (None,
         ((0, 0, 0), (0, 0, 0), (-10, 0, -10), (0, 0, 10), (0, 0, 0), (0, 0, 0)),
         ((0, 0, -15), (0, -8, 4), (-60, 0, -10), (0, 0, 60), (-10, 0, -10), (0, 0, 0)),
         ((0, 0, 0), (0, -16, 8), (-120, 0, 10), (0, 0, 120), (-20, 0, -20), (0, 0, 0)),
         ((0, 0, 15), (0, -24, 12), (-170, 0, 10), (0, 0, 170), (-30, 0, -30), (0, 0, 0))),
        bounce=True)

    def brewing_stand_loop(step):
        for j in range(0, 3):
            if j in step.elem:
                water_potion = Item('potion', components={'potion_contents': 'water'})
                yield item().replace().block(r(0, 3, 0), f'container.{j:d}').with_(water_potion, 1)
            else:
                yield item().replace().block(r(0, 3, 0), f'container.{j:d}').with_('air')

    room.function('brewing_stand_init').add(setblock(r(0, 3, 0), 'brewing_stand'))
    room.loop('brewing_stand', main_clock).add(
        item().replace().block(r(0, 3, 0), 'container.3').with_('air'),
        item().replace().block(r(0, 3, 0), 'container.4').with_('air'),
        data().merge(r(0, 3, 0), {'BrewTime': 0, 'Fuel': 0}),
    ).loop(brewing_stand_loop, ((), (0,), (1,), (2,), (2, 0), (1, 2), (0, 1), (0, 1, 2)))

    def cake_loop(step):
        yield setblock(r(0, 3, 0), Block('cake', {'bites': step.elem}))
        yield Sign.change(r(0, 2, -1), (None, None, f'Bites: {step.elem:d}'))

    room.function('cake_init').add(WallSign((None, 'Cake')).place(r(0, 2, -1), NORTH))
    room.loop('cake', main_clock).loop(cake_loop, range(0, 7), bounce=True)

    def chest_loop(step):
        step.elem.merge_state({'facing': NORTH})
        yield setblock(r(0, 3, 0), step.elem)
        txt = [None, 'Trapped' if 'T' in step.elem.name else '',
               'Double Chest' if 'type' in step.elem.state else 'Chest']
        if 'Ender' in step.elem.name:
            txt[1] = 'Ender'
        yield Sign.change(r(0, 2, -1), txt)
        if 'type' in step.elem.state:
            step.elem.state['type'] = 'left'
            yield setblock(r(-1, 3, 0), step.elem)
        else:
            yield setblock(r(-1, 3, 0), 'air')

    room.loop('chest', main_clock).loop(chest_loop, (
        Block('Chest'), Block('Trapped Chest'), Block('Ender Chest'), Block('Chest', state={'type': 'right'}),
        Block('Trapped Chest', state={'type': 'right'})))

    def command_block_loop(step):
        block = Block(step.elem[0], {'facing': WEST, 'conditional': str(step.elem[1]).lower()})
        yield setblock(r(0, 3, 0), block)
        words = step.elem[0].split(' ')
        modifier = '' if len(words) == 2 else words[0]
        sign_nbt = Sign.lines_nbt((None, modifier, 'Command Block', '(Conditional)' if step.elem[1] else ''))
        yield data().merge(r(0, 2, 1), {'front_text': sign_nbt})

    room.function('command_blocks_init').add(WallSign((None, None, 'Command Block', None)).place(r(0, 2, 1), SOUTH))
    room.loop('command_blocks', main_clock).loop(command_block_loop, (
        ('Command Block', True), ('Command Block', False),
        ('Chain Command Block', False), ('Chain Command Block', True),
        ('Repeating Command Block', True), ('Repeating Command Block', False),
        ('Command Block', False), ('Command Block', True),
        ('Chain Command Block', True), ('Chain Command Block', False),
        ('Repeating Command Block', False), ('Repeating Command Block', True),
    ))

    def dripstone_loop(step):
        for j in range(0, step.elem):
            yield setblock(r(0, 4 + j, 0), Block('pointed_dripstone', {
                'thickness': 'tip', 'vertical_direction': 'up'}))
            yield setblock(r(0, 11 - j, 0), Block('pointed_dripstone', {
                'thickness': 'tip_merge' if j == step.elem - 1 else 'tip', 'vertical_direction': 'down'}))
        if step.elem != 4:
            yield fill(r(0, 4 + step.elem, 0), r(0, 11 - step.elem, 0), 'air')

    room.function('dripstone_init').add(
        setblock(r(0, 3, 0), 'dripstone_block'),
        setblock(r(0, 12, 0), 'dripstone_block'),
        WallSign((None, 'Dripstone')).place(r(0, 2, -1), NORTH),
    )
    room.loop('dripstone', main_clock).loop(dripstone_loop, range(1, 5), bounce=True)

    def fire_loop(step):
        dirs = ({'up': True}, {'north': True}, {})
        surround = ((-1, 0, 'west'), (1, 0, 'east'), (0, 1, 'south'), (0, -1, 'north'),)
        if 'soul' in step.elem:
            yield setblock(r(0, 3, 0), step.elem)
            yield setblock(r(0, 4, 0), 'soul_fire')
        else:
            yield setblock(r(0, 3 + step.i, 0), step.elem)
            if step.i == 1:
                for j in range(0, 4):
                    s = surround[j]
                    yield setblock(r(s[0], 4, s[1]), Block('fire', {s[2]: True}))
            else:
                yield setblock(r(0, 4, -1 if step.i == 1 else 0), Block('fire', dirs[step.i]))
        nbt = Sign.lines_nbt((None, 'Soul Fire' if step.elem == 'soul_soil' else 'Fire'))
        yield data().merge(r(0, 2, -1), {'front_text': nbt})

    room.function('fire_init').add(WallSign((None, 'Fire')).place(r(0, 2, -1), NORTH))
    room.loop('fire', main_clock).add(fill(r(0, 3, 0), r(0, 5, 0), 'air')).loop(fire_loop, (
        'oak_log', 'oak_log', 'oak_log', 'soul_soil'))
    # <% types = ("Ice", "Packed Ice", "Blue Ice") %>
    blocks('ice', SOUTH, ('Ice', 'Packed Ice', 'Blue Ice'))

    infestables = []
    for b in ('Cobblestone', 'Deepslate', 'Stone', 'Stone Bricks', 'Chiseled|Stone Bricks', 'Cracked|Stone Bricks',
              'Mossy|Stone Bricks'):
        infestables.extend((b, f'Infested|{b}'))
    blocks('infested', NORTH, infestables)
    two = room.score('two')
    room.function('infested_init', exists_ok=True).add(
        room.label(r(-1, 2, 0), 'Infested Only', SOUTH),
        two.set(2))
    i_even = room.score('infested_even')
    infested = room.score('infested')
    room.loop('infested_main', main_clock, exists_ok=True).before.extend((
        i_even.operation(EQ, infested),
        i_even.operation(MOD, two),
        execute().if_().score(i_even).matches(0).if_().score(room.score('infested_only')).matches(1).run(
            infested.add(1))))

    def item_frame_loop(step):
        yield step.elem.merge_nbt({'Tags': ['item_frame_as_block']}).summon(r(0, 3, -1)),
        yield data().merge(r(0, 2, -1), {'front_text': Sign.lines_nbt((None, *step.elem.sign_text))})

    item_frame_init = kill(e().tag('item_frame_as_block'))
    room.function('item_frame_init').add(item_frame_init)
    frames = (ItemFrame(NORTH).item('Lapis Lazuli'),
              ItemFrame(NORTH),
              ItemFrame(NORTH, glowing=True),
              ItemFrame(NORTH, glowing=True).item('Lapis Lazuli'))
    room.loop('item_frame', main_clock).add(item_frame_init).loop(item_frame_loop, frames)

    def lantern_loop(step) -> Commands:
        lantern = Block('Lantern' if step.i < 2 else 'Soul Lantern', {'hanging': False})
        if step.i in (0, 3):
            yield setblock(r(0, 3, 0), lantern),
            yield fill(r(0, 4, 0), r(0, 5, 0), 'air'),
            yield Sign.change(r(0, 2, -1), (None, '', lantern.name, ' Chain'))
        else:
            lantern.merge_state({'hanging': True}),
            yield setblock(r(0, 3, 0), lantern),
            yield setblock(r(0, 4, 0), 'chain'),
            yield setblock(r(0, 5, 0), 'smooth_stone_slab'),
            yield Sign.change(r(0, 2, -1), (None, 'Hanging', lantern.name, 'and Chain'))

    room.function('lantern_init').add(WallSign((None, None, 'Lantern')).place(r(0, 2, -1, ), NORTH))
    room.loop('lantern', main_clock).loop(lantern_loop, range(0, 4))

    room.function('ore_blocks_init').add(room.label(r(-1, 2, 0), 'Deepslate', SOUTH))
    basic = ['Coal', 'Iron', 'Copper', 'Gold', 'Lapis', 'Redstone', 'Diamond', 'Emerald']
    odder = ['Nether Quartz', 'Nether Gold']
    ores = list(f'{t} Ore' for t in basic + odder) + ['Ancient Debris', ]
    slate_ores = list(f'Deepslate|{t} Ore' for t in basic)
    slate_ores.extend(ores[len(slate_ores):])
    ore_blocks = [f'{x} Block' for x in basic + ['Quartz', 'Gold']] + ['Netherite Block', ]
    blocks('ore_blocks', NORTH, (ores, ore_blocks), dz=3)
    blocks('deepslate_ore_blocks', NORTH, (slate_ores, ore_blocks), dz=3, score=room.score('ore_blocks'))
    room.function('ore_blocks_init', exists_ok=True).add(
        tag(e().tag('ore_blocks_home')).add('ore_blocks_base'),
        tag(e().tag('deepslate_ore_blocks_home')).add('ore_blocks_base'))
    room.function('switch_to_ore_blocks').add(
        tag(e().tag('ore_blocks_base')).add('ore_blocks_home'),
        tag(e().tag('ore_blocks_base')).remove('deepslate_ore_blocks_home'),
        execute().at(e().tag('ore_blocks_base')).run(function('restworld:blocks/ore_blocks_cur')))
    room.function('switch_to_deepslate_ore_blocks').add(
        tag(e().tag('ore_blocks_base')).remove('ore_blocks_home'),
        tag(e().tag('ore_blocks_base')).add('deepslate_ore_blocks_home'),
        execute().at(e().tag('ore_blocks_base')).run(function('restworld:blocks/deepslate_ore_blocks_cur')))

    def ladder_loop(step):
        yield fill(r(0, 3, 0), r(0, 5, 0), 'air')
        yield fill(r(0, 3, 0), r(0, 3 + step.elem, 0), 'ladder')

    room.loop('ladder', main_clock).loop(ladder_loop, range(0, 3), bounce=True)

    def scaffolding_loop(step):
        i = step.i
        if i == 0:
            yield setblock(r(0, 4, 0), 'scaffolding')
        elif i == 1:
            yield setblock(r(0, 5, 0), 'scaffolding')
        elif i == 2:
            yield setblock(r(0, 5, -1), Block('scaffolding', {'distance': 1}))
        elif i == 3:
            yield setblock(r(0, 5, -2), Block('scaffolding', {'distance': 2}))
        elif i == 4:
            yield setblock(r(0, 5, -2), 'air')
        elif i == 5:
            yield setblock(r(0, 5, -1), 'air')
        elif i == 6:
            yield setblock(r(0, 5, 0), 'air')
        elif i == 7:
            yield setblock(r(0, 4, 0), 'air')

    room.loop('scaffolding', main_clock).loop(scaffolding_loop, range(0, 5), bounce=True)

    blocks('sculk_blocks', NORTH, (
        Block('Sculk Vein', {SOUTH: True, DOWN: True}),
        'Sculk', 'Sculk Sensor',
        # Shows up waterlogged by default; see https://bugs.mojang.com/browse/MC-261388
        Block('Calibrated|Sculk Sensor', {'waterlogged': False, 'facing': SOUTH}),
        Block('Sculk Catalyst'),
        Block('sculk_catalyst', {'bloom': True}, name='Sculk Catalyst|Blooming'),
        Block('sculk_shrieker', {'can_summon': True, 'shrieking': False}, name='Sculk Shrieker|Can Summon'),
        Block('sculk_shrieker', {'can_summon': True, 'shrieking': True},
              name='Sculk Shrieker|Can Summon|Shrieking'),
        Block('sculk_shrieker', {'can_summon': False, 'shrieking': False}, name='Sculk Shrieker|Can\'t Summon'),
        Block('sculk_shrieker', {'can_summon': False, 'shrieking': True},
              name='Sculk Shrieker|Can\'t Summon|Shrieking'),
    ))
    skulk_loop = room.functions['sculk_blocks_main']
    assert isinstance(skulk_loop, Loop)
    skulk_loop.add(
        execute().if_().score(skulk_loop.score).matches(7).positioned(r(0, 3, 0)).run(
            function('restworld:particles/shriek_particles')),
        execute().if_().score(skulk_loop.score).matches(9).positioned(r(0, 3, 0)).run(
            function('restworld:particles/shriek_particles')),
    )

    def snow_depth_loop(step):
        yield setblock(r(0, 3, 0), Block('grass_block', {'snowy': True}))
        yield setblock(r(0, 4, 0), Block('snow', {'layers': step.elem}))
        yield Sign.change(r(0, 2, 1), (None, None, f'Layers: {step.elem:d}'))

    room.loop('snow_depth', main_clock).loop(snow_depth_loop, range(1, 9), bounce=True)

    def spawner_loop(step):
        # As of 1.20.3+x the trial spawner only sets the visible mob after the first spawn, and we don't have one, so
        # this does nothing. I leave this here in case someday it works. (It's a no-op for the vault.)
        sign_pos = r(0, 2, -1)
        if isinstance(step.elem, str):
            spawner_nbt = {'SpawnData': {'entity': {'id': f'minecraft:{to_id(step.elem)}'}}}
            yield data().merge(r(0, 3, 0), spawner_nbt)
            yield Sign.change(sign_pos, (None, None, step.elem))

    room.function('spawner_init').add(setblock(r(0, 3, 0), 'spawner').nbt(
        {'SpawnRange': 0, 'MinSpawnDelay': 799, 'MaxSpawnDelay': 799, 'RequiredPlayerRange': 0, 'SpawnCount': 0}))
    room.loop('spawner', main_clock).loop(spawner_loop, ('Skeleton', 'Zombie', 'Cave Spider', 'Blaze'))

    vault_states = {'waiting_for_players': 'inactive', 'cooldown': 'inactive',
                    'waiting_for_reward_ejection': 'unlocking', 'ejecting_reward': 'ejecting'}
    base_vault_nbt = {'state_updating_resumes_at': 0xfff_ffff_ffff_ffff}
    no_pickup = {'PickupDelay': -1}
    items_to_eject = [
        Item.nbt_for('emerald', no_pickup), Item.nbt_for('wind_charge', no_pickup), Item.nbt_for('trident', no_pickup),
        Item.nbt_for('golden_carrot', no_pickup), Item.nbt_for('guster_banner_pattern', no_pickup),
        Item.nbt_for('ominous bottle', no_pickup), Item.nbt_for('trial_key', no_pickup)]
    ominous_items_to_eject = [
        Item.nbt_for('emerald', no_pickup), Item.nbt_for('wind_charge', no_pickup),
        Item.nbt_for('heavy_core', no_pickup), Item.nbt_for('golden_apple', no_pickup),
        Item.nbt_for('flow_banner_pattern', no_pickup), Item.nbt_for('ominous bottle', no_pickup),
        Item.nbt_for('ominous_trial_key', no_pickup)]
    active_vault_nbt = Nbt(base_vault_nbt).merge({
        'config': {'activation_range': 100, 'deactivation_range': 100, },
        'server_data': {'items_to_eject': items_to_eject, 'total_ejections_needed': len(items_to_eject)},
    })
    vault_nbts = {
        'inactive': Nbt(base_vault_nbt).merge({'config': {'activation_range': 0, 'deactivation_range': 0}}),
        'active': active_vault_nbt,
        'ejecting': active_vault_nbt,
        'unlocking': active_vault_nbt,
    }
    trials = ((r(0, 3, 0)), (r(-3, 3, 0)), (r(0, 3, 3)), (r(-3, 3, 3)))
    # As of 1.20.3+x the trial spawner only sets the visible mob after the first spawn, and we don't have one, so
    # nothing is shown. I leave stuff here for the mob definition in case someday it works.
    spawner_config = {
        'simultaneous_mobs': 4.0,
        'simultaneous_mobs_added_per_player': 2.0,
        'ticks_between_spawn': 0xfff_ffff_ffff_ffff,
        'spawn_potentials': [{'data': {'entity': {'id': "minecraft:stray"}}, 'weight': 1}],
        'loot_tables_to_eject': [{'data': "minecraft:spawners/ominous/trial_chamber/consumables", 'weight': 1}],
    }
    base_trial_spawner_nbt = Nbt({
        'required_player_range': 1,
        'target_cooldown_length': 0xfff_ffff,
        'spawn_potentials': [{'data': {'entity': {'id': 'minecraft:stray'}}, 'weight': 1}],
        'normal_config': spawner_config,
        'ominous_config': spawner_config,
        'spawn_data': {'entity': {'id': "minecraft:stray"}},
    })
    trial_spawner_nbts = {
        'inactive': base_trial_spawner_nbt.merge({'required_player_range': 1}),
        'waiting_for_players': base_trial_spawner_nbt.merge({'required_player_range': 100}),
        'active': base_trial_spawner_nbt.merge({
            'required_player_range': 100, 'next_mob_spawns_at': 0xfff_ffff_ffff_ffff, 'total_mobs_spawned': 1}),
        'waiting_for_reward_ejection': base_trial_spawner_nbt.merge({
            'required_player_range': 100,
            'ejecting_loot_table': "minecraft:spawners/ominous/trial_chamber/consumables"}),
        'ejecting_reward': base_trial_spawner_nbt.merge({
            'required_player_range': 100,
            'ejecting_loot_table': "minecraft:spawners/ominous/trial_chamber/consumables"}),
        'cooldown': base_trial_spawner_nbt.merge({
            'required_player_range': 1, 'cooldown_ends_at': 0xfff_ffff_ffff_ffff}),
    }
    trial_blocks = (
        Block('trial_spawner', None, base_trial_spawner_nbt),
        Block('trial_spawner', {'ominous': True}, base_trial_spawner_nbt),
        Block('vault', None, vault_nbts['inactive']),
        Block('vault', {'ominous': True}, vault_nbts['inactive']),
    )
    sign_offset = (0, -1, -1)

    def trial_loop(step):
        spawner_state = step.elem
        vault_state = vault_states[step.elem] if step.elem in vault_states else step.elem
        for i in range(len(trial_blocks)):
            is_spawner = i < 2
            is_ominous = i % 2 == 1
            pos = trials[i]
            block = trial_blocks[i].clone()
            if is_spawner:
                block.merge_state({'trial_spawner_state': spawner_state}).merge_nbt(trial_spawner_nbts[spawner_state])
            else:
                block.merge_state({'vault_state': vault_state})
                block.nbt = vault_nbts[vault_state].clone()
                server_data = block.nbt['server_data']
                if is_ominous and 'items_to_eject' in server_data:
                    server_data['items_to_eject'] = ominous_items_to_eject
                    server_data['total_ejections_needed'] = len(ominous_items_to_eject)
            yield setblock(pos, 'air')
            yield setblock(pos, block)
            # if is_spawner:
            #     yield data().modify(pos, 'registered_players').append().from_(p(), 'UUID')
            # else:
            #     yield data().modify(pos, 'server_data.rewarded_players').append().from_(p(), 'UUID')
            sign_pos = RelCoord.add(pos, sign_offset)
            text = [None, None, to_name(spawner_state if i < 2 else vault_state), '']
            if 'Waiting' in text[2]:
                text[3] = text[2].replace('Waiting For ', '')
                text[2] = 'Waiting For'
            yield Sign.change(sign_pos, text)

    def trial_init():
        for i in range(len(trial_blocks)):
            pos = trials[i]
            yield setblock(pos, trial_blocks[i])
            text = list(trial_blocks[i].full_text)
            if i % 2 == 1:
                text[1] = f'Ominous {text[1]}'
            sign = WallSign().front(text)
            yield sign.place(RelCoord.add(pos, sign_offset), NORTH)

    room.function('trial_init').add(trial_init())
    trial = room.loop('trial', main_clock)
    trial.add(
        kill(e().type('item').distance((None, 10)))
    ).loop(
        trial_loop,
        ('inactive', 'waiting_for_players', 'active', 'waiting_for_reward_ejection', 'ejecting_reward', 'cooldown'),
    )

    def structure_blocks_loop(step):
        yield Sign.change(r(0, 2, 1), (None, step.elem))
        yield data().merge(r(0, 3, 0), {'mode': step.elem.upper()})

    room.function('structure_blocks_init').add(WallSign((None, None, 'Structure Block')).place(r(0, 2, 1), SOUTH))
    room.loop('structure_blocks', main_clock).loop(structure_blocks_loop, ('Data', 'Save', 'Load', 'Corner'))

    def tnt_loop(step):
        if step.i < 2:
            yield setblock(r(0, 3, 0), Block('tnt', {'unstable': step.elem == 'unstable'}))
        else:
            yield setblock(r(0, 3, 0), 'air')
            yield summon(('tnt', {'fuse': 0x7fff, 'Tags': ['block_tnt']}), r(0, 3, 0))
        yield Sign.change(r(0, 2, 1), (None, None, step.elem.title()))

    room.loop('tnt', main_clock).add(kill(e().tag('block_tnt'))).loop(tnt_loop, ('stable', 'unstable', 'primed'))

    torches = (Block('Torch'), Block('Soul Torch'), Block('Redstone Torch'), Block('Redstone Torch'))
    wall_torches = tuple(Block(x.name.replace('Torch', 'Wall Torch')) for x in torches)

    def torches_loop(step):
        text = ((None, '', None, ''), (None, 'Soul', None, ''), (None, 'Redstone', None, '(On)'),
                (None, 'Redstone', None, '(Off)'))
        yield Sign.change(r(0, 2, -1), text[step.i])
        if step.i == len(torches) - 1:
            yield execute().if_().score(wall_torches_score).matches(0).run(setblock(r(0, 2, 0), 'redstone_block'))
            yield execute().if_().score(wall_torches_score).matches(1).run(setblock(r(0, 3, 1), 'redstone_block'))
        yield execute().if_().score(wall_torches_score).matches(0).run(setblock(r(0, 3, 0), step.elem))
        yield execute().if_().score(wall_torches_score).matches(1).run(setblock(r(0, 3, 0), wall_torches[step.i]))

    wall_torches_score = room.score('wall_torches')
    room.function('torches_init').add(
        WallSign((None, None, 'Torch')).place(r(0, 2, -1), NORTH),
        room.label(r(-1, 2, 0), 'Wall-ness', SOUTH),
        wall_torches_score.set(0)
    )
    room.loop('torches', main_clock).add(
        execute().if_().score(wall_torches_score).matches(0).run(Sign.change(r(0, 2, -1), (None, None, 'Torch'))),
        execute().if_().score(wall_torches_score).matches(1).run(Sign.change(r(0, 2, -1), (None, None, 'Wall Torch'))),
        setblock(r(0, 3, 0), 'air'),
        execute().unless().block(r(0, 3, 1), 'air').run(setblock(r(0, 3, 1), 'air')),
        execute().unless().block(r(0, 2, 0), 'air').run(setblock(r(0, 2, 0), 'barrier')),
    ).loop(torches_loop, torches)

    color_functions(room)
    expansion_functions(room)
    stepable_functions(room)

    for b in (
            'amethyst', 'anvil', 'bell', 'brewing_stand', 'cake', 'campfire', 'chest', 'colored_beam', 'colorings',
            'frosted_ice', 'grindstone', 'item_frame', 'lantern', 'armor_stand', 'torches', 'blocks_room', 'ladder',
            'stepable', 'tnt'):
        room.function(b + '_init', exists_ok=True).add(tag(e().tag(b + '_home')).add('no_expansion'))


def room_init_functions(room, block_list_score):
    room.functions['blocks_room_init'].add(
        room.label(r(-16, 2, 3), 'List Blocks', SOUTH), room.label(r(-16, 2, -3), 'List Blocks', NORTH),
        room.label(r(-46, 2, 3), 'List Blocks', SOUTH), room.label(r(-46, 2, -3), 'List Blocks', NORTH),
        kill(e().tag('block_list')))
    # The 'zzz' makes sure this is run last
    room.function('zzz_blocks_sign_init').add(execute().at(e().tag('blocks_home', '!no_expansion')).run(
        Sign.change(r(0, 2, -1), ("",), ('function restworld:blocks/toggle_expand',))),
        execute().at(e().tag('blocks_home', '!no_expansion')).run(
            Sign.change(r(0, 2, 1), ("",), ('function restworld:blocks/toggle_expand',))),
        execute().at(e().tag('blocks_home', 'no_expansion')).run(
            Sign.change(r(0, 2, -1), ("",), (say('Sorry, cannot expand this block'),))),
        execute().at(e().tag('blocks_home', 'no_expansion')).run(
            Sign.change(r(0, 2, 1), ("",), (say('Sorry, cannot expand this block'),))),
        tag(e().tag('block_sign_home')).add('no_expansion'))
    room.loop('toggle_block_list', score=block_list_score).loop(
        lambda step: execute().as_(e().tag('block_list')).run(
            data().modify(s(), 'text_opacity').set().value(25 if step.i == 0 else 255)),
        range(2))
    room.function('toggle_block_list_init').add(block_list_score.set(0))


def armor_frame(which, where):
    frame = Entity('item_frame',
                   {'Facing': 3, 'Tags': ['colorings_item', f'colorings_frame_{which}'], 'Fixed': True})
    return frame.summon(where)


def color_functions(room):
    coloring_coords = (r(1, 4, 6), r(-13, 2, -1))
    volume = Region(*coloring_coords)
    lit_candles = room.score('lit_candles')
    plain = room.score('plain')

    def colorings(is_plain, color):
        fills = (
            'stained_glass', 'stained_glass_pane', 'wool', 'banner', 'shulker_box', 'carpet', 'concrete',
            'concrete_powder', 'terracotta')
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
                filler = Block(f'{color.id}_{which}', state)
            yield volume.replace(filler, '#restworld:' + which)

        candle = Block('candle' if is_plain else color.name + '_candle', {'lit': True})
        for count in range(1, 6):
            if count < 5:
                candle.merge_state({'candles': count})
                filter = f'#restworld:candle[candles={count:d}]'
            else:
                candle = Block(candle.id + '_cake', {'lit': True})
                filter = '#restworld:candle_cake'
            candle.merge_state({'lit': False})
            yield execute().if_().score(lit_candles).matches(0).run(volume.replace(candle, filter))
            candle.merge_state({'lit': True})
            yield execute().unless().score(lit_candles).matches(0).run(volume.replace(candle, filter))

        yield data().merge(r(-7, 0, 3), {'name': f'restworld:{color.id}_terra', 'showboundingbox': False})

        if is_plain:
            yield fill(r(-9, 2, 2), r(-9, 2, 3), 'air')
            yield volume.replace('air', '#standing_signs')
            yield data().remove(e().tag('colorings_item_frame').limit(1), 'Item')
        else:
            yield setblock(r(-9, 2, 2), Block(f'{color.id}_bed', {'facing': NORTH, 'part': 'head'}))
            yield setblock(r(-9, 2, 3), Block(f'{color.id}_bed', {'facing': NORTH, 'part': 'foot'}))
            frame_nbt = {'Item': Item.nbt_for(f'{color.id}_dye'), 'ItemRotation': 0}
            yield data().merge(e().tag('colorings_item_frame').limit(1), frame_nbt)

        if is_plain:
            leather_color = {}
            sheep_nbt = {'Sheared': True}
        else:
            leather_color = {'components': {'dyed_color': {'rgb': color.leather}}}
            sheep_nbt = {'Color': color.num, 'Sheared': False}

        if is_plain:
            yield kill_em(e().tag('colorings_horse'))
            yield kill_em(e().tag('colorings_dog'))
            yield kill_em(e().tag('colorings_cat'))
            horse = Entity('horse', nbt=horse_nbt.merge({'body_armor_item': {'id': 'leather_horse_armor'}}))
            yield horse.summon(r(0.7, 2, 4.4))

        yield data().merge(e().tag('colorings_armor_stand').limit(1), {
            'ArmorItems': [Item.nbt_for('leather_boots', nbt=leather_color),
                           Item.nbt_for('leather_leggings', nbt=leather_color),
                           Item.nbt_for('leather_chestplate', nbt=leather_color),
                           Item.nbt_for('leather_helmet', nbt=leather_color)]})
        for w in armor_frames:
            yield data().modify(e().tag(f'colorings_frame_{w}').limit(1), 'Item').set().value(
                Item.nbt_for(w, nbt=leather_color)),
        for w in 'horse', 'dog':
            yield data().modify(e().tag(f'colorings_{w}').limit(1),
                                'body_armor_item.components.minecraft:dyed_color.rgb').set().value(color.leather)
        for w in 'cat', 'dog':
            yield data().merge(e().tag(f'colorings_{w}').limit(1), {'CollarColor': color.num})
        if is_plain:
            yield data().remove(e().tag('colorings_llama').limit(1), 'body_armor_item')
        else:
            yield data().modify(e().tag('colorings_llama').limit(1), 'body_armor_item').set().value(
                {'id': color.id + '_carpet'})
        yield data().merge(e().tag('colorings_sheep').limit(1), sheep_nbt)

        yield Sign.change(r(-4, 2, 4), (None, color.name))
        yield execute().as_(e().tag('colorings_names')).run(data().merge(s(), {'CustomName': color.name}))

        yield data().merge(r(0, 0, -1), {'name': f'restworld:{"plain" if is_plain else color.id}_terra'})
        yield Sign.change(r(1, 2, -0), (color.name,))

    def colored_signs(color, render):
        signables = info.woods + stems
        for w in range(0, len(signables)):
            wood = signables[w]
            row_len = 4 if w < 8 else 3
            x = w % row_len - 13
            y = int(w / 4) + 2
            z = -(w % row_len) + 4
            if row_len < 4:
                x += 1
                z -= 1
            yield from render(x, y, z, color, Block(wood))

    def render_signs_glow(x, y, z, _, _2):
        lit_signs = room.score('lit_signs')
        yield execute().if_().score(lit_signs).matches(0).run(
            data().merge(r(x, y, z), {'front_text': {'has_glowing_text': False}}))
        yield execute().if_().score(lit_signs).matches(1).run(
            data().merge(r(x, y, z), {'front_text': {'has_glowing_text': True}}))

    def render_signs(x, y, z, color, _):
        yield Sign.change(r(x, y, z), (None, None, color.name))
        yield data().merge(r(x, y, z), {'front_text': {'color': color.id}})

    def colorings_loop(step):
        yield from colorings(False, step.elem)
        yield from colored_signs(step.elem, render_signs)

    mob_nbt = {'Time': True, 'NoAI': True, 'Silent': True}
    horse_nbt = Nbt({
        'Variant': 5, 'Tags': ['colorings_horse', 'colorings_item', 'colorings_names'],
        'body_armor_item': Item.nbt_for('leather_horse_armor'), 'Rotation': [-25, 0]}).merge(mob_nbt)
    dog_nbt = Nbt(
        {'Owner': 'dummy', 'Tags': ['colorings_dog', 'colorings_item'], 'body_armor_item': Item.nbt_for('wolf_armor'),
         'Rotation': [-65, 0]}).merge(mob_nbt)
    cat_nbt = Nbt(
        {'variant': 'persian', 'Owner': 'dummy', 'Tags': ['colorings_cat', 'colorings_item'], 'ColorColor': 3,
         'Rotation': [110, 0]}).merge(mob_nbt)
    llama_nbt = Nbt(
        {'Tags': ['colorings_llama', 'colorings_item', 'colorings_names'], 'Variant': 1, 'Rotation': [20, 0],
         'Leashed': True}).merge(mob_nbt)
    sheep_nbt = Nbt(
        {'Tags': ['colorings_sheep', 'colorings_item'], 'Variant': 1, 'Rotation': [-35, 0], 'Leashed': True}).merge(
        mob_nbt)
    stand_nbt = {'Tags': ['colorings_armor_stand', 'colorings_item'], 'Rotation': [30, 0]}
    armor_frames = {
        'wolf_armor': r(-8, 4, 1),
        'leather_boots': r(0, 2, 1),
        'leather_leggings': r(0, 3, 1),
        'leather_chestplate': r(0, 4, 1),
        'leather_helmet': r(0, 5, 1),
        'leather_horse_armor': r(1, 5, 1),
    }
    room.function('colorings_init').add(
        kill(e().tag('colorings_item')),
        plain.set(0),
        Entity('item_frame', {
            'Facing': 3, 'Tags': ['colorings_item_frame', 'colorings_item'],
            'Fixed': True}).summon(r(-4.5, 4, 0.5)),
        Entity('horse', horse_nbt).summon(r(0.7, 2, 4.4)),
        Entity('wolf', dog_nbt).summon(r(-7.5, 2, 2)),
        Entity('cat', cat_nbt).summon(r(-2.7, 2, 2)),
        Entity('armor_stand', stand_nbt).summon(r(-1.1, 2, 3)),
        Entity('llama', llama_nbt).summon(r(-11, 2, 5.8)),
        Entity('sheep', sheep_nbt).summon(r(-9.0, 2, 5.0)),
        (armor_frame(k, v) for k, v in armor_frames.items()),
        execute().as_(e().tag('colorings_names')).run(
            data().merge(s(), {'CustomNameVisible': True})),
        WallSign((None, 'Terracotta')).place(r(-1, 3, 1), SOUTH),
        WallSign((None, 'Shulker Box')).place(r(-3, 3, 1), SOUTH),
        WallSign((None, 'Dye')).place(r(-4, 3, 1, ), SOUTH),
        WallSign((None, 'Concrete')).place(r(-5, 3, 1), SOUTH),
        WallSign((None, 'Glass')).place(r(-7, 3, 1), SOUTH),
        colored_signs(None,
                      lambda x, y, z, _, wood: Sign((wood.name, 'Sign With', 'Default', 'Text'), wood=wood.id).place(
                          r(x, y, z), 14)),
        WallSign([]).place(r(-4, 2, 4, ), SOUTH), kill(e().type('item')),
        room.label(r(-1, 2, 7), 'Lit Candles', NORTH), room.label(r(-8, 2, 7), 'Plain', NORTH),
        room.label(r(-11, 2, 3), 'Glowing', NORTH)),
    room.loop('colorings', main_clock).add(fill(r(-9, 2, 2), r(-9, 2, 3), 'air')).loop(colorings_loop, colors).add(
        colored_signs(None, render_signs_glow), setblock(r(-7, -1, 3), 'redstone_block'), setblock(r(-7, -1, 3), 'air'))
    room.function('colorings_plain_off', home=False).add(
        execute().unless().score(plain).matches(0).run(
            clone((coloring_coords[0][0], coloring_coords[0][1].value - coloring_coords[1][1].value + 1,
                   coloring_coords[0][2]),
                  (coloring_coords[1][0], 0, coloring_coords[1][2]),
                  (coloring_coords[1][0], coloring_coords[1][1] - 1, coloring_coords[1][2]))),
        plain.set(0),
        tag(e().tag('colorings_base_home')).add('colorings_home'),
        execute().at(e().tag('colorings_home')).run(function('restworld:blocks/colorings_init')),
        execute().at(e().tag('colorings_home')).run(function('restworld:blocks/colorings_cur')),
        kill(e().type('item').distance((None, 20))))
    room.function('colorings_plain_on', home=False).add(
        execute().if_().score(plain).matches(0).run(
            clone((coloring_coords[0][0], coloring_coords[0][1], coloring_coords[0][2]),
                  (coloring_coords[1][0], coloring_coords[1][1] - 1, coloring_coords[1][2]),
                  (coloring_coords[1][0], 0, coloring_coords[1][2]))),
        plain.set(1),
        tag(e().tag('colorings_base_home')).remove('colorings_home'),
        item().replace().entity(e().tag('colorings_item_frame'), 'container.0').with_('air'),
        colorings(True, Color('Plain', 0x0)), setblock(r(-7, -1, 3), 'redstone_torch'), setblock(r(-7, -1, 3), 'air'),
        kill(e().type('item').distance((None, 20))))
    room.functions['colorings_home'].add(tag(e().tag('colorings_home')).add('colorings_base_home'))
    room.function('colorings_enter').add(
        execute().as_(e().tag('colorings_names')).run(data().merge(s(), {'CustomNameVisible': True})))
    room.function('colorings_exit').add(
        execute().as_(e().tag('colorings_names')).run(data().merge(s(), {'CustomNameVisible': False})))
    room.function('colored_beam_enter').add(setblock(r(0, 1, 0), 'iron_block'))
    room.function('colored_beam_exit').add(setblock(r(0, 1, 0), 'white_concrete'))


# Expansion is complex.
#
# Each 'homer' armor stand is assumed to be an expander for its block or blocks. Though it can be tagged 'no_expansion'
# if the block is not to be expanded, typically in its _init file.
#
# During the _init phase, every expanding homer modifies its sign to toggle expansion when tapped. Non-expanding
# homers modify the sign to say 'Sorry' when tapped.
#
# Toggling actual expansion for a single target is in toggle_expand_at. It places or removes the 'expander' tag on
# the homer, and runs either the expander or contracter function as itself as appropriate to give the immediate effect.
#
# Expanding or contracting all simply runs this script on all expanding homers. Which means, frankly, that it
# doesn't 'expand all' it 'toggles all'.
#
# Homers that handle multiple blocks are helped by 'just_expand' armor stands under the blocks it manages. These
# are expander homers that do nothing but the expansion work for the blocks above them. So if homer X puts up
# blocks X and Y, a regular homer will be under X and a 'just_expand' homer will be under Y.
#
# Each main tick, the 'expand' function is run at every 'expander' during the 'main_finish' phase. This keeps the
# block expanded as it changes.
def expansion_functions(room):
    room.function('toggle_expand', home=False).add(
        execute().positioned(r(0, -2, -1)).run(function('restworld:blocks/toggle_expand_at')),
        execute().positioned(r(0, -2, 1)).run(function('restworld:blocks/toggle_expand_at')))
    room.function('toggle_expand_at', home=False).add(
        execute().as_(e().tag('expander').distance((None, 1))).run(tag(s()).add('stop_expanding')),
        execute().as_(e().tag('!expander', '!no_expansion').distance((None, 1))).run(tag(s()).add('expander')),
        execute().as_(e().tag('stop_expanding').distance((None, 1))).run(tag(s()).remove('expander')),
        execute().as_(e().tag('stop_expanding').distance((None, 1))).run(tag(s()).remove('stop_expanding')),
        execute().at(e().tag('expander').distance((None, 1))).run(function('restworld:blocks/expander')),
        execute().at(e().tag('!expander', '!no_expansion').distance((None, 1))).run(
            function('restworld:blocks/contracter')),
        execute().at(e().tag('no_expansion').distance((None, 1))).run(say('Sorry, cannot expand this.')),
        execute().at(e().tag('no_expansion', 'fire_home').distance((None, 1))).run(say('Sorry, cannot expand this.')))
    room.function('expander').add(
        execute().if_().entity(e().tag('fire_home').distance((None, 1))).run(function('restworld:blocks/expand_fire')),
        execute().if_().entity(e().tag('dripstone_home').distance((None, 1))).run(
            function('restworld:blocks/expand_dripstone')),
        execute().unless().entity(e().tag('fire_home').distance((None, 1))).unless().entity(
            e().tag('dripstone_home').distance((None, 1))).run(function('restworld:blocks/expand_generic')))
    room.function('expand_all', home=False).add(execute().as_(e().tag('blocks_home', '!no_expansion', '!expander')).run(
        execute().at(s()).run(function('restworld:blocks/toggle_expand_at'))))
    room.function('expand', main_clock).add(
        execute().at(e().tag('expander')).run(function('restworld:blocks/expander')))
    room.function('expand_dripstone', home=False).add(clone(r(0, 12, 0), r(0, 3, 0), r(-1, 3, 0)),
                                                      clone(r(0, 12, 0), r(0, 3, 0), r(1, 3, 0)),
                                                      clone(r(1, 12, 0), r(-1, 3, 0), r(-1, 3, -1)),
                                                      clone(r(1, 12, 0), r(-1, 3, 0), r(-1, 3, 1)))
    fire_score = room.score('fire')
    room.function('expand_fire', home=False).add(
        execute().unless().score(fire_score).matches(1).run(fill(r(-2, 4, 1), r(-2, 4, -1), 'air')),
        execute().unless().score(fire_score).matches(1).run(fill(r(2, 4, 1), r(2, 4, -1), 'air')),
        execute().unless().score(fire_score).matches(1).run(fill(r(1, 4, -2), r(-1, 4, -2), 'air')),
        execute().unless().score(fire_score).matches(1).run(fill(r(1, 4, 2), r(-1, 4, 2), 'air')),
        clone(r(0, 5, 0), r(0, 3, 0), r(1, 3, 0)), clone(r(0, 5, 0), r(0, 3, 0), r(-1, 3, 0)),
        clone(r(1, 5, 0), r(-1, 3, 0), r(-1, 3, 1)), clone(r(1, 5, 0), r(-1, 3, 0), r(-1, 3, -1)),
        execute().if_().score(fire_score).matches(1).run(fill(r(-2, 4, 1), r(-2, 4, -1), 'fire[west=true]')),
        execute().if_().score(fire_score).matches(1).run(fill(r(2, 4, 1), r(2, 4, -1), 'fire[east=true]')),
        execute().if_().score(fire_score).matches(1).run(fill(r(1, 4, -2), r(-1, 4, -2), 'fire[north=true]')),
        execute().if_().score(fire_score).matches(1).run(fill(r(1, 4, 2), r(-1, 4, 2), 'fire[south=true]')))
    room.function('expand_generic', home=False).add(execute().if_().block(r(0, 3, 0), '#restworld:falling').run(
        fill(r(-1, 2, -1), r(1, 2, 1), 'barrier').replace('air')),
        execute().unless().block(r(0, 4, 0), 'snow').run(fill(r(-1, 4, -1), r(1, 4, 1), 'air')),
        clone(r(0, 4, 0), r(0, 3, 0), r(-1, 3, 0)), clone(r(0, 4, 0), r(0, 3, 0), r(1, 3, 0)),
        clone(r(1, 4, 0), r(-1, 3, 0), r(-1, 3, -1)), clone(r(1, 4, 0), r(-1, 3, 0), r(-1, 3, 1)),
        clone(r(1, 4, 1), r(-1, 3, -1), r(-1, 5, -1)),
        execute().if_().block(r(0, 5, 0), '#restworld:soil').run(fill(r(-1, 3, -1), r(1, 4, 1), 'dirt')),
        execute().unless().block(r(0, 5, 0), '#restworld:soil').run(clone(r(1, 5, 1), r(-1, 5, -1), r(-1, 4, -1))))

    room.function('contracter').add(execute().if_().entity(e().tag('fire_home').distance((None, 1))).run(
        function('restworld:blocks/contract_fire')),
        execute().if_().entity(e().tag('dripstone_home').distance((None, 1))).run(
            function('restworld:blocks/contract_dripstone')),
        execute().unless().entity(e().tag('fire_home').distance((None, 1))).unless().entity(
            e().tag('dripstone_home').distance((None, 1))).run(function('restworld:blocks/contract_generic')))
    room.function('contract_all', home=False).add(
        execute().as_(e().tag('blocks_home', '!no_expansion', 'expander')).run(
            execute().at(s()).run(function('restworld:blocks/toggle_expand_at'))))
    room.function('contract_dripstone').add(fill(r(1, 12, 1), r(-1, 3, 1), 'air'),
                                            fill(r(1, 12, -1), r(-1, 3, -1), 'air'),
                                            fill(r(1, 12, 0), r(1, 3, 0), 'air'),
                                            fill(r(-1, 12, 0), r(-1, 3, 0), 'air'))
    room.function('contract_fire').add(fill(r(1, 5, 1), r(-1, 3, -1), 'air'), function('restworld:blocks/fire_cur'))
    room.function('contract_generic').add(clone(r(0, 5, 0), r(0, 6, 0), r(0, -10, 0)),
                                          fill(r(-1, 3, -1), r(1, 6, 1), 'air'),
                                          clone(r(0, -9, 0), r(0, -10, 0), r(0, 3, 0)).replace(MOVE),
                                          setblock(r(0, 2, 0), 'stone'),
                                          fill(r(-1, 2, -1), r(1, 2, 1), 'air').replace('barrier'),
                                          setblock(r(0, 2, 0), 'barrier'))

    room.function('generic_home', home=False).add(kill(e().tag('generic_home').distance((None, 2))),
                                                  summon('armor_stand', r(0, 0.5, 0),
                                                         {'Tags': ['generic_home', 'homer', 'blocks_home'],
                                                          'NoGravity': True, 'Small': True}))
    # generic_home is used for entirely static blocks. This is used for blocks that are changed, but
    # by a different command block than the one under it. These want to be expanded as they change,
    room.function('just_expand_home', home=False).add(kill(e().tag('just_expand_home').distance((None, 2))),
                                                      summon('armor_stand', r(0, 0.5, 0),
                                                             {'Tags': ['just_expand_home', 'homer', 'blocks_home'],
                                                              'NoGravity': True, 'Small': True}))


def stepable_functions(room):
    def stepable_loop(step):
        volume = Region(r(0, 2, 0), r(3, 6, 6))
        i = step.i
        yield volume.replace(step.elem, '#restworld:stepable_planks')
        yield volume.replace_slabs(slabs[i], '#restworld:stepable_slabs')
        yield volume.replace_stairs(stairs[i], '#restworld:stepable_stairs')
        sign_text = Sign.lines_nbt(Block(step.elem).full_text)
        yield data().merge(r(1, 2, -1), {'front_text': sign_text})

    blocks = [
        'Stone', 'Cobblestone', 'Mossy|Cobblestone',
        'Bricks', 'Stone Bricks', 'Mossy|Stone Bricks', 'Mud Bricks',
        'Sandstone', 'Smooth|Sandstone', 'Red|Sandstone', 'Smooth Red|Sandstone',
        'Andesite', 'Polished|Andesite',
        'Diorite', 'Polished|Diorite',
        'Granite', 'Polished|Granite',
        'Tuff', 'Polished|Tuff', 'Tuff Bricks',
        'Cobbled|Deepslate',
        'Polished|Deepslate',
        'Deepslate|Bricks',
        'Deepslate|Tiles',
        'Cut Copper',
        'Exposed Cut Copper',
        'Weathered Cut Copper',
        'Oxidized Cut Copper',
        'Prismarine', 'Prismarine|Bricks', 'Dark|Prismarine',
        'Acacia Planks', 'Birch Planks', 'Cherry Planks', 'Jungle Planks', 'Mangrove Planks',
        'Oak Planks', 'Dark Oak Planks', 'Spruce Planks', 'Bamboo Planks', 'Bamboo Mosaic Block',
        'Warped Planks', 'Crimson Planks',
        'Nether Bricks', 'Red|Nether Bricks',
        'Blackstone', 'Polished|Blackstone',
        'Polished|Blackstone Bricks', 'Quartz Block', 'Smooth|Quartz',
        'End Stone Bricks', 'Purpur Block',
    ]
    stairs = tuple(re.sub('(marine|ite)$', r'\1 Stairs', re.sub('[Ss]tone$', 'Stone Stairs',
                                                                re.sub('[Tt]uff$', 'Tuff Stairs',
                                                                       f.replace('Planks', 'Stairs')
                                                                       .replace('Tiles', 'Tile Stairs')
                                                                       .replace('Copper', 'Copper Stairs')
                                                                       .replace('Bricks', 'Brick Stairs')
                                                                       .replace('Block', 'Stairs')
                                                                       .replace('|Quartz', ' Quartz Stairs')
                                                                       .replace('|Deepslate', '|Deepslate Stairs'))))
                   for f in blocks)
    slabs = tuple(f.replace('Stairs', 'Slab') for f in stairs)
    # The mosaic's "Block" is here so it fits in the patterns, but it actually doesn't exist, so we remove it.
    blocks[blocks.index('Bamboo Mosaic Block')] = 'Bamboo Mosaic'

    room.function('stepable_init').add(WallSign((None, 'Block')).place(r(3, 4, 5, ), NORTH),
                                       WallSign((None, 'Double slab')).place(r(3, 5, 5, ), NORTH),
                                       WallSign((None, 'Slabs & Stairs')).place(r(1, 2, -1, ), NORTH))
    room.loop('stepable', fast_clock).loop(stepable_loop, blocks)
