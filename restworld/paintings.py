from __future__ import annotations

from pynecraft.base import NORTH, ROTATION_270, SOUTH, WEST, as_facing, r
from pynecraft.commands import JsonText, e, fill, kill, summon
from pynecraft.simpler import TextDisplay
from pynecraft.values import PAINTING_GROUP, paintings
from restworld.rooms import Room
from restworld.world import restworld


# noinspection SpellCheckingInspection
def room():
    room = Room('paintings', restworld, NORTH, (None, 'Paintings'))
    room.reset_at((0, 3))
    unused = set(PAINTING_GROUP)

    def wall(ids, facing, x, z):
        if isinstance(ids, str):
            ids = (ids,)
        facing = as_facing(facing)
        moving = facing.turn(ROTATION_270)
        for id in ids:
            if isinstance(id, int):
                x += id * moving.dx
                z += id * moving.dz
                continue
            thing = paintings[id]
            yield from painting(id, facing, moving, x, z)
            x += (thing.size[0] + 1) * moving.dx
            z += (thing.size[0] + 1) * moving.dz

    def painting(id, facing, moving, x, z, sx=0, sy=0, sz=0, note=''):
        thing = paintings[id]
        px, pz = (0, 0)
        y = 2 if thing.size[1] >= 4 else 3
        if thing.size[0] > 2 and thing.size[1] > 2:
            px += moving.dx
            pz += moving.dz
            y += px
        yield summon('painting', r(x + px, y, z + pz),
                     {'variant': thing.name, 'facing': facing.painting_number, 'Tags': ['painting']})
        yield summon(TextDisplay(nbt={'Rotation': facing.rotation}).scale(0.5).text(JsonText().text(thing.value)))
        # yield WallSign((None, thing.value, note)).place(r(x - moving.dx, 2, z - moving.dz), facing)
        unused.remove(thing.value)

    room.function('all_paintings_init').add(
        kill(e().tag('painting')),
        kill(e().type('item')),
        fill(r(-2, 2, 0), r(16, 6, 26), 'air').replace('oak_wall_sign'),

        wall(('Skull On Fire', 7, 'Pointer'), SOUTH, -1, 0),
        wall(('Skull and Roses', 'The void', 'The Stage Is Set', 'Wither', 'Bust', 'Match'), WEST, 14, 2),

        # painting('Pigscene', 2, 12, 26, sx=1),
        # painting('Earth', 2, 8, 26, note='(unused)'),
        # painting('Wind', 2, 5, 26, note='(unused)'),
        # painting('Graham', 2, 2, 26),
        # painting('Wanderer', 2, 0, 26),
        # painting('Prairie Ride', 2, -2, 26),
        #
        # painting('Unpacked', 3, -2, 18, sz=1),
        # painting('Fighters', 3, -2, 13, sz=1),
        # painting('Kong', 3, -2, 8, sz=1),
        # painting('Mortal Coil', 3, -2, 3, sz=1),
        #
        # painting('Wasteland', 2, 4, 4),
        # painting('Kebab med tre pepperoni', 2, 6, 4),
        # painting('Albanian', 2, 8, 4),
        # painting('Target Successfully Bombed', 0, 9, 6),
        # painting('Paradisträd', 0, 7, 6),
        # painting('sunset_dense', 0, 4, 6),
        #
        # painting('Creebet', 2, 5, 9),
        # painting('Bonjour Monsieur Courbet', 2, 8, 9),
        # painting('The Pool', 0, 7, 11),
        # painting('Seaside', 0, 4, 11),
        #
        # painting('Meditative', 2, 4, 20),
        # painting('de_aztec 2', 2, 6, 20),
        # painting('de_aztec', 2, 8, 20),
        # painting('Water', 0, 4, 22, note='(unused)'),
        # painting('Fire', 0, 7, 22, note='(unused)')
    )

    if unused:
        print('WARNING: Unused paintings: ' + ', '.join(unused))
