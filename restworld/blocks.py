from __future__ import annotations

import re
from typing import Iterable, Union

from pynecraft.base import DOWN, EAST, NORTH, Nbt, SOUTH, WEST, good_facing, r, to_name
from pynecraft.commands import Block, Entity, JsonText, MOVE, clone, data, e, execute, fill, function, \
    good_block, item, \
    kill, s, say, setblock, summon, tag
from pynecraft.function import Loop
from pynecraft.info import Color, colors, stems, woods
from pynecraft.simpler import Item, ItemFrame, Sign, Volume, WallSign
from restworld.rooms import Room, label
from restworld.world import fast_clock, kill_em, main_clock, restworld, slow_clock


def room():
    room = Room('blocks', restworld, EAST, ('Blocks,', 'Paintings,', 'Banners,', 'DIY'))

    block_list_score = room.score('block_list')

    name_stand = Entity('armor_stand', nbt={'Invisible': True, 'NoGravity': True, 'CustomNameVisible': True})
    name_stand.tag('block_list')

    def blocks(name, facing, block_lists: Iterable[Union[Block, str]] | Iterable[Iterable[Union[Block, str]]], dx=0,
               dz=0, size=0, labels=None, clock=main_clock, score=None):
        facing = good_facing(facing)

        if not isinstance(block_lists, list):
            block_lists = list(block_lists)
        if not isinstance(block_lists[0], Iterable) or isinstance(block_lists[0], str):
            block_lists = [block_lists, ]
        for i, sublist in enumerate(block_lists):
            nsublist = []
            for block in sublist:
                nsublist.append(good_block(block))
            block_lists[i] = nsublist
        show_list = len(set(x.id for x in block_lists[0])) > 1

        block_loop = room.loop(name, clock, score=score)
        block_init = room.function(name + '_init', exists_ok=True).add(
            WallSign(()).place(r(facing.dx, 2, facing.dz), facing)
        )
        if show_list:
            block_init.add(
                execute().if_().score(block_list_score).matches(0).run(kill(e().tag(f'block_list_{name}'))))
            names = room.function(name + '_names', home=False)
            block_init.add(function(names.full_name))

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

                yield setblock(r(x, 3, z), block)
                sign_nbt = Sign.lines_nbt(signage)
                # Preserve the 'expand' response
                del sign_nbt['Text1']
                yield data().merge(r(x + facing.dx, 2, z + facing.dz), sign_nbt)

                if show_list:
                    stand = name_stand.clone()
                    block_list_name = f'block_list_{name}_{x:d}_{z:d}'
                    block_list_block_name = f'block_list_{name}_{x:d}_{z:d}_{i:d}'
                    stand.tag('blocks', f'block_list_{name}', block_list_name, block_list_block_name)
                    stand.merge_nbt({'CustomName': block.name, 'CustomNameVisible': False})
                    stand_y = 2.5 + i * 0.24
                    names.add(stand.summon(r(x, stand_y, z)))

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
    blocks('bricks', NORTH, (
        'Bricks', 'Quartz Bricks', 'Mud Bricks', 'Deepslate|Bricks', 'Cracked|Deepslate|Bricks', 'Deepslate|Tiles',
        'Cracked|Deepslate|Tiles', 'Prismarine Bricks', 'Nether Bricks', 'Cracked|Nether Bricks',
        'Chiseled|Nether Bricks', 'Red|Nether Bricks'))
    blocks('campfire', NORTH, (
        Block('Campfire', {'lit': True}),
        Block('campfire', {'lit': False}, name='Campfire|Unlit'),
        Block('Soul Campfire', {'lit': True}),
        Block('soul_campfire', {'lit': False}, name='Soul Campfire|Unlit'),
    ))
    room.function('campfire_enter').add(function('restworld:/blocks/campfire_cur'))
    room.function('campfire_exit').add(setblock(r(0, 3, 0), Block('campfire', {'lit': False})))
    blocks('clay', SOUTH, ('Clay', 'Mud', 'Muddy|Mangrove Roots', 'Packed Mud'))
    blocks('cobble', NORTH, ('Cobblestone', 'Mossy|Cobblestone', 'Cobbled|Deepslate'))
    blocks('deepslate', NORTH, (
        'Deepslate', 'Chiseled|Deepslate', 'Polished|Deepslate', 'Cracked|Deepslate|Bricks', 'Cracked|Deepslate|Tiles',
        'Deepslate|Bricks', 'Deepslate|Tiles', 'Cobbled|Deepslate', 'Reinforced|Deepslate'))
    blocks('dirt', SOUTH, ('Dirt', 'Coarse Dirt', 'Rooted Dirt', 'Farmland'))
    blocks('end', NORTH, ('End Stone', 'End Stone|Bricks'))
    blocks('frosted_ice', SOUTH,
           list(Block('frosted_ice', {'age': i}, name=f'Frosted Ice|Age: {i}') for i in range(0, 4)))
    blocks('glass', NORTH, ('Glass', 'Tinted Glass'))
    blocks('ice', SOUTH, ('Ice', 'Packed Ice', 'Blue Ice'))
    blocks('lighting', NORTH, (
        'Glowstone', 'Sea Lantern', 'Shroomlight', 'Ochre|Froglight', 'Pearlescent|Froglight', 'Verdant|Froglight',
        'End Rod'))
    blocks('light', SOUTH, (Block('light', {'level': x}) for x in range(0, 15)),
           labels=tuple(('light', f'Level: {i:d}') for i in range(0, 15)), clock=slow_clock)
    blocks('music', SOUTH, (
        Block('Note Block'), Block('Jukebox'), Block('jukebox', {'has_record': True}, name='Jukebox|Playing')))
    blocks('netherrack', NORTH, ('Netherrack', 'Warped Nylium', 'Crimson Nylium'))
    blocks('obsidian', NORTH, ('Obsidian', 'Crying Obsidian'))
    blocks('prismarine', NORTH, ('Prismarine', 'Prismarine Bricks', 'Dark Prismarine'))
    blocks('pumpkin', SOUTH, (
        'Pumpkin', Block('Carved Pumpkin', {'facing': SOUTH}), Block('Jack O Lantern', {'facing': SOUTH})))
    blocks('purpur', NORTH, ('Purpur Block', 'Purpur Pillar'))
    blocks('quartz', NORTH, (
        'Quartz Block', 'Smooth Quartz', 'Quartz Pillar', 'Chiseled Quartz Block', 'Quartz Bricks'))
    blocks('raw_metal', NORTH, ('Raw Iron|Block', 'Raw Copper|Block', 'Raw Gold|Block'))
    blocks('respawn_anchor', NORTH, (Block('Respawn Anchor', {'charges': x}) for x in range(0, 5)),
           labels=tuple((None, f'Charges: {x:d}') for x in range(0, 5)))
    red_sandstone = ('Red Sandstone', 'Smooth|Red Sandstone', 'Cut|Red Sandstone', 'Chiseled|Red Sandstone')
    blocks('sandstone', SOUTH, (red_sandstone, tuple(re.sub(' *Red *', '', f) for f in red_sandstone)), dx=3)
    blocks('slabs', NORTH, ('Smooth Stone|Slab', 'Petrified Oak|Slab'))
    _, loop = blocks('snow_blocks', SOUTH, ('Powder Snow', 'Snow Block'))
    loop.add(execute().if_().block(r(0, 3, 0), 'powder_snow').run(data().merge(r(0, 2, 1), {'Text3': 'Step In!'})))
    _, loop = blocks('soil', SOUTH, ('Grass Block', 'Podzol', 'Mycelium', 'Dirt Path'))
    # Make sure the block above is air so it doesn't turn dirt path to dirt instantly.
    loop.add(setblock(r(0, 4, 0), 'air'))
    blocks('soul_stuff', NORTH, ('Soul Sand', 'Soul Soil'))
    blocks('sponge', SOUTH, ('Sponge', 'Wet Sponge'))
    blocks('sticky', SOUTH, ('Slime Block', 'Honey block'))
    blocks('stone_bricks', NORTH, (
        'Stone Bricks', 'Mossy|Stone Bricks', 'Cracked|Stone Bricks', 'Chiseled|Stone Bricks',
        'Polished|Blackstone Bricks', 'Cracked Polished|Blackstone Bricks', 'End Stone|Bricks'))
    stone_types = ('Basalt', 'Stone', 'Deepslate', 'Andesite', 'Diorite', 'Granite', 'Blackstone', 'Basalt')
    blocks('stone', NORTH, ('Smooth Basalt', 'Smooth Stone') + tuple(f'Polished|{t}' for t in stone_types[2:]))

    types = ('Copper Block', 'Exposed Copper', 'Weathered|Copper', 'Oxidized Copper')
    block = list(x.replace('Copper', 'Cut Copper').replace(' Block', '').replace(' Cut', '|Cut') for x in types)
    waxed_types = tuple(f'Waxed|{x}' for x in types)
    waxed_block = tuple(f'Waxed|{x}' for x in block)
    blocks('copper', NORTH, (types, block), dx=-3)
    blocks('waxed_copper', NORTH, (waxed_types, waxed_block), dx=-3, score=room.score('copper'))
    room.function('copper_init', exists_ok=True).add(
        tag(e().tag('copper_home')).add('copper_base'),
        tag(e().tag('waxed_copper_home')).add('copper_base'))
    room.function('switch_to_copper').add(
        tag(e().tag('copper_base')).add('copper_home'),
        tag(e().tag('copper_base')).remove('copper_waxed_home'),
        execute().at(e().tag('copper_base')).run(function('restworld:blocks/copper_cur')))
    room.function('switch_to_waxed_copper').add(
        tag(e().tag('copper_base')).remove('copper_home'),
        tag(e().tag('copper_base')).add('copper_waxed_home'),
        execute().at(e().tag('copper_base')).run(function('restworld:blocks/waxed_copper_cur')))

    woodlike = woods + stems
    leaves = [f'{x} Leaves' for x in woods] + ['Warped Wart Block', 'Nether Wart Block']
    logs = [f'{x} Log' for x in woods] + [f'{x} Stem' for x in stems]
    wood = [f'{x} Wood' for x in woods] + [f'{x} Hyphae' for x in stems]
    stripped_logs = [f'Stripped|{x} Log' for x in woods] + [f'Stripped|{x} Stem' for x in stems]
    stripped_woods = [f'Stripped|{x} Wood' for x in woods] + [f'Stripped|{x} Hyphae' for x in stems]
    blocks('wood_blocks', SOUTH, (tuple(f'{f} Planks' for f in woodlike),
                                  stripped_logs, logs, wood, leaves, stripped_woods), dx=-3, dz=-3, size=2)

    sites = ('Cauldron', 'Water Cauldron', 'Lava Cauldron', 'Powder Snow|Cauldron')
    stages = {'Water Cauldron': list({'level': t} for t in range(1, 4)),
              'Powder Snow Cauldron': list({'level': t} for t in range(3, 0, -1)), }
    job_sites('cauldron', NORTH, sites, stages)
    job_sites('composter', NORTH, ('Composter',), {'Composter': tuple({'level': t} for t in range(0, 9))})
    job_sites('grindstone', NORTH, ('Grindstone',),
              {'Grindstone': list({'face': f} for f in ('floor', 'wall', 'ceiling'))})
    job_sites('job_sites_1', NORTH,
              ('Crafting Table', 'Cartography Table', 'Fletching Table', 'Smithing Table', 'Loom', 'Stonecutter'))
    job_sites('job_sites_2', NORTH, ('Blast Furnace', 'Smoker', 'Barrel', 'Lectern'),
              {'Blast Furnace': ({'lit': False}, {'lit': True}),
               'Smoker': ({'lit': False}, {'lit': True}),
               'Barrel': ({'facing': NORTH, 'open': True}, {'facing': NORTH, 'open': False}),
               'Lectern': ({'has_book': False}, {'has_book': True})})

    for f in ('amethyst',):
        room.function(f + '_init').add(tag(e().tag(f + '_home')))
    amethyst_phases = (
        'Amethyst Block', 'Budding Amethyst', 'Small Amethyst|Bud', 'Medium Amethyst|Bud', 'Large Amethyst|Bud',
        'Amethyst Cluster')

    def amethyst_loop(step):
        block = good_block(step.elem)
        if step.elem == amethyst_phases[0]:
            yield setblock(r(0, 4, 0), block.id)
        else:
            yield setblock(r(0, 4, 0), 'budding_amethyst')
            if ' Bud' in block.name or 'Cluster' in block.name:
                yield setblock(r(0, 3, 0), block.clone().merge_state({'facing': 'down'}))
                yield setblock(r(0, 5, 0), block.clone().merge_state({'facing': 'up'}))
                for offset in (NORTH, EAST, WEST, SOUTH):
                    facing = good_facing(offset)
                    yield setblock(r(facing.dx, 4, facing.dz), block.clone().merge_state({'facing': offset}))
        yield data().merge(r(0, 2, -1), block.sign_nbt)

    room.loop('amethyst', main_clock).add(
        fill(r(-1, 3, -1), r(1, 5, 1), 'air')
    ).loop(
        amethyst_loop, amethyst_phases, bounce=True
    ).add(
        kill(e().type('item').nbt({'Item': {'id': 'minecraft:amethyst_shard'}}))
    )

    def bell_loop(step):
        if step.i == 0:
            yield setblock(r(-1, 3, 0), 'air')
            yield setblock(r(1, 3, 0), 'air')
            yield setblock(r(0, 4, 0), 'stone_slab')
        elif step.i == 1:
            yield setblock(r(-1, 3, 0), Block('stone_stairs', state={'facing': EAST}))
            yield setblock(r(1, 3, 0), 'air')
            yield setblock(r(0, 4, 0), 'air')
        elif step.i == 2:
            yield setblock(r(-1, 3, 0), 'air')
            yield setblock(r(1, 3, 0), 'air')
            yield setblock(r(0, 4, 0), 'air')
        else:
            yield setblock(r(-1, 3, 0), Block('stone_stairs', {'facing': EAST}))
            yield setblock(r(1, 3, 0), Block('stone_stairs', {'facing': WEST}))
            yield setblock(r(0, 4, 0), 'air')
        yield setblock(r(0, 3, 0), Block('bell', state={'attachment': step.elem, 'facing': facing[step.i]}))

    attachments = ('ceiling', 'single_wall', 'floor', 'double_wall')
    facing = (NORTH, WEST, NORTH, WEST)
    room.loop('bell', main_clock).add(setblock(r(0, 3, 0), 'air')).loop(bell_loop, attachments)

    def armor_stand_loop(step):
        if step.elem is None:
            nbt = Nbt(ShowArms=False)
        else:
            nbt = Nbt(ShowArms=True,
                      Pose={'LeftArm': [step.elem[0], 0, step.elem[1]], 'RightArm': [step.elem[2], 0, step.elem[3]]})
        yield data().merge(e().tag('armor_stand').limit(1), nbt)

    room.function('armor_stand_init').add(
        room.mob_placer(r(0, 3, 0), NORTH, adults=True).summon('armor_stand'),
        label(r(-1, 2, 0), "Get Small"))
    room.loop('armor_stand', main_clock).loop(
        armor_stand_loop,
        (None, (-10, -10, 0, 10), (-60, -10, 0, 60), (-120, 10, 0, 120), (-170, 10, 0, 170)),
        bounce=True)

    def brewing_stand_loop(step):
        for j in range(0, 3):
            if j in step.elem:
                yield item().replace().block(r(0, 3, 0), f'container.{j:d}').with_(
                    Block('potion', nbt={'Potion': 'water'}), 1)
            else:
                yield item().replace().block(r(0, 3, 0), f'container.{j:d}').with_('air')

    room.function('brewing_stand_init').add(function('restworld:containers/brewing_init'))
    room.loop('brewing_stand', main_clock).add(
        item().replace().block(r(0, 3, 0), 'container.3').with_('air'),
        item().replace().block(r(0, 3, 0), 'container.4').with_('air'),
        data().merge(r(0, 3, 0), {'BrewTime': 0, 'Fuel': 0}),
    ).loop(brewing_stand_loop, ((), (0,), (1,), (2,), (2, 0), (1, 2), (0, 1), (0, 1, 2)))

    def cake_loop(step):
        yield setblock(r(0, 3, 0), Block('cake', {'bites': step.elem}))
        yield data().merge(r(0, 2, -1), {'Text3': f'Bites: {step.elem:d}'})

    room.function('cake_init').add(data().merge(r(0, 2, -1), {'Text2': 'Cake'}))
    room.loop('cake', main_clock).loop(cake_loop, range(0, 7), bounce=True)

    def chest_loop(step):
        step.elem.merge_state({'facing': NORTH})
        yield setblock(r(0, 3, 0), step.elem)
        txt = {'Text2': 'Trapped' if 'T' in step.elem.name else '',
               'Text3': 'Double Chest' if 'type' in step.elem.state else 'Chest'}
        if 'Ender' in step.elem.name:
            txt['Text2'] = 'Ender'
        yield data().merge(r(0, 2, -1), txt)
        if 'type' in step.elem.state:
            step.elem.state['type'] = 'left'
            yield setblock(r(-1, 3, 0), step.elem)
        else:
            yield setblock(r(-1, 3, 0), 'air')

    room.loop('chest', main_clock).loop(chest_loop, (
        Block('Chest'), Block('Ender Chest'), Block('Trapped Chest'), Block('Chest', state={'type': 'right'}),
        Block('Trapped Chest', state={'type': 'right'})))

    def command_block_loop(step):
        block = Block(step.elem[0], {'facing': WEST, 'conditional': str(step.elem[1]).lower()})
        yield setblock(r(0, 3, 0), block)
        words = step.elem[0].split(' ')
        modifier = '' if len(words) == 2 else words[0]
        yield data().merge(r(0, 2, 1),
                           Sign.lines_nbt((None, modifier, None, '(Conditional)' if step.elem[1] else '')))

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
        yield data().merge(r(0, 2, -1), Sign.lines_nbt((None, 'Soul Fire' if step.elem == 'soul_soil' else 'Fire')))

    room.function('fire_init').add(WallSign((None, 'Fire')).place(r(0, 2, -1), NORTH))
    room.loop('fire', main_clock).add(fill(r(0, 3, 0), r(0, 5, 0), 'air')).loop(fire_loop, (
        'oak_log', 'oak_log', 'oak_log', 'soul_soil'))

    def item_frame_loop(step):
        yield step.elem.merge_nbt({'Tags': ['item_frame_as_block']}).summon(r(0, 3, -1)),
        yield data().merge(r(0, 2, -1), Sign.lines_nbt((None, *step.elem.sign_text)))

    item_frame_init = kill(e().tag('item_frame_as_block'))
    room.function('item_frame_init').add(item_frame_init)
    frames = (ItemFrame(NORTH).item('Lapis Lazuli'),
              ItemFrame(NORTH),
              ItemFrame(NORTH, glowing=True),
              ItemFrame(NORTH, glowing=True).item('Lapis Lazuli'))
    room.loop('item_frame', main_clock).add(item_frame_init).loop(item_frame_loop, frames)

    def lantern_loop(step):
        lantern = Block('Lantern' if step.i < 2 else 'Soul Lantern', {'hanging': False})
        if step.i in (0, 3):
            yield setblock(r(0, 3, 0), lantern),
            yield setblock(r(0, 4, 0), 'air'),
            yield data().merge(r(0, 2, -1), {'Text2': '', 'Text4': ''}),
        else:
            lantern.merge_state({'hanging': True}),
            yield setblock(r(0, 3, 0), lantern),
            yield setblock(r(0, 4, 0), 'chain'),
            yield data().merge(r(0, 2, -1), {'Text2': 'Hanging', 'Text4': 'and Chain'}),
        yield data().merge(r(0, 2, -1), {'Text3': lantern.name})

    room.function('lantern_init').add(
        WallSign([]).place(r(0, 2, -1, ), NORTH),
        data().merge(r(0, 2, -1), {'Text3': 'Lantern'}))
    room.loop('lantern', main_clock).loop(lantern_loop, range(0, 4))

    room.function('ore_blocks_init').add(label(r(-1, 2, 0), 'Deepslate'))
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
        execute().if_().score(skulk_loop.score).matches(6).positioned(r(0, 3, 0)).run(
            function('restworld:particles/shriek_particles')),
        execute().if_().score(skulk_loop.score).matches(8).positioned(r(0, 3, 0)).run(
            function('restworld:particles/shriek_particles')),
    )

    def snow_loop(step):
        yield setblock(r(0, 3, 0), Block('grass_block', {'snowy': True}))
        yield setblock(r(0, 4, 0), Block('snow', {'layers': step.elem}))
        yield data().merge(r(0, 2, 1), {'Text3': f'Layers: {step.elem:d}'})

    room.loop('snow', main_clock).loop(snow_loop, range(1, 9), bounce=True)

    def spawner_loop(step):
        yield data().merge(r(0, 3, 0), {'SpawnData': {'entity': {'id': Entity(step.elem).id}}})
        yield data().merge(r(0, 2, -1), {'Text2': step.elem})

    room.function('spawner_init').add(setblock(r(0, 3, 0), 'spawner'))
    room.loop('spawner', main_clock).loop(spawner_loop, ('Pig', 'Zombie', 'Skeleton', 'Spider', 'Cave Spider', 'Blaze'))

    def structure_blocks_loop(step):
        yield data().merge(r(0, 2, 1), {'Text2': step.elem})
        yield data().merge(r(0, 3, 0), {'mode': step.elem.upper()})

    room.function('structure_blocks_init').add(data().merge(r(0, 2, 1), {'Text3': 'Structure Block'}))
    room.loop('structure_blocks', main_clock).loop(structure_blocks_loop, ('Data', 'Save', 'Load', 'Corner'))

    def tnt_loop(step):
        yield kill(e().type('tnt').distance((None, 10)))
        yield setblock(r(0, 3, 0), Block('tnt', {'unstable': step.elem == 'unstable'}))
        yield data().merge(r(0, 2, -1), {'Text3': step.elem.title()})

    room.loop('tnt', main_clock).loop(tnt_loop, ('stable', 'unstable'))

    torches = (Block('Torch'), Block('Soul Torch'), Block('Redstone Torch'), Block('Redstone Torch'))
    wall_torches = tuple(Block(x.name.replace('Torch', 'Wall Torch')) for x in torches)

    def torches_loop(step):
        text = ({'Text2': '', 'Text4': ''}, {'Text2': 'Soul', 'Text4': ''}, {'Text2': 'Redstone', 'Text4': '(On)'},
                {'Text2': 'Redstone', 'Text4': '(Off)'})
        yield data().merge(r(0, 2, -1), text[step.i])
        if step.i == len(torches) - 1:
            yield execute().if_().score(wall_torches_score).matches(0).run(setblock(r(0, 2, 0), 'redstone_block'))
            yield execute().if_().score(wall_torches_score).matches(1).run(setblock(r(0, 3, 1), 'redstone_block'))
        yield execute().if_().score(wall_torches_score).matches(0).run(setblock(r(0, 3, 0), step.elem))
        yield execute().if_().score(wall_torches_score).matches(1).run(setblock(r(0, 3, 0), wall_torches[step.i]))

    wall_torches_score = room.score('wall_torches')
    room.function('torches_init').add(
        WallSign((None, None, 'Torch')).place(r(0, 2, -1), NORTH),
        label(r(-1, 2, 0), 'Wall-ness'),
        wall_torches_score.set(0)
    )
    room.loop('torches', main_clock).add(
        execute().if_().score(wall_torches_score).matches(0).run(data().merge(r(0, 2, -1), {'Text3': 'Torch'})),
        execute().if_().score(wall_torches_score).matches(1).run(data().merge(r(0, 2, -1), {'Text3': 'Wall Torch'})),
        setblock(r(0, 3, 0), 'air'),
        execute().unless().block(r(0, 3, 1), 'air').run(setblock(r(0, 3, 1), 'air')),
        execute().unless().block(r(0, 2, 0), 'air').run(setblock(r(0, 2, 0), 'barrier')),
    ).loop(torches_loop, torches)

    color_functions(room)
    expansion_functions(room)
    stepable_functions(room)

    for b in (
            'amethyst', 'anvil', 'bell', 'brewing_stand', 'cake', 'campfire', 'cauldron', 'chest', 'colored_beam',
            'colorings', 'composter', 'frosted_ice', 'grindstone', 'item_frame', 'job_sites_1', 'job_sites_2',
            'lantern', 'armor_stand'):
        room.function(b + '_init', exists_ok=True).add(tag(e().tag(b + '_home')).add('no_expansion'))


