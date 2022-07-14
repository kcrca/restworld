from __future__ import annotations

import re

from pyker.base import NORTH, SOUTH, WEST, r
from pyker.commands import Block, JsonText, clone, fill, setblock
from pyker.simpler import Book, ItemFrame, WallSign
from restworld.rooms import Room, ensure, label
from restworld.world import restworld


def room():
    room = Room('maps', restworld, WEST, (None, 'Maps'))

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
        p_mid.summon(ItemFrame(WEST).item(map(19))),
        p_mid.summon(ItemFrame(WEST).item(map(14))),
        p_mid.summon(ItemFrame(WEST).item(map(21)).named('Banner Icons')),
        room.mob_placer(r(8, 3, 0), WEST, adults=True).summon(ItemFrame(WEST).item(map(20))),
        WallSign((None, 'Center', 'Area')).place(r(8, 3, 1), WEST),

        room.mob_placer(r(6, 4, 3), NORTH, adults=True).summon(ItemFrame(NORTH).item(map(32))),
        WallSign((None, 'Connected', 'Textures'), NORTH).place(r(5, 3, 3), NORTH),

        room.mob_placer(r(3, 4, 3), NORTH, adults=True).summon(ItemFrame(NORTH).item(map(22))),
        WallSign((None, 'Photo', 'Area'), NORTH).place(r(2, 3, 3), NORTH),

        setblock(r(8, 2, 2), 'cartography_table'),

        label(r(6, 2, 0), "Reset"),
    )
    room.function('apologia', home=False).add(
        ensure(r(0, 2, 0), Block('lectern', {'facing': WEST, 'has_book': True}),
               nbt=apologia().as_item()))


def simplify(text):
    return re.sub(r'\s{2,}', ' ', text.strip())


def apologia():
    book = Book()
    book.sign_book('On Maps', 'RestWorld', 'A Map Apologia')

    book.add(r'       ', JsonText.text('On Maps').bold(), r'\n\n')
    book.add(simplify("""All you can see here are the general map textures, how they look for partially completed 
maps (both on the wall and in your hand (just take one from the chest), and indicators for you, map placement, 
and banners."""))
    book.next_page()
    book.add(simplify("""Minecraft maps consult the real world when deciding what to show. Most other things have 
internal state that can be set to show what you want, but not maps. So to see your marker, pick up a map and look 
at it as you move around. To see what a separate player looks like, you'll have to get"""))
    book.next_page()
    book.add(simplify("""someone else to log in to the world. And the treasure, woodland explorer, and ocean explorer 
maps would require some place that has those features, which this world doesn't and (AFAICT) cannot have. So we 
cannot show those things. Sorry."""))

    return book


def map(num: int):
    return ('filled_map', {}, {'tag': {'map': num}})
