from __future__ import annotations

from pynecraft.base import Arg, EAST, NORTH, SOUTH, WEST, as_facing, r
from pynecraft.commands import clone, data, e, execute, fill, function, loot
from pynecraft.simpler import Item, WallSign
from restworld.rooms import Room, label
from restworld.world import restworld


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
        fill(r(size, -15, size), r(0, -19, 0), Arg('to')).replace(Arg('from')),
        clone(r(size, -15, size), r(0, -19, 0), r(0, 2, 0)).filtered(Arg('to')),
    )

    mid = e().tag('connect_mid_home').limit(1)
    miner = Item('iron_pickaxe', nbt={'Enchantments': [{'lvl': 1, 'id': "silk_touch"}]})
    center = r(13, 1, 13)

    def redo_one_example(dir):
        facing = as_facing(dir)
        yield execute().positioned(center).run(
            loot().replace().entity(mid, 'armor.head').mine(r(*facing.block_delta), miner))
        yield data().modify('redo', 'to').set().from_(mid, 'ArmorItems[3].id')
        yield data().modify('redo', 'from').set().value(block_map[dir])
        yield function(redo_one).with_().storage('redo')

    redo_run = room.function('redo_run', home=False)
    clear_below = fill(r(size, -15, size), r(0, -19, 0), 'air')
    for dir in block_map:
        redo_run.add(
            clear_below,
            clone(r(size, -5, size), r(0, -9, 0), r(0, -19, 0)).filtered(block_map[dir]),
            redo_one_example(dir)
        )
    redo_run.add(clear_below)
    
    room.function('redo').add(
        execute().unless().block(r(0, 3, 0), 'air').at(e().tag('redo_home')).run(function(redo_run)))
