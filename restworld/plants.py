from __future__ import annotations

from pyker.commands import SOUTH, mc, r, Block, EQ, EAST, WEST, NORTH
from pyker.info import woods, tulips, small_flowers, stems
from pyker.simpler import WallSign, Volume
from restworld.friendlies import _to_id
from restworld.rooms import Room, label
from restworld.world import restworld, main_clock, fast_clock


def crop(stages, which, x, y, z, step, name='age'):
    for s in range(0, 3):
        yield mc.fill(r(x, y, z - s), r(x + 2, y, z - s), Block(which, {name: stages[(step.i + s) % len(stages)]}))
        yield mc.data().merge(r(x + 3, 2, z - 1), {'Text2': 'Stage: %d' % stages[(step.i + 1) % len(stages)]})


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
        yield mc.setblock(r(0, 3, 0), step.elem.id)
        yield mc.data().merge(r(1, 2, 0), step.elem.sign_nbt)

    room.loop('azalea', main_clock).loop(azalea_loop, (Block('Azalea'), Block('Flowering Azalea')))

    bamboo_funcs(room)

    def up_down(step, which):
        if step.elem == 0:
            yield mc.fill(r(0, 4, 0), r(0, 5, 0), 'air')
        elif step.elem == 1:
            yield mc.setblock(r(0, 4, 0), which)
            yield mc.setblock(r(0, 5, 0), 'air')
        else:
            yield mc.fill(r(0, 4, 0), r(0, 5, 0), which)

    def cactus_loop(step):
        yield from up_down(step, 'cactus')

    room.loop('cactus', main_clock).loop(cactus_loop, range(0, 3), bounce=True)
    room.loop('cactus_soil', main_clock).loop(lambda step: mc.setblock(r(0, 2, 1), step.elem), ('Sand', 'Red Sand'))

    def cane_loop(step):
        yield from up_down(step, 'Sugar Cane')

    room.function('cane_enter').add(room.score('cane').operation(EQ, room.score('cactus')))
    room.function('cane_init').add(
        WallSign((None, 'Sugar Cane')).place(r(-2, 2, 0), EAST),
        mc.setblock(r(-1, 2, -1), 'structure_void'),
        mc.setblock(r(-1, 2, 1), 'structure_void'),
        mc.setblock(r(-1, 2, 0), 'water'))
    room.loop('cane', main_clock).loop(cane_loop, range(0, 3), bounce=True)
    room.loop('cane_soil', main_clock).loop(lambda step: mc.setblock(r(0, 2, 1), step.elem), (
        'Grass Block', 'Dirt', 'Coarse Dirt', 'Podzol', 'Sand', 'Red Sand', 'Moss Block', 'Mycelium', 'Mud'))
    room.function('cave_vines_init').add(label(r(0, 2, -1), 'Cave Vine Age 25'))
    cave_vines_tops = room.score('cave_vines_tops')

    def cave_vines_loop(step):
        yield mc.setblock(r(0, 3, 0), Block('cave_vines_plant', {'berries': step.elem[1]}))
        yield mc.execute().unless().score(cave_vines_tops).matches(1).run().setblock(r(0, 2, 0), Block('cave_vines', {
            'berries': step.elem[0]}))
        yield mc.execute().if_().score(cave_vines_tops).matches(1).run().setblock(r(0, 2, 0), Block('cave_vines', {
            'berries': step.elem[0], 'age': 25}))

    room.loop('cave_vines', main_clock).loop(cave_vines_loop,
                                             ((True, True), (True, False), (False, False), (False, True)))
    room.function('chorus_plant_init').add(WallSign((None, 'Chorus Plant')).place(r(1, 2, 0), EAST))

    def cocoa_loop(step):
        yield mc.setblock(r(1, 4, 0), ('cocoa', {'age': step.elem, 'facing': WEST}))
        yield mc.setblock(r(-1, 4, 0), ('cocoa', {'age': step.elem, 'facing': EAST}))
        yield mc.setblock(r(0, 4, 1), ('cocoa', {'age': step.elem, 'facing': NORTH}))
        yield mc.setblock(r(0, 4, -1), ('cocoa', {'age': step.elem, 'facing': SOUTH}))
        yield mc.data().merge(r(1, 2, 0), {'Text2': 'Stage: %d' % step.i})

    room.loop('cocoa', main_clock).loop(cocoa_loop, range(0, 3), bounce=True)
    room.function('coral_init').add(WallSign(()).place(r(0, 2, -2), WEST, water=True))

    volume = Volume(r(-1, 2, -5), r(1, 4, 1))
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
        yield mc.data().merge(r(0, 2, -2), {'Text2': step.elem})

    room.loop('coral', main_clock).loop(coral_loop, ('Brain', 'Bubble', 'Fire', 'Horn', 'Tube'))
    room.loop('dead_bush_soil', main_clock).loop(lambda step: mc.setblock(r(0, 2, 1), step.elem),
                                                 ('Sand', 'Red Sand', 'Terracotta', 'Dirt', 'Podzol', 'Mud'))
    room.function('dripleaf_init').add(WallSign(()).place(r(1, 2, 0), EAST))

    tilts = ('none', 'unstable', 'partial', 'full')
    upper = tuple(Block('Big Dripleaf', {'tilt': x, 'facing': EAST}) for x in tilts) + (
        Block('Small Dripleaf', {'half': 'upper', 'facing': EAST}),)
    lower = tuple((Block('Big Dripleaf Stem', {'facing': EAST}),)) * (len(upper) - 1) + (
        Block('Small Dripleaf', {'half': 'lower', 'facing': EAST}),)

    def dripleaf_loop(step):
        i = step.i
        yield mc.setblock(r(1, 2, 0), 'air')
        yield mc.setblock(r(0, 3, 0), 'air')
        yield mc.setblock(r(0, 2, 0), 'air')
        yield mc.setblock(r(0, 2, 0), lower[i])
        yield mc.setblock(r(0, 3, 0), upper[i])
        yield mc.data().merge(r(1, 2, 0), {'Text3': 'Tilt: %s' % tilts[i].title() if i < len(tilts) else ''})

    room.loop('dripleaf', main_clock).loop(dripleaf_loop, upper)
    room.loop('dripleaf_soil', main_clock).loop(lambda step: mc.setblock(r(0, 1, 1), step.elem),
                                                ('Clay', 'Moss Block'))

    def farmland_loop(step):
        for i in range(0, 8):
            yield mc.setblock(r(0, 1, i), ('farmland', {'moisture': 7 - i}))
            yield mc.setblock(r(0, 1, -i), ('farmland', {'moisture': 7 - i}))

    room.loop('farmland_strip', main_clock).loop(farmland_loop, range(0, 1))
    kelp_init = room.function('kelp_init').add(mc.fill(r(0, 2, 0), r(2, 6, 0), 'water'))
    for x in range(0, 3):
        kelp_init.add(mc.fill(r(x, 2, 0), r(x, 5, 0), 'kelp'))
        if x > 0:
            kelp_init.add(mc.setblock(r(x, 6, 0), ('kelp', {'age': 25})))
    room.function('lily_pad_init').add(WallSign((None, 'Lily Pad')).place(r(0, 2, 0), WEST))

    def mushroom_loop(step):
        yield mc.data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': 'restworld:%s_mushroom' % step.elem})
        yield mc.setblock(r(-1, -1, -1), 'redstone_block')
        yield mc.setblock(r(-1, -1, -1), 'air')

    room.loop('mushrooms', main_clock).loop(mushroom_loop, ('red', 'brown'))

    def pottable_loop(step):
        if isinstance(step.elem, str):
            step.elem = Block(step.elem)
        sign_nbt = step.elem.sign_nbt
        if sign_nbt['Text1'] == '':
            sign_nbt['Text1'] = 'Potted'
        else:
            sign_nbt['Text1'] = 'Potted ' + sign_nbt['Text1']
        yield mc.setblock(r(0, 3, 0), 'potted_%s' % step.elem.id)
        yield mc.data().merge(r(1, 2, 0), sign_nbt)

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
        mc.setblock(r(0, 5, 0), 'mangrove_leaves'),
        WallSign(('Mangrove', 'Propagule', 'Stage:  N', '(vanila shows 4)')).place(r(1, 2, 0), EAST))

    def propagule_loop(step):
        yield mc.setblock(r(0, 4, 0), ('mangrove_propagule', {'hanging': True, 'age': step.elem}))
        yield mc.data().merge(r(1, 2, 0), {'Text3': 'Stage %d' % step.elem})

    room.loop('propagule', main_clock).loop(propagule_loop, range(0, 4))

    def sea_pickles_loop(step):
        yield mc.setblock(r(0, 3, 0), ('sea_pickle', {'pickles': step.elem}))
        yield mc.setblock(r(0, 3, -2), ('sea_pickle', {'waterlogged': False, 'pickles': step.elem}))

    room.loop('sea_pickles', main_clock).loop(sea_pickles_loop, range(1, 4))

    room.function('shrooms_init').add(label(r(1, 2, 1), 'Vine Age 25'))

    def shrooms_loop(step):
        yield mc.data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': 'restworld:%s_shroom' % step.elem})
        yield mc.setblock(r(-1, -1, -1), 'redstone_block')
        yield mc.setblock(r(-1, -1, -1), 'air')
        shrooms_tops = room.score('shrooms_tops')
        vines = 'weeping_vines' if step.elem == 'crimson' else 'twisting_vines'
        yield mc.execute().unless().score(shrooms_tops).matches(1).run().setblock(r(1, 3, 0), (vines, {'age': 0}))
        yield mc.execute().if_().score(shrooms_tops).matches(1).run().setblock(r(1, 3, 0), (vines, {'age': 25}))

    room.loop('shrooms', main_clock).loop(shrooms_loop, ('crimson', 'warped'))

    def stems_loop(step):
        yield mc.setblock(r(0, 3, -2), 'air')
        yield mc.setblock(r(2, 3, -2), 'air')
        i = step.i
        if i < 8:
            yield mc.setblock(r(0, 3, -1), ('pumpkin_stem', {'age': i}))
            yield mc.setblock(r(2, 3, -1), ('melon_stem', {'age': i}))
            yield mc.data().merge(r(3, 2, -1), {'Text2': 'Stage: %d' % i})
        else:
            yield mc.setblock(r(0, 3, -2), 'pumpkin')
            yield mc.setblock(r(2, 3, -2), 'melon')
            yield mc.setblock(r(0, 3, -1), ('attached_pumpkin_stem', {'facing': NORTH}))
            yield mc.setblock(r(2, 3, -1), ('attached_melon_stem', {'facing': NORTH}))
            yield mc.data().merge(r(3, 2, -1), {'Text2': 'Stage:  Attached'})

    room.loop('stems', main_clock).loop(stems_loop, range(0, 9))

    def sweet_berry_loop(step):
        yield mc.setblock(r(0, 3, 0), ('Sweet Berry Bush', {'age': step.elem}))
        yield mc.data().merge(r(1, 2, 0), {'Text2': 'Stage: %d' % step.elem})

    room.loop('sweet_berry', main_clock).loop(sweet_berry_loop, range(0, 4), bounce=True)
    room.loop('sweet_berry_soil', main_clock).loop(lambda step: mc.setblock(r(0, 2, 1), step.elem),
                                                   ('Grass Block', 'Dirt', 'Podzol', 'Coarse Dirt'))

    def trees_loop(step):
        yield mc.data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': 'restworld:%s_trees' % _to_id(step.elem)})
        yield mc.setblock(r(-1, -1, -1), 'redstone_block')
        yield mc.setblock(r(-1, -1, -1), 'air')
        yield WallSign((None, '%s Trees' % step.elem)).place(r(1, 2, 7), WEST)
        yield WallSign((None, 'Lilly')).place(r(4, 2, 15), WEST)

    room.loop('trees', main_clock).loop(trees_loop, woods)

    def tulips_loop(step):
        yield mc.setblock(r(0, 3, 0), '%s_tulip' % _to_id(step.elem))
        yield mc.data().merge(r(1, 2, 0), {'Text3': step.elem})
        yield mc.data().merge(r(-1, 2, 0), {'Text3': step.elem})

    room.loop('tulips', main_clock).loop(tulips_loop, tulips)


