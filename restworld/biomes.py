import collections

from pynecraft.base import NORTH, OVERWORLD, SOUTH, r, to_id
from pynecraft.commands import CLEAR, data, e, execute, fill, fillbiome, function, kill, say, setblock, weather
from pynecraft.simpler import PLAINS, WallSign
from pynecraft.values import BASALT_DELTAS, NETHER_WASTES, SMALL_END_ISLANDS, WARM_OCEAN, as_biome
from restworld.rooms import Room
from restworld.world import restworld

biome_groups = collections.OrderedDict()
biome_groups['Temperate'] = (
    'Plains', 'Forest', 'Flower Forest', 'Birch Forest', 'Cherry Grove', 'Dark Forest', 'Pale Garden', 'Swamp',
    'Mangrove Swamp',
    'Jungle', 'Mushroom Fields')
biome_groups['Warm'] = ('Desert', 'Savanna', 'Badlands')
biome_groups['Cold'] = ('Taiga', 'Stony Shore')
biome_groups['Snowy'] = ('Snowy Taiga', 'Ice Spikes', 'Snowy Taiga')
biome_groups['Ocean'] = ('Warm Ocean', 'Ocean', 'Frozen Ocean')
biome_groups['Cave'] = ('Lush Caves', 'Dripstone Caves', 'Deep Dark')
biome_groups['Nether'] = ('Nether Wastes', 'Soul Sand Valley', 'Crimson Forest', 'Warped Forest', 'Basalt Deltas')
biome_groups['End'] = ('The End', 'End City', 'End Island')
biome_groups['Structures'] = ('Mineshaft', 'Monument', 'Stronghold', 'Trial Chambers', 'Bastion Remnant', 'Fortress')
biomes = [item for sublist in list(biome_groups.values()) for item in sublist]

biome_ids = {'End City': SMALL_END_ISLANDS, 'Monument': WARM_OCEAN, 'Bastion Remnant': BASALT_DELTAS,
             'Fortress': NETHER_WASTES}


def categories():
    yield fill(r(6, 0, 6), r(-8, 0, 6), 'air')
    for i, group in enumerate(biome_groups):
        yield category_sign(group, 6 - i)


def category_sign(category, x):
    text3 = type_text(category)
    yield WallSign().messages((None, category, text3), (
        None,
        None,
        execute().at(e().tag('category_home')).run(function(f'restworld:biomes/{to_id(category)}_signs'))),
                              ).place(r(x, 1, 6), NORTH)


def type_text(category):
    return '' if category == 'Structures' else 'Biomes'


# noinspection PyUnusedLocal
def illuminate(biome, prefix, i, x, y, z, handback):
    illuminate_score = handback
    yield execute().if_().score(illuminate_score).matches(1).run(fill(r(x, y + 1, z), r(x + 31, y + 32, z + 31),
                                                                      'light').replace('#restworld:air')),
    yield execute().unless().score(illuminate_score).matches(1).run(fill(r(x, y + 1, z), r(x + 31, y + 32, z + 31),
                                                                         'air').replace('light')),


def load_biome(renderer, biome, handback=None):
    for i in range(0, 4):
        yield from renderer(biome, execute().at(e().tag('biome_loading_action_home')),
                            i + 4, 32 * int(i / 2), 33, 32 * int(i % 2), handback)
    for i in range(0, 4):
        yield from renderer(biome, execute().at(e().tag('biome_loading_action_home')),
                            i, 32 * int(i / 2), 1, 32 * int(i % 2), handback)


def group_signs(group, score):
    yield from categories()

    x = list(biome_groups.keys()).index(group)
    at_biome_loading = execute().at(e().tag('biome_loading_action_home'))
    for i, biome in enumerate(list(biome_groups[group])):
        yield WallSign().messages((None, biome), (
            at_biome_loading.run(function('restworld:biomes/clear_biome')),
            score.set(biomes.index(biome)),
            at_biome_loading.run(function('restworld:biomes/load_biome_cur')),
            at_biome_loading.run(function('restworld:biomes/cleanup_biome')),
        )).place(r(6 - i - x, 0, 6), NORTH)
    yield WallSign(wood='birch').messages((None, group, type_text(group)),
                                          (execute().at(e().tag('category_home')).run(
                                              function('restworld:biomes/category')))).place(r(6 - x, 1, 6), NORTH)


