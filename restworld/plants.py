from __future__ import annotations

from typing import Callable

from pynecraft import info
from pynecraft.base import EAST, NORTH, Nbt, SOUTH, WEST, r, to_id, to_name
from pynecraft.commands import Block, JsonText, data, e, execute, fill, fillbiome, function, kill, setblock, tag
from pynecraft.info import small_flowers, stems, tulips
from pynecraft.simpler import JUNGLE, PLAINS, Region, SAVANNA, Sign, WallSign
from pynecraft.values import BIRCH_FOREST, DARK_FOREST, MANGROVE_SWAMP, SNOWY_TAIGA
from restworld.rooms import Room, label
from restworld.world import fast_clock, main_clock, restworld, text_display


def crop(stages, which: str | Callable[[int, str], Block], x, y, z, step, name='age', extra=None):
    base_state = Nbt.as_nbt(extra) if extra else Nbt()
    for s in range(0, 3):
        stage = stages[((step.i + s) % len(stages))]
        if isinstance(which, str):
            block = Block(which, base_state.merge({name: stage}))
        else:
            block = which(stage, name)
        yield fill(r(x, y, z - s), r(x + 2, y, z - s), block)
    if z == 0:
        yield Sign.change(r(x + 3, 2, -1),
                          (None, None, f'{name.title()}: {stages[(step.i + 1) % len(stages)]} of {step.count - 2}'))


