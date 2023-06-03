from __future__ import annotations

import re

from pynecraft.base import NORTH, Nbt, NbtDef, SOUTH, WEST, r
from pynecraft.commands import Block, JsonText, clone, data, e, fill, setblock, execute, kill, schedule, REPLACE
from pynecraft.simpler import Book, ItemFrame, WallSign, TextDisplay
from restworld.rooms import Room, ensure
from restworld.world import restworld


def name_nbt(name: str) -> NbtDef:
    return {'tag': {'display': {'Name': JsonText.text(name)}}}


def room():
    room = Room('maps', restworld, WEST, (None, 'Maps'))
    room.reset_at((5, 0))

    room.function('maps_room_enter', exists_ok=True).add(
        clone(r(8, -5, 0), r(8, -5, 0), r(8, 1, 0)),
        fill(r(0, -1, -3), r(9, -1, 3), 'redstone_block').replace('glass')
    )
    room.function('maps_room_exit').add(fill(r(0, -1, -3), r(9, -1, 3), 'glass').replace('redstone_block'))
    p_north = room.mob_placer(r(3, 4, -3), SOUTH, -1, adults=True)
    p_mid = room.mob_placer(r(8, 4, -1), WEST, -1, adults=True)
    icons = {
        'Target X': {'id': "_0", 'type': 4, 'x': 128, 'z': -32, 'rot': 180},
        'Target Point': {'id': "_1", 'type': 5, 'x': 88, 'z': -16, 'rot': 180},
        'Mansion': {'id': "_2", 'type': 8, 'x': 128, 'z': 0, 'rot': 180},
        'Monument': {'id': "_3", 'type': 9, 'x': 88, 'z': 16, 'rot': 180},
        'Red X': {'id': "_4", 'type': 26, 'x': 128, 'z': 32, 'rot': 180},
    }
    icon_frame_tag = 'map_icon_frame'
    banner_frame_tag = 'map_banner_frame'
    banner_label = TextDisplay('Banner icons',
                               {'background': 0, 'shadow_radius': 0}).scale(0.2).tag('map_label', 'map_banner_label')
    set_map_icon = room.function('set_map_icons', home=False).add(
        data().modify(e().tag(icon_frame_tag).limit(1), 'Item.tag.Decorations').set().value(list(icons.values())))
    room_init = room.function('maps_room_init', exists_ok=True).add(
        p_north.summon(ItemFrame(SOUTH).item(map(142, name_nbt('Biomes')))),
        WallSign((None, 'Biome', 'Sampler'), SOUTH).place(r(4, 3, -3), SOUTH),

        room.mob_placer(r(6, 4, -3), SOUTH, adults=True).summon(
            ItemFrame(SOUTH).item(map(23, name_nbt('Battle Arena')))),
        WallSign((None, 'Battle', 'Arena'), SOUTH).place(r(7, 3, -3), SOUTH),

        kill(e().tag('map_label')),
        room.mob_placer(r(8, 5, 0), WEST, adults=True).summon(ItemFrame(WEST).item(map(18, name_nbt('Main (top)')))),
        p_mid.summon(ItemFrame(WEST).item(map(124, name_nbt('Main (left)'))).tag(banner_frame_tag)),
        p_mid.summon(ItemFrame(WEST).item(map(14, name_nbt('Main (center)')))),
        p_mid.summon(ItemFrame(WEST).item(map(133, name_nbt('Main (right)'))).tag(icon_frame_tag)),
        room.mob_placer(r(8, 3, 0), WEST, adults=True).summon(ItemFrame(WEST).item(map(20, name_nbt('Main (bot)')))),
        WallSign((None, 'Center', 'Area')).place(r(8, 3, 1), WEST),
        schedule().function(set_map_icon, "1s", REPLACE),

        room.mob_placer(r(6, 4, 3), NORTH, adults=True).summon(ItemFrame(NORTH).item(map(32, name_nbt('Optifine')))),
        WallSign(('Optifine', 'Connected', 'Textures,', 'Mob Textures'), NORTH).place(r(5, 3, 3), NORTH),

        room.mob_placer(r(3, 4, 3), NORTH, adults=True).summon(ItemFrame(NORTH).item(map(22, name_nbt('Photo')))),
        WallSign((None, 'Photo', 'Area'), NORTH).place(r(2, 3, 3), NORTH),

        setblock(r(8, 2, 2), 'cartography_table'),

        execute().at(e().tag(banner_frame_tag)).run(banner_label.summon(r(-0.04, 0.2, -0.11), facing=WEST)),
    )
    for i, (k, v) in enumerate(icons.items()):
        label = TextDisplay(k, {'background': 0, 'shadow_radius': 0}).scale(0.1).tag('map_label', f'map_label_{i}')
        y = v['z'] / 128.0 + 0.05
        z = v['x'] / 128.0 - 1
        room_init.add(execute().at(e().tag(icon_frame_tag)).run(label.summon(r(-0.04, y, z), facing=WEST)))
    label = TextDisplay('Frame',
                        {'background': 0, 'shadow_radius': 0}).scale(0.1).tag('map_label', f'map_label_{len(icons)}')
    room_init.add(execute().at(e().tag(icon_frame_tag)).run(label.summon(r(-0.04, 0, -0.42), facing=WEST)))

    map_chest_pos = r(0, -5, 1)
    room.function('map_chest_init').add(
        data().modify(map_chest_pos, 'Items[{Slot:6b}]').merge().value(name_nbt('Optifine')),
        data().modify(map_chest_pos, 'Items[{Slot:20b}]').merge().value(name_nbt('Photo')),

        data().modify(map_chest_pos, 'Items[{Slot:4b}]').merge().value(name_nbt('Main (top)')),
        data().modify(map_chest_pos, 'Items[{Slot:12b}]').merge().value(name_nbt('Main (left)')),
        data().modify(map_chest_pos, 'Items[{Slot:13b}]').merge().value(name_nbt('Main (center)')),
        data().modify(map_chest_pos, 'Items[{Slot:14b}]').merge().value(name_nbt('Main (right)')),
        data().modify(map_chest_pos, 'Items[{Slot:22b}]').merge().value(name_nbt('Main (bot)')),

        data().modify(map_chest_pos, 'Items[{Slot:2b}]').merge().value(name_nbt('Biomes')),
        data().modify(map_chest_pos, 'Items[{Slot:24b}]').merge().value(name_nbt('Battle Arena)')),
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
    book.add(simplify("""Here you can see general map textures, and some map icons. Yet there are several icons,
    such as for players, that can't be shown without real players. If you hold a map you can see the icon for you,
    but to see other players' icons, you will need to"""))
    book.next_page()
    # noinspection GrazieInspection
    book.add(simplify("""recruit friends to join the world. Also, treasure maps show sketched versions of areas you
    haven't visited, but there no normal looking areas in this world for that to work with."""))

    return book


def map(num: int, added_nbt: NbtDef = None):
    nbt = Nbt({'tag': {'map': num}})
    if added_nbt:
        nbt = nbt.merge(added_nbt)
    return 'filled_map', {}, nbt
