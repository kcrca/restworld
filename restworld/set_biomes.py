# import math
# import sys
#
# import amulet
# from amulet import SelectionBox
#

class Samples:
    def __init__(self, x, z, x_width, z_width):
        self.x = x
        self.z = z
        self.x_width = x_width
        self.z_width = z_width

    def params(self):
        return self.x, self.z, self.x_width, self.z_width


class BiomeSampler:
    land_biomes = {
        'Badlands': ('Badlands', 'Wooded Badlands', 'Eroded Badlands'),
        'Desert': ('Desert',),
        'Savanna': ('Savanna',),
        'Swamp': ('Swamp',),
        'Mangrove Swamp': ('Mangrove Swamp',),
        'Birch Forest': ('Birch Forest',),
        'Ocean': ('Ocean', 'River', 'Cold Ocean', 'Deep Ocean'),
        'Grove': ('Grove', 'Snowy Taiga', 'Frozen River', 'Frozen Ocean'),
        'Beach': (),
        'Meadow': ('Meadow',),
        'Taiga': ('Taiga',),
        'Stone Shore': ('Stone Shore', 'Windswept Hills', 'Windswept Forest'),
        'Plains': ('Plains', 'Beach', 'Sunflower Plains', 'Stony Peaks'),
        'Forest': ('Forest', 'Flower Forest'),
        'Jungle': ('Jungle', 'Bamboo Jungle',),
        'Mushroom Fields': ('Mushroom Fields',),
        'Dark Forest': ('Dark Forest',),
    }
    land_samples = Samples(-1136, -1024, 16, 16)

    water_biomes = (
        'Warm Ocean',
        'Lukewarm Ocean',
        'Ocean',
        'Cold Ocean',
        'Frozen Ocean',
        'Mangrove Swamp',
        'Swamp',
    )
    water_samples = Samples(-1008, -1040, 16, 16)

#
# dimension = "minecraft:overworld"
#
#
# def main():
#     level = amulet.load_level(sys.argv[1])
#     set_land_biomes(level)
#     set_water_biomes(level)
#     level.save()
#     level.close()
#
#
# def set_land_biomes(level):
#     x, z, xw, zw = BiomeSampler.land_samples.params()
#     for i, biome in enumerate(BiomeSampler.land_biomes):
#         biome_id = 'universal_minecraft:%s' % biome.replace(' ', '_').lower()
#         box = SelectionBox((x, 50, z - 16), (x + xw, 150, z + zw + 16))
#         for chunk, slices, _ in (level.get_chunk_slice_box(dimension, box, True)):
#             set_biome(level, biome_id, chunk, slices)
#         x += xw
#
#
# def set_water_biomes(level):
#     x, z, xw, zw = BiomeSampler.water_samples.params()
#     zw += 4  # "+4" here is to avoid server-side blending the near edge of the first water biome.
#     for i, biome in enumerate(BiomeSampler.water_biomes):
#         biome_id = f'universal_minecraft:{biome.replace(" ", "_").lower()}'
#         box = SelectionBox((x - 4, 50, z), (x + xw + 4, 150, z + zw))
#         print(box)
#         for chunk, slices, _ in (level.get_chunk_slice_box(dimension, box, True)):
#             set_biome(level, biome_id, chunk, slices)
#         if i == 0:
#             zw -= 4
#         z -= zw
#
#
# def set_biome(level, biome_id, chunk, slices):
#     new_biome = chunk.biome_palette.get_add_biome(biome_id)
#     bounds = level.bounds(dimension)
#     chunk_slices = (
#         slice(slices[0].start // 4, math.ceil(slices[0].stop / 4)),
#         slice(bounds.min_y // 4, math.ceil(bounds.max_y / 4)),
#         slice(slices[2].start // 4, math.ceil(slices[2].stop / 4)),
#     )
#     chunk.biomes[chunk_slices] = new_biome
#     chunk.changed = True
#
#
# if __name__ == '__main__':
#     main()