def bamboo_funcs(room):
    max = 6
    top = max - 1

    def bamboo_loop(step):
        if step.i == 0:
            yield mc.setblock(r(0, 3, 0), 'bamboo_sapling')
            yield mc.fill(r(0, 3 + top, 0), r(0, 4, 0), 'air')
        else:
            if step.elem < max:
                height = step.elem
            elif step.elem > max + 1:
                height = max - (step.elem - max) + 1
            else:
                height = max
            age = 0 if step.i <= max else 1
            yield mc.data().merge(r(1, 2, 0), {'Text3': 'Shoot' if step.i == 0 else 'Age: %d' % age})
            yield mc.fill(r(0, 3, 0), r(0, 3 + height - 1, 0), Block('bamboo', {'age': age, 'leaves': 'none'}))
            if height < max:
                yield mc.fill(r(0, 3 + max - 1, 0), r(0, 3 + height, 0), 'air')
            if height >= 2:
                yield mc.setblock(r(0, 3 + height - 1, 0), Block('bamboo', {'age': age, 'leaves': 'small'}))
            if height >= 3:
                yield mc.setblock(r(0, 3 + height - 2, 0), Block('bamboo', {'age': age, 'leaves': 'large'}))

    room.loop('bamboo', main_clock).loop(bamboo_loop, range(0, 2 * max + 1))
    room.loop('bamboo_soil', main_clock).loop(lambda step: mc.setblock(r(0, 2, 1), step.elem), (
        'Grass Block', 'Dirt', 'Coarse Dirt', 'Rooted Dirt', 'Podzol', 'Sand', 'Moss Block', 'Mycelium', 'Red Sand',
        'Mud'))
