from __future__ import annotations

from pynecraft.base import EAST, NORTH, SOUTH, WEST, r, to_id, to_name
from pynecraft.commands import Block, data, e, execute, fill, fillbiome, function, kill, setblock, tag
from pynecraft.enums import BiomeId
from pynecraft.info import small_flowers, stems, tulips, woods
from pynecraft.simpler import Region, Sign, WallSign
from restworld.rooms import Room, label
from restworld.world import fast_clock, main_clock, restworld


def crop(stages, which, x, y, z, step, name='age'):
    for s in range(0, 3):
        yield fill(r(x, y, z - s), r(x + 2, y, z - s), Block(which, {name: stages[(step.i + s) % len(stages)]}))
        yield data().merge(r(x + 3, 2, z - 1), {'Text2': 'Stage: %d' % stages[(step.i + 1) % len(stages)]})


def room():
    room = Room('plants', restworld, SOUTH, ('Plants,', 'Mob Effects,', 'Particles,', 'Fonts'))

    stages_4 = list(range(0, 4)) + [3, 3]

    def crops_4_loop(step):
        yield from crop(stages_4, 'beetroots', 0, 3, 0, step)
        yield from crop(stages_4, 'nether_wart', 0, 3, -15, step)

    room.loop('4_crops', main_clock).loop(crops_4_loop, stages_4)

    stages_6 = list(range(0, 6)) + [5, 5]
    room.loop('6_crops', main_clock).loop(lambda step: crop(stages_6, 'chorus_flower', 0, 3, 0, step), stages_6)

    def crops_8_loop(step):
        yield from crop(stages_8, 'wheat', 0, 3, 0, step)
        yield from crop(stages_8, 'carrots', 0, 3, -5, step)
        yield from crop(stages_8, 'potatoes', 0, 3, -10, step)
        yield from crop(stages_8, 'farmland', 5, 2, -10, step, 'moisture')

    stages_8 = list(range(0, 8)) + [7, 7]
    room.loop('8_crops', main_clock).loop(crops_8_loop, stages_8)

    def azalea_loop(step):
        yield setblock(r(0, 3, 0), step.elem.id)
        yield data().merge(r(1, 2, 0), step.elem.sign_nbt)

    room.loop('azalea', main_clock).loop(azalea_loop, (Block('Azalea'), Block('Flowering Azalea')))

    bamboo_funcs(room)
    three_funcs(room)

    room.function('cave_vines_init').add(label(r(0, 2, -1), 'Cave Vine Age 25'))
    cave_vines_tops = room.score('cave_vines_tops')

    def cave_vines_loop(step):
        yield setblock(r(0, 3, 0), Block('cave_vines_plant', {'berries': step.elem[1]}))
        yield execute().unless().score(cave_vines_tops).matches(1).run(
            setblock(r(0, 2, 0), Block('cave_vines', {'berries': step.elem[0]})))
        yield execute().if_().score(cave_vines_tops).matches(1).run(
            setblock(r(0, 2, 0), Block('cave_vines', {'berries': step.elem[0], 'age': 25})))

    room.loop('cave_vines', main_clock).loop(cave_vines_loop,
                                             ((True, True), (True, False), (False, False), (False, True)))
    room.function('chorus_plant_init').add(WallSign((None, 'Chorus Plant')).place(r(1, 2, 0), EAST))

    def cocoa_loop(step):
        yield setblock(r(1, 4, 0), ('cocoa', {'age': step.elem, 'facing': WEST}))
        yield setblock(r(-1, 4, 0), ('cocoa', {'age': step.elem, 'facing': EAST}))
        yield setblock(r(0, 4, 1), ('cocoa', {'age': step.elem, 'facing': NORTH}))
        yield setblock(r(0, 4, -1), ('cocoa', {'age': step.elem, 'facing': SOUTH}))
        yield data().merge(r(1, 2, 0), {'Text2': 'Stage: %d' % step.i})

    room.loop('cocoa', main_clock).loop(cocoa_loop, range(0, 3), bounce=True)
    room.function('coral_init').add(WallSign((None, None, 'Coral')).place(r(0, 2, -2), WEST, water=True))

    volume = Region(r(-1, 2, -5), r(1, 4, 1))
    watered = {'waterlogged': True}

    def coral_loop(step):
        yield volume.replace(('%s Coral' % step.elem, watered), '#coral_plants', )
        yield volume.replace('%s Coral Block' % step.elem, '#coral_blocks')
        yield volume.replace(('%s Coral Fan' % step.elem, watered), '#restworld:coral_fans')
        yield volume.replace_facing(('%s Coral Wall Fan' % step.elem, watered), '#wall_corals')
        yield volume.replace(('Dead %s Coral' % step.elem, watered), '#restworld:dead_coral_plants', )
        yield volume.replace('Dead %s Coral Block' % step.elem, '#restworld:dead_coral_blocks')
        yield volume.replace(('Dead %s Coral Fan' % step.elem, watered), '#restworld:dead_coral_fans')
        yield volume.replace_facing(('Dead %s Coral Wall Fan' % step.elem, watered), '#restworld:dead_wall_corals')
        yield data().merge(r(0, 2, -2), {'Text2': step.elem})

    room.loop('coral', main_clock).loop(coral_loop, ('Brain', 'Bubble', 'Fire', 'Horn', 'Tube'))
    room.loop('dead_bush_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem),
                                                 ('Sand', 'Red Sand', 'Terracotta', 'Dirt', 'Podzol', 'Mud'))

    tilts = ('none', 'unstable', 'partial', 'full')
    upper = tuple(Block('Big Dripleaf', {'tilt': x, 'facing': EAST}) for x in tilts) + (
        Block('Small Dripleaf', {'half': 'upper', 'facing': EAST}),)
    lower = tuple((Block('Big Dripleaf Stem', {'facing': EAST}),)) * (len(upper) - 1) + (
        Block('Small Dripleaf', {'half': 'lower', 'facing': EAST}),)

    def dripleaf_loop(step):
        i = step.i
        yield setblock(r(0, 2, 0), lower[i])
        yield setblock(r(0, 3, 0), upper[i])
        text = (None, upper[i].name)
        if i < len(tilts):
            text = text + (f'Tilt: {tilts[i].title()}',)
        yield WallSign(text).place(r(1, 2, 0), EAST)

    room.loop('dripleaf', main_clock).add(
        setblock(r(1, 2, 0), 'air'),
        setblock(r(0, 3, 0), 'air'),
        setblock(r(0, 2, 0), 'air')).loop(dripleaf_loop, upper)
    room.loop('dripleaf_soil', main_clock).loop(lambda step: setblock(r(0, 1, 1), step.elem),
                                                ('Clay', 'Moss Block'))

    def farmland_loop(_):
        for i in range(0, 8):
            yield setblock(r(0, 1, i), ('farmland', {'moisture': 7 - i}))
            yield setblock(r(0, 1, -i), ('farmland', {'moisture': 7 - i}))

    room.loop('farmland_strip', main_clock).loop(farmland_loop, range(0, 1))
    kelp_init = room.function('kelp_init').add(fill(r(0, 2, 0), r(2, 6, 0), 'water'))
    for x in range(0, 3):
        kelp_init.add(fill(r(x, 2, 0), r(x, 5, 0), 'kelp'))
        if x > 0:
            kelp_init.add(setblock(r(x, 6, 0), ('kelp', {'age': 25})))
    room.function('lily_pad_init').add(WallSign((None, 'Lily Pad')).place(r(0, 2, 0), WEST))

    def mushroom_loop(step):
        yield data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': 'restworld:%s_mushroom' % step.elem})
        yield setblock(r(-1, -1, -1), 'redstone_block')
        yield setblock(r(-1, -1, -1), 'air')

    room.loop('mushrooms', main_clock).loop(mushroom_loop, ('red', 'brown'))

    def pottable_loop(step):
        if isinstance(step.elem, str):
            step.elem = Block(step.elem)
        sign_nbt = step.elem.sign_nbt
        if sign_nbt['Text1'] == '':
            sign_nbt['Text1'] = 'Potted'
        else:
            sign_nbt['Text1'] = 'Potted ' + sign_nbt['Text1']
        yield setblock(r(0, 3, 0), 'potted_%s' % step.elem.id)
        yield data().merge(r(1, 2, 0), sign_nbt)

    saplings = list(woods)
    misc = [
        Block('Brown Mushroom'),
        Block('Red Mushroom'),
        Block('Cactus'),
        Block('Dead Bush'),
        Block('Fern'),
        Block('Azalea Bush'), Block('Flowering Azalea Bush'),
        Block('Mangrove Propagule'),
    ]
    pottables = [Block('Mangrove|Propagule' if w == 'Mangrove' else '%s Sapling' % w) for w in saplings] + [
        Block('%s Tulip' % t) for t in tulips] + list(small_flowers) + misc + [Block('%s Roots' % x) for x in stems] + [
                    Block('%s Fungus' % x) for x in stems] + [Block('Wither Rose'), ]
    room.loop('pottable', fast_clock).loop(pottable_loop, pottables)
    room.function('propagule_init').add(
        setblock(r(0, 5, 0), 'mangrove_leaves'),
        WallSign(('Mangrove', 'Propagule', 'Stage:  N', '(vanilla shows 4)')).place(r(1, 2, 0), EAST))

    def propagule_loop(step):
        yield setblock(r(0, 4, 0), ('mangrove_propagule', {'hanging': True, 'age': step.elem}))
        yield data().merge(r(1, 2, 0), {'Text3': 'Stage %d' % step.elem})

    room.loop('propagule', main_clock).loop(propagule_loop, range(0, 4))

    def sea_pickles_loop(step):
        yield setblock(r(0, 3, 0), ('sea_pickle', {'pickles': step.elem}))
        yield setblock(r(0, 3, -2), ('sea_pickle', {'waterlogged': False, 'pickles': step.elem}))

    room.loop('sea_pickles', main_clock).loop(sea_pickles_loop, range(1, 4))

    room.function('shrooms_init').add(label(r(1, 2, 1), 'Vine Age 25'))

    def shrooms_loop(step):
        yield data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': 'restworld:%s_shroom' % step.elem})
        yield setblock(r(-1, -1, -1), 'redstone_block')
        yield setblock(r(-1, -1, -1), 'air')
        shrooms_tops = room.score('shrooms_tops')
        vines = 'weeping_vines' if step.elem == 'crimson' else 'twisting_vines'
        yield execute().unless().score(shrooms_tops).matches(1).run(setblock(r(1, 3, 0), (vines, {'age': 0})))
        yield execute().if_().score(shrooms_tops).matches(1).run(setblock(r(1, 3, 0), (vines, {'age': 25})))

    room.loop('shrooms', main_clock).loop(shrooms_loop, ('crimson', 'warped'))

    def stems_loop(step):
        yield setblock(r(0, 3, -2), 'air')
        yield setblock(r(2, 3, -2), 'air')
        i = step.i
        if i < 8:
            yield setblock(r(0, 3, -1), ('pumpkin_stem', {'age': i}))
            yield setblock(r(2, 3, -1), ('melon_stem', {'age': i}))
            yield data().merge(r(3, 2, -1), {'Text2': 'Stage: %d' % i})
        else:
            yield setblock(r(0, 3, -2), 'pumpkin')
            yield setblock(r(2, 3, -2), 'melon')
            yield setblock(r(0, 3, -1), ('attached_pumpkin_stem', {'facing': NORTH}))
            yield setblock(r(2, 3, -1), ('attached_melon_stem', {'facing': NORTH}))
            yield data().merge(r(3, 2, -1), {'Text2': 'Stage:  Attached'})

    room.loop('stems', main_clock).loop(stems_loop, range(0, 9))

    def sweet_berry_loop(step):
        yield setblock(r(0, 3, 0), ('Sweet Berry Bush', {'age': step.elem}))
        yield data().merge(r(1, 2, 0), {'Text2': 'Stage: %d' % step.elem})

    room.loop('sweet_berry', main_clock).loop(sweet_berry_loop, range(0, 4), bounce=True)
    room.loop('sweet_berry_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem),
                                                   ('Grass Block', 'Dirt', 'Podzol', 'Coarse Dirt'))

    tree_types = {'Acacia': BiomeId.SAVANNA, 'Birch': BiomeId.BIRCH_FOREST, 'Jungle': BiomeId.JUNGLE,
                  'Mangrove': BiomeId.MANGROVE_SWAMP, 'Oak': BiomeId.PLAINS, 'Dark Oak': BiomeId.DARK_FOREST,
                  'Spruce': BiomeId.SNOWY_TAIGA}

    def trees_loop(step):
        tree, biome = step.elem
        yield data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': f'restworld:{to_id(tree)}_trees'})
        yield setblock(r(-1, -1, -1), 'redstone_block')
        yield setblock(r(-1, -1, -1), 'air')
        yield WallSign((None, f'{tree} Trees', 'Biome:', to_name(str(biome)))).place(r(1, 2, 7), WEST)
        yield execute().at(e().tag('biome_home')).run(fillbiome(r(0, 1, 0), r(33, 5, 52), biome))
        yield fillbiome(r(0, 1, 0), r(18, 30, 17), biome)

    room.loop('trees', main_clock).loop(trees_loop, tree_types.items()).add(
        execute().at(e().tag('biome_home')).run(fill(r(0, 1, 0), r(33, 6, 52), 'water').replace('ice')),
        WallSign((None, 'Lilly')).place(r(4, 2, 15), WEST))
    room.function('biome')

    def tulips_loop(step):
        yield setblock(r(0, 3, 0), f'{to_id(step.elem)}_tulip')
        yield data().merge(r(1, 2, 0), {'Text3': step.elem})
        yield data().merge(r(-1, 2, 0), {'Text3': step.elem})

    room.loop('tulips', main_clock).loop(tulips_loop, tulips)


