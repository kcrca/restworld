from __future__ import annotations

import math

from pynecraft.base import EAST, NE, NORTH, NW, SE, SOUTH, SW, WEST, good_facing, r, rotated_facing
from pynecraft.commands import JsonText, comment, e, execute, fill, function, kill, setblock, tag
from pynecraft.info import mobs
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
    room = Room('multimob', restworld, WEST, (None, 'Random', 'Entities', '(Optifine)'))

    menu_home = e().tag('mob_menu_home').limit(1)
    at_home = execute().at(menu_home)
    menu_clear = room.function('mob_menu_clear', home=False).add(
        fill(r(-2, 3, -2), r(2, 5, 2), 'air').replace('#wall_signs'))
    clear = at_home.run(function(menu_clear))
    menu_init = room.function('mob_menu_init').add(
        label(r(0, 2, 0), 'Reset'),
        function(menu_clear),
        fill(r(-9, 2, -9), r(9, 4, 9), 'air').replace('water'),
        fill(r(-9, 2, -9), r(9, 4, 9), 'air').replace('structure_void'))
    max_per_group = math.ceil(len(mobs) / NUM_GROUPS)
    full_groups = NUM_GROUPS - (max_per_group * NUM_GROUPS - len(mobs))
    start = 0
    stride = max_per_group
    dir_order = (NORTH, EAST, SOUTH, WEST)
    within = 0
    all_mobs = tuple(mobs.keys())
    for dir in (NW, SW, NE, SE):
        room.function(f'multimob_{dir}').add(comment('Just for the home func'))
        dir_home = f'multimob_{dir}_home'
        room.function(dir_home, exists_ok=True).add(tag(e().tag(dir_home)).add('multimob_summoner'))

    for i in range(NUM_GROUPS):
        if i == full_groups and full_groups != NUM_GROUPS:
            stride -= 1
        dir = dir_order[i // 3]
        facing = good_facing(dir)
        x, _, z = facing.scale(2)
        move_facing = rotated_facing(facing, 90)
        sign_facing = rotated_facing(facing, 180)
        dx, _, dz = move_facing.scale(1)

        popup = room.function(f'mob_menu_{i:02}', home=False)
        up = room.score('mob_menu_up')
        for j, m in enumerate(range(start, start + stride)):
            mob = mobs[all_mobs[m]]
            summon_mob = summon_mob_commands(room, mob)
            row_count = math.ceil(stride / 3)
            top_y = 2 + row_count
            sign_x = x + (-1 + j % 3) * dx
            sign_z = z + (-1 + j % 3) * dz
            sign_y = top_y - j // 3
            popup.add(
                WallSign((None, mob.name),
                         (clear, execute().if_().block(r(0, 1, 0), 'air').run(function(summon_mob))),
                         wood='birch').place(r(sign_x, sign_y, sign_z), sign_facing))

        x += (-1 + within) * dx
        z += (-1 + within) * dz
        menu_init.add(
            WallSign((None, all_mobs[start], JsonText.text('to').italic(), all_mobs[start + stride - 1]),
                     (clear, at_home.run(function(popup)))).place(r(x, 2, z), sign_facing))

        start += stride
        within = (within + 1) % 3

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
