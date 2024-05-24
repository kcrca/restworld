from __future__ import annotations

from pynecraft.base import EAST, NORTH, ROTATION_270, SOUTH, Transform, WEST, as_facing, r
from pynecraft.commands import JsonText, e, kill, summon
from pynecraft.simpler import TextDisplay
from pynecraft.values import PAINTING_GROUP, paintings
from restworld.rooms import Room
from restworld.world import restworld


# noinspection SpellCheckingInspection
def room():
    room = Room('paintings', restworld, NORTH, (None, 'Paintings'))
    room.reset_at((0, 3), note="and Labels")
    unused = set(PAINTING_GROUP)

    def wall(ids, facing, x, z, y=3, note=None):
        if isinstance(ids, str):
            ids = (ids,)
        facing = as_facing(facing)
        moving = facing.turn(ROTATION_270)
        for id in ids:
            if isinstance(id, int):
                x += id * moving.dx
                z += id * moving.dz
                continue
            img = paintings[id]
            yield from painting(id, facing, moving, x, z, y, note)
            x += (img.size[0] + 1) * moving.dx
            z += (img.size[0] + 1) * moving.dz

    def painting(id, facing, moving, x, z, y=3, note=None):
        img = paintings[id]
        px, pz = (0, 0)
        label_y = y
        if img.size[1] >= 4:
            y -= 1
        if img.size[0] > 2:
            px += moving.dx
            pz += moving.dz
        if img.size[1] > 3:
            y += 1
        yield summon('painting', r(x + px, y, z + pz),
                     {'variant': img.name, 'facing': facing.painting_number, 'Tags': ['painting']})
        title = img.value
        if note:
            title += f' {note}'
        txt = JsonText.translate(f'painting.minecraft.{img.name}.title').bold().italic(False)
        if note:
            txt = txt.extra(fr' {note}')
        txt = txt.extra(r'\n')
        txt = txt.extra(JsonText.translate(
            f'painting.minecraft.{img.name}.author').plain(),
                        JsonText.text(fr'\n{img.name} {img.size[0]}×{img.size[1]}\n').plain().italic())
        display = TextDisplay(txt, nbt={
            'alignment': 'left', 'line_width': 84, 'background': 0}).tag(
            'painting').transform(
            Transform.quaternion(facing, 0.45))

        def adj(v, facing_d, moving_d):
            return v + (img.size[0] - 0) * moving_d - facing_d / 2.01

        yield display.summon(r(adj(x, facing.dx, moving.dx), label_y, adj(z, facing.dz, moving.dz)))
        try:
            unused.remove(img.value)
        except KeyError:
            print(f'Duplicate: {img.value}')

    f = room.function('all_paintings_init').add(
        kill(e().tag('painting')),
        kill(e().type('item')),

        wall(('Fern', 'Orb', 'Kebab med tre pepperoni', 'Skull On Fire', 'Fighters', 'Unpacked'), NORTH, 23, 26),
        wall(('Mortal Coil', 'Kong', 'Bonjour Monsieur Courbet', 'Pond', 'Cavebird', 'Pigscene'), EAST, -2, 25),
        #
        wall(('Tides', 'Pointer', 8, 'Passage', 'Wanderer', 'Prairie Ride'), SOUTH, -1, 0),
        wall(('Backyard', 'Owlemons', 'The void', 'Skull and Roses', 'Wither', 'The Stage Is Set', 'Graham', 'Endboss'),
             WEST, 24, 1),

        wall(('Earth', 'Wind', 6, 'Water', 'Fire'), SOUTH, 3, 21, note='(unused)'),
        wall(('Cotán', 'Humble', 5, 'Albanian', 'Changing'), NORTH, 20, 19),

        wall(('Target Successfully Bombed', 'Baroque', 'Paradisträd', 5, 'Sunflowers',
              'sunset_dense'), SOUTH, 2, 14),
        wall(('The Pool', 'Bust', 5, 'Meditative', 'Finding'), NORTH, 19, 12),

        wall(('Bouquet', 'Match', 6, 'Creebet', 'Seaside'), SOUTH, 2, 7),
        wall(('de_aztec', 'de_aztec 2', 'Wasteland', 6, 'Lowmist'), NORTH, 19, 5),
    )

    if unused:
        w = 0
        print('WARNING: Unused paintings: ', end='')
        for p in unused:
            img = paintings[p]
            print(f'{p} {img.size}', end=', ')
            w += img.size[0] + 1
        print(f'\nTotal run: {w}')
        f.add(
            wall(tuple(x for x in unused), WEST, 24, -1, y=9),
        )