def three_funcs(room):
    def three_height_loop(step):
        def height(z, which):
            count = step.elem
            yield fill(r(0, 5, z), r(0, 5 - (1 - count), z), 'air')
            yield fill(r(0, 3, z), r(0, 3 + count, z), which)
            yield data().merge(r(1, 2, z), Sign.lines_nbt(('', to_name(which), '', '')))

        yield from height(0, 'cactus')
        yield from height(-3, 'sugar_cane')

    def three_age_loop(step):
        def age(z, which):
            age = step.elem
            yield setblock(r(0, 5, z), 'air')
            yield setblock(r(0, 4, z), f'{which}[age={age}]')
            yield data().merge(r(1, 2, z),
                               Sign.lines_nbt(
                                   (to_name(which), f'Top Block Age: {age}', '16 ages', '(vanilla shows 1)')))

        yield from age(0, 'cactus')
        yield from age(-3, 'sugar_cane')

    def switch_to_func(which):
        room.function(f'three_change_{which}', home=False).add(
            kill(e().tag('three_runner')),
            execute().at(e().tag('three_home')).positioned(r(-1, -0.5, 2)).run(
                function(f'restworld:plants/three_{which}_home')),
            tag(e().tag(f'three_{which}_home')).add('three_runner'),
            execute().at(e().tag(f'three_{which}_home')).run(function(f'restworld:plants/three_{which}_cur')))

    room.loop('three_height', main_clock).loop(three_height_loop, range(3), bounce=True)
    room.loop('three_age', fast_clock).add(
        fill(r(0, 5, 0), (0, 5, -3), 'air'),
        setblock(r(0, 3, 0), 'cactus'),
        setblock(r(0, 3, -3), 'sugar_cane')
    ).loop(three_age_loop, range(16))
    room.function('three_init').add(label(r(-1, 2, 0), 'Change Age'))
    switch_to_func('height')
    switch_to_func('age')
    room.loop('cactus_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem), ('Sand', 'Red Sand'))
    room.loop('cane_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem), (
        'Grass Block', 'Dirt', 'Coarse Dirt', 'Podzol', 'Sand', 'Red Sand', 'Moss Block', 'Mycelium', 'Mud'))
    room.function('cane_init').add(
        function('restworld:plants/three_change_height'),
        WallSign((None, 'Sugar Cane')).place(r(-2, 2, 0), EAST),
        setblock(r(-1, 2, -1), 'structure_void'),
        setblock(r(-1, 2, 1), 'structure_void'),
        setblock(r(-1, 2, 0), 'water'))


