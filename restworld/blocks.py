from __future__ import annotations

from typing import Iterable

from pyker.commands import EAST, r, mc, entity, Entity, facing_info, good_block, Block, NORTH, SOUTH
from pyker.simpler import Sign
from restworld.rooms import Room, label, woods, stems
from restworld.world import restworld, main_clock


def room():
    room = Room('blocks', restworld, EAST, ('Blocks,', 'Paintings,', 'Banners,', 'DIY'))

    block_list_score = room.score('block_list')

    name_stand = Entity('armor_stand', nbt={'Invisible': True, 'NoGravity': True, 'CustomNameVisible': True})
    name_stand.tag('block_list')
    all_names = room.function('all_names', needs_home=False)

    def blocks(name, block_lists: Iterable[Block, str] | Iterable[Iterable[Block, str]], facing, dx=0, dz=0, size=0,
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
        block_init = room.function(name + '_init').add(
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

    room.functions['blocks_room_init'].add(
        label(r(-16, 2, 3), 'List Blocks'),
        label(r(-16, 2, -3), 'List Blocks'),
        label(r(-43, 2, 3), 'List Blocks'),
        label(r(-43, 2, -3), 'List Blocks'),
        mc.kill(entity().tag('block_list'))
    )

    for f in ('amethyst',):
        room.function(f + '_init').add(mc.tag(entity().tag(f + '_Home')).add('no_expansion'))

    amethyst_phases = (
        'Amethyst Block', 'Budding Amethyst', 'Small Amethyst|Bud', 'Medium Amethyst|Bud', 'Large Amethyst|Bud',
        'Amethyst Cluster')
    # room.loop('amethyst', main_clock).add(mc.fill(r(-1, 3, -1), r(1, 5, 1), 'air')).loop(amethyst_loop,
    #                                                                                      amethyst_phases).add(
    #     mc.kill(entity().type('item').nbt(Item.nbt('amethyst_shard'))))
    blocks('cobble', ("Cobblestone", "Mossy|Cobblestone", "Cobbled|Deepslate"), NORTH)

    woodlike = woods + stems
    leaves = ["%s Leaves" % x for x in woods] + ["Warped Wart Block", "Nether Wart Block"]
    logs = ["%s Log" % x for x in woods] + [("%s Stem" % x) for x in stems]
    wood = ["%s Wood" % x for x in woods] + [("%s Hyphae" % x) for x in stems]
    stripped_logs = ["Stripped|%s Log" % x for x in woods] + [("Stripped|%s Stem" % x) for x in stems]
    stripped_woods = ["Stripped|%s Wood" % x for x in woods] + [("Stripped|%s Hyphae" % x) for x in stems]
    blocks('wood_blocks',
           (tuple("%s Planks" % f for f in woodlike),
            stripped_logs,
            logs,
            wood,
            leaves,
            stripped_woods), SOUTH,
           dx=-3, dz=-3, size=2)
