from __future__ import annotations

from typing import Callable

from titlecase import titlecase

from pynecraft import info
from pynecraft.base import EAST, NORTH, Nbt, SOUTH, WEST, r, to_id, to_name
from pynecraft.commands import Block, Text, data, e, execute, fill, function, kill, setblock, tag
from pynecraft.info import small_flowers, stems, tulips
from pynecraft.simpler import JUNGLE, PLAINS, Region, SAVANNA, Sign, WallSign
from pynecraft.values import BIRCH_FOREST, CHERRY_GROVE, DARK_FOREST, MANGROVE_SWAMP, PALE_GARDEN, SNOWY_TAIGA
from restworld.rooms import Room, erase
from restworld.world import fast_clock, main_clock, restworld, slow_clock, text_display


def room():
    room = Room('plants', restworld, SOUTH, ('Plants,', 'Mob Effects,', 'Particles,', 'Fonts'))

    def crop(stages, which: str | Callable[[int, str], Block], x, y, z, step, name='age', extra=None):
        base_state = Nbt.as_nbt(extra) if extra else Nbt()
        for s in range(0, 3):
            stage = stages[((step.i + s) % len(stages))]
            if isinstance(which, str):
                block = Block(which, base_state.merge({name: stage}))
            else:
                block = which(stage, name)
                if block is None:
                    continue
            yield fill(r(x, y, z - s), r(x + 2, y, z - s), block)
            room.particle(block, step.loop.name.replace('_main', ''), r(x + 1, 4, z - s), step)
        yield Sign.change(r(x + 3, 2, z - 1),
                          (None, None, f'{titlecase(name)}: {stages[(step.i + 1) % len(stages)]} of {step.count - 2}'))

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

    def pitcher_crop(stage: int, name: str) -> Block | None:
        if stage < 3:
            return None
        else:
            return Block('pitcher_crop', {name: stage, 'half': 'upper'})

    stages_5_upper = list(range(0, 5)) + [4, 4]
    stages_5_lower = list(range(0, 5)) + [4, 4]

    def crops_5_loop(step):
        yield from crop(stages_5_lower, 'pitcher_crop', 0, 3, 0, step, name='age', extra={'half': 'lower'})
        yield from crop(stages_5_upper, pitcher_crop, 0, 4, 0, step, name='age', extra={'half': 'upper'})

    # setting the top block to air drops a pitcher plant, the kill removes them.
    room.loop('5_crops', main_clock).add(erase(r(0, 3, 0), r(2, 4, -2))).loop(crops_5_loop, stages_5_upper).add(
        kill(e().nbt({'Item': {'id': 'minecraft:pitcher_plant'}})))

    stages_8 = list(range(0, 8)) + [7, 7]

    def crops_8_loop(step):
        yield from crop(stages_8, 'wheat', 0, 3, 0, step)
        yield from crop(stages_8, 'carrots', 0, 3, -5, step)
        yield from crop(stages_8, 'potatoes', 0, 3, -10, step)

    room.loop('8_crops', main_clock).loop(crops_8_loop, stages_8)

    def azalea_loop(step):
        yield setblock(r(0, 3, 0), step.elem.id)
        yield data().merge(r(1, 2, 0), step.elem.sign_nbt())
        room.particle(step.elem.id, 'azalea', r(0, 4, 0), step)

    room.loop('azalea', main_clock).loop(azalea_loop, (Block('Azalea'), Block('Flowering Azalea')))
    room.particle('moss_block', 'azalea', r(0, 4, 2))

    bamboo_funcs(room)
    three_funcs(room)

    room.function('cave_vines_init').add(room.label(r(0, 2, -1), 'Cave Vine Age 25', EAST))
    cave_vines_tops = room.score('cave_vines_tops')

    def cave_vines_loop(step):
        yield setblock(r(0, 3, 0), Block('cave_vines_plant', {'berries': step.elem[1]}))
        yield execute().unless().score(cave_vines_tops).matches(1).run(
            setblock(r(0, 2, 0), Block('cave_vines', {'berries': step.elem[0]})))
        yield execute().if_().score(cave_vines_tops).matches(1).run(
            setblock(r(0, 2, 0), Block('cave_vines', {'berries': step.elem[0], 'age': 25})))

    room.loop('cave_vines', main_clock).loop(cave_vines_loop,
                                             ((True, True), (True, False), (False, False), (False, True)))
    room.particle('cave_vines', 'cave_vines', r(0, 3, 0))
    room.particle('glow_lichen', 'cave_vines', r(0, 3, 2))
    room.particle('spore_blossom', 'cave_vines', r(0, 4.5, 2))
    room.particle('rooted_dirt', 'cave_vines', r(0, 5, 4))
    room.particle('hanging_roots', 'cave_vines', r(0, 3.5, 4))
    room.particle('azalea_leaves', 'cave_vines', r(-1, 7, 0))
    room.particle('flowering_azalea_leaves', 'cave_vines', r(-1, 7, 1))

    room.function('chorus_plant_init').add(WallSign((None, 'Chorus Plant')).place(r(1, 2, 0), EAST))
    room.particle('Chorus Plant', 'chorus_plant', r(-1, 4, 1))

    def chorus_flower_loop(step):
        spec = Block('chorus_flower', {'age': step.i})
        yield setblock(r(0, 3, 0), spec)
        room.particle(spec, 'chorus_flower', r(0, 4, 0), step)
        yield Sign.change(r(1, 2, 0), (None, None, f'Age: {step.i} of 6'))

    room.function('chorus_flower_init').add(
        setblock(r(0, 2, 0), 'chorus_plant'),
        WallSign((None, 'Chorus Flower', None, '(vanilla shows 2)')).place(r(1, 2, 0), EAST))
    room.loop('chorus_flower', main_clock).loop(chorus_flower_loop, range(6))

    def cocoa_loop(step):
        def pod(pos, dir, plus):
            pod_spec = Block('cocoa', {'age': (step.elem + plus) % step.count, 'facing': dir})
            yield setblock(pos, pod_spec)
            room.particle(pod_spec, 'cocoa', (pos[0], pos[1] + 1, pos[2]), step)

        yield from pod(r(1, 4, 0), WEST, 0)
        yield from pod(r(-1, 4, 0), EAST, 0)
        yield from pod(r(0, 4, 1), NORTH, 1)
        yield from pod(r(0, 4, -1), SOUTH, 2)
        yield Sign.change(r(1, 2, 0), (None, None, 'Stage: %d of 3' % step.stage))

    room.loop('cocoa', main_clock).loop(cocoa_loop, range(0, 3), bounce=True)

    tilts = ('none', 'unstable', 'partial', 'full')
    upper = tuple(Block('Big Dripleaf', {'tilt': x, 'facing': EAST}) for x in tilts) + (
        Block('Small Dripleaf', {'half': 'upper', 'facing': EAST}),)
    lower = tuple((Block('Big Dripleaf Stem', {'facing': EAST}),)) * (len(upper) - 1) + (
        Block('Small Dripleaf', {'half': 'lower', 'facing': EAST}),)

    def dripleaf_loop(step):
        i = step.i
        yield erase(r(0, 2, 0), r(0, 3, 0))
        yield setblock(r(0, 2, 0), lower[i])
        yield setblock(r(0, 3, 0), upper[i])
        text = (None, upper[i].name)
        if i < len(tilts):
            text = text + (f'Tilt: {titlecase(tilts[i])}',)
        yield WallSign(text).place(r(1, 2, 0), EAST)

    room.loop('dripleaf', main_clock).add(
        setblock(r(1, 2, 0), 'air'),
        setblock(r(0, 3, 0), 'air'),
        setblock(r(0, 2, 0), 'air')).loop(dripleaf_loop, upper)
    room.loop('dripleaf_soil', main_clock).loop(lambda step: setblock(r(0, 1, 1), step.elem),
                                                ('Clay', 'Moss Block'))

    def farmland_loop(_):
        for i in range(0, 8):
            block = Block('farmland', {'moisture': 7 - i})
            yield setblock(r(0, 1, i), block)
            yield setblock(r(0, 1, -i), block)
            room.particle(block, 'farmland_strip', r(0, 2, -i))

    room.loop('farmland_strip', main_clock).loop(farmland_loop, range(0, 1)).add(
        kill(e().type('item').nbt({'Item': {'id': 'minecraft:pitcher_pod'}})))
    farmland_init = room.function('farmland_strip_init').add(
        kill(e().tag('farmland_strip_labels')),
        room.label(r(-3, 2, 0), 'Moisture Values', EAST))

    farmland_init.add(text_display('Moisture').tag('farmland_strip_labels').summon(r(0, 2.3, 0)))
    for i in range(0, 8):
        td = text_display(str(7 - i)).tag('farmland_strip_labels')
        farmland_init.add(td.summon(r(0, 2.1, i)))
        farmland_init.add(td.summon(r(0, 2.1, -i)))

    def grass_loop(step):
        grass = ' '.join(('short',) + step.elem + ('grass',))
        yield setblock(r(0, 3, 2), grass)
        yield Sign.change(r(1, 2, 2), (None, titlecase(grass)))
        room.particle(grass, 'grass', r(0, 3.5, 2), step)
        grass = grass.replace('short', 'tall')
        if 'dry' in grass:
            yield erase(r(0, 3, 0), r(0, 4, 0))
            yield setblock(r(0, 3, 0), grass)
            room.particle(grass, 'grass', r(0, 4, 0), step)
        else:
            yield setblock(r(0, 3, 0), (grass, {'half': 'lower'}))
            yield setblock(r(0, 4, 0), (grass, {'half': 'upper'}))
            room.particle(grass, 'grass', r(0, 4.5, 0), step)
        yield Sign.change(r(1, 2, 0), (None, titlecase(grass)))

    room.loop('grass', main_clock).loop(grass_loop, ((), ('dry',)))
    room.particle('large_fern', 'grass', r(0, 4.5, 4))
    room.particle('fern', 'grass', r(0, 3.5, 6))

    def bushes_loop(step):
        bush = ' '.join(step.elem + ('bush',))
        yield setblock(r(0, 3, 0), bush)
        yield Sign.change(r(1, 2, 0), (None, titlecase(bush)))
        room.particle(bush, 'bushes', r(0, 4, 0), step)

    room.loop('bushes', main_clock).loop(bushes_loop, ((), ('firefly',), ('dead',)))

    ground_covers = {'leaf_litter': 'segment_amount', 'wildflowers': 'flower_amount', 'pink_petals': 'flower_amount'}

    def ground_cover_loop(step):
        for i, (cover, count) in enumerate(ground_covers.items()):
            yield setblock(r(i * 2, 3, 0), Block(cover, {count: step.elem}))
            yield Sign.change(r(i * 2, 2, 1), (None, None, f'{count}: {step.elem}'))
            yield Sign.change(r(i * 2, 2, -1), (None, None, f'{count}: {step.elem}'))

    room.loop('ground_cover', main_clock).loop(ground_cover_loop, range(1, 5), bounce=True)
    gc_init = room.function('ground_cover_init')
    for i, cover in enumerate(ground_covers):
        gc_init.add(WallSign((None, to_name(cover))).place(r(i * 2, 2, 1), SOUTH))
        gc_init.add(WallSign((None, to_name(cover))).place(r(i * 2, 2, -1), NORTH))
    room.particle('leaf_litter', 'ground_cover', r(0, 3.5, 0))
    room.particle('wildflowers', 'ground_cover', r(2, 3.5, 0))
    room.particle('pink_petals', 'ground_cover', r(4, 3.5, 0))

    def mushroom_loop(step):
        type = f'{step.elem}_mushroom'
        yield data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': f'restworld:{type}'})
        yield setblock(r(-1, -1, -1), 'redstone_block')
        yield setblock(r(-1, -1, -1), 'air')
        yield setblock(r(1, 2, 0), 'mushroom_stem')
        yield setblock(r(1, 2, 4), f'{type}_block')
        room.particle(type, 'mushrooms', r(1, 3.5, 2), step)
        room.particle('mushroom_stem', 'mushrooms', r(1, 3, 0), step)
        room.particle(f'{type}_block', 'mushrooms', r(1, 3, 4), step)

    room.loop('mushrooms', main_clock).loop(mushroom_loop, ('red', 'brown'))

    def pottable_loop(step):
        if not step.elem:
            yield setblock(r(0, 3, 0), 'flower_pot')
            yield Sign.change(r(1, 2, 0), ('', 'Flower Pot', '', ''))
            return
        if isinstance(step.elem, str):
            step.elem = Block(step.elem)
        sign_nbt = step.elem.sign_nbt()

        base_text = sign_nbt['front_text']['messages'][0]['text']
        if base_text == '':
            sign_nbt['front_text']['messages'][0] = Text.text('Potted')
        else:
            sign_nbt['front_text']['messages'][0] = Text.text('Potted ' + base_text)
        if len(sign_nbt['front_text']['messages'][3]['text']) == 0:
            sign_nbt['front_text']['messages'] = (Text.text(''),) + tuple(sign_nbt['front_text']['messages'][:-1])
        elem_id = 'potted_%s' % step.elem.id
        yield setblock(r(0, 3, 0), elem_id)
        room.particle(elem_id, 'pottable', r(0, 4, 0), step)
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
    pottables = [None] + [Block('Mangrove|Propagule' if w == 'Mangrove' else '%s Sapling' % w) for w in saplings] + [
        Block('%s Tulip' % t) for t in tulips] + list(small_flowers) + misc + [Block('%s Roots' % x) for x in stems] + [
                    Block('%s Fungus' % x) for x in stems] + [
                    Block('Torchflower'), Block('Wither Rose'), Block('Closed|Eyeblossom'), Block('Open|Eyeblossom')]
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
        yield setblock(r(0, 3, 0), ('mangrove_propagule', {'hanging': False, 'age': step.stage}))
        yield Sign.change(r(1, 2, 0), (None, None, 'Stage: %d of 4' % step.stage))

    room.loop('propagule', main_clock).loop(propagule_loop, range(4))

    room.function('shrooms_init').add(room.label(r(1, 2, 1), 'Vine Age 25', WEST))

    def shrooms_loop(step):
        yield data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': 'restworld:%s_shroom' % step.elem})
        yield fill(r(-1, 1, -2), r(13, 1, 10), f'{step.elem}_nylium').replace('#nylium')
        yield setblock(r(-1, -1, -1), 'redstone_block')
        yield setblock(r(-1, -1, -1), 'air')
        shrooms_tops = room.score('shrooms_tops')
        vines = 'weeping_vines' if step.elem == 'crimson' else 'twisting_vines'
        y_off = 3 if step.elem == 'crimson' else 5
        yield execute().unless().score(shrooms_tops).matches(1).run(setblock(r(1, y_off, 0), (vines, {'age': 0})))
        yield execute().if_().score(shrooms_tops).matches(1).run(setblock(r(1, y_off, 0), (vines, {'age': 25})))
        room.particle(f'{step.elem} roots', 'shrooms', r(1, 4, 2), step)
        room.particle(f'{step.elem} fungus', 'shrooms', r(1, 4, 4), step)
        room.particle(vines, 'shrooms', r(1, y_off, 0), step)

    room.loop('shrooms', main_clock).loop(shrooms_loop, ('crimson', 'warped'))
    room.particle('nether_sprouts', 'shrooms', r(1, 3.5, 6))

    def stems_loop(step):
        yield setblock(r(0, 3, -2), 'air')
        yield setblock(r(2, 3, -2), 'air')
        i = step.i
        if i < 8:
            ps = Block('pumpkin_stem', {'age': i})
            ms = Block('melon_stem', {'age': i})
            yield setblock(r(0, 3, -1), ps)
            yield setblock(r(2, 3, -1), ms)
            room.particle(ps, 'stems', r(0, 4, -1), step)
            room.particle(ms, 'stems', r(2, 4, -1), step)
            yield Sign.change(r(3, 2, -1), (None, None, f'Stage: {i} of {step.count}'))
        else:
            yield setblock(r(0, 3, -2), 'pumpkin')
            yield setblock(r(2, 3, -2), 'melon')
            room.particle('pumpkin', 'stems', r(0, 4, -2), step)
            room.particle('melon', 'stems', r(2, 4, -2), step)
            yield setblock(r(0, 3, -1), ('attached_pumpkin_stem', {'facing': NORTH}))
            yield setblock(r(2, 3, -1), ('attached_melon_stem', {'facing': NORTH}))
            room.particle('attached_pumpkin_stem', 'stems', r(0, 4, -1), step)
            room.particle('attached_melon_stem', 'stems', r(2, 4, -1), step)
            yield Sign.change(r(3, 2, -1), (None, None, 'Stage:  Attached'))

    room.loop('stems', main_clock).loop(stems_loop, range(0, 9))

    def sweet_berry_loop(step):
        bush = Block('Sweet Berry Bush', {'age': step.elem})
        yield setblock(r(0, 3, 0), bush)
        yield Sign.change(r(1, 2, 0), (None, None, f'Age: {step.elem} of {step.count}'))
        room.particle(bush, 'sweet_berry', r(0, 4, 0), step)

    room.loop('sweet_berry', main_clock).loop(sweet_berry_loop, range(0, 4), bounce=True)
    room.function('sweet_berry_init').add(room.label(r(5, 2, 2), 'Show Particles', SOUTH))
    room.loop('sweet_berry_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem),
                                                   ('Grass Block', 'Dirt', 'Podzol', 'Coarse Dirt'))

    tree_types = {
        'Acacia': SAVANNA, 'Birch': BIRCH_FOREST, 'Oak': PLAINS, 'Cherry': CHERRY_GROVE, 'Jungle': JUNGLE,
        'Mangrove': MANGROVE_SWAMP, 'Dark Oak': DARK_FOREST, 'Pale Oak': PALE_GARDEN, 'Spruce': SNOWY_TAIGA
    }

    freeze_biome = room.score('freeze_biome')

    floor_tag = 'floor_block'

    def trees_loop(step):
        tree, biome = step.elem
        yield data().merge(r(-1, 0, -1), {'mode': 'LOAD', 'name': f'restworld:{to_id(tree)}_trees'})
        yield setblock(r(-1, -1, -1), 'redstone_block')
        yield setblock(r(-1, -1, -1), 'air')
        yield WallSign((None, f'{tree} Trees', 'Biome:', to_name(str(biome)))).place(r(1, 2, 7), WEST)
        plant_room = Region(r(0, -5, -1), r(31, 30, 58))
        yield execute().unless().score(freeze_biome).matches(1).run(
            execute().at(e().tag('plants_room_beg_home')).run(
                plant_room.fillbiome(biome),
                plant_room.fill('air', replace='snow')))

    tree_items = tree_types.items()
    sorted(tree_items)
    room.loop('trees', slow_clock).add(kill(e().tag(floor_tag))).loop(trees_loop, tree_items).add(
        execute().at(e().tag('plants_room_beg_home')).run(fill(r(0, 1, 0), r(33, 6, 52), 'water').replace('ice')),
        WallSign((None, 'Lily Pad')).place(r(3, 2, 15), WEST))
    room.function('trees_init').add(room.label(r(0, 2, 16), 'Freeze Biome', WEST))

    def tulips_loop(step):
        which = f'{to_id(step.elem)}_tulip'
        yield setblock(r(0, 3, 0), which)
        yield Sign.change(r(1, 2, 0), (None, step.elem))
        room.particle(which, 'tulips', r(0, 4, 0), step)

    room.loop('tulips', main_clock).loop(tulips_loop, tulips)
    flowers = (
        'blue_orchid', 'allium', 'azure_bluet', 'tulip', 'poppy', 'oxeye_daisy', 'dandelion', 'lily_of_the_valley',
        'cornflower', 'wither_rose')
    for i, flower in enumerate(flowers):
        if flower != 'tulip':
            room.particle(flower, 'tulips', r(0, 4, 3 - i))
    high_flowers = ('sunflower', 'lilac', 'rose_bush', 'peony')
    for i, flower in enumerate(high_flowers):
        room.particle(flower, 'tulips', r(-3, 5, 2 - i * 2))

    def eyeblossom_loop(step):
        which = f'{step.elem}_eyeblossom'
        yield setblock(r(0, 3, 0), which)
        yield Sign.change(r(1, 2, 0), (None, titlecase(step.elem)))
        room.particle(which, 'eyeblossom', r(0, 4, 0), step)

    room.loop('eyeblossom', main_clock).loop(eyeblossom_loop, ('open', 'closed'))
    room.particle('pale_moss_block', 'eyeblossom', r(-3, 4, 1))