def bamboo_funcs(room):
    max = 6
    top = max - 1

    def bamboo_loop(step):
        if step.i == 0:
            yield setblock(r(0, 3, 0), 'bamboo_sapling')
            yield fill(r(0, 3 + top, 0), r(0, 4, 0), 'air')
        else:
            if step.elem < max:
                height = step.elem
            elif step.elem > max + 1:
                height = max - (step.elem - max) + 1
            else:
                height = max
            age = 0 if step.i <= max else 1
            yield data().merge(r(1, 2, 0), {'Text3': 'Shoot' if step.i == 0 else f'Age: {age:d}'})
            yield fill(r(0, 3, 0), r(0, 3 + height - 1, 0), Block('bamboo', {'age': age, 'leaves': 'none'}))
            if height < max:
                yield fill(r(0, 3 + max - 1, 0), r(0, 3 + height, 0), 'air')
            if height >= 2:
                yield setblock(r(0, 3 + height - 1, 0), Block('bamboo', {'age': age, 'leaves': 'small'}))
            if height >= 3:
                yield setblock(r(0, 3 + height - 2, 0), Block('bamboo', {'age': age, 'leaves': 'large'}))

    room.loop('bamboo', main_clock).loop(bamboo_loop, range(0, 2 * max + 1))
    room.loop('bamboo_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem), (
        'Grass Block', 'Dirt', 'Coarse Dirt', 'Rooted Dirt', 'Podzol', 'Sand', 'Moss Block', 'Mycelium', 'Red Sand',
        'Mud'))
