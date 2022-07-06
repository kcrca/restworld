import math
import sys

import amulet
from amulet import SelectionBox

biomes = {
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


# box = SelectionBox((456, 76, -727), (456, 76, -727))


def main():
    dimension = "minecraft:overworld"
    level = amulet.load_level(sys.argv[1])
    x = -1136
    for i, biome in enumerate(biomes):
        if x == -1008:
            x += 16
        biome_id = 'universal_minecraft:%s' % biome.replace(' ', '_').lower()
        box = SelectionBox((x, 95, -1040), (x + 15, 125, -992))
        # box = SelectionBox((160, 81, -1353), (161, 82, -1352))
        for chunk, slices, _ in (level.get_chunk_slice_box(dimension, box, True)):
            new_biome = chunk.biome_palette.get_add_biome(biome_id)
            bounds = level.bounds(dimension)
            slices = (
                slice(slices[0].start // 4, math.ceil(slices[0].stop / 4)),
                slice(bounds.min_y // 4, math.ceil(bounds.max_y / 4)),
                slice(slices[2].start // 4, math.ceil(slices[2].stop / 4)),
            )
            chunk.biomes[slices] = new_biome
            chunk.changed = True
        x += 16
    level.save()
    level.close()


if __name__ == '__main__':
    main()
