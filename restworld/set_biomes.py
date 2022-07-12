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
    'Beach': (),
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
        biome_id = 'universal_minecraft:%s' % biome.replace(' ', '_').lower()
        box = SelectionBox((x, 50, -1040), (x + 16, 150, -992))
        for chunk, slices, _ in (level.get_chunk_slice_box(dimension, box, True)):
            set_biome(level, biome_id, chunk, slices)
        x += 16


def set_water_biomes(level):
    z = -1024 + 4  # "+4" here is to avoid server-side blending the near edge of the first water biome.
    z_width = 16 + 4
    x = -1008 - 4  # "+4" ensures the area beside the biome is the same to avoid server-side blending.
    x_width = 16 + 8
    for i, biome in enumerate(water_biomes):
        biome_id = f'universal_minecraft:{biome.replace(" ", "_").lower()}'
        box = SelectionBox((x, 50, z), (x + x_width, 150, z - z_width))
        for chunk, slices, _ in (level.get_chunk_slice_box(dimension, box, True)):
            set_biome(level, biome_id, chunk, slices)
        z -= z_width
        if i == 0:
            z_width = 16


def set_biome(level, biome_id, chunk, slices):
    new_biome = chunk.biome_palette.get_add_biome(biome_id)
    bounds = level.bounds(dimension)
    chunk_slices = (
        slice(slices[0].start // 4, math.ceil(slices[0].stop / 4)),
        slice(bounds.min_y // 4, math.ceil(bounds.max_y / 4)),
        slice(slices[2].start // 4, math.ceil(slices[2].stop / 4)),
    )
    chunk.biomes[chunk_slices] = new_biome
    chunk.changed = True


if __name__ == '__main__':
    main()
