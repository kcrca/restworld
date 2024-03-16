from __future__ import annotations

import re

from pynecraft.base import NORTH, Nbt, NbtDef, SOUTH, WEST, r
from pynecraft.commands import Block, JsonText, clone, data, e, execute, fill, kill, setblock
from pynecraft.simpler import Book, ItemFrame, TextDisplay, WallSign
from restworld.rooms import Room, ensure
from restworld.world import restworld


def name_nbt(name: str) -> NbtDef:
    return {'components': {'custom_name': JsonText.text(name)}}


def room():
    room = Room('maps', restworld, WEST, (None, 'Maps'))
    room.reset_at((5, 0))

    room.function('maps_room_enter', exists_ok=True).add(
        clone(r(8, -5, 0), r(8, -5, 0), r(8, 1, 0)),
        fill(r(0, -1, -3), r(9, -1, 3), 'redstone_torch').replace('glass')
    )
    room.function('maps_room_exit').add(fill(r(0, -1, -3), r(9, -1, 3), 'glass').replace('redstone_torch'))
    p_north = room.mob_placer(r(3, 4, -3), SOUTH, -1, adults=True)
    p_mid = room.mob_placer(r(8, 4, -1), WEST, -1, adults=True)
    icons = {
        'Target X': 'target_x',
        'Target Point': 'target_point',
        'Red X': 'red_x',
        'Monument': 'monument',
        'Mansion': 'mansion',
        'Desert Village': 'village_desert',
        'Plains Village': 'village_plains',
        'Savanna Village': 'village_savanna',
        'Snowy Village': 'village_snowy',
        'Taiga Village': 'village_taiga',
        'Jungle Temple': 'jungle_temple',
        'Swamp Hut': 'swamp_hut'
    }
    decorations = Nbt()
    four_per_z = 128 / 5
    xs = (88, 128, 168)
    col = 0
    z = -64 + four_per_z
    for i, (name, id) in enumerate(icons.items()):
        decorations[id] = {'rotation': 180, 'x': xs[col], 'z': z, 'type': id, 'name': name}
        if i % 4 == 3:
            col += 1
            z = -64
        z += four_per_z
    icon_frame_tag = 'map_icon_frame'
    banner_frame_tag = 'map_banner_frame'
    banner_label = TextDisplay('Banner Icons',
                               {'background': 0, 'shadow_radius': 0}).scale(0.2).tag('map_label', 'map_banner_label')
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
        data().modify(e().tag(icon_frame_tag).limit(1), 'Item.components.map_decorations').set().value(decorations),
        room.mob_placer(r(6, 4, 3), NORTH, adults=True).summon(ItemFrame(NORTH).item(map(32, name_nbt('Optifine')))),
        WallSign(('Optifine:', 'Connected', 'Textures and', 'Mob Textures'), NORTH).place(r(5, 3, 3), NORTH),

        room.mob_placer(r(3, 4, 3), NORTH, adults=True).summon(ItemFrame(NORTH).item(map(22, name_nbt('Photo')))),
        WallSign((None, 'Photo', 'Area'), NORTH).place(r(2, 3, 3), NORTH),

        setblock(r(8, 2, 2), 'cartography_table'),

        execute().at(e().tag(banner_frame_tag)).run(banner_label.summon(r(-0.04, -0.23, -0.13), facing=WEST)),
    )
    for i, (k, v) in enumerate(decorations.items()):
        label = TextDisplay(v['name'], {'background': 0, 'shadow_radius': 0}).scale(0.1).tag('map_label',
                                                                                             f'map_label_{i}')
        y = v['z'] / -128.0 - 0.07
        z = v['x'] / 128.0 - 1
        room_init.add(execute().at(e().tag(icon_frame_tag)).run(label.summon(r(-0.04, y, z), facing=WEST)))
    label = TextDisplay('Frame',
                        {'background': 0, 'shadow_radius': 0}).scale(0.1).tag('map_label', f'map_label_{len(icons)}')
    room_init.add(execute().at(e().tag(icon_frame_tag)).run(label.summon(r(-0.04, -0.06, -0.47), facing=WEST)))

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
    nbt = Nbt({'components': {'map_id': num}})
    if added_nbt:
        nbt = nbt.merge(added_nbt)
    return 'filled_map', {}, nbt
