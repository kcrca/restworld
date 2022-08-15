from __future__ import annotations

import re
from dataclasses import dataclass

from pynecraft.base import NORTH, SOUTH, WEST, r
from pynecraft.commands import Block, Entity, JsonText, clone, data, e, fill, item, setblock
from pynecraft.simpler import Book, ItemFrame, Sign, WallSign
from restworld.rooms import Room, ensure, label
from restworld.world import main_clock, restworld


def room():
    room = Room('maps', restworld, WEST, (None, 'Maps'))

    @dataclass
    class MapIcon:
        name: str
        type_id: int

    # To set an icon on a map, go to -128, ~, 0 and create a map. Then put that map into an item frame, and set the
    # desired icon via something like:
    #   /data modify entity <frame-entity> Item.tag.Decorations set value [{Id:"_",type:1,x:-128,z:0,rot:180}]
    # Note the map number, and then you can use it in the table below.
    map_icons = {
        75: MapIcon("Red X", 26),
        76: MapIcon("Ocean Monument", 9),
        96: MapIcon("Woodland Mansion", 8),
        78: MapIcon('Target Point', 5),
        97: MapIcon('Target X', 4),
        81: MapIcon('Frame', 1),
    }

    room.function('maps_room_enter', exists_ok=True).add(
        clone(r(8, -5, 0), r(8, -5, 0), r(8, 1, 0)),
        fill(r(0, -1, -3), r(9, -1, 3), 'redstone_block').replace('glass')
    )
    room.function('maps_room_exit').add(fill(r(0, -1, -3), r(9, -1, 3), 'glass').replace('redstone_block'))
    p_north = room.mob_placer(r(2, 4, -3), SOUTH, -1, adults=True)
    p_mid = room.mob_placer(r(8, 4, -1), WEST, -1, adults=True)
    room.function('maps_room_init', exists_ok=True).add(
        room.mob_placer(r(3, 5, -3), SOUTH, adults=True).summon(ItemFrame(SOUTH).item(map(31))),
        p_north.summon(ItemFrame(SOUTH).item(map(29))),
        p_north.summon(ItemFrame(SOUTH).item(map(26))),
        p_north.summon(ItemFrame(SOUTH).item(map(30))),
        room.mob_placer(r(3, 3, -3), SOUTH, adults=True).summon(ItemFrame(SOUTH).item(map(28))),
        WallSign((None, 'Biome', 'Sampler'), SOUTH).place(r(4, 3, -3), SOUTH),

        room.mob_placer(r(6, 4, -3), SOUTH, adults=True).summon(ItemFrame(SOUTH).item(map(23))),
        WallSign((None, 'Battle', 'Arena'), SOUTH).place(r(7, 3, -3), SOUTH),

        room.mob_placer(r(8, 5, 0), WEST, adults=True).summon(ItemFrame(WEST).item(map(18))),
        p_mid.summon(ItemFrame(WEST).item(map(19)).tag('map_icon_frame')),
        p_mid.summon(ItemFrame(WEST).item(map(14))),
        p_mid.summon(ItemFrame(WEST).item(map(21))),
        room.mob_placer(r(8, 3, 0), WEST, adults=True).summon(ItemFrame(WEST).item(map(20))),
        WallSign((None, 'Center', 'Area')).place(r(8, 3, 1), WEST),

        room.mob_placer(r(6, 4, 3), NORTH, adults=True).summon(ItemFrame(NORTH).item(map(32))),
        WallSign((None, 'Connected', 'Textures'), NORTH).place(r(5, 3, 3), NORTH),

        room.mob_placer(r(3, 4, 3), NORTH, adults=True).summon(ItemFrame(NORTH).item(map(22))),
        WallSign((None, 'Photo', 'Area'), NORTH).place(r(2, 3, 3), NORTH),

        setblock(r(8, 2, 2), 'cartography_table'),

        label(r(5, 2, 0), 'Reset'),
    )

    icon_frame = e().tag('map_icon_frame').limit(1)
    chest_pos = r(0, -2, 1)
    map_slot = 'container.15'

    # Maps are weird. They aren't stored in the same way as other entities/items, so a direct approach (put up a map
    # and keep changing its decorations) doesn't work. So we (1) conjure up the map we want by number,
    # with the decoration specified even though we specify it _every time_; (2) update the sign, and finally (3) move
    # the conjured map into the frame. The chest is just a workspace where the item conjuring is done, it could be
    # any container.
    def icon_loop(step):
        map_num, map_icon = step.elem
        yield item().replace().block(chest_pos, map_slot).with_(
            Entity('filled_map',
                   dict(map=map_num, Decorations=[dict(Id='_', type=map_icon.type_id, x=-128, z=0, rot=180)])))
        yield data().merge(r(0, 4, -1), Sign.lines_nbt((None, map_icon.name)))

    room.loop('map_icons', main_clock).loop(icon_loop, map_icons.items()).add(
        item().replace().entity(icon_frame, 'container.0').from_().block(chest_pos, map_slot))
    room.function('map_icons_init').add(WallSign(()).place(r(0, 4, -1), WEST))

    room.function('apologia', home=False).add(
        ensure(r(0, 2, 0), Block('lectern', {'facing': WEST, 'has_book': True}),
               nbt=apologia().as_item()))


def simplify(text):
    return re.sub(r'\s{2,}', ' ', text.strip())


def apologia():
    book = Book()
    book.sign_book('On Maps', 'RestWorld', 'A Map Apologia')

    book.add(r'       ', JsonText.text('On Maps').bold(), r'\n\n')
    book.add(simplify("""Here you can see general map textures, and some map icons. Yet there are several icons,
    such as for players, that can't be shown without real players. If you hold a map you can see the icon for you,
    but to see other players' icons, you will need to"""))
    book.next_page()
    book.add(simplify("""recruit friends to join the world. Also, treasure maps show sketched versions of areas you
    haven't visited, but there no normal looking areas in this world for that to work with."""))

    return book


def map(num: int):
    return 'filled_map', {}, {'tag': {'map': num}}