def room():
    room = Room('plants', restworld, SOUTH, ('Plants,', 'Mob Effects,', 'Particles,', 'Fonts'))

    stages_3 = list(range(0, 3)) + [2, 2]

    def torchflower_crop(stage: int, name: str) -> Block:
        if stage >= 2:
            return Block('torchflower')
        else:
            return Block('torchflower_crop', {name: stage})

    def crops_3_loop(step):
        yield from crop(stages_3, torchflower_crop, 0, 3, 0, step)

    room.loop('3_crops', main_clock).loop(crops_3_loop, stages_3)

    stages_4 = list(range(0, 4)) + [3, 3]

    def crops_4_loop(step):
        yield from crop(stages_4, 'beetroots', 0, 3, 0, step)
        yield from crop(stages_4, 'nether_wart', -5, 3, -15, step)

    room.loop('4_crops', main_clock).loop(crops_4_loop, stages_4)

    def pitcher_crop(stage: int, name: str) -> Block:
        if stage < 3:
            return Block('air')
        else:
            return Block('pitcher_crop', {name: stage, 'half': 'upper'})

    stages_5_upper = list(range(0, 5)) + [4, 4]
    stages_5_lower = list(range(0, 5)) + [4, 4]

    def crops_5_loop(step):
        yield from crop(stages_5_upper, pitcher_crop, 0, 4, 0, step, name='age', extra={'half': 'upper'})
        yield from crop(stages_5_lower, 'pitcher_crop', 0, 3, 0, step, name='age', extra={'half': 'lower'})

    # setting the top block to air drops a pitcher plant, the kill removes them.
    room.loop('5_crops', main_clock).loop(crops_5_loop, stages_5_upper).add(
        kill(e().nbt({'Item': {'id': 'minecraft:pitcher_plant'}})))

    def crops_8_loop(step):
        yield from crop(stages_8, 'wheat', 0, 3, 0, step)
        yield from crop(stages_8, 'carrots', 0, 3, -5, step)
        yield from crop(stages_8, 'potatoes', 0, 3, -10, step)

    stages_8 = list(range(0, 8)) + [7, 7]
    room.loop('8_crops', main_clock).loop(crops_8_loop, stages_8)

    def azalea_loop(step):
        yield setblock(r(0, 3, 0), step.elem.id)
        yield data().merge(r(1, 2, 0), step.elem.sign_nbt())

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

    def chorus_flower_loop(step):
        yield setblock(r(0, 3, 0), ('chorus_flower', {'age': step.i}))
        yield Sign.change(r(1, 2, 0), (None, None, f'Age: {step.i} of 6'))

    room.function('chorus_flower_init').add(
        setblock(r(0, 2, 0), 'chorus_plant'),
        WallSign((None, 'Chorus Flower', None, '(vanilla shows 2)')).place(r(1, 2, 0), EAST))
    room.loop('chorus_flower', main_clock).loop(chorus_flower_loop, range(6))

    def cocoa_loop(step):
        yield setblock(r(1, 4, 0), ('cocoa', {'age': step.elem, 'facing': WEST}))
        yield setblock(r(-1, 4, 0), ('cocoa', {'age': step.elem, 'facing': EAST}))
        yield setblock(r(0, 4, 1), ('cocoa', {'age': (step.elem + 1) % step.count, 'facing': NORTH}))
        yield setblock(r(0, 4, -1), ('cocoa', {'age': (step.elem + 2) % step.count, 'facing': SOUTH}))
        yield Sign.change(r(1, 2, 0), (None, None, 'Stage: %d of 3' % step.stage))

    room.loop('cocoa', main_clock).loop(cocoa_loop, range(0, 3), bounce=True)

    room.loop('dead_bush_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem),
                                                 ('Sand', 'Red Sand', 'Terracotta', 'Dirt', 'Podzol', 'Mud',
                                                  'Moss Block'))

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

    room.loop('farmland_strip', main_clock).loop(farmland_loop, range(0, 1)).add(
        kill(e().type('item').nbt({'Item': {'id': 'minecraft:pitcher_pod'}}))
    )
    farmland_init = room.function('farmland_strip_init').add(
        kill(e().tag('farmland_strip_labels')),
        label(r(-3, 2, 0), 'Moisture Values')
    )

    farmland_init.add(text_display('Moisture').tag('farmland_strip_labels').summon(r(0, 2.3, 0)))
    for i in range(0, 8):
        td = text_display(str(7 - i)).tag('farmland_strip_labels')
        farmland_init.add(td.summon(r(0, 2.1, i)))
        farmland_init.add(td.summon(r(0, 2.1, -i)))

    room.function('lily_pad_init').add(WallSign((None, 'Lily Pad')).place(r(0, 2, 0), WEST))

    def mushroom_loop(step):
        yield data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': 'restworld:%s_mushroom' % step.elem})
        yield setblock(r(-1, -1, -1), 'redstone_block')
        yield setblock(r(-1, -1, -1), 'air')

    room.loop('mushrooms', main_clock).loop(mushroom_loop, ('red', 'brown'))

    def pottable_loop(step):
        if isinstance(step.elem, str):
            step.elem = Block(step.elem)
        sign_nbt = step.elem.sign_nbt()

        base_text = sign_nbt['front_text']['messages'][0]['text']
        if base_text == '':
            sign_nbt['front_text']['messages'][0] = JsonText.text('Potted')
        else:
            sign_nbt['front_text']['messages'][0] = JsonText.text('Potted ' + base_text)
        if len(sign_nbt['front_text']['messages'][3]['text']) == 0:
            sign_nbt['front_text']['messages'] = (JsonText.text(''),) + tuple(sign_nbt['front_text']['messages'][:-1])
        yield setblock(r(0, 3, 0), 'potted_%s' % step.elem.id)
        yield data().merge(r(1, 2, 0), sign_nbt)

    saplings = list(info.woods)
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
                    Block('%s Fungus' % x) for x in stems] + [Block('Torchflower'), Block('Wither Rose')]
    try:
        pottables[pottables.index(Block('Bamboo Sapling'))] = Block('Bamboo')
    except ValueError:
        pass  # if it's not there, that's OK
    room.loop('pottable', fast_clock).loop(pottable_loop, pottables)
    room.function('propagule_init').add(
        setblock(r(0, 5, 0), 'mangrove_leaves'),
        WallSign(('Mangrove', 'Propagule', 'Stage: N of 4', '(vanilla shows 4)')).place(r(1, 2, 0), EAST))

    def propagule_loop(step):
        yield setblock(r(0, 4, 0), ('mangrove_propagule', {'hanging': True, 'age': step.stage}))
        yield Sign.change(r(1, 2, 0), (None, None, 'Stage: %d of 4' % step.stage))

    room.loop('propagule', main_clock).loop(propagule_loop, range(4))

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
            yield Sign.change(r(3, 2, -1), (None, None, f'Stage: {i} of {step.count}'))
        else:
            yield setblock(r(0, 3, -2), 'pumpkin')
            yield setblock(r(2, 3, -2), 'melon')
            yield setblock(r(0, 3, -1), ('attached_pumpkin_stem', {'facing': NORTH}))
            yield setblock(r(2, 3, -1), ('attached_melon_stem', {'facing': NORTH}))
            yield Sign.change(r(3, 2, -1), (None, None, 'Stage:  Attached'))

    room.loop('stems', main_clock).loop(stems_loop, range(0, 9))

    def sweet_berry_loop(step):
        yield setblock(r(0, 3, 0), ('Sweet Berry Bush', {'age': step.elem}))
        yield Sign.change(r(1, 2, 0), (None, None, f'Age: {step.elem} of {step.count}'))

    room.loop('sweet_berry', main_clock).loop(sweet_berry_loop, range(0, 4), bounce=True)
    room.loop('sweet_berry_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem),
                                                   ('Grass Block', 'Dirt', 'Podzol', 'Coarse Dirt'))

    tree_types = {
        'Acacia': SAVANNA, 'Birch': BIRCH_FOREST, 'Cherry': "cherry_grove", 'Jungle': JUNGLE,
        'Mangrove': MANGROVE_SWAMP, 'Oak': PLAINS, 'Dark Oak': DARK_FOREST, 'Spruce': SNOWY_TAIGA
    }

    def trees_loop(step):
        tree, biome = step.elem
        yield data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': f'restworld:{to_id(tree)}_trees'})
        yield setblock(r(-1, -1, -1), 'redstone_block')
        yield setblock(r(-1, -1, -1), 'air')
        yield WallSign((None, f'{tree} Trees', 'Biome:', to_name(str(biome)))).place(r(1, 2, 7), WEST)
        plant_room = Region(r(0, -5, -1), r(33, 10, 52))
        yield execute().at(e().tag('plants_room_beg_home')).run(plant_room.fillbiome(biome),
                                                                plant_room.fill('air', replace='snow'))
        # Fill the tall tree area
        yield fillbiome(r(0, 8, 0), r(18, 30, 17), biome)

    room.loop('trees', main_clock).loop(trees_loop, tree_types.items()).add(
        execute().at(e().tag('plants_room_beg_home')).run(fill(r(0, 1, 0), r(33, 6, 52), 'water').replace('ice')),
        WallSign((None, 'Lilly')).place(r(4, 2, 15), WEST))

    def tulips_loop(step):
        yield setblock(r(0, 3, 0), f'{to_id(step.elem)}_tulip')
        yield Sign.change(r(1, 2, 0), (None, step.elem))

    room.loop('tulips', main_clock).loop(tulips_loop, tulips)