def room_init_functions(room, block_list_score):
    room.functions['blocks_room_init'].add(
        label(r(-16, 2, 3), 'List Blocks'),
        label(r(-16, 2, -3), 'List Blocks'),
        label(r(-43, 2, 3), 'List Blocks'),
        label(r(-43, 2, -3), 'List Blocks'),
        kill(e().tag('block_list'))
    )
    room.function('blocks_sign_init').add(
        execute().at(e().tag('blocks_home', '!no_expansion')).run(data().merge(r(0, 2, -1), {
            'Text1': JsonText.text("").click_event().run_command('function restworld:blocks/toggle_expand')})),
        execute().at(e().tag('blocks_home', '!no_expansion')).run(data().merge(r(0, 2, 1), {
            'Text1': JsonText.text("").click_event().run_command('function restworld:blocks/toggle_expand')})),

        execute().at(e().tag('blocks_home', 'no_expansion')).run(data().merge(r(0, 2, -1), {
            'Text1': JsonText.text("").click_event().run_command('say Sorry, cannot expand this block')})),
        execute().at(e().tag('blocks_home', 'no_expansion')).run(data().merge(r(0, 2, 1), {
            'Text1': JsonText.text("").click_event().run_command('say Sorry, cannot expand this block')})),
        tag(e().tag('block_sign_home')).add('no_expansion'),
    )
    room.loop('toggle_block_list', score=block_list_score).loop(
        lambda step: execute().as_(e().tag('block_list')).run(data().merge(s(), {"CustomNameVisible": step.i > 0})),
        range(0, 2))
    room.function('toggle_block_list_init').add(block_list_score.set(0))


