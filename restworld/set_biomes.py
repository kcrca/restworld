import math
import sys

import amulet
from amulet import SelectionBox

land_biomes = {
    'Badlands': ('Badlands', 'Wooded Badlands', 'Eroded Badlands'),
    'Desert': ('Desert',),
    'Savanna': ('Savanna',),
    'Swamp': ('Swamp',),
    'Mangrove Swamp': ('Mangrove Swamp',),
    'Birch Forest': ('Birch Forest',),
    'Ocean': ('Ocean', 'Cold Ocean', 'Deep Ocean', 'River'),
    'Grove': ('Grove', 'Snowy Taiga', 'Frozen River', 'Frozen Ocean'),
    'Meadow': ('Meadow',),
    'Taiga': ('Taiga',),
    'Stone Shore': ('Stony Shore', 'Windswept Hills', 'Windswept Forest'),
    'Plains': ('Plains', 'Sunflower Plains', 'Beach', 'Stony Peaks'),
    'Forest': ('Forest', 'Flower Forest'),
    'Jungle': ('Jungle Bamboo Jungle',),
    'Mushroom Fields': ('Mushroom Fields',),
    'Dark Forest': ('Dark Forest',),
}

water_biomes = (
    'Warm Ocean',
    'Lukewarm Ocean',
    'Ocean',
    'Cold Ocean',
    'Frozen Ocean',
    'Mangrove Swamp',
    'Swamp',
)

dimension = "minecraft:overworld"


def main():
    level = amulet.load_level(sys.argv[1])
    set_land_biomes(level)
    set_water_biomes(level)
    level.save()
    level.close()


def set_land_biomes(level):
    x = -1136
    for i, biome in enumerate(land_biomes):
        if x == -1008:
            x += 16
        biome_id = 'universal_minecraft:%s' % biome.replace(' ', '_').lower()
        box = SelectionBox((x, 95, -1040), (x + 15, 125, -992))
        for chunk, slices, _ in (level.get_chunk_slice_box(dimension, box, True)):
            set_biome(level, biome_id, chunk, slices)
        x += 16


def set_water_biomes(level):
    z = -1040
    x = -1008
    x_width = 16
    for i, biome in enumerate(water_biomes):
        biome_id = f'universal_minecraft:{biome.replace(" ", "_").lower()}'
        box = SelectionBox((x, 95, z), (x + x_width - 1, 125, z + 15))
        for chunk, slices, _ in (level.get_chunk_slice_box(dimension, box, True)):
            set_biome(level, biome_id, chunk, slices)
        z -= 16
        if i == 0:
            x -= 16
            x_width += 32


def set_biome(level, biome_id, chunk, slices):
    new_biome = chunk.biome_palette.get_add_biome(biome_id)
    bounds = level.bounds(dimension)
    slices = (
        slice(slices[0].start // 4, math.ceil(slices[0].stop / 4)),
        slice(bounds.min_y // 4, math.ceil(bounds.max_y / 4)),
        slice(slices[2].start // 4, math.ceil(slices[2].stop / 4)),
    )
    chunk.biomes[slices] = new_biome
    chunk.changed = True


if __name__ == '__main__':
    main()