def three_funcs(room):
    def three_height_loop(step):
        def height(z, which):
            count = step.elem
            yield fill(r(0, 5, z), r(0, 5 - (1 - count), z), 'air')
            yield fill(r(0, 3, z), r(0, 3 + count, z), which)
            yield data().merge(r(1, 2, z), {'front_text': Sign.lines_nbt(('', to_name(which), '', ''))})

        yield from height(0, 'cactus')
        yield from height(-3, 'sugar_cane')

    def three_age_loop(step):
        def age(z, which):
            age = step.elem
            yield setblock(r(0, 5, z), 'air')
            yield setblock(r(0, 4, z), f'{which}[age={age}]')
            yield data().merge(r(1, 2, z),
                               {'front_text': Sign.lines_nbt(
                                   (None, to_name(which), f'Top Age: {age} of 16', '(vanilla shows 1)'))})

        yield from age(0, 'cactus')
        yield from age(-3, 'sugar_cane')

    def switch_to_func(which):
        room.function(f'three_change_{which}', home=False).add(kill(e().tag('three_runner')),
                                                               execute().at(e().tag('three_home')).positioned(
                                                                   r(-1, -0.5, 2)).run(
                                                                   function(f'restworld:plants/three_{which}_home')),
                                                               tag(e().tag(f'three_{which}_home')).add('three_runner'),
                                                               execute().at(e().tag(f'three_{which}_home')).run(
                                                                   function(f'restworld:plants/three_{which}_cur')))

    room.loop('three_height', main_clock).loop(three_height_loop, range(3), bounce=True)
    room.loop('three_age', fast_clock).add(fill(r(0, 5, 0), r(0, 5, -3), 'air'), setblock(r(0, 3, 0), 'cactus'),
                                           setblock(r(0, 3, -3), 'sugar_cane')).loop(three_age_loop, range(16))
    room.function('three_init').add(label(r(-1, 2, 0), 'Change Age'))
    switch_to_func('height')
    switch_to_func('age')
    room.loop('cactus_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem), ('Sand', 'Red Sand'))
    room.loop('cane_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem), (
        'Grass Block', 'Dirt', 'Coarse Dirt', 'Podzol', 'Sand', 'Red Sand', 'Moss Block', 'Mycelium', 'Mud'))
    room.function('cane_init').add(function('restworld:plants/three_change_height'),
                                   WallSign((None, 'Sugar Cane')).place(r(-2, 2, 0), EAST),
                                   setblock(r(-1, 2, -1), 'structure_void'), setblock(r(-1, 2, 1), 'structure_void'),
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
            yield Sign.change(r(1, 2, 0), (None, None, 'Shoot' if step.i == 0 else f'Age: {age:d} of 2'))
            yield fill(r(0, 3, 0), r(0, 3 + height - 1, 0), Block('bamboo', {'age': age, 'leaves': 'none'}))
            if height < max:
                yield fill(r(0, 3 + max - 1, 0), r(0, 3 + height, 0), 'air')
            if height >= 2:
                yield setblock(r(0, 3 + height - 1, 0), Block('bamboo', {'age': age, 'leaves': 'small'}))
            if height >= 3:
                yield setblock(r(0, 3 + height - 2, 0), Block('bamboo', {'age': age, 'leaves': 'large'}))

    room.loop('bamboo', main_clock).loop(bamboo_loop, range(0, 2 * max + 1))
    room.loop('bamboo_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem), (
        'Grass Block', 'Dirt', 'Coarse Dirt', 'Rooted Dirt', 'Podzol', 'Sand', 'Gravel', 'Moss Block', 'Mycelium',
        'Red Sand', 'Mud'))

    water_funcs(room)


def water_funcs(room):
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
        yield Sign.change(r(0, 2, -2), (None, step.elem))

    room.loop('coral', main_clock).loop(coral_loop, ('Brain', 'Bubble', 'Fire', 'Horn', 'Tube'))
    room.function('coral_init').add(WallSign((None, None, 'Coral')).glowing(True).place(r(0, 2, -2), WEST, water=True))

    kelp_init = room.function('kelp_init').add(fill(r(0, 2, 0), r(2, 6, 0), 'water'))
    for x in range(0, 3):
        kelp_init.add(fill(r(x, 2, 0), r(x, 5, 0), 'kelp'))
        if x > 0:
            kelp_init.add(setblock(r(x, 6, 0), ('kelp', {'age': 25})))

    def sea_pickles_loop(step):
        yield setblock(r(0, 3, 0), ('sea_pickle', {'pickles': step.elem}))
        yield setblock(r(0, 3, -2), ('sea_pickle', {'waterlogged': False, 'pickles': step.elem}))

    room.loop('sea_pickles', main_clock).loop(sea_pickles_loop, range(1, 4))
