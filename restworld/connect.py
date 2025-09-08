from __future__ import annotations

from pynecraft.base import Arg, E, EAST, N, NE, NORTH, NW, S, SE, SOUTH, SW, UP, W, WEST, as_facing, r
from pynecraft.commands import SUCCESS, clone, data, e, execute, fill, function, kill, n, setblock
from pynecraft.simpler import ItemFrame, WallSign
from restworld.rooms import Room
from restworld.world import restworld


# Replacements are done in a multistep process using macros. When a new block is placed in one of the 'fill' spots,
# a function is run that, for each of the eight directions...
#
# (1) clears out the working area below the lower level.
# (2) copies all the exemplar blocks for that direction into the lower level (and nothing else)
# (3) Gets the ID of the block in the frame that's that direction from the middle.
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
    room.reset_at((-10, 0), facing=EAST)

    room.function('connect_room_init', exists_ok=True).add(room.label(r(8, 2, 0), 'Go Home', NORTH))

    above = ('Change a block', 'in an item frame', 'to change the', 'block used')
    below1 = ('These blocks are', 'templates for the', 'blocks above')
    below2 = ('Change them, then', 'change a "type"', 'block in the', 'floor above.')

    # The pattern block for each direction.
    block_map = {
        E: {'orig': 'redstone_ore'},
        N: {'orig': 'grass_block'},
        NE: {'orig': 'cobblestone'},
        NW: {'orig': 'dripstone_block'},
        S: {'orig': 'diamond_block'},
        SE: {'orig': 'stone'},
        SW: {'orig': 'magenta_wool'},
        W: {'orig': 'diorite'},
    }
    for k in block_map:
        block_map[k]['to'] = block_map[k]['orig']

    init = room.function('copy_connected_init').add(kill(e().tag('connect_frame')))
    for dir, v in block_map.items():
        if v['to'].startswith('redstone'):
            v['to'] = 'glass'
        frame = ItemFrame(UP).item(v['to']).tag('connect_frame', f'connect_frame_{dir}').fixed(False)
        init.add(execute().positioned(r(0, 2, 0)).run(frame.summon(r(*as_facing(dir).block_delta))))
    init.add(
        data().modify(room.store, 'cur').set().value(block_map),
        WallSign(above).place(r(0, 2, 2), NORTH),
        WallSign(above).place(r(0, 2, -2), SOUTH),
        WallSign(('Connected', 'Textures', '(needs OptiFine)')).place(r(2, 2, 0), WEST),
        WallSign(('Connected', 'Textures', '(needs OptiFine)')).place(r(-2, 2, 0), EAST),

        fill(r(2, -8, 2), r(-2, -9, -2), 'air'),

        WallSign(below1).back((None, '⇧', 'Go Up')).place(r(0, -8, 2), SOUTH),
        WallSign(below1).back((None, '⇧', 'Go Up')).place(r(0, -8, -2), NORTH),
        WallSign().messages(below1).place(r(2, -8, 0), EAST),
        WallSign().messages(below1).place(r(-2, -8, 0), WEST),
        WallSign(below2).place(r(0, -9, 2), SOUTH),
        WallSign(below2).place(r(0, -9, -2), NORTH),
        WallSign().messages(below2).place(r(2, -9, 0), EAST),
        WallSign().messages(below2).place(r(-2, -9, 0), WEST),

        room.label(r(0, 2, 0), 'Go Home', NORTH),
    )
    room.function('copy_connected_enter').add(setblock(r(0, -3, 0), 'redstone_block'))
    room.function('copy_connected_exit').add(setblock(r(0, -3, 0), 'air'))

    size = 26
    clear_below = fill(r(size, -15, size), r(0, -19, 0), 'air')
    redo_one = room.function('redo_one', home=False).add(
        clear_below,
        setblock(r(0, -20, 0), 'stone'),
        clone(r(size, -5, size), r(0, -9, 0), r(0, -19, 0)).filtered(Arg('orig')),
        fill(r(size, -15, size), r(0, -19, 0), Arg('to')).replace(Arg('orig')),
        fill(r(size, 2, size), r(0, 6, 0), 'air').replace(Arg('from')),
        clone(r(size, -15, size), r(0, -19, 0), r(0, 2, 0)).filtered(Arg('to')),
        clear_below,
    )

    changed = room.score('changed')
    monitor = room.function('copy_connected').add(
        data().modify(room.store, 'prev').set().from_(room.store, 'cur'))
    for dir in block_map:
        monitor.add(
            execute().store(SUCCESS).score(changed).run(
                data().modify(room.store, f'cur.{dir}.to').set().from_(
                    n().tag(f'connect_frame_{dir}'), 'Item.id')),
            execute().if_().score(changed).matches(1).run(
                data().modify(room.store, f'cur.{dir}.from').set().from_(room.store, f'prev.{dir}.to'),
                execute().at(e().tag('redo_home')).run(function(redo_one).with_().storage(room.store, f'cur.{dir}'))
            )
        )

