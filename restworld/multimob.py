from __future__ import annotations

import copy
import math

from pynecraft import info
from pynecraft.base import Arg, EAST, NE, NORTH, NW, SE, SOUTH, SW, WEST, as_facing, r, rotate_facing
from pynecraft.commands import Entity, Text, comment, data, e, execute, fill, function, n, return_, s, \
    setblock, \
    summon, \
    tag
from pynecraft.simpler import VILLAGER_BIOMES, VILLAGER_PROFESSIONS, WallSign
from restworld.rooms import Room, kill_em
from restworld.world import restworld

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
    'Bogged',
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


# each summoning point has a homer (summon_mob_nw_home is our example case).
#
# selecting the sector means removing the summon_mob_cur tag from any summon_mob_nw_home
# that has it, then setting the tag summon_mob_cur on the correct sector homer.
#
# the thing to summon is built up in storage, under multimob.mob
#
# The sign initializes it to the mob-specific values: id, nbt, water(T/F), is_none(T/F),
# large(T/F), and y, then invokes summon_mobs (not as a macro)
#
# summon mobs adds the general stuff to the nbt, and then for each sector sets the Rotation
# value for the nbt, and then invokes
#
#       /summon_nw with storage multimobs mob
#
# at the tags summon_nw_home AND summon_mobs_cur. This will only actually run
# in one place
#
# summon_nw (etc.) know where to fill with water or air, and other specifics

