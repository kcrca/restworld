from __future__ import annotations

from pyker.commands import NORTH, r, Block, mc, e
from pyker.simpler import WallSign
from restworld.rooms import Room
from restworld.world import restworld


def room():
    room = Room('paintings', restworld, NORTH, (None, 'Paintings'))

    def painting(id, facing, x, z, sx=0, sy=0, sz=0, note=''):
        thing = Block(id)
        px, pz = ((-1, 0), (0, -1), (1, 0), (0, 1))[facing]
        px += sx
        pz += sz
        dir = ('south', 'west', 'north', 'east')[facing]
        yield mc.summon('painting', r(x, 3, z), {'variant': thing.id, 'facing': facing, 'Tags': ['painting']})
        yield WallSign((None, thing.display_name, note)).place(r(x + px, 2 + sy, z + pz), dir)

    room.function('all_paintings_init').add(
        mc.kill(e().tag('painting')),
        mc.fill(r(-2, 2, 0), r(16, 6, 22), 'air').replace('oak_wall_sign'),

        painting('Burning Skull', 0, 0, 0, sx=-1),
        painting('Pointer', 0, 11, 0, sx=4, sy=1),

        painting('Skull and Roses', 1, 14, 2),
        painting('Bust', 1, 14, 5),
        painting('Void', 1, 14, 8),
        painting('Match', 1, 14, 11),
        painting('Stage', 1, 14, 14),
        painting('Wither', 1, 14, 17),

        painting('Pigscene', 2, 12, 20, sx=1),
        painting('Earth', 2, 8, 20, note='(unused)'),
        painting('Wind', 2, 5, 20, note='(unused)'),
        painting('Graham', 2, 1, 20),
        painting('Wanderer', 2, -1, 20),

        painting('Fighters', 3, -2, 16, sz=1),
        painting('Donkey Kong', 3, -2, 10, sz=1),
        painting('Skeleton', 3, -2, 4, sz=1),

        painting('Wasteland', 2, 4, 4),
        painting('Kebab', 2, 6, 4),
        painting('Alban', 2, 8, 4),
        painting('Bomb', 0, 9, 6),
        painting('Plant', 0, 7, 6),
        painting('Sunset', 0, 4, 6),

        painting('Creebet', 2, 5, 9),
        painting('Courbet', 2, 8, 9),
        painting('Pool', 0, 7, 11),
        painting('Sea', 0, 4, 11),

        painting('Aztec2', 2, 4, 14),
        painting('Aztec', 2, 7, 14),
        painting('Water', 0, 4, 16, note='(unused)'),
        painting('Fire', 0, 7, 16, note='(unused)')
    )
