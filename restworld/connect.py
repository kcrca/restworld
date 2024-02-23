from __future__ import annotations

from pynecraft.base import Arg, EAST, NORTH, RelCoord, SOUTH, UP, WEST, as_facing, r
from pynecraft.commands import clone, data, e, execute, fill, function, kill, return_, s, say
from pynecraft.simpler import ItemFrame, WallSign
from pynecraft.utils import strcmp, utils_init
from restworld.rooms import Room, label
from restworld.world import fast_clock, restworld


# Replacements are done in a multistep process using macros. When a new block is placed in one of the 'fill' spots,
# a function is run that, for each of the eight directions...
#
# (1) clears out the working area below the lower level.
# (2) copies all the exemplar blocks for that direction into the lower level (and nothing else)
# (3) Gets the ID of the block in that direction from the middle. (The hack is to do this is commented.)
# (4) Puts that ID, and that of the example block into a storage area
# (5) Invokes a function with that storage area as the incoming parameters.
# (6) That function fills the cloned blocks with the replacement block
# (7) ... and then clones the resulting blocks to the play area
#
# This must be done on the side to avoid problems when one of the fill blocks is the same as one of the exemplar blocks.
#
# We could just do the one replaced block, but this mechanism repairs any damage anywhere else, plus adapts to any
# changes made to the blow area since the last fill. Plus it just ain't that expensive.


def room():
    room = Room('connect', restworld, EAST, (None, 'Connected', 'Textures', '(Optifine)'),
                room_name='Connected Textures')

    room.function('connect_room_init', exists_ok=True).add(label(r(8, 2, 0), 'Go Home'))

    above = ('Change the block', 'in the floor', 'to change the', 'block used')
    below1 = ('These blocks are', 'templates for the', 'blocks above')
    below2 = ('Change them, then', 'change a "type"', 'block in the', 'floor above.')

    room.function('connect_mid_init').add(
        utils_init(),
        WallSign(above).place(r(0, 2, 2), NORTH),
        WallSign(above).place(r(0, 2, -2), SOUTH),
        WallSign(('Connected', 'Textures', '(needs OptiFine)')).place(r(2, 2, 0), WEST),
        WallSign(('Connected', 'Textures', '(needs OptiFine)')).place(r(-2, 2, 0), EAST),

        fill(r(2, -8, 2), r(-2, -9, -2), 'air'),

        WallSign(below1).back((None, '⇧', 'Go Up')).place(r(0, -8, 2), SOUTH),
        WallSign(below1).back((None, '⇧', 'Go Up')).place(r(0, -8, -2), NORTH),
        WallSign(below1).place(r(2, -8, 0), EAST),
        WallSign(below1).place(r(-2, -8, 0), WEST),
        WallSign(below2).place(r(0, -9, 2), SOUTH),
        WallSign(below2).place(r(0, -9, -2), NORTH),
        WallSign(below2).place(r(2, -9, 0), EAST),
        WallSign(below2).place(r(-2, -9, 0), WEST),

        label(r(0, 2, 0), 'Go Home'),
    )

    # The pattern block for each direction.
    block_map = {
        'e': 'redstone_ore',
        'n': 'grass_block',
        'ne': 'cobblestone',
        'nw': 'dripstone_block',
        's': 'diamond_block',
        'se': 'stone',
        'sw': 'magenta_wool',
        'w': 'diorite',
    }

    size = 26
    redo_one = room.function('redo_one', home=False).add(
        say('$(from) -> $(to)'),
        fill(r(size, -15, size), r(0, -19, 0), Arg('to')).replace(Arg('from')),
        clone(r(size, -15, size), r(0, -19, 0), r(0, 2, 0)).filtered(Arg('to')),
    )

    center = r(13, 1, 13)

    def redo_one_example(dir):
        yield data().modify('redo', 'to').set().from_(e().tag(f'redo_frame_{dir}').limit(1), 'Item.id')
        yield data().modify('redo', 'from').set().value(block_map[dir])
        yield function(redo_one).with_().storage('redo')

    # check_one = room.function('check_one').add(
    #     say('prev: $(prev), dir: $(dir)'),
    #     execute().unless().data('redo', '{$(dir).cur: $(prev)').run(filled.set(1))
    # )
    #
    # redo = room.function('redo')
    # for dir, v in block_map.items():
    #     redo.add(
    #         data().modify('redo', f'{dir}.cur').set().from_(e().tag(f'redo_frame_{dir}').limit(1), 'Item.id'),
    #         data().modify('redo', 'check.prev').set().from_('redo', f'{dir}.prev'),
    #         data().modify('redo', 'check.dir').set().value(dir),
    #         function(check_one).with_().storage('redo.check'),
    #     )

    init = room.function('redo_init').add(kill(e().tag('redo_frame')))
    for dir, v in block_map.items():
        frame = ItemFrame(UP).item(v).tag('redo_frame', f'redo_frame_{dir}').fixed(False)
        pos = RelCoord.add(r(*as_facing(dir).block_delta), (0, 1, 0))
        init.add(execute().positioned(center).run(frame.summon(pos)))

    concat = room.function('concat', home=False).add(
        data().modify('redo', 'concat.all').set().value('"$(all),$(add)"')
    )

    filled = room.score('filled')
    redo = room.function('redo', fast_clock).add(
        filled.set(0),
        execute().as_(e().tag('redo_frame').nbt({'Item':{}})).run(filled.add(1)),
        execute().unless().score(filled).matches(8).run(say('empty'), return_(0)),
        data().modify('redo', 'prev').set().from_('redo', 'cur'),
        data().modify('redo', 'concat.all').set().value(''),
    )

    for dir in block_map:
        redo.add(
            data().modify('redo', 'concat.add').set().from_(e().tag(f'redo_frame_{dir}').limit(1), 'Item.id'),
            function(concat).with_().storage('redo', 'concat'),
        )

    redo.add(
        data().modify('redo', 'cur').set().from_('redo', 'concat.all'),
        strcmp(('redo', 'prev'), ('redo', 'cur')),
        # execute().if_().score(Scores.strcmp).matches(0).run(say('same'), return_(0)),
        say('redo'),
    )

    clear_below = fill(r(size, -15, size), r(0, -19, 0), 'air')
    for dir in block_map:
        redo.add(
            clear_below,
            clone(r(size, -5, size), r(0, -9, 0), r(0, -19, 0)).filtered(block_map[dir]),
            redo_one_example(dir)
        )
    redo.add(clear_below)

    append_id = room.function('append_id', home=False).add(
        filled.add(1),
        data().modify('redo', 'concat.add').set().from_(s(), 'Item.id'),
        function(concat).with_().storage('redo.concat')
    )

    # redo = room.loop('redo', fast_clock).add(
    #     filled.set(0),
    #     data().modify('redo', 'concat.all').set().value(''),
    #     execute().as_(e().tag('redo_frame').sort(NEAREST)).run(function(append_id)),
    # )
    # for dir, v in block_map.items():
    #     redo.add(
    #         data().modify('redo', f'{dir}.cur').set().from_(e().tag(f'redo_frame_{dir}').limit(1), 'Item.id'),
    #         data().modify('redo', 'check.prev').set().from_('redo', f'{dir}.prev'),
    #         data().modify('redo', 'check.dir').set().value(dir),
    #         function(check_one).with_().storage('redo.check'),
    #     )
