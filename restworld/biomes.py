import collections

from pyker.commands import NORTH, mc, CLEAR, OVERWORLD, r, entity
from pyker.simpler import WallSign
from restworld.rooms import Room, label
from restworld.world import restworld

biome_groups = collections.OrderedDict()
biome_groups['Temperate'] = (
    'Plains', 'Forest', 'Flower Forest', 'Birch Forest', 'Dark Forest', 'Swamp', 'Mangrove Swamp', 'Jungle',
    'Mushroom Field')
biome_groups['Warm'] = ('Desert', 'Savanna', 'Badlands')
biome_groups['Cold'] = ('Tiaga', 'Stone Shore')
biome_groups['Snowy'] = ('Snowy Tundra', 'Ice Spikes', 'Snowy Tiaga')
biome_groups['Ocean'] = ('Warm Ocean', 'Ocean', 'Frozen Ocean')
biome_groups['Caves and Cliffs'] = ('Lush Caves', 'Dripstone Caves')
biome_groups['Nether'] = ('Nether Wastes', 'Soul Sand Valley', 'Crimson Forest', 'Warped Forest', 'Basalt Deltas')
biome_groups['End'] = ('The End', 'End Island', 'End City')
biome_groups['Structures'] = ('Mineshaft', 'Monument', 'Stronghold', 'Bastion Remnant', 'Fortress')
biomes = [item for sublist in list(biome_groups.values()) for item in sublist]


def categories():
    yield mc.fill(r(6, 0, 6), r(-6, 0, 6), 'air')
    for i, group in enumerate(biome_groups):
        yield category_sign(group, 6 - i)


def category_sign(category, x):
    text3 = '' if category == 'Structures' else 'Biomes'
    yield WallSign((None, category, text3), (
        None,
        None,
        mc.execute().at(entity().tag('category_home')).run().function('restworld:biomes/%s_signs' % to_id(category))),
                   ).place(r(x, 1, 6), NORTH)


def illuminate(biome, prefix, i, x, y, z, handback):
    illuminate_score = handback
    yield mc.execute().if_().score(illuminate_score).matches(1).run().fill(r(x, y + 1, z), r(x + 31, y + 32, z + 31),
                                                                           'light').replace('#restworld:air'),
    yield mc.execute().unless().score(illuminate_score).matches(1).run().fill(r(x, y + 1, z), r(x + 31, y + 32, z + 31),
                                                                              'air').replace('light'),


def load_biome(renderer, biome, handback=None):
    for i in range(0, 4):
        yield from renderer(biome, mc.execute().at(entity().tag('biome_loading_action_home')).run(),
                 i + 4, 32 * int(i / 2), 33, 32 * int(i % 2), handback)
    for i in range(0, 4):
        yield from renderer(biome, mc.execute().at(entity().tag('biome_loading_action_home')).run(),
                 i, 32 * int(i / 2), 1, 32 * int(i % 2), handback)


def group_signs(group, score):
    yield from categories()

    x = list(biome_groups.keys()).index(group)
    at_biome_loading = mc.execute().at(entity().tag('biome_loading_action_home')).run()
    for i, biome in enumerate(list(biome_groups[group])):
        yield WallSign((None, biome), (
            at_biome_loading.function('restworld:biomes/clear_biome'),
            score.set(biomes.index(biome)),
            at_biome_loading.function('restworld:biomes/load_biome_cur'),
            at_biome_loading.function('restworld:biomes/cleanup_biome'),
        )).place(r(6 - i - x, 0, 6), NORTH)
    yield WallSign((None, group),
                   (mc.execute().at(entity().tag('category_home')).run().function('restworld:biomes/category')),
                   'birch'
                   ).place(r(6 - x, 1, 6), NORTH)


def to_id(name):
    return name.lower().replace(' ', '_')


def clear(biome, prefix, i, x, y, z, handback):
    yield mc.data().merge(r(x, 1, z), {'name': 'restworld:air', 'mode': 'LOAD'})


def trigger(biome, prefix, i, x, y, z, handback):
    yield mc.setblock(r(x, y - 1, z), 'redstone_torch')
    yield mc.setblock(r(x, y - 1, z), 'air')


def load_biome_loop(step):
    def setup(biome, prefix, i, x, y, z, handback):
        if i > 4:
            yield mc.setblock(r(x, y, z), 'structure_block')
        yield mc.data().merge(r(x, y, z), {'name': 'restworld:%s_%d' % (to_id(biome), i + 1), 'mode': 'LOAD'})

    yield mc.say('Switching to biome', step.elem)
    yield from load_biome(setup, step.elem)


def save_biome(biome, prefix, i, x, z, handback, raised=False):
    return [
        prefix.data().merge(r(x, 1, z), {'mode': 'SAVE'}),
        prefix.setblock(r(x, 0, z), 'redstone_torch'),
        prefix.setblock(r(x, 0, z), 'air'),
    ]


def room():
    room = Room('biomes', restworld, NORTH, (None, 'Biome'))

    room.function('arrive_biome').add(mc.execute().in_(OVERWORLD).run().weather(CLEAR))
    room.function('arrive_biome_init').add(
        label(r(0, 3, -6), "Go Home"),
        label(r(-1, 3, -6), "Go Home"),
        label(r(0, 3, -2), "Go Home"),
        label(r(-1, 3, -2), "Go Home"),
    )
    room.home_func('biome_loading_action')

    room.home_func('category_action')
    room.function('category_init').add(
        categories(),
        label(r(5, -1, 6), 'Illuminate'),
    )
    load_biome_score = room.score('load_biome')
    for g in biome_groups:
        room.function(to_id(g) + '_signs', needs_home=False).add(group_signs(g, load_biome_score))

    room.function('cleanup_biome').add(mc.kill(entity().type('item')))
    clear_previous_mobs = mc.execute().at(entity().tag('biome_loading_action_home')).positioned(
        r(-5, -5, -5)).run().kill(
        entity().type('!player').tag('!homer').delta((74, 42, 74))),

    room.function('clear_biome').add(
        mc.fill(r(-2, -4, -2), r(-1, 42, 66), 'air').replace('#restworld:liquid'),
        mc.fill(r(-2, -4, -2), r(66, 42, -1), 'air').replace('#restworld:liquid'),
        mc.fill(r(-2, -4, 65), r(65, 42, 64), 'air').replace('#restworld:liquid'),
        mc.fill(r(64, -4, -2), r(65, 42, 65), 'air').replace('#restworld:liquid'),
        mc.fill(r(0, 34, 0), r(31, 65, 31), 'air'),
        mc.fill(r(32, 34, 0), r(63, 65, 31), 'air'),
        mc.fill(r(0, 34, 32), r(31, 65, 63), 'air'),
        mc.fill(r(32, 34, 32), r(63, 65, 63), 'air'),

        load_biome(clear, 'clear'),
        load_biome(trigger, 'trigger'),

        ## Three times because slimes take three to kill
        clear_previous_mobs,
        clear_previous_mobs,
        clear_previous_mobs,

        mc.kill(entity().type('item')))
    illuminate_score  = room.score('illuminate')
    room.function('illuminate_biome').add(load_biome(illuminate, 'illuminate', handback=illuminate_score))
    room.loop('load_biome').loop(load_biome_loop, biomes).add(
        load_biome(trigger, 'trigger'),
        load_biome(illuminate, 'illuminate', handback=room.score('illuminate'))
    )
    room.home_func('reaper')

    room.function('save_biome').add(load_biome(save_biome, 'save'))