def room():
    room = Room('multimob', restworld, WEST, (None, 'Random', 'Entities', '(Optifine)'), room_name='Random Entities')
    room.reset_at((11, 0))

    def tag_for(sector):
        return f'{sector}_mob'

    menu_home = e().tag('mob_menu_home').limit(1)
    at_home = execute().at(menu_home)
    row_len = 3
    menu_clear = room.function('mob_menu_clear', home=False).add(
        fill(r(-2, 3, -2), r(2, 6, 2), 'air').replace('#wall_signs'))
    clear_menus = at_home.run(function(menu_clear))
    menu_init = room.function('mob_menu_init').add(
        function(menu_clear),
        fill(r(-9, 2, -9), r(9, 4, 9), 'air').replace('water'),
        fill(r(-9, 2, -9), r(9, 4, 9), 'air').replace('structure_void'),
        room.label(r(-2, 2, -2), 'This Corner\\n\u21e7', NW),
        room.label(r(2, 2, -2), 'This Corner\\n\u21e7', NE),
        room.label(r(2, 2, 2), 'This Corner\\n\u21e7', SE),
        room.label(r(-2, 2, 2), 'This Corner\\n\u21e7', SW),
    )
    room.function('mob_menu_home', exists_ok=True).add(
        tag(n().tag('mob_menu_home')).add('summon_mobs_home'))
    my_mobs = copy.deepcopy(info.mobs)
    if 'Creaking' not in my_mobs:
        my_mobs['Creaking'] = Entity('Creaking')
        my_mobs = dict(sorted(my_mobs.items()))
    if 'Illusioner' not in my_mobs:
        my_mobs['Illusioner'] = Entity('Illusioner')
        my_mobs = dict(sorted(my_mobs.items()))
    my_mobs['<None>'] = Entity('none', name='<None>')
    all_mobs = tuple(my_mobs.keys())
    max_per_group = math.ceil(len(all_mobs) / NUM_GROUPS)
    full_groups = NUM_GROUPS - (max_per_group * NUM_GROUPS - len(all_mobs))
    start = 0
    stride = max_per_group
    dir_order = (NORTH, EAST, SOUTH, WEST)
    within = 0
    sectors = (NW, SW, NE, SE)
    for sector in sectors:
        room.function(f'multimob_{sector}').add(comment('Just for the home func'))
        sector_home = f'multimob_{sector}_home'
        room.function(sector_home, exists_ok=True).add(tag(e().tag(sector_home)).add('multimob_summoner'))

    summon_mobs = room.function('summon_mobs', home=False).add((
        (
            data().modify(room.store, 'mob.nbt.Rotation').set().value(
                rotate_facing(as_facing(sector), 180).rotation),
            data().modify(room.store, 'mob.nbt.Tags').set().value(['multimob', 'adult', tag_for(sector)]),
            execute().at(e().tag(f'summon_{sector}_home', 'summon_cur')).run(
                function(f'restworld:multimob/summon_{sector}').with_().storage(room.store, 'mob'))
        )
        for sector in sectors),
        # We remove the rotation tag so we can merge data into the nbt to update the mobs later without changing it
        data().remove(room.store, 'mob.nbt.Rotation'),
        # This sets the sector tag in the NBT to be the one that was actually sued
        data().remove(room.store, 'mob.nbt.Tags[2]'),
        data().modify(room.store, 'mob.nbt.Tags').append().from_(room.store, 'mob.sector_tag'),
    )

    def summon_mob_commands(mob):
        mob.merge_nbt({
            'NoAI': True, 'Silent': True, 'PersistenceRequired': True,
            'IsImmuneToZombification': True, 'Invulnerable': True, 'CustomName': mob.name
        })
        yield data().modify(room.store, 'mob').set().value({
            'id': mob.id,
            'nbt': mob.nbt,
            'y': 3 if mob.name in HIGHER else 2,
            'water': mob.name in WATER,
            'big': mob.name in BIG,
            'undead': mob.name in UNDEAD,
            'is_none': mob.name == '<None>',
        })
        yield function(summon_mobs)
        return

    update_mob = room.function('update_mob', home=False).add(
        execute().as_(e().tag(Arg('sector_tag'))).run(data().merge(s(), Arg('nbt'))))
    update_type = room.function('update_type', home=False).add(
        execute().as_(e().tag(Arg('sector_tag'))).run(data().modify(s(), 'VillagerData.type').set().value(Arg('type')))
    )

    def set_profession(pro):
        age = -2147483648 if pro == 'Child' else 0
        nbt = {'mob': {'nbt': {'VillagerData': {'profession': pro}}, 'Age': age}}
        return (data().merge(room.store, nbt),
                function(update_mob).with_().storage(room.store, 'mob'),
                at_home.run(function('restworld:multimob/type')))

    def set_type(type):
        return (data().modify(room.store, 'mob.type').set().value(type),
                function(update_type).with_().storage(room.store, 'mob'))

    init_mobs = ((NW, -2, -2, 'Allay'), (NE, 2, -2, 'Guardian'), (SE, -2, -2, 'Piglin Brute'), (SW, -2, 2, 'Villager'))
    room.function('summon_mobs_init').add(
        ((
            execute().as_(e().tag('summon_cur')).run(tag(s()).remove('summon_cur')),
            tag(n().tag(f'summon_{sector}_home')).add('summon_cur'),
            summon_mob_commands(my_mobs[mob_id])
        )
            for sector, x, y, mob_id in init_mobs),
        set_profession('mason'),
        clear_menus,
        setblock(r(-2, 1, -2), 'redstone_block')
    )

    water_score = room.score('water')
    is_none_score = room.score('is_none')
    big_score = room.score('big')
    undead_score = room.score('undead')
    for sector in sectors:
        sector_tag = tag_for(sector)
        f = room.function(f'summon_{sector}').add(
            data().modify(room.store, 'mob.sector_tag').set().value(sector_tag),
            kill_em(e().tag(sector_tag)),
            water_score.set(Arg('water')),
            is_none_score.set(Arg('is_none')),
            big_score.set(Arg('big')),
            undead_score.set(Arg('undead')),
            execute().if_().score(water_score).matches(1).run(
                fill(r(-1, 2, -1), r(5, 4, 5), 'structure_void').replace('air'),
                fill(r(0, 2, 0), r(4, 4, 4), 'water').replace('structure_void')),
            execute().unless().score(water_score).matches(1).run(
                fill(r(0, 2, 0), r(4, 4, 4), 'air').replace('water'),
                fill(r(-1, 2, -1), r(5, 4, 5), 'air').replace('structure_void')),
            fill(r(-1, 200, -1), r(5, 200, 5), 'air'),
            execute().if_().score(is_none_score).matches(1).run(return_())
        )

        big_places = ((0, 4), (4, 0)) if sector in (NW, SE) else ((0, 0), (4, 4))
        for mx in range(0, 6, 2):
            for mz in range(0, 6, 2):
                cmd = summon(Arg('id'), (r(mx), '~$(y)', r(mz)), Arg('nbt'))
                if (mx, mz) not in big_places:
                    cmd = execute().unless().score(big_score).matches(1).run(cmd)
                f.add(cmd)
        f.add(
            execute().if_().score(undead_score).matches(1).at(e().tag(sector_tag)).run(
                setblock(r(0, 200, 0), 'smooth_quartz')))

    for i in range(NUM_GROUPS):
        if i == full_groups and full_groups != NUM_GROUPS:
            stride -= 1
        sector = dir_order[i // row_len]
        facing = as_facing(sector)
        x, _, z = facing.scale(2)
        move_facing = rotate_facing(facing, 90)
        sign_facing = rotate_facing(facing, 180)
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
                    WallSign((None, value.title()), (clear_menus, *func_gen(value)), wood='birch').place(
                        r(sx, sy, sz), sign_facing))
            return popup

        def summoner(mob_id):
            mob = my_mobs[mob_id]
            summon_mob = tuple(str(x) for x in summon_mob_commands(mob))
            setup = execute().if_().block(r(0, 1, 0), 'air').run(summon_mob)
            return *setup, follow_on(mob)

        def sign_pos(sign_num, x_base, y_base, z_base, matrix_row_len):
            sign_y = y_base - sign_num // matrix_row_len
            sign_x = x_base + (-1 + sign_num % matrix_row_len) * dx
            sign_z = z_base + (-1 + sign_num % matrix_row_len) * dz
            return sign_x, sign_y, sign_z

        def follow_on(mob):
            if not mob.name.endswith('Villager'):
                return None

            menu_matrix('type', VILLAGER_BIOMES, row_len, set_type)
            professions = list(VILLAGER_PROFESSIONS)
            if mob.name == 'Villager':
                professions.append('child')
            pro_popup = menu_matrix('profession', professions, 4, set_profession)
            return at_home.run(function(pro_popup))

        popup = menu_matrix(f'mob_menu_{i:02}', all_mobs[start:start + stride], row_len, summoner)

        x += (-1 + within) * dx
        z += (-1 + within) * dz
        menu_init.add(WallSign((None, all_mobs[start], Text.text('to').italic(), all_mobs[start + stride - 1]),
                               (clear_menus, at_home.run(function(popup)))).place(r(x, 2, z), sign_facing))

        start += stride
        within = (within + 1) % row_len

    room.function('sector_setup', home=False).add(
        execute().as_(e().tag('summon_cur')).run(tag(s()).remove('summon_cur')),
        fill(r(-5, 1, -5), r(5, 1, 5), 'redstone_lamp').replace('shroomlight'),
        setblock(r(0, 1, 0), 'shroomlight'))
