from __future__ import annotations

import re
from typing import Iterable, Union

from pynecraft import commands, info
from pynecraft.base import DOWN, E, EAST, EQ, FacingDef, N, NORTH, Nbt, RelCoord, S, SOUTH, UP, W, WEST, as_facing, \
    r, \
    rotate_facing, to_id, to_name
from pynecraft.commands import Block, Commands, Entity, MOD, MOVE, REPLACE, SUCCESS, ScoreName, as_block, \
    as_score, \
    clone, data, e, execute, fill, function, item, kill, n, p, s, say, schedule, setblock, summon, tag
from pynecraft.function import Function, Loop
from pynecraft.info import Color, armor_equipment, colors, sherds, stems
from pynecraft.simpler import Item, ItemFrame, Region, Sign, TextDisplay, WallSign
from restworld.materials import enchant
from restworld.rooms import Clock, Room, erase, if_clause, kill_em
from restworld.world import fast_clock, main_clock, restworld


def room():
    room = Room('blocks', restworld, EAST, ('Blocks,', 'Paintings,', 'Banners,', 'DIY, Models'))

    block_list_score = room.score('block_list')

    list_scale = 0.6

    def blocks(name: str, facing: FacingDef,
               block_lists: Iterable[Union[Block, str]] | Iterable[Iterable[Union[Block, str]]],
               dx: float = 0, dz: float = 0, size: int = 0, labels=None, clock: Clock = main_clock,
               score: ScoreName = None, air: bool = False, expandable=True) -> tuple[Function, Loop]:
        facing = as_facing(facing)

        # Ensure we have a list (so we can modify it)
        if not isinstance(block_lists, list):
            block_lists = list(block_lists)
        # Convert a single list into a list of that one list
        if not isinstance(block_lists[0], Iterable) or isinstance(block_lists[0], str):
            block_lists = [block_lists]
        lengths = set(len(x) for x in block_lists)
        if len(lengths) != 1:
            raise ValueError(f'All lists must be the same length, got lenghts {lengths}')
        # Convert all to Block objects, handling '' as a nameless structure_void
        for i, sublist in enumerate(block_lists):
            block_lists[i] = list(
                map(lambda x: Block(id='structure_void', name='') if x == '' else as_block(x), sublist))
        # If there are names to show, set bool that will show them
        # noinspection PyUnresolvedReferences
        show_list = len(set(x.id for x in block_lists[0])) > 1

        # A one-element list doesn't require a loop
        singleton = len(block_lists[0]) == 1
        if not singleton:
            block_loop = room.loop(name, clock, score=as_score(score))
        else:
            block_loop = None

        block_init = room.function(name + '_init', exists_ok=True).add(
            WallSign(()).place(r(facing.dx, 2, facing.dz), facing),
            tag(e().tag(f'{name}_home')).add('particulate')
        )
        if expandable:
            block_init.add(tag(e().tag(f'{name}_home')).add('expansion'))
        if show_list:
            block_init.add(execute().if_().score(block_list_score).matches(0).run(kill(e().tag(f'block_list_{name}'))))
            names = room.function(name + '_names', home=False)
            block_init.add(function(names.full_name))

        def signage_for(block, i):
            if block.name == 'structure void':
                return ()
            return labels[i] if labels else block.sign_text

        # Find the max length of a sign change so we blank out all lines when a given block has fewer.
        max_lines = 0
        for j, _ in enumerate(block_lists):
            max_lines = max(max_lines, *(len(signage_for(block, i)) for i, block in enumerate(block_lists[j])))

        # show a single block from the list. "step" will be present if in a loop (i.e., not a singleton)
        def one_block(block: Block, pos, step: Loop.Step | None):
            signage = signage_for(block, step.i if step else 0)
            if air:
                yield setblock(pos, 'air')
            yield setblock(pos, block)
            # Pad out shorter signs to max length
            signage += ("",) * (max_lines - len(signage))

            x, y, z = pos
            if step:
                room.particle(block, name, (x, y + 1, z), step)
            else:
                room.particle(block, name, (x, y + 1, z))
            # start=1: Preserve the 'expansion' response; blanks=True: Erase longer answers from other blocks
            yield Sign.change(r(x + facing.dx, 2, z + facing.dz), signage, start=1, blanks=True)
            return block

        if singleton:
            assert len(block_lists) == 1  # Don't have code for a list of singletons
            block_init.add(one_block(block_lists[0][0], r(0, 3, 0), None))
        else:
            def blocks_loop_body(step):
                i = step.i
                x = z = 0
                x_size = 0

                for block_list in block_lists:
                    block = yield from one_block(block_list[i], r(x, 3, z), step)

                    if show_list:
                        block_list_name = f'block_list_{name}_{x}_{z}'
                        block_list_block_name = f'block_list_{name}_{x}_{z}_{i}'
                        # The opacity of 25 means "invisible" so it starts out that way
                        holder = TextDisplay(
                            block.name,
                            nbt={'Rotation': [180.0, 0.0], 'text_opacity': 25, 'background': 0,
                                 'billboard': 'vertical', 'shadow_radius': 0}).scale(list_scale).tag(
                            'blocks', 'block_list', f'block_list_{name}', block_list_name, block_list_block_name)
                        names.add(holder.summon(r(x, 4.25 + (len(block_list) - i) * (list_scale / 4), z)))

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

    def job_sites(name, facing, sites, stages=None, expandable=True):
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
        blocks(name, facing, all, expandable=expandable)

    room_init_functions(room, block_list_score)

    room.function('anvil_init', exists_ok=True).add(WallSign((None, 'Anvil')).place(r(0, 2, -1), NORTH))
    blocks('anvil', NORTH, list(Block(b, state={'facing': WEST}) for b in ('Anvil', 'Chipped Anvil', 'Damaged Anvil')),
           expandable=False)
    blocks('bedrock', SOUTH, ('Bedrock',))
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
    blocks('deepslate_bricks', NORTH, (
        'Deepslate|Bricks', 'Cracked|Deepslate|Bricks', 'Deepslate|Tiles', 'Cracked|Deepslate|Tiles'))
    blocks('bricks', NORTH, (
        'Bricks', 'Quartz Bricks', 'Mud Bricks', 'Prismarine Bricks', 'Tuff Bricks', 'Resin Bricks'))
    blocks('nether_bricks', NORTH, (
        'Nether Bricks', 'Cracked|Nether Bricks', 'Chiseled|Nether Bricks', 'Red|Nether Bricks'))
    blocks('stone_bricks', NORTH, (
        'Stone Bricks', 'Mossy|Stone Bricks', 'Cracked|Stone Bricks', 'Chiseled|Stone Bricks',
        'Polished|Blackstone Bricks', 'Cracked Polished|Blackstone Bricks'))
    blocks('calcite', NORTH, ('Calcite',))
    campfire_food = room.score('campfire_food')
    campfire_init, campfire_main = blocks('campfire', NORTH, (
        Block('Campfire', {'lit': True}),
        Block('campfire', {'lit': False}, name='Campfire|Unlit'),
        Block('Soul Campfire', {'lit': True}),
        Block('soul_campfire', {'lit': False}, name='Soul Campfire|Unlit'),
    ), expandable=False)
    campfire_init.add(room.label(r(-1, 2, 0), 'Cook', NORTH))
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
    blocks('chiseled', NORTH, (
        'Chiseled|Deepslate', 'Chiseled|Polished|Blackstone', 'Chiseled Tuff|Bricks', 'Chiseled|Quartz Block',
        'Chiseled|Tuff', 'Chiseled|Resin Bricks'))
    blocks('clay', SOUTH, ('Clay', 'Mud', 'Muddy|Mangrove Roots', 'Packed Mud'))
    blocks('cobble', NORTH, ('Cobblestone', 'Mossy|Cobblestone', 'Cobbled|Deepslate'))
    blocks('cobweb', NORTH, ('Cobweb',))

    crafter_states = ({}, {'triggered': True}, {'crafting': True})
    blocks('crafter', NORTH, (Block('crafter', state) for state in crafter_states),
           labels=tuple(('Crafter', x) for x in ('', 'Triggered', 'Crafting')))

    natural_heart = room.score('natural_heart')

    def creaking_heart_loop(step):
        yield execute().if_().score(natural_heart).matches(0).run(
            setblock(r(0, 4, 0), 'air'),
            setblock(r(0, 2, 0), 'barrier'),
        )
        yield execute().unless().score(natural_heart).matches(0).run(
            setblock(r(0, 4, 0), 'air' if step.elem == 'disabled' else 'pale_oak_log'),
            setblock(r(0, 2, 0), 'pale_oak_log'),
        )
        block = Block('creaking_heart', {'creaking_heart_state': step.elem, 'natural': True})
        yield setblock(r(0, 3, 0), block),
        yield Sign.change(r(0, 2, 1), (None, None, step.elem.title()))
        room.particle(block, 'creaking_heart', r(0, 4, 0), step)

    room.loop('creaking_heart', main_clock).loop(creaking_heart_loop, ('awake', 'dormant', 'uprooted'))
    room.function('creaking_heart_init').add(
        WallSign((None, 'Creaking Heart')).place(r(0, 2, 1), SOUTH),
        room.label(r(1, 2, 0), "With Logs", SOUTH),
    )
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
    blocks('dried_kelp', SOUTH, ('Dried Kelp Block',))

    dry_ghast = room.score('dry_ghast')

    def dried_ghast_loop(step):
        block = Block('dried_ghast', {'hydration': step.i, 'facing': NORTH})
        pos = r(0, 3, 0)
        yield execute().unless().score(dry_ghast).matches(0).run(setblock(pos, block))
        yield execute().if_().score(dry_ghast).matches(0).run(setblock(pos, block.merge_state({'waterlogged': True})))
        yield Sign.change(r(0, 2, -1), (None, None, f'Hydration: {step.i}'))

    room.function('dried_ghast_init').add(
        WallSign((None, 'Dried Ghast')).place(r(0, 2, -1), NORTH),
        setblock(r(0, 3, 1), 'structure_void'),
        setblock(r(0, 3, -1), 'structure_void'),
        setblock(r(1, 3, 0), 'structure_void'),
        setblock(r(-1, 3, 0), 'structure_void'),
        room.label(r(-1, 2, 0), 'Waterlogged', NORTH),
        room.label(r(1, 2, 0), 'Ghastling', NORTH),
    )
    room.loop('dried_ghast', main_clock).loop(dried_ghast_loop, range(4))

    blocks('end', NORTH, ('End Stone', 'End Stone|Bricks'))
    blocks('frosted_ice', SOUTH,
           [Block('frosted_ice', {'age': i}, name=f'Frosted Ice|Age: {i}') for i in range(0, 4)] + [
               Block('water', name='Water|')], expandable=False)
    room.function('frosted_ice_enter').add(setblock(r(1, 0, 0), 'redstone_block'))
    room.function('frosted_ice_exit').add(setblock(r(1, 0, 0), 'air'))
    blocks('gilded_blackstone', NORTH, ('Gilded Blackstone',))
    blocks('glass', SOUTH, ('Glass', 'Tinted Glass'))
    blocks('hay', SOUTH, ('Hay Block',))
    blocks('heavy_core', NORTH, ('Heavy Core',))
    blocks('honeycomb', SOUTH, ('Honeycomb Block',))
    room.function('ladder_init').add(setblock(r(0, 3, 0), 'ladder'))
    blocks('jigsaw', SOUTH, (Block('Jigsaw', {'orientation': 'up_east'}),))
    blocks('lighting', SOUTH, (
        'Glowstone', 'Sea Lantern', 'Shroomlight', 'Ochre|Froglight', 'Pearlescent|Froglight', 'Verdant|Froglight',
        'End Rod'))
    blocks('ladder', NORTH, ('Ladder',), expandable=False)
    blocks('lodestone', SOUTH, ('Lodestone',))
    blocks('magma_block', SOUTH, ('Magma Block',))
    blocks('moss', SOUTH, (('Moss Block', 'Pale Moss Block'), ('Moss Carpet', 'Pale Moss Carpet')), dz=3)
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
    blocks('red_sand', SOUTH, ('Red Sand',))
    blocks('resin', SOUTH, ('Resin Block', 'Resin Bricks', 'Chiseled|Resin Bricks'))
    blocks('respawn_anchor', NORTH, (Block('Respawn Anchor', {'charges': x}) for x in range(0, 5)),
           labels=tuple(('Respawn Anchor', f'Charges: {x:d}') for x in range(0, 5)))

    def suspicious(which):
        suspicious_data = {'item': {'id': 'emerald'}}
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
    blocks('sticky', SOUTH, ('Slime Block', 'Honey block'))

    stone_types = ('Stone', 'Basalt', 'Deepslate', 'Andesite', 'Diorite', 'Granite', 'Tuff', 'Blackstone')
    polished_types = ('Smooth Basalt', 'Smooth Stone') + tuple(f'Polished|{t}' for t in stone_types[2:])
    blocks('stone', NORTH, (stone_types, polished_types), dz=3)

    test_block_modes = ('start', 'log', 'accept', 'fail')
    blocks('test', SOUTH, tuple(Block('test_block', {'mode': mode}) for mode in test_block_modes),
           labels=(tuple(('Test Block', f'Mode: {mode.title()}') for mode in test_block_modes)))
    blocks('test_instance', SOUTH, ('Test Instance Block',), expandable=True)

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
        room.label(r(-2, 2, -1), 'Waxed', NORTH),
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
    stripped_woods = list(map(lambda x: '' if x == 'Stripped|Bamboo Mosaic' else x, ['Stripped|' + x for x in wood]))
    blocks('wood_blocks', SOUTH, (tuple(f'{f} Planks' for f in woodlike),
                                  stripped_logs, logs, wood, leaves, stripped_woods), dx=-3, dz=-3, size=2)

    sites = ('Cauldron', 'Water Cauldron', 'Lava Cauldron', 'Powder Snow|Cauldron')
    stages = {'Water Cauldron': list({'level': t} for t in range(1, 4)),
              'Powder Snow|Cauldron': list({'level': t} for t in range(3, 0, -1)), }
    job_sites('cauldron', NORTH, sites, stages)
    job_sites('composter', NORTH, ('Composter',), {'Composter': tuple({'level': t} for t in range(0, 9))})
    job_sites('grindstone', NORTH, ('Grindstone',),
              {'Grindstone': list({'face': f} for f in ('floor', 'wall', 'ceiling'))}, expandable=False)
    job_sites('job_sites_1', NORTH,
              ('Crafting Table', 'Cartography Table', 'Fletching Table', 'Smithing Table', 'Loom', 'Stonecutter'))
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
        particle_pos = r(0, 5, 0)
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
                particle_pos = r(0, 5 + step.stage / 4 - 0.25, 0)
        room.particle(block, 'amethyst', particle_pos, step)

        sign_nbt = block.sign_nbt()
        sign_nbt['back_text'] = sign_nbt['front_text']
        yield data().merge(r(0, 2, -1), sign_nbt)

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
        yield Sign.change(r(0, 2, -1), (None, None, to_name(step.elem)))

    attachments = ('ceiling', 'single_wall', 'double_wall', 'floor')
    room.loop('bell', main_clock).add(setblock(r(0, 3, 0), 'air')).loop(bell_loop, attachments)
    room.particle('bell', 'bell', r(0, 4, 0))

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
        room.label(r(-1, 2, 0), "Get Small", NORTH))
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
    room.particle('brewing_stand', 'brewing_stand', r(0, 4, 0))

    def cake_loop(step):
        yield setblock(r(0, 3, 0), Block('cake', {'bites': step.elem}))
        yield Sign.change(r(0, 2, -1), (None, None, f'Bites: {step.elem:d}'))

    room.function('cake_init').add(WallSign((None, 'Cake')).place(r(0, 2, -1), NORTH))
    room.loop('cake', main_clock).loop(cake_loop, range(0, 7), bounce=True)
    room.particle('cake', 'cake', r(0, 4, 0))

    def chest_loop(step):
        step.elem.merge_state({'facing': NORTH})
        yield setblock(r(0, 3, 0), step.elem)
        room.particle(step.elem, 'chest', r(0, 4, 0), step)
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

    def to_command_block(type, cond):
        type = type.strip()
        state = {'facing': 'west'}
        name = f'{type}|Block'
        if cond:
            name += '|(Conditional)'
            state['conditional'] = True
        cb = Block(id=f'{to_id(type)}_block', name=name, state=state)
        return cb

    blocks('command_blocks', SOUTH, (to_command_block(*x) for x in (
        ('Command ', True), ('Command ', False), ('Chain Command ', False),
        ('Chain Command ', True), ('Repeating Command ', True),
        ('Repeating Command ', False), ('Command ', False), ('Command ', True),
        ('Chain Command ', True), ('Chain Command ', False),
        ('Repeating Command ', False),
        ('Repeating Command ', True))))

    def dripstone_loop(step):
        for j in range(0, step.elem):
            yield setblock(r(0, 4 + j, 0), Block('pointed_dripstone', {
                'thickness': 'tip', 'vertical_direction': 'up'}))
            yield setblock(r(0, 11 - j, 0), Block('pointed_dripstone', {
                'thickness': 'tip_merge' if j == step.elem - 1 else 'tip', 'vertical_direction': 'down'}))
        if step.elem != 4:
            yield fill(r(0, 4 + step.elem, 0), r(0, 11 - step.elem, 0), 'air')
            if step.elem == 0:
                room.particle('dripstone_block', 'dripstone', r(0, 4, 0), step)
            else:
                room.particle('pointed_dripstone', 'dripstone', r(0, 4 + step.stage, 0), step)

    room.function('dripstone_init').add(
        setblock(r(0, 3, 0), 'dripstone_block'),
        setblock(r(0, 12, 0), 'dripstone_block'),
        WallSign((None, 'Dripstone')).place(r(0, 2, -1), NORTH),
    )
    room.loop('dripstone', main_clock).loop(dripstone_loop, range(0, 5), bounce=True)

    def fire_loop(step):
        dirs = ({'up': False}, {'north': True}, {'up': True})
        surround = ((1, 0, 'west'), (-1, 0, 'east'), (0, -1, 'south'), (0, 1, 'north'),)
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
    blocks('ice', SOUTH, ('Ice', 'Packed Ice', 'Blue Ice'))

    infestables = []
    for b in ('Cobblestone', 'Deepslate', 'Stone', 'Stone Bricks', 'Chiseled|Stone Bricks', 'Cracked|Stone Bricks',
              'Mossy|Stone Bricks'):
        infestables.extend((b, f'Infested|{b}'))
    blocks('infested', NORTH, infestables)
    two = room.score('two')
    room.function('infested_init', exists_ok=True).add(
        room.label(r(-1, 2, 0), 'Infested Only', NORTH),
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
        lines = Sign.lines_nbt((None, *step.elem.sign_text))
        yield data().merge(r(0, 2, -1), {'front_text': lines, 'back_text': lines})

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
            yield Sign.change(r(0, 2, -1), (None, 'Hanging', lantern.name, 'and Chain'))
            room.particle('chain', 'lantern', r(0, 5, 0), step)
        room.particle(lantern, 'lantern', r(0, 4, 0), step)

    room.function('lantern_init').add(WallSign((None, None, 'Lantern')).place(r(0, 2, -1, ), NORTH))
    room.loop('lantern', main_clock).loop(lantern_loop, range(0, 4))

    room.function('ore_blocks_init').add(room.label(r(-1, 2, 0), 'Deepslate', NORTH))
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

    def resin_clumps_loop(step):
        block = Block(step.elem)
        yield setblock(r(0, 4, 0), block),
        # Remove the final line in case the block text went from two lines to one
        yield Sign.change(r(0, 2, -1), block.sign_text, start=2, min_len=2)
        for dir in (N, E, W, S, UP, DOWN):
            f = as_facing(dir)
            if dir == UP:
                o = as_facing(DOWN)
            elif dir == DOWN:
                o = as_facing(UP)
            else:
                o = rotate_facing(f, 180)
            delta = f.block_delta
            delta[1] += 4
            offset = r(*delta)
            yield setblock(offset, ('resin_clump', {o.name: True}))

    room.loop('resin_clumps', main_clock).loop(resin_clumps_loop, (
        'Pale Oak Log', 'Pale Oak Wood', 'Stripped|Pale Oak Log', 'Stripped|Pale Oak Wood'))
    room.particle('resin_clump', 'resin_clumps', r(0, 5.1, 0))

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
    room.particle('scaffolding', 'scaffolding', r(0, 4, 0))

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
        sign_pos = r(0, 2, -1)
        if isinstance(step.elem, str):
            spawner_nbt = {'SpawnData': {'entity': {'id': f'minecraft:{to_id(step.elem)}'}}}
            yield data().merge(r(0, 3, 0), spawner_nbt)
            yield Sign.change(sign_pos, (None, None, step.elem))

    room.function('spawner_init').add(setblock(r(0, 3, 0), 'spawner').nbt(
        {'SpawnRange': 0, 'MinSpawnDelay': 799, 'MaxSpawnDelay': 799, 'RequiredPlayerRange': 0, 'SpawnCount': 0}))
    room.particle('spawner', 'spawner', r(0, 4, 0))
    room.loop('spawner', main_clock).loop(spawner_loop, ('Skeleton', 'Zombie', 'Cave Spider', 'Blaze'))

    vault_states = {'waiting_for_players': 'inactive', 'cooldown': 'inactive',
                    'waiting_for_reward_ejection': 'unlocking', 'ejecting_reward': 'ejecting'}
    base_vault_nbt = {'state_updating_resumes_at': 0xfff_ffff_ffff_ffff}
    no_pickup = {'Tags': ['huh'], 'Age': -32768, 'PickupDelay': 2147483647}
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
        'simultaneous_mobs': 0.0,
        'simultaneous_mobs_added_per_player': 2.0,
        'ticks_between_spawn': 0x7fff_ffff,
        'spawn_potentials': [{'data': {'entity': {'id': "minecraft:stray"}}, 'weight': 1}],
        'loot_tables_to_eject': [{'data': "minecraft:spawners/ominous/trial_chamber/key", 'weight': 1}]}
    base_trial_spawner_nbt = Nbt({
        'required_player_range': 100,
        'target_cooldown_length': 0xfff_ffff,
        'next_mob_spawns_at': 0x7fff_ffff_ffff_ffff,
    })
    trial_spawner_spawns = {
        'normal_config': spawner_config,
        'ominous_config': spawner_config,
        'spawn_potentials': [{'data': {'entity': {'id': 'minecraft:stray'}}, 'weight': 1}],
        'spawn_data': {'entity': {'id': "minecraft:stray"}},
    }
    trial_spawner_nbts = {
        'inactive': base_trial_spawner_nbt.merge({'required_player_range': 1}),
        'waiting_for_players': base_trial_spawner_nbt.merge(trial_spawner_spawns).merge({'required_player_range': 1}),
        'active': base_trial_spawner_nbt.merge(trial_spawner_spawns),
        'waiting_for_reward_ejection': base_trial_spawner_nbt.merge(trial_spawner_spawns).merge({
            'total_ejections_needed': 6,
            'ejecting_loot_table': "minecraft:spawners/ominous/trial_chamber/key"}),
        'ejecting_reward': base_trial_spawner_nbt.merge({
            'total_ejections_needed': 6, 'total_mobs_spawned': 1000,
            'ejecting_loot_table': "minecraft:spawners/ominous/trial_chamber/key"}),
        'cooldown': base_trial_spawner_nbt.merge({
            'required_player_range': 1, 'cooldown_ends_at': 0x7fff_ffff_ffff_ffff}),
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
        for i, block in enumerate(trial_blocks):
            is_spawner = i < 2
            is_ominous = i % 2 == 1
            pos = trials[i]
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
            if step.i == 0:
                room.particle(block, 'trial', (pos[0], pos[1] + 1, pos[2]))
            # Right now active and waiting for ejection aren't showing. This is because /gamerule doMobSpawning false
            # stops trial spawners showing these states. See https://bugs.mojang.com/browse/MC-270885?filter=26400.
            # Turning the rule on causes spawns in the nether room (at least) so we can't do that. So we have to live
            # with this until that bug is fixed or they do something else.
            #
            # Also, ejecting items doesn't seem to work right, possibly due to the same thing.
            if step.i in range(2, 4):
                if is_spawner:
                    yield data().modify(pos, 'registered_players').append().from_(p(), 'UUID')
                else:
                    yield data().modify(pos, 'server_data.rewarded_players').append().from_(p(), 'UUID')
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
            yield WallSign(text).place(RelCoord.add(pos, sign_offset), NORTH)

    room.function('trial_init').add(trial_init())
    trial = room.loop('trial', main_clock)
    trial.add(
        kill(e().type('item').distance((None, 10)))
    ).loop(
        trial_loop,
        ('inactive', 'waiting_for_players', 'active', 'waiting_for_reward_ejection', 'ejecting_reward', 'cooldown'),
    )

    blocks('structure_blocks', SOUTH, list(
        Block('structure_block', name=f'{x}|Structure Block', state={'mode': x.lower()}) for x in
        ('Data', 'Save', 'Load', 'Corner')), air=True)

    # def structure_blocks_loop(step):
    #     yield Sign.change(r(0, 2, 1), (None, step.elem))
    #     yield data().merge(r(0, 3, 0), {'mode': step.elem.upper()})
    #
    # room.function('structure_blocks_init').add(WallSign((None, None, 'Structure Block')).place(r(0, 2, 1), SOUTH))
    # room.loop('structure_blocks', main_clock).loop(structure_blocks_loop, ('Data', 'Save', 'Load', 'Corner'))

    def tnt_loop(step):
        if step.i < 2:
            yield setblock(r(0, 3, 0), Block('tnt', {'unstable': step.elem == 'unstable'}))
        else:
            yield setblock(r(0, 3, 0), 'air')
            yield summon(('tnt', {'fuse': 0x7fff, 'Tags': ['block_tnt']}), r(0, 3, 0))
        yield Sign.change(r(0, 2, -1), (None, None, step.elem.title()))

    room.loop('tnt', main_clock).add(kill(e().tag('block_tnt'))).loop(tnt_loop, ('stable', 'unstable', 'primed'))
    room.particle('tnt', 'tnt', r(0, 4, 0))

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
        room.particle(step.elem, 'torches', r(0, 4, 0), step)

    wall_torches_score = room.score('wall_torches')
    room.function('torches_init').add(
        WallSign((None, None, 'Torch')).place(r(0, 2, -1), NORTH),
        room.label(r(-1, 2, 0), 'Wall-ness', NORTH),
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


def room_init_functions(room, block_list_score):
    room.functions['blocks_room_init'].add(
        room.label(r(-16, 2, 3), 'List Blocks', NORTH), room.label(r(-16, 2, -3), 'List Blocks', SOUTH),
        room.label(r(-46, 2, 3), 'List Blocks', NORTH), room.label(r(-46, 2, -3), 'List Blocks', SOUTH),
        room.label(r(-34, 2, 1), 'Show Particles', EAST),
        room.label(r(-34, 2, -1), 'Expand All', EAST),
        kill(e().tag('block_list')))

    # Ensure that setting up the expansion work on signs is done after all other things
    dbsi = room.function('do_blocks_sign_init', home=False).add(
        execute().at(e().tag('blocks_home', 'expansion')).run(
            Sign.change(r(0, 2, -1), (), ('function restworld:blocks/toggle_expand',)),
            Sign.change(r(0, 2, 1), (), ('function restworld:blocks/toggle_expand',))),
        execute().at(e().tag('blocks_home', '!expansion')).run(
            Sign.change(r(0, 2, -1), (), (say('Sorry, cannot expand this block'),)),
            Sign.change(r(0, 2, 1), (), (say('Sorry, cannot expand this block'),)))
    )
    room.function('blocks_sign_init').add(
        schedule().function(dbsi, 1, REPLACE)
    )

    room.loop('toggle_block_list', score=block_list_score).loop(
        lambda step: execute().as_(e().tag('block_list')).run(
            data().modify(s(), 'text_opacity').set().value(25 if step.i == 0 else 255)),
        range(2))
    room.function('toggle_block_list_init').add(block_list_score.set(0))


def armor_frame(which, where):
    frame = Entity('item_frame',
                   {'Facing': 3, 'Fixed': True, 'Item': Item.nbt_for(f'{which}'),
                    'Tags': ['colorings_item', 'colorings_frame', f'colorings_frame_{which}', 'colorings_enchantable']})
    return frame.summon(where)


def color_functions(room):
    coloring_coords = (r(1, 4, 6), r(-13, 2, -1))
    volume = Region(*coloring_coords)
    lit_candles = room.score('lit_candles')
    plain = room.score('plain')

    armor_stand = e().tag('colorings_armor_stand').limit(1)

    def colorings(is_plain, color, step=None):
        fills = {
            'stained_glass': r(-7, 5, 0), 'stained_glass_pane': r(-7, 3, 1), 'wool': r(-1, 3, 1), 'banner': r(1, 5, 2),
            'shulker_box': r(-3, 5, 0), 'carpet': r(-3, 2.1, 1), 'concrete': r(-5, 3, 1),
            'concrete_powder': r(-5, 5, 0), 'terracotta': r(-1, 5, 0)}
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
            if filler.id != 'air':
                room.particle(filler, 'colorings_base', fills[which], step, if_clause(plain, int(is_plain)))
            yield volume.replace(filler, '#restworld:' + which)

        candle = Block('candle' if is_plain else color.name + '_candle', {'lit': True})
        for count in range(1, 6):
            if count < 5:
                candle.merge_state({'candles': count})
                filter = f'#restworld:candle[candles={count:d}]'
                if count == 1:
                    room.particle(candle, 'colorings_base', r(-2, 2, 6), step, if_clause(plain, int(is_plain)))
            else:
                candle = Block(candle.id + '_cake', {'lit': True})
                filter = '#restworld:candle_cake'
                room.particle(candle, 'colorings_base', r(-2, 3, 5), step, if_clause(plain, int(is_plain)))
            candle.merge_state({'lit': False})
            yield execute().if_().score(lit_candles).matches(0).run(volume.replace(candle, filter))
            candle.merge_state({'lit': True})
            yield execute().unless().score(lit_candles).matches(0).run(volume.replace(candle, filter))

        yield commands.place().template(f'restworld:{color.id}_terra', r(-7, 1, 3))
        yield data().merge(r(-7, 0, 3), {'name': f'restworld:{color.id}_terra', 'showboundingbox': False})
        if not is_plain:
            room.particle(f'{color.id}_glazed_terracotta', 'colorings_base', r(-5.5, 2, 4.5), step, if_clause(plain, 0))

        if is_plain:
            color_name = 'Plain'
            sheep_nbt = {'Sheared': True, 'Color': 0}
            bundle = Item.nbt_for('bundle')
            yield erase(r(-9, 2, 2), r(-9, 2, 3))  # remove bed
            yield erase(volume.start, volume.end, '#standing_signs')
            yield data().remove(e().tag('colorings_item_frame').limit(1), 'Item.components.dyed_color')
            yield execute().as_(e().tag('colorings_dog')).run(
                data().remove(s(), 'equipment.body.components.dyed_color'))
            yield data().remove(e().tag('colorings_cat').limit(1), 'Owner')
            yield data().remove(e().tag('colorings_llama').limit(1), 'equipment.body')
            yield data().remove(e().tag('colorings_ghast').limit(1), 'equipment.body')
            for f in armor_equipment.keys():
                yield data().remove(armor_stand,
                                    f'equipment.{f}.components.dyed_color')
            yield execute().as_(e().tag('colorings_frame')).run(
                data().remove(s(), 'Item.components.dyed_color'))
            yield execute().as_(e().tag('colorings_horse')).run(
                data().remove(s(), 'equipment.body.components.dyed_color'))
        else:
            color_name = color.name
            leather_color = {'components': {'dyed_color': color.leather}}
            sheep_nbt = {'Color': color.num, 'Sheared': False}
            bed_head = Block(f'{color.id}_bed', {'facing': NORTH, 'part': 'head'})
            yield setblock(r(-9, 2, 2), bed_head)
            yield setblock(r(-9, 2, 3), Block(f'{color.id}_bed', {'facing': NORTH, 'part': 'foot'}))
            room.particle(bed_head, 'colorings_base', r(-9, 2.75, 2), step, if_clause(plain, int(is_plain)))
            yield data().merge(e().tag('colorings_item_frame').limit(1),
                               {'Item': Item.nbt_for(f'{color.id}_dye'), 'ItemRotation': 0})
            yield data().merge(e().tag('colorings_frame_harness').limit(1),
                               {'Item': Item.nbt_for(f'{color.id}_harness'), 'ItemRotation': 0})
            bundle = Item.nbt_for(f'{color.id}_bundle')
            yield data().merge(armor_stand, {
                'equipment': {'feet': leather_color, 'legs': leather_color, 'chest': leather_color,
                              'head': leather_color}})
            yield execute().as_(e().tag('colorings_frame')).run(data().merge(s(), {'Item': leather_color}))
            for w in 'horse', 'dog':
                yield data().merge(e().tag(f'colorings_{w}').limit(1), {'equipment': {'body': leather_color}})
            for w in 'cat', 'dog':
                yield data().merge(e().tag(f'colorings_{w}').limit(1), {'CollarColor': color.num})
            yield data().modify(e().tag('colorings_llama').limit(1), 'equipment.body').set().value(
                {'id': color.id + '_carpet'})
            yield data().modify(e().tag('colorings_ghast').limit(1), 'equipment.body').set().value(
                {'id': color.id + '_harness'})

        yield data().merge(n().tag('colorings_bundle_frame'), {'Item': bundle, 'ItemRotation': 0})
        yield data().merge(e().tag('colorings_sheep').limit(1), sheep_nbt)

        yield Sign.change(r(-4, 2, 4), (None, color_name))
        yield Sign.change(r(1, 2, -0), (color_name,))
        yield execute().as_(e().tag('colorings_names')).run(data().merge(s(), {'CustomName': color_name}))
        yield data().merge(r(0, 0, -1), {'name': f'restworld:{"plain" if is_plain else color.id}_terra'})

    def colored_signs(color, render):
        signables = info.woods + stems
        for w, wood in enumerate(signables):
            row_len = 4
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
            data().merge(r(x, y, z),
                         {'front_text': {'has_glowing_text': False}, 'back_text': {'has_glowing_text': False}}))
        yield execute().if_().score(lit_signs).matches(1).run(
            data().merge(r(x, y, z),
                         {'front_text': {'has_glowing_text': True}, 'back_text': {'has_glowing_text': True}}))

    def render_signs(x, y, z, color, _):
        yield Sign.change(r(x, y, z), (None, None, color.name), front=None)
        yield data().merge(r(x, y, z), {'front_text': {'color': color.id}, 'back_text': {'color': color.id}})

    enchanted = room.score('enchanted')

    def colorings_loop(step):
        yield from colorings(False, step.elem, step)
        yield from colored_signs(step.elem, render_signs)
        yield from enchant(enchanted, 'colorings_enchantable')

    mob_nbt = {'Time': True, 'NoAI': True, 'Silent': True}
    horse_nbt = Nbt({
        'Variant': 5, 'Tags': ['colorings_horse', 'colorings_item', 'colorings_names', 'colorings_enchantable'],
        'equipment': {'body': Item.nbt_for('leather_horse_armor')}, 'Rotation': [-25, 0]}).merge(mob_nbt)
    dog_nbt = Nbt(
        {'Owner': 'dummy', 'Tags': ['colorings_dog', 'colorings_item', 'colorings_enchantable'],
         'Rotation': [-65, 0]}).merge(mob_nbt)
    wolf_armor_nbt = Nbt({'equipment': {'body': Item.nbt_for('wolf_armor')}})
    cat_nbt = Nbt(
        {'variant': 'persian', 'Owner': 'dummy', 'Tags': ['colorings_cat', 'colorings_item'], 'ColorColor': 3,
         'Rotation': [110, 0]}).merge(mob_nbt)
    llama_nbt = Nbt(
        {'Tags': ['colorings_llama', 'colorings_item', 'colorings_names', 'colorings_enchantable'], 'Variant': 1,
         'Rotation': [20, 0], 'Leashed': True}).merge(mob_nbt)
    sheep_nbt = Nbt(
        {'Tags': ['colorings_sheep', 'colorings_item'], 'Variant': 1, 'Rotation': [-35, 0], 'Leashed': True}).merge(
        mob_nbt)
    ghast_nbt = Nbt(
        {'Tags': ['colorings_ghast', 'colorings_item', 'colorings_enchantable'], 'Rotation': [55, 0],
         'equipment': {'body': Item.nbt_for('white_harness')}}).merge(
        mob_nbt)
    stand_nbt = {'Tags': ['colorings_armor_stand', 'colorings_item', 'colorings_enchantable'], 'Rotation': [30, 0],
                 'equipment': {}}
    for place, piece in armor_equipment.items():
        stand_nbt['equipment'][place] = Item.nbt_for(f'leather_{piece}')
    armor_frames = {
        'harness': r(-2.5, 4, 0.5),
        'wolf_armor': r(-8, 4, 1),
        'leather_boots': r(0, 2, 1),
        'leather_leggings': r(0, 3, 1),
        'leather_chestplate': r(0, 4, 1),
        'leather_helmet': r(0, 5, 1),
        'leather_horse_armor': r(1, 5, 1),
    }

    def colored_signs_init(x, y, z, _, wood):
        sign = Sign((wood.name, 'Sign With', 'Default', 'Text'), wood=wood.id, front=None)
        room.particle(sign, 'colorings_base', r(x, y + 1, z), clause=if_clause(plain, 0))
        yield sign.place(r(x, y, z), 14)

    wolf_armor_on = room.function('wolf_armor_on', home=False).add(
        data().merge(n().tag('colorings_dog'), wolf_armor_nbt),
        execute().at(e().tag('colorings_home')).run(function('restworld:blocks/colorings_cur')))
    room.function('wolf_armor_off', home=False).add(
        data().remove(n().tag('colorings_dog'), 'equipment.body'),
        execute().at(e().tag('colorings_home')).run(function('restworld:blocks/colorings_cur')))
    rider_count = 'rider_count'
    room.function('colorings_init').add(
        kill_em(e().tag('colorings_item')),
        plain.set(0),
        Entity('item_frame', {
            'Facing': 3, 'Tags': ['colorings_item_frame', 'colorings_item'],
            'Fixed': True}).summon(r(-4.5, 4, 0.5)),
        Entity('item_frame', {
            'Facing': 3, 'Tags': ['colorings_item', 'colorings_bundle_frame'],
            'Fixed': True}).summon(r(-6.5, 4, 0.5)),
        Entity('horse', horse_nbt).summon(r(0.9, 2, 5.3)),
        Entity('wolf', dog_nbt).summon(r(-7.4, 2, 2)),
        function(wolf_armor_on),
        Entity('cat', cat_nbt).summon(r(-2.7, 2, 2)),
        Entity('armor_stand', stand_nbt).summon(r(-1.1, 2, 3)),
        Entity('llama', llama_nbt).summon(r(-11, 2, 5.8)),
        Entity('sheep', sheep_nbt).summon(r(-9.0, 2, 5.0)),
        Entity('happy_ghast', ghast_nbt).summon(r(-5.5, 5.3, -2.0)),
        (armor_frame(k, v) for k, v in armor_frames.items()),
        execute().as_(e().tag('colorings_names')).run(
            data().merge(s(), {'CustomNameVisible': True})),
        WallSign((None, 'Terracotta')).place(r(-1, 3, 1), SOUTH),
        WallSign((None, 'Harness')).place(r(-2, 3, 1), SOUTH),
        WallSign((None, 'Shulker Box')).place(r(-3, 3, 1), SOUTH),
        WallSign((None, 'Dye')).place(r(-4, 3, 1, ), SOUTH),
        WallSign((None, 'Concrete')).place(r(-5, 3, 1), SOUTH),
        WallSign((None, 'Bundle')).place(r(-6, 3, 1), SOUTH),
        WallSign((None, 'Glass')).place(r(-7, 3, 1), SOUTH),
        colored_signs(None, colored_signs_init),
        WallSign([]).place(r(-4, 2, 4, ), SOUTH), kill(e().type('item')),
        room.label(r(-1, 2, 7), 'Lit Candles', SOUTH),
        room.label(r(-3, 2, 7), 'Enchanted', SOUTH),
        room.label(r(-7, 2, 7), 'Plain', SOUTH),
        room.label(r(-9, 2, 7), 'Ghast Riders', SOUTH),
        room.label(r(-9, 2, 6.85), '0', SOUTH, tags=rider_count),
        room.label(r(-11, 2, 3), 'Glowing', SOUTH),
        room.label(r(-8, 2, 3), 'Collar', SOUTH),
        room.label(r(0, 2, 3), 'Leggings', SOUTH),
    )
    room.loop('colorings', main_clock).add(erase(r(-9, 2, 2), r(-9, 2, 3))).loop(colorings_loop, colors).add(
        colored_signs(None, render_signs_glow))
    room.function('riders_on', home=False).add(room.rider_on(e().tag('saddle', 'adult')))
    room.function('riders_off', home=False).add(room.rider_off())
    ghast = n().tag('colorings_ghast')
    rider_on = room.function('colorings_ghasts_rider_on', home=False).add(room.rider_on(ghast))
    rider_off = room.function('colorings_ghasts_rider_off', home=False).add(room.rider_off())

    def show_rider_count(count):
        return data().modify(n().tag(rider_count), 'text').set().value(f'{count}')

    ghast_full = room.score('ghast_full')
    room.function('colorings_ghasts_riders', home=False).add(
        execute().store(SUCCESS).score(ghast_full).run(data().get(n().tag('colorings_ghast'), 'Passengers[3]')),
        execute().if_().score(ghast_full).matches(0).run(function(rider_on)),
        execute().unless().score(ghast_full).matches(0).run(function(rider_off)),
        show_rider_count(0),
        execute().if_().data(ghast, 'Passengers[0]').run(show_rider_count(1)),
        execute().if_().data(ghast, 'Passengers[1]').run(show_rider_count(2)),
        execute().if_().data(ghast, 'Passengers[2]').run(show_rider_count(3)),
        execute().if_().data(ghast, 'Passengers[3]').run(show_rider_count(4)),
    )
    store_start = (coloring_coords[0][0], coloring_coords[0][1].value - coloring_coords[1][1].value + 1,
                   coloring_coords[0][2])
    store_end = (coloring_coords[1][0], 0, coloring_coords[1][2])
    top_start = (coloring_coords[0][0], coloring_coords[0][1], coloring_coords[0][2])
    top_end = (coloring_coords[1][0], coloring_coords[1][1] - 1, coloring_coords[1][2])
    room.function('colorings_plain_off', home=False).add(
        execute().unless().score(plain).matches(0).run(
            # These create particle explosions, and there is no negative "#!wall_signs" filter for clone
            fill(store_start, store_end, 'air').replace('#wall_signs'),
            clone(store_start, store_end, top_end)),
        plain.set(0),
        tag(e().tag('colorings_base_home')).add('colorings_home'),
        execute().at(e().tag('colorings_home')).run(function('restworld:blocks/colorings_init')),
        kill(e().type('item').distance((None, 20))))
    room.function('colorings_plain_on', home=False).add(
        execute().if_().score(plain).matches(0).run(clone(top_start, top_end, store_end)),
        plain.set(1),
        tag(e().tag('colorings_base_home')).remove('colorings_home'),
        data().remove(n().tag('colorings_item_frame'), 'Item'),
        data().remove(n().tag('colorings_frame_harness'), 'Item'),
        colorings(True, Color('Plain', 0x0)), setblock(r(-7, -1, 3), 'redstone_torch'), setblock(r(-7, -1, 3), 'air'),
        kill(e().type('item').distance((None, 20))))
    room.functions['colorings_home'].add(tag(e().tag('colorings_home')).add('colorings_base_home'))
    room.function('colorings_enter').add(
        execute().as_(e().tag('colorings_names')).run(data().merge(s(), {'CustomNameVisible': True})))
    room.function('colorings_exit').add(
        execute().as_(e().tag('colorings_names')).run(data().merge(s(), {'CustomNameVisible': False})))
    room.function('colored_beam_enter').add(setblock(r(0, 1, 0), 'iron_block'))
    room.function('colored_beam_exit').add(setblock(r(0, 1, 0), 'white_concrete'))
    room.function('colored_leggings_start', home=False).add(data().remove(armor_stand, 'equipment.chest'))
    room.function('colored_leggings_stop', home=False).add(
        data().modify(armor_stand, 'equipment.chest').set().value(
            Item.nbt_for('leather_chestplate')),
        data().modify(armor_stand, 'equipment.chest.components').set().from_(
            e().tag('colorings_armor_stand').limit(1), 'equipment.legs.components')
    )


# Expansion is complex.
#
# Most blocks are expandable, so the blocks() function marks their 'homer' armor stand with 'expansion' by default in its
# _init function.
#
# During the _init phase, every expanding homer modifies its sign to toggle expansion when tapped. Non-expanding
# homers modify the sign to say 'Sorry' when tapped.
#
# Toggling actual expansion for a single target is in toggle_expand_at. It places or removes the 'expander' tag on
# the homer, and runs either the expander or contracter function as itself to give the immediate effect.
#
# Expanding or contracting "all"" simply runs this script on all expanding homers.
#
# Homers that handle multiple blocks are helped by 'just_expand' armor stands under the blocks it manages. These
# are expander homers that do nothing but the expansion work for the blocks above them. So if homer X puts up
# blocks X and Y, a regular homer will be under X and a 'just_expand' homer will be under Y.
#
# On each main tick, the 'expansion' function is run at every 'expander' during the 'main_finish' phase. This keeps the
# block expanded as it changes.
def expansion_functions(room):
    expand_all = room.function('expand_all', home=False)
    contract_all = room.function('contract_all', home=False)
    room.function('toggle_expand', home=False).add(
        execute().positioned(r(0, -2, -1)).run(function('restworld:blocks/toggle_expand_at')),
        execute().positioned(r(0, -2, 1)).run(function('restworld:blocks/toggle_expand_at')))
    room.function('toggle_expand_at', home=False).add(
        execute().as_(e().tag('expander').distance((None, 1))).run(tag(s()).add('stop_expanding')),
        execute().as_(e().tag('!expander', 'expansion').distance((None, 1))).run(tag(s()).add('expander')),
        execute().as_(e().tag('stop_expanding').distance((None, 1))).run(tag(s()).remove('expander')),
        execute().as_(e().tag('stop_expanding').distance((None, 1))).run(tag(s()).remove('stop_expanding')),
        execute().at(e().tag('expander').distance((None, 1))).run(function('restworld:blocks/expander')),
        execute().at(e().tag('!expander', 'expansion').distance((None, 1))).run(
            function('restworld:blocks/contracter')),
        execute().at(e().tag('!expansion').distance((None, 1))).run(say('Sorry, cannot expand this.')),
        execute().at(e().tag('!expansion', 'fire_home').distance((None, 1))).run(say('Sorry, cannot expand this.')))
    room.function('expander').add(
        execute().if_().entity(e().tag('fire_home').distance((None, 1))).run(function('restworld:blocks/expand_fire')),
        execute().if_().entity(e().tag('dripstone_home').distance((None, 1))).run(
            function('restworld:blocks/expand_dripstone')),
        execute().unless().entity(e().tag('fire_home').distance((None, 1))).unless().entity(
            e().tag('dripstone_home').distance((None, 1))).run(function('restworld:blocks/expand_generic')))
    expand_all.add(execute().as_(e().tag('blocks_home', 'expansion', '!expander')).run(
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
    room.function('expand_generic', home=False).add(
        execute().if_().block(r(0, 3, 0), '#restworld:falling').run(
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
    contract_all.add(
        execute().as_(e().tag('blocks_home', 'expansion', 'expander')).run(
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

    # This is used for blocks that are changed, but by a different command block than the one under it. These want to
    # be expanded as they change,
    room.function('just_expand_home', home=False).add(
        kill(e().tag('just_expand_home').distance((None, 2))),
        summon('armor_stand', r(0, 0.5, 0),
               {'Tags': ['just_expand_home', 'homer', 'blocks_home', 'expansion'], 'NoGravity': True, 'Small': True}))
    # ... and this is like just_expand_home, but it doesn't expand.
    room.function('dont_expand_home', home=False).add(
        kill(e().tag('dont_expand_home').distance((None, 2))),
        summon('armor_stand', r(0, 0.5, 0),
               {'Tags': ['dont_expand_home', 'homer', 'blocks_home'], 'NoGravity': True, 'Small': True}))


def stepable_functions(room):
    def stepable_loop(step):
        volume = Region(r(0, 2, 0), r(3, 6, 6))
        i = step.i
        yield volume.replace(step.elem, '#restworld:stepable_planks')
        yield volume.replace_slabs(slabs[i], '#restworld:stepable_slabs')
        yield volume.replace_stairs(stairs[i], '#restworld:stepable_stairs')
        sign_text = Sign.lines_nbt(Block(step.elem).full_text)
        yield data().merge(r(1, 2, -1), {'front_text': sign_text})
        room.particle(step.elem, 'stepable', r(0, 4, 0), step)

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
        'Exposed|Cut Copper',
        'Weathered|Cut Copper',
        'Oxidized|Cut Copper',
        'Resin Bricks',
        'Prismarine', 'Prismarine|Bricks', 'Dark|Prismarine',
        'Acacia Planks', 'Birch Planks', 'Cherry Planks', 'Jungle Planks', 'Mangrove Planks',
        'Oak Planks', 'Dark Oak Planks', 'Pale Oak Planks', 'Spruce Planks', 'Bamboo Planks', 'Bamboo Mosaic Block',
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