def color_functions(room):
    coloring_coords = (r(1, 4, 6), r(-13, 2, -1))
    volume = Volume(*coloring_coords)
    lit_candles = room.score('lit_candles')

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
            fill(r(-9, 2, 2), r(-9, 2, 3), 'air')
            volume.replace('air', '#standing_signs')
            data().merge(e().tag('colorings_item_frame').limit(1), {'Item': {'Count': 0}})
        else:
            yield setblock(r(-9, 2, 2), Block(f'{color.id}_bed', {'facing': NORTH, 'part': 'head'}))
            yield setblock(r(-9, 2, 3), Block(f'{color.id}_bed', {'facing': NORTH, 'part': 'foot'}))
            frame_nbt = {'Item': Item.nbt_for(f'{color.id}_dye'), 'ItemRotation': 0}
            yield data().merge(e().tag('colorings_item_frame').limit(1), frame_nbt)

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
            yield kill_em(e().tag('colorings_horse'))
            horse = Entity('horse', nbt=horse_nbt.merge({'ArmorItem': {'id': 'leather_horse_armor', 'Count': 1}}))
            yield horse.summon(r(0.7, 2, 4.4))

        yield data().merge(e().tag('colorings_armor_stand').limit(1), {
            'ArmorItems': [Item.nbt_for('leather_boots', nbt=leather_color),
                           Item.nbt_for('leather_leggings', nbt=leather_color),
                           Item.nbt_for('leather_chestplate', nbt=leather_color),
                           Item.nbt_for('leather_helmet', nbt=leather_color)]})
        yield data().merge(e().tag('colorings_horse').limit(1),
                           {'ArmorItem': Item.nbt_for('leather_horse_armor', nbt=horse_leather_color)})
        yield data().merge(e().tag('colorings_llama').limit(1), {'DecorItem': llama_decor})
        yield data().merge(e().tag('colorings_sheep').limit(1), sheep_nbt)

        yield data().merge(r(-4, 2, 4), {'Text2': color.name})
        yield execute().as_(e().tag('colorings_names')).run(data().merge(s(), {'CustomName': color.name}))

        yield data().merge(r(0, 0, -1), {'name': f'restworld:{"plain" if is_plain else color.id}_terra'})
        yield data().merge(r(1, 2, -0), {'Text1': color.name})

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
        yield execute().if_().score(lit_signs).matches(0).run(
            data().merge(r(x, y, z), {'GlowingText': False, 'Text4': 'Text'}))
        yield execute().if_().score(lit_signs).matches(1).run(
            data().merge(r(x, y, z), {'GlowingText': True, 'Text4': 'Text'}))

    def render_signs(x, y, z, color, _):
        yield data().merge(r(x, y, z), {'Color': color.id, 'Text3': color.name})

    def colorings_loop(step):
        yield from colorings(False, step.elem)
        yield from colored_signs(step.elem, render_signs)

    horse_nbt = Nbt({
        'Variant': 5, 'Tags': ['colorings_horse', 'colorings_item', 'colorings_names'],
        'ArmorItem': Item.nbt_for('leather_horse_armor'), 'Rotation': [-25, 0], 'Tame': True, 'NoAI': True,
        'Silent': True})
    room.function('colorings_init').add(
        kill(e().tag('colorings_item')),

        Entity('item_frame', {
            'Facing': 3, 'Tags': ['colorings_item_frame', 'colorings_item'], 'Item': Item.nbt_for('stone'),
            'Fixed': True}).summon(r(-4.5, 4, 0.5)),
        Entity('horse', horse_nbt).summon(r(0.7, 2, 4.4)),
        Entity('armor_stand', {
            'Tags': ['colorings_armor_stand', 'colorings_item'], 'Rotation': [30, 0]}).summon(r(-1.1, 2, 3)),
        Entity('llama', {
            'Tags': ['colorings_llama', 'colorings_item', 'colorings_names'], 'Variant': 1, 'Tame': True, 'NoAI': True,
            'Silent': True, 'Rotation': [20, 0], 'Leashed': True}).summon(r(-11, 2, 5.8)),
        Entity('sheep', {
            'Tags': ['colorings_sheep', 'colorings_item'], 'Variant': 1, 'NoAI': True, 'Silent': True,
            'Rotation': [-35, 0], 'Leashed': True}).summon(r(-9.0, 2, 5.0)),

        execute().as_(e().tag('colorings_names')).run(data().merge(s(), {'CustomNameVisible': True})),

        WallSign((None, 'Terracotta')).place(r(-1, 3, 1), SOUTH),
        WallSign((None, 'Shulker Box')).place(r(-3, 3, 1), SOUTH),
        WallSign((None, 'Dye')).place(r(-4, 3, 1, ), SOUTH),
        WallSign((None, 'Concrete')).place(r(-5, 3, 1), SOUTH),
        WallSign((None, 'Glass')).place(r(-7, 3, 1), SOUTH),

        colored_signs(None,
                      lambda x, y, z, _, wood:
                      Sign((wood.name, 'Sign With', 'Default', 'Text'), wood=wood.id).place(r(x, y, z), 14)),
        WallSign([]).place(r(-4, 2, 4, ), SOUTH),

        kill(e().type('item')),

        label(r(-1, 2, 7), 'Lit Candles'),
        label(r(-7, 2, 7), 'Plain'),
        label(r(-11, 2, 3), 'Glowing'),
    ),
    room.loop('colorings', main_clock).add(
        fill(r(-9, 2, 2), r(-9, 2, 3), 'air')
    ).loop(colorings_loop, colors).add(
        colored_signs(None, render_signs_glow),
        setblock(r(-7, -1, 3), 'redstone_block'),
        setblock(r(-7, -1, 3), 'air'),
    )
    room.function('colorings_plain_off', home=False).add(
        clone((coloring_coords[0][0], coloring_coords[0][1].value - coloring_coords[1][1].value + 1,
               coloring_coords[0][2]),
              (coloring_coords[1][0], 0, coloring_coords[1][2]),
              (coloring_coords[1][0], coloring_coords[1][1] - 1, coloring_coords[1][2])),

        tag(e().tag('colorings_base_home')).add('colorings_home'),
        execute().at(e().tag('colorings_home')).run(function('restworld:/blocks/colorings_cur')),
        kill(e().type('item').distance((None, 20))),
    )
    room.function('colorings_plain_on', home=False).add(
        clone((coloring_coords[0][0], coloring_coords[0][1], coloring_coords[0][2]),
              (coloring_coords[1][0], coloring_coords[1][1] - 1, coloring_coords[1][2]),
              (coloring_coords[1][0], 0, coloring_coords[1][2])),

        tag(e().tag('colorings_base_home')).remove('colorings_home'),
        colorings(True, Color('Plain', 0x0)),
        setblock(r(-7, -1, 3), 'redstone_torch'),
        setblock(r(-7, -1, 3), 'air'),
        kill(e().type('item').distance((None, 20))),
    )
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
        # There are two possible cases: Either this homer is already
        # expanding or it is not.  We need to swap that.

        # If it's an expander, add a temporary 'to be stopped' tag to it
        execute().as_(e().tag('expander').distance((None, 1))).run(tag(s()).add('stop_expanding')),
        # If it's not an expander, tag it as one
        execute().as_(e().tag('!expander', '!no_expansion').distance((None, 1))).run(tag(s()).add('expander')),
        # If it has the 'to be stopped' tag, remove the expander tag
        execute().as_(e().tag('stop_expanding').distance((None, 1))).run(tag(s()).remove('expander')),
        # ... and then remove the 'to be stopped' tag
        execute().as_(e().tag('stop_expanding').distance((None, 1))).run(tag(s()).remove('stop_expanding')),

        # Now it has the right tagging, do an immediate().action on it
        execute().at(e().tag('expander').distance((None, 1))).run(function('restworld:blocks/expander')),
        execute().at(e().tag('!expander', '!no_expansion').distance((None, 1))).run(
            function('restworld:blocks/contracter')),

        # And, as a cleanup, if it never will be an expander, say 'sorry'
        execute().at(e().tag('no_expansion').distance((None, 1))).run(say('Sorry, cannot expand this.')),
        execute().at(e().tag('no_expansion', 'fire_home').distance((None, 1))).run(say('Sorry, cannot expand this.')),
    )
    room.function('expander').add(
        execute().if_().entity(e().tag('fire_home').distance((None, 1))).run(function('restworld:blocks/expand_fire')),
        execute().if_().entity(e().tag('dripstone_home').distance((None, 1))).run(
            function('restworld:blocks/expand_dripstone')),
        execute().unless().entity(e().tag('fire_home').distance((None, 1))).unless().entity(
            e().tag('dripstone_home').distance((None, 1))).run(function('restworld:blocks/expand_generic'))
    )
    room.function('expand_all', home=False).add(
        execute().as_(e().tag('blocks_home', '!no_expansion', '!expander')).run(
            execute().at(s()).run(function('restworld:blocks/toggle_expand_at'))))
    room.function('expand', main_clock).add(
        execute().at(e().tag('expander')).run(function('restworld:blocks/expander')))
    room.function('expand_dripstone', home=False).add(
        # Clone the original stack to either side to form a line, including anything on top of the block
        clone(r(0, 12, 0), r(0, 3, 0), r(-1, 3, 0)),
        clone(r(0, 12, 0), r(0, 3, 0), r(1, 3, 0)),

        # Clone the line to either side to get a 3x3 level
        clone(r(1, 12, 0), r(-1, 3, 0), r(-1, 3, -1)),
        clone(r(1, 12, 0), r(-1, 3, 0), r(-1, 3, 1)),
    )
    fire_score = room.score('fire')
    room.function('expand_fire', home=False).add(
        execute().unless().score(fire_score).matches(1).run(fill(r(-2, 4, 1), r(-2, 4, -1), 'air')),
        execute().unless().score(fire_score).matches(1).run(fill(r(2, 4, 1), r(2, 4, -1), 'air')),
        execute().unless().score(fire_score).matches(1).run(fill(r(1, 4, -2), r(-1, 4, -2), 'air')),
        execute().unless().score(fire_score).matches(1).run(fill(r(1, 4, 2), r(-1, 4, 2), 'air')),
        clone(r(0, 5, 0), r(0, 3, 0), r(1, 3, 0)),
        clone(r(0, 5, 0), r(0, 3, 0), r(-1, 3, 0)),
        clone(r(1, 5, 0), r(-1, 3, 0), r(-1, 3, 1)),
        clone(r(1, 5, 0), r(-1, 3, 0), r(-1, 3, -1)),
        execute().if_().score(fire_score).matches(1).run(fill(r(-2, 4, 1), r(-2, 4, -1), 'fire[west=true]')),
        execute().if_().score(fire_score).matches(1).run(fill(r(2, 4, 1), r(2, 4, -1), 'fire[east=true]')),
        execute().if_().score(fire_score).matches(1).run(fill(r(1, 4, -2), r(-1, 4, -2), 'fire[north=true]')),
        execute().if_().score(fire_score).matches(1).run(fill(r(1, 4, 2), r(-1, 4, 2), 'fire[south=true]')),
    )
    room.function('expand_generic', home=False).add(
        # Sand blocks will fall if they aren't supported, so we place barriers under them
        execute().if_().block(r(0, 3, 0), '#restworld:sand').run(
            fill(r(-1, 2, -1), r(1, 2, 1), 'barrier').replace('air')),

        # We want to clone up the snow topper, if_().it exists. If it doesn't, we need that layer
        # to be cleared (it might have something from a previous expansion). And snow is the
        # only thing that is normally placed on that level.
        execute().unless().block(r(0, 4, 0), 'snow').run(fill(r(-1, 4, -1), r(1, 4, 1), 'air')),

        # Clone the original block to either side to form a line, including anything on top of the block
        clone(r(0, 4, 0), r(0, 3, 0), r(-1, 3, 0)),
        clone(r(0, 4, 0), r(0, 3, 0), r(1, 3, 0)),

        # Clone the line to either side to get a 3x3 level
        clone(r(1, 4, 0), r(-1, 3, 0), r(-1, 3, -1)),
        clone(r(1, 4, 0), r(-1, 3, 0), r(-1, 3, 1)),

        # Clone the fill bottom level to the top
        clone(r(1, 4, 1), r(-1, 3, -1), r(-1, 5, -1)),

        # Soil needs the middle level filled with dirt
        execute().if_().block(r(0, 5, 0), '#restworld:soil').run(fill(r(-1, 3, -1), r(1, 4, 1), 'dirt')),

        # Otherwise fill the middle level with the top level
        execute().unless().block(r(0, 5, 0), '#restworld:soil').run(clone(r(1, 5, 1), r(-1, 5, -1), r(-1, 4, -1))),
    )

    room.function('contracter').add(
        execute().if_().entity(e().tag('fire_home').distance((None, 1))).run(
            function('restworld:blocks/contract_fire')),
        execute().if_().entity(e().tag('dripstone_home').distance((None, 1))).run(
            function('restworld:blocks/contract_dripstone')),
        execute().unless().entity(e().tag('fire_home').distance((None, 1))).unless().entity(
            e().tag('dripstone_home').distance((None, 1))).run(function('restworld:blocks/contract_generic')),
    )
    room.function('contract_all', home=False).add(
        execute().as_(e().tag('blocks_home', '!no_expansion', 'expander')).run(
            execute().at(s()).run(function('restworld:blocks/toggle_expand_at'))))
    room.function('contract_dripstone').add(
        # Erase the front and back lines
        fill(r(1, 12, 1), r(-1, 3, 1), 'air'),
        fill(r(1, 12, -1), r(-1, 3, -1), 'air'),

        # Erase either side
        fill(r(1, 12, 0), r(1, 3, 0), 'air'),
        fill(r(-1, 12, 0), r(-1, 3, 0), 'air'),
    )
    room.function('contract_fire').add(
        fill(r(1, 5, 1), r(-1, 3, -1), 'air'),
        function('restworld:blocks/fire_cur'))
    room.function('contract_generic').add(
        clone(r(0, 5, 0), r(0, 6, 0), r(0, -10, 0)),
        fill(r(-1, 3, -1), r(1, 6, 1), 'air'),
        clone(r(0, -9, 0), r(0, -10, 0), r(0, 3, 0)).replace(MOVE),
        setblock(r(0, 2, 0), 'stone'),
        fill(r(-1, 2, -1), r(1, 2, 1), 'air').replace('barrier'),
        setblock(r(0, 2, 0), 'barrier')
    )

    room.function('generic_home', home=False).add(
        kill(e().tag('generic_home').distance((None, 2))),
        summon('armor_stand', r(0, 0.5, 0),
               {'Tags': ['generic_home', 'homer', 'blocks_home'], 'NoGravity': True, 'Small': True}),
    )
    # generic_home is used for entirely static blocks. This is used for blocks that are changed, but
    # by a different command block than the one under it. These want to be expanded as they change,
    room.function('just_expand_home', home=False).add(
        kill(e().tag('just_expand_home').distance((None, 2))),
        summon('armor_stand', r(0, 0.5, 0),
               {'Tags': ['just_expand_home', 'homer', 'blocks_home'], 'NoGravity': True, 'Small': True}))