def three_funcs(room):
    flower = room.score('cactus_flower')

    def three_height_loop(step):
        def height(z, which):
            count = step.elem
            yield fill(r(0, 3, z), r(0, 3 + count, z), which)
            yield data().merge(r(1, 2, z), {'front_text': Sign.lines_nbt(('', to_name(which), '', ''))})
            room.particle(which, 'three_height', r(0, 4 + count, z), step)
            if which == 'cactus':
                yield execute().unless().score(flower).matches(0).run(setblock(r(0, 4 + count, z), 'cactus_flower'))

        yield from height(0, 'cactus')
        yield from height(-3, 'sugar_cane')

    def three_age_loop(step):
        def age(z, which):
            age = step.elem
            block = Block(which, state={'age': age})
            yield setblock(r(0, 4, z), block)
            yield data().merge(r(1, 2, z),
                               {'front_text': Sign.lines_nbt(
                                   (None, to_name(which), f'Top Age: {age} of 16', '(vanilla shows 1)'))})
            room.particle(block, 'three_age', r(0, 5, z), step)

        yield from age(0, 'cactus')
        yield from age(-3, 'sugar_cane')

    def switch_to_func(which):
        room.function(f'three_change_{which}', home=False).add(
            kill(e().tag('three_runner')),
            execute().at(e().tag('three_home')).positioned(r(-1, -0.5, 2)).run(
                function(f'restworld:plants/three_{which}_home')),
            tag(e().tag(f'three_{which}_home')).add('three_runner'),
            execute().at(e().tag(f'three_{which}_home')).run(function(f'restworld:plants/three_{which}_cur')))

    room.loop('three_height', main_clock).add(erase(r(0, 3, 0), r(0, 6, -3))).loop(
        three_height_loop, range(3), bounce=True)
    room.loop('three_age', fast_clock).add(
        fill(r(0, 5, 0), r(0, 5, -3), 'air'),
        setblock(r(0, 3, 0), 'cactus'),
        setblock(r(0, 3, -3), 'sugar_cane'),
    ).loop(three_age_loop, range(16)).add(
        execute().unless().score(flower).matches(0).run(setblock(r(0, 5, 0), 'cactus_flower')))
    room.function('three_init').add(
        room.label(r(-1, 2, 0), 'Change Age', EAST),
        room.label(r(-1, 2, 3), 'Cactus Flower', EAST))
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
            bamboo = 'bamboo_sapling'
            yield setblock(r(0, 3, 0), bamboo)
            yield fill(r(0, 3 + top, 0), r(0, 4, 0), 'air')
            height = 1
        else:
            if step.elem < max:
                height = step.elem
            elif step.elem > max + 1:
                height = max - (step.elem - max) + 1
            else:
                height = max
            age = 0 if step.i <= max else 1
            yield Sign.change(r(1, 2, 0), (None, None, 'Shoot' if step.i == 0 else f'Age: {age:d}'))
            bamboo = Block('bamboo', {'age': age, 'leaves': 'none'})
            yield fill(r(0, 3, 0), r(0, 3 + height - 1, 0), bamboo)
            if height < max:
                yield fill(r(0, 3 + max - 1, 0), r(0, 3 + height, 0), 'air')
            if height >= 2:
                yield setblock(r(0, 3 + height - 1, 0), Block('bamboo', {'age': age, 'leaves': 'small'}))
            if height >= 3:
                yield setblock(r(0, 3 + height - 2, 0), Block('bamboo', {'age': age, 'leaves': 'large'}))
        room.particle(bamboo, 'bamboo', r(0, 3 + height, 0), step)

    room.loop('bamboo', main_clock).loop(bamboo_loop, range(0, 2 * max + 1))
    room.loop('bamboo_soil', main_clock).loop(lambda step: setblock(r(0, 2, 1), step.elem), (
        'Grass Block', 'Dirt', 'Coarse Dirt', 'Rooted Dirt', 'Podzol', 'Sand', 'Gravel', 'Moss Block', 'Mycelium',
        'Red Sand', 'Mud'))

    water_funcs(room)


