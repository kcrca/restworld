from __future__ import annotations

import copy
import math

from pynecraft.base import EAST, NE, NORTH, NW, SE, SOUTH, SW, WEST, good_facing, r, rotated_facing
from pynecraft.commands import Entity, JsonText, comment, data, e, execute, fill, function, kill, s, setblock, tag
from pynecraft.info import mobs, villager_biomes, villager_professions
from pynecraft.simpler import Item, WallSign
from restworld.rooms import Room, label
from restworld.world import kill_em, restworld

NUM_GROUPS = 12

WATER = {
    'Cod',
    'Dolphin',
    'Elder Guardian',
    'Glow Squid',
    'Guardian',
    'Pufferfish',
    'Salmon',
    'Squid',
    'Tadpole',
    'Tropical Fish',
}
UNDEAD = {
    'Drowned',
    'Phantom',
    'Skeleton',
    'Stray',
    'Zombie',
    'Zombie Villager',
}
BIG = {
    'Elder Guardian',
    'Ender Dragon',
    'Ghast',
    'Ravager',
}
HIGHER = {
    'Allay',
    'Axolotl',
    'Bat',
    'Bee',
    'Cave Spider',
    'Chicken',
    'Cod',
    'Dolphin',
    'Endermite',
    'Ghast',
    'Glow Squid',
    'Guardian',
    'Parrot',
    'Phantom',
    'Pufferfish',
    'Salmon',
    'Shulker',
    'Silverfish',
    'Spider',
    'Squid',
    'Tadpole',
    'Tropical Fish',
    'Turtle',
    'Vex',
}