def stepable_functions(room):
    def stepable_loop(step):
        volume = Volume(r(0, 2, 0), r(3, 6, 6))
        i = step.i
        yield volume.replace(step.elem, '#restworld:stepable_planks')
        yield volume.replace_slabs(slabs[i], '#restworld:stepable_slabs')
        yield volume.replace_stairs(stairs[i], '#restworld:stepable_stairs')
        sign_text = Sign.lines_nbt(Block(step.elem).full_text)
        yield data().merge(r(1, 2, -1), sign_text)

    blocks = (
        'Stone', 'Cobblestone', 'Mossy|Cobblestone',
        'Bricks', 'Stone Bricks', 'Mossy|Stone Bricks', 'Mud Bricks',
        'Sandstone', 'Smooth|Sandstone', 'Red|Sandstone', 'Smooth Red|Sandstone',
        'Andesite', 'Polished|Andesite',
        'Diorite', 'Polished|Diorite',
        'Granite', 'Polished|Granite',
        'Cobbled|Deepslate',
        'Polished|Deepslate',
        'Deepslate|Bricks',
        'Deepslate|Tiles',
        'Cut Copper',
        'Exposed Cut Copper',
        'Weathered Cut Copper',
        'Oxidized Cut Copper',
        'Prismarine', 'Prismarine|Bricks', 'Dark|Prismarine',
        'Acacia Planks', 'Birch Planks', 'Jungle Planks',
        'Mangrove Planks',
        'Oak Planks', 'Dark Oak Planks', 'Spruce Planks',
        'Warped Planks', 'Crimson Planks',
        'Nether Bricks', 'Red|Nether Bricks',
        'Blackstone', 'Polished|Blackstone',
        'Polished|Blackstone Bricks', 'Quartz Block', 'Smooth|Quartz',
        'End Stone Bricks', 'Purpur Block',
    )
    stairs = tuple(re.sub('(marine|ite)$', r'\1 Stairs', re.sub('[Ss]tone$', 'Stone Stairs',
                                                                f.replace('Planks', 'Stairs').replace('Tiles',
                                                                                                      'Tile Stairs').replace(
                                                                    'Copper', 'Copper Stairs').replace('Bricks',
                                                                                                       'Brick Stairs').replace(
                                                                    'Block', 'Stairs').replace('|Quartz',
                                                                                               ' Quartz Stairs').replace(
                                                                    '|Deepslate', '|Deepslate Stairs'))) for f in
                   blocks)
    slabs = tuple(f.replace('Stairs', 'Slab') for f in stairs)

    room.function('stepable_init').add(
        WallSign((None, 'Block')).place(r(3, 4, 5, ), NORTH),
        WallSign((None, 'Double slab')).place(r(3, 5, 5, ), NORTH),
        WallSign((None, 'Slabs & Stairs')).place(r(1, 2, -1, ), NORTH))
    room.loop('stepable', fast_clock).loop(stepable_loop, blocks)