def water_funcs(room):
    volume = Region(r(-1, 2, -5), r(1, 4, 1))
    watered = {'waterlogged': True}

    def coral_loop(step):
        def one(pattern, replace, pos):
            nbt = None if 'Block' in pattern else watered
            state = {'facing': SOUTH} if 'Wall' in pattern and 'Dead' not in pattern else None
            block = Block(pattern % step.elem, state=state, nbt=nbt)
            yield volume.replace(block, replace)
            room.particle(block, 'coral', pos, step)

        yield from one('%s Coral', '#coral_plants', r(0, 4, -1))
        yield from one('%s Coral Block', '#coral_blocks', r(-1, 3, -1))
        yield from one('%s Coral Fan', '#restworld:coral_fans', r(0, 3.5, 0))
        yield from one('%s Coral Wall Fan', '#wall_corals', r(0, 3, 1))
        yield from one('Dead %s Coral', '#restworld:dead_coral_plants', r(0, 4, -3))
        yield from one('Dead %s Coral Block', '#restworld:dead_coral_blocks', r(-1, 3, -3))
        yield from one('Dead %s Coral Fan', '#restworld:dead_coral_fans', r(0, 3.5, -4))
        yield from one('Dead %s Coral Wall Fan', '#restworld:dead_wall_corals', r(0, 3, -5))
        yield Sign.change(r(0, 2, -2), (None, step.elem))

    room.loop('coral', main_clock).loop(coral_loop, ('Brain', 'Bubble', 'Fire', 'Horn', 'Tube'))
    room.function('coral_init').add(
        WallSign((None, None, 'Coral'), front=None).glowing(True).place(r(0, 2, -2), WEST, water=True))

    kelp_init = room.function('kelp_init').add(fill(r(0, 2, 0), r(2, 6, 0), 'water'))
    for x in range(0, 3):
        block = 'kelp'
        kelp_init.add(fill(r(x, 2, 0), r(x, 5, 0), block))
        if x > 0:
            block = Block('kelp', {'age': 25})
            kelp_init.add(setblock(r(x, 6, 0), block))
    room.particle('kelp', 'kelp', r(0, 6, 0))
    room.particle('tall_seagrass', 'kelp', r(0, 6, -3))
    room.particle('seagrass', 'kelp', r(0, 5, -5))

    def sea_pickles_loop(step):
        block = Block('sea_pickle', {'pickles': step.elem})
        yield setblock(r(0, 3, 0), block)
        room.particle(block, 'sea_pickles', r(0, 4, 0), step)
        dead_block = Block('sea_pickle', {'waterlogged': False, 'pickles': step.elem})
        yield setblock(r(0, 3, -2), dead_block)
        room.particle(block, 'sea_pickles', r(0, 4, -2), step)

    room.loop('sea_pickles', main_clock).loop(sea_pickles_loop, range(1, 5))
    room.particle('lily_pad', 'sea_pickles', r(-3, 2, -2))
