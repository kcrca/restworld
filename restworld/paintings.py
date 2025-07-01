from __future__ import annotations

from pynecraft.base import EAST, NORTH, ROTATION_270, SOUTH, Transform, WEST, as_facing, r
from pynecraft.commands import Text, e, kill, summon
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
        txt = Text.translate(f'painting.minecraft.{img.name}.title').bold().italic(False)
        if note:
            txt = txt.extra(fr' {note}')
        txt = txt.extra(r'\n')
        txt = txt.extra(Text.translate(
            f'painting.minecraft.{img.name}.author', fallback="[artist unknown]").plain(),
                        Text.text(fr'\n{img.name} {img.size[0]}×{img.size[1]}\n').plain().italic())
        display = TextDisplay(txt, nbt={
            'alignment': 'left', 'line_width': 84, 'background': 0}).tag(
            'painting').transform(
            Transform.quaternion(facing, 0.45))

        def adj(v, facing_d, moving_d):
            return v + (img.size[0] - 0) * moving_d - facing_d / 2.01

        label_y = y
        label_x = x
        label_z = z
        if img.size == (1, 1):
            label_y -= 0.7
            label_x -= moving.dx
            label_z -= moving.dz
        yield display.summon(r(adj(label_x, facing.dx, moving.dx), label_y, adj(label_z, facing.dz, moving.dz)))
        try:
            unused.remove(img.value)
        except KeyError:
            print(f'Duplicate: {img.value}')

    f = room.function('all_paintings_init').add(
        kill(e().tag('painting')),
        kill(e().type('item')),

        wall(('Fern', 'Orb', 'Skull On Fire', 'Fighters', 'sunset_dense', 'Bouquet'), NORTH, 23, 26),
        wall(('Mortal Coil', 'Kong', 'Bonjour Monsieur Courbet', 'Pond', 'Cavebird', 'Pigscene'), EAST, -2, 25),

        wall(('Tides', 'Pointer', 8, 'Passage', 'Wanderer', 'Prairie Ride'), SOUTH, -1, 0),
        # wall(('Backyard', 'Owlemons', 'The void', 'Skull and Roses', 'Wither', 'The Stage Is Set', 'Graham', 'Endboss'), WEST, 24, 1),
        wall(('Backyard', 'Owlemons', 'Humble', 'Cotán', 'Changing', 'Graham', 'Endboss'), WEST, 24, 1),

        wall(('Finding',), WEST, 19, 11),
        wall(('Dennis',), EAST, 21, 14),
        wall(('Unpacked', ), EAST, 3, 15),
        wall(('Sunflowers',), WEST, 1, 12),

        wall(('Earth', 'Wind', 6, 'Water', 'Fire'), SOUTH, 3, 21, note='(unused)'),
        # wall(('Cotán', 'Humble', 5, 'Albanian', 'Changing'), NORTH, 20, 19),
        wall((1, 'The void', 'Skull and Roses', 6, 'Wither', 'The Stage Is Set'), NORTH, 20, 19),


        # 1x1's
        wall(('de_aztec', 4, 'Meditative'), NORTH, 14, 12),
        wall(('de_aztec 2',), EAST, 15, 13),
        wall(('Kebab med tre pepperoni',), WEST, 13, 13),
        wall(('Paradisträd', 4, 'Wasteland'), SOUTH, 8, 14),
        wall(('Albanian',), EAST, 9, 13),
        wall(('Target Successfully Bombed',), WEST, 7, 13),

        wall(('The Pool', 'Match', 6, 'Creebet', 'Seaside'), SOUTH, 3, 7),
        wall(('Bust', 'Baroque',6, 'Lowmist'), NORTH, 19, 5),
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