# noinspection PyUnusedLocal
def clear(biome, prefix, i, x, y, z, handback):
    yield data().merge(r(x, 1, z), {'name': 'restworld:air', 'mode': 'LOAD'})


# noinspection PyUnusedLocal
def trigger(biome, prefix, i, x, y, z, handback):
    yield setblock(r(x, y - 1, z), 'redstone_torch')
    yield setblock(r(x, y - 1, z), 'air')


def load_biome_loop(step):
    try:
        biome_id = as_biome(to_id(step.elem))
    except ValueError:
        biome_id = biome_ids.get(step.elem, PLAINS)

    # noinspection PyUnusedLocal
    def setup(biome, prefix, i, x, y, z, handback):
        if i > 4:
            yield setblock(r(x, y, z), 'structure_block')
        yield data().merge(r(x, y, z), {'name': f'restworld:{to_id(biome)}_{i + 1:d}', 'mode': 'LOAD'})
        yield fillbiome(r(x, y, z), r(x + 31, y + 31, z + 31), biome_id)

    yield say('Switching to biome', step.elem)
    yield from load_biome(setup, step.elem)


# noinspection PyUnusedLocal
def save_biome(biome, prefix, i, x, z, handback, raised=False):
    return [
        prefix.run(data().merge(r(x, 1, z), {'mode': 'SAVE'})),
        prefix.run(setblock(r(x, 0, z), 'redstone_torch')),
        prefix.run(setblock(r(x, 0, z), 'air')),
    ]


def room():
    room = Room('biomes', restworld)

    room.function('arrive_biome').add(execute().in_(OVERWORLD).run(weather(CLEAR)))
    room.function('arrive_biome_init').add(
        room.label(r(0, 3, -2), 'Go Home', NORTH),
        room.label(r(-1, 3, -2), 'Go Home', NORTH),
    )
    room.home_func('biome_loading_action')

    room.home_func('category_action')
    room.function('category_init').add(
        categories(),
        room.label(r(5, -1, 6), 'Illuminate', SOUTH),
    )
    load_biome_score = room.score('load_biome')
    for g in biome_groups:
        room.function(to_id(g) + '_signs', home=False).add(group_signs(g, load_biome_score))

    room.function('cleanup_biome').add(kill(e().type('item')))
    clear_previous_mobs = execute().at(e().tag('biome_loading_action_home')).positioned(
        r(-5, -5, -5)).run(kill(e().type('!player').tag('!homer').volume((74, 42, 74)))),

    room.function('clear_biome').add(
        fill(r(-2, -4, -2), r(-1, 42, 66), 'air').replace('#restworld:liquid'),
        fill(r(-2, -4, -2), r(66, 42, -1), 'air').replace('#restworld:liquid'),
        fill(r(-2, -4, 65), r(65, 42, 64), 'air').replace('#restworld:liquid'),
        fill(r(64, -4, -2), r(65, 42, 65), 'air').replace('#restworld:liquid'),
        fill(r(0, 34, 0), r(31, 65, 31), 'air'),
        fill(r(32, 34, 0), r(63, 65, 31), 'air'),
        fill(r(0, 34, 32), r(31, 65, 63), 'air'),
        fill(r(32, 34, 32), r(63, 65, 63), 'air'),

        load_biome(clear, 'clear'),
        load_biome(trigger, 'trigger'),

        # Three times because slimes take three to kill
        clear_previous_mobs,
        clear_previous_mobs,
        clear_previous_mobs,

        kill(e().type('item')))
    illuminate_score = room.score('illuminate')
    room.function('illuminate_biome').add(load_biome(illuminate, 'illuminate', handback=illuminate_score))
    room.loop('load_biome').loop(load_biome_loop, biomes).add(
        load_biome(trigger, 'trigger'),
        load_biome(illuminate, 'illuminate', handback=room.score('illuminate'))
    )
    room.home_func('reaper')
