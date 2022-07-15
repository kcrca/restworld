from __future__ import annotations

from pynecraft.base import EAST, NORTH, SOUTH, WEST, r
from pynecraft.commands import clone, e, execute, fill
from pynecraft.simpler import WallSign
from restworld.rooms import Room, label
from restworld.world import restworld


def room():
    room = Room('connect', restworld)

    def connect(src, sx, sz):
        for x in range(-12, 13):
            for y in range(0, 5):
                for z in range(-12, 13):
                    yield execute().at(e().tag('connect_mid_home')).if_(
                    ).block(r(x, -9 + y, z), src).run(clone(r(sx, 1, sz), r(sx, 1, sz), r(x, 2 + y, z)))

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

    room.function('connect_e', home=False).add(connect('redstone_ore', 1, 0))
    room.function('connect_n', home=False).add(connect('grass_block', 0, -1))
    room.function('connect_ne', home=False).add(connect('cobblestone', 1, -1))
    room.function('connect_nw', home=False).add(connect('dripstone_block', -1, -1))
    room.function('connect_s', home=False).add(connect('diamond_block', 0, 1))
    room.function('connect_se', home=False).add(connect('stone', 1, 1))
    room.function('connect_sw', home=False).add(connect('magenta_wool', -1, 1))
    room.function('connect_w', home=False).add(connect('diorite', -1, 0))