def room():
    room = Room('multimob', restworld, WEST, (None, 'Random', 'Entities', '(Optifine)'), room_name='Random Entities')

    menu_home = e().tag('mob_menu_home').limit(1)
    at_home = execute().at(menu_home)
    row_len = 3
    menu_clear = room.function('mob_menu_clear', home=False).add(
        fill(r(-2, 3, -2), r(2, 6, 2), 'air').replace('#wall_signs'))
    clear = at_home.run(function(menu_clear))
    menu_init = room.function('mob_menu_init').add(
        label(r(0, 2, 0), 'Reset Room'),
        function(menu_clear),
        fill(r(-9, 2, -9), r(9, 4, 9), 'air').replace('water'),
        fill(r(-9, 2, -9), r(9, 4, 9), 'air').replace('structure_void'))
    my_mobs = copy.deepcopy(mobs)
    my_mobs['<None>'] = Entity('none', name='<None>')
    all_mobs = tuple(my_mobs.keys())
    max_per_group = math.ceil(len(all_mobs) / NUM_GROUPS)
    full_groups = NUM_GROUPS - (max_per_group * NUM_GROUPS - len(all_mobs))
    start = 0
    stride = max_per_group
    dir_order = (NORTH, EAST, SOUTH, WEST)
    within = 0
    for dir in (NW, SW, NE, SE):
        room.function(f'multimob_{dir}').add(comment('Just for the home func'))
        dir_home = f'multimob_{dir}_home'
        room.function(dir_home, exists_ok=True).add(tag(e().tag(dir_home)).add('multimob_summoner'))

    for i in range(NUM_GROUPS):
        if i == full_groups and full_groups != NUM_GROUPS:
            stride -= 1
        dir = dir_order[i // row_len]
        facing = good_facing(dir)
        x, _, z = facing.scale(2)
        move_facing = rotated_facing(facing, 90)
        sign_facing = rotated_facing(facing, 180)
        dx, _, dz = move_facing.scale(1)

        def menu_matrix(name, values, matrix_row_len, func_gen):
            popup = room.function(name, exists_ok=True, home=False)
            if popup.commands():
                return popup

            row_count = math.ceil(len(values) / matrix_row_len)
            top_y = 2 + row_count
            for i, value in enumerate(values):
                sx, sy, sz = sign_pos(i, x, top_y, z, matrix_row_len)
                popup.add(
                    WallSign((None, value), (clear, *func_gen(value)), wood='birch').place(r(sx, sy, sz), sign_facing))
            return popup

        def set_villager(key, which):
            func = room.function(f'{key.lower()}_{which.lower()}', home=False)
            for sector in (NW, SW, NE, SE):
                facing_tag = f'multimob_{sector}_mob'
                func.add(
                    execute().at(e().tag(f'multimob_{sector}_home')).as_(e().tag(facing_tag)).run(
                        data().merge(s(), {'VillagerData': {key: which.lower()}})))
            func.add(clear)
            return func

        def set_profession(pro):
            return function(set_villager('profession', pro).add(at_home.run(function('restworld:multimob/type')))),

        def set_type(type):
            return function(set_villager('type', type)),

        def summoner(mob_key):
            mob = my_mobs[mob_key]
            summon_mob = summon_mob_commands(room, mob)
            return execute().if_().block(r(0, 1, 0), 'air').run(function(summon_mob)), follow_on(mob)

        def sign_pos(sign_num, x_base, y_base, z_base, matrix_row_len):
            sign_y = y_base - sign_num // matrix_row_len
            sign_x = x_base + (-1 + sign_num % matrix_row_len) * dx
            sign_z = z_base + (-1 + sign_num % matrix_row_len) * dz
            return sign_x, sign_y, sign_z

        def follow_on(mob):
            if not mob.name.endswith('Villager'):
                return None

            menu_matrix('type', villager_biomes, row_len, set_type)
            professions = list(villager_professions)
            if mob.name == 'Villager':
                professions.append('Child')
            pro_popup = menu_matrix('profession', professions, 4, set_profession)
            return at_home.run(function(pro_popup))

        popup = menu_matrix(f'mob_menu_{i:02}', all_mobs[start:start + stride], row_len, summoner)

        x += (-1 + within) * dx
        z += (-1 + within) * dz
        menu_init.add(
            WallSign((None, all_mobs[start], JsonText.text('to').italic(), all_mobs[start + stride - 1]),
                     (clear, at_home.run(function(popup)))).place(r(x, 2, z), sign_facing))

        start += stride
        within = (within + 1) % row_len

    room.function('sector_setup', home=False).add(
        kill(e().tag('multimob_summoner')),
        fill(r(-5, 2, -5), r(5, 2, 5), 'redstone_lamp').replace('shroomlight'),
        setblock(r(0, 2, 0), 'shroomlight'))


def summon_mob_commands(room, mob):
    summon_mob = room.function(f'summon_{mob.id}', home=False)
    for sector in (NW, SW, NE, SE):
        facing_tag = f'multimob_{sector}_mob'
        run_at = execute().at(e().tag(f'multimob_{sector}_home')).run
        summon_mob.add(run_at(kill_em(e().tag(facing_tag))))
        if mob.name in WATER:
            summon_mob.add(
                run_at(fill(r(-1, 2, -1), r(5, 4, 5), 'structure_void').replace('air')),
                run_at(fill(r(0, 2, 0), r(4, 4, 4), 'water').replace('structure_void')))
        else:
            summon_mob.add(
                run_at(fill(r(0, 2, 0), r(4, 4, 4), 'air').replace('water')),
                run_at(fill(r(-1, 2, -1), r(5, 4, 5), 'air').replace('structure_void')))

        if mob.name == '<None>':
            continue

        mob_facing = rotated_facing(sector, 90)
        mob.merge_nbt({'IsImmuneToZombification': True, 'Invulnerable': True})
        if mob.name in UNDEAD:
            mob.merge_nbt({'ArmorItems': [{}, {}, {}, Item.nbt_for('chainmail_helmet')]})
        big_places = ((0, 4), (4, 0)) if sector in (NW, SE) else ((0, 0), (4, 4))
        for mx in range(0, 6, 2):
            for mz in range(0, 6, 2):
                y = 3 if mob.name in HIGHER else 2
                if mob.name not in BIG or (mx, mz) in big_places:
                    summon_mob.add(run_at(room.mob_placer(
                        r(mx, y, mz), mob_facing, adults=True, tags=(facing_tag,)).summon(mob)))
    return summon_mob
