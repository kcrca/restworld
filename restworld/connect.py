from __future__ import annotations

from pynecraft.__init__ import EAST, NORTH, SOUTH, WEST, r
from pynecraft.commands import MOVE, clone, fill, function
from pynecraft.simpler import WallSign
from restworld.rooms import Room, label
from restworld.world import restworld


# There is no way to fill in a block that is named at runtime. There is also no way to filter a clone for everything
# _except_ a certain value. So when the user puts in a sampler block for (say) the SE position...
#
# (1) We fill up a 'workspace' region of space with the sampler block by successive cloning of the block the user
# placed.
#
# (2) We know that for any given position, there is one block in the pattern space below the area that corresponds to
# it. For SE, that is 'stone'. So we clear out a 'source' area with air, and clone the downstairs area filtered on that
# block. So now the source area is that block plus air everywhere else.
#
# (3) We clone 'source' area into the workspace filtered on 'air'. All the sampler blocks in the workspace are thus
# replaced by air, except those that are the original pattern block. So now thw the workspace is only the sampler block
# in the shape of the pattern block.
#
# (4) We then copy the workspace to the main area using a masked copy, which copies everything but the air; that is, it
# copies the pattern-block-shaped set of sampler blocks.

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

        WallSign(below1).place(r(0, -8, 2), SOUTH),
        WallSign(below1).place(r(0, -8, -2), NORTH),
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

    # The function that spreads out the user's sample block into the workspace. This is invoked by the direction-specific
    # functions.
    spread_height = 15
    spread_start = r(0, spread_height, 0)

    def spread_func():
        def needed(value, largest):
            if value * 2 < largest:
                return value - 1
            else:
                return largest - value - 1

        x = 1
        while x < 25:
            yield clone(spread_start, r(needed(x, 25), spread_height, 0), r(x, spread_height, 0))
            x *= 2
        z = 1
        while z < 25:
            yield clone(r(25, spread_height, 0), r(0, spread_height, needed(z, 25)), r(0, spread_height, z))
            z *= 2
        y = 1
        while y < 5:
            yield clone(r(25, spread_height, 25), r(0, spread_height + needed(y, 5), 0), r(0, spread_height + y, 0))
            y *= 2
        # Fill the source with air so the direction-specific code that invoked this will start with a clean area.
        yield fill(r(13, -14, 13), r(-12, -19, -12), 'air')

    spread = room.function('spread_source').add(spread_func())

    # This generates the function for a specific direction.
    def connect_func(dir, sx, sz):
        room.function(f'connect_{dir}', home=False).add(
            fill(r(0, spread_height, 0), r(25, spread_height + 5, 25), 'air'),
            clone(r(sx, 1, sz), r(sx, 1, sz), spread_start),
            function(spread),
            clone(r(13, -4, 13), r(-12, -9, -12), r(-12, -19, -12)).filtered(block_map[dir]),
            clone(r(13, -14, 13), r(-12, -19, -12), spread_start).filtered('air'),
            clone(r(25, spread_height + 5, 25), spread_start, r(-12, 2, -12)).masked(MOVE),
        )

    # Generate each direction-specific function
    connect_func('e', 1, 0)
    connect_func('n', 0, -1)
    connect_func('ne', 1, -1)
    connect_func('nw', -1, -1)
    connect_func('s', 0, 1)
    connect_func('se', 1, 1)
    connect_func('sw', -1, 1)
    connect_func('w', -1, 0)
