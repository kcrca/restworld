import re

from pyker.commands import COLORS
from pyker.function import BLOCKS
from restworld.world import restworld


def tags():
    colorings = {
        'banner': None,
        'carpet': None,
        'concrete': None,
        'concrete_powder': None,
        'wool': None,
        'candle': 'candle',
        'candle_cake': ('candle_cake', 'cake'),
        'shulker_box': 'shulker_box',
        'stained_glass': 'glass',
        'stained_glass_pane': 'glass_pane',
        'terracotta': 'terracotta'}

    blocks = restworld.tags(BLOCKS)
    for thing, added in colorings.items():
        blocks[thing] = {
            'values': ['%s_%s' % (c, thing) for c in COLORS]
        }
        if isinstance(added, tuple):
            blocks[thing]['values'].extend(added)
        elif added:
            blocks[thing]['values'].append(added)

    blocks['air'] = {
        'values': [
            'air',
            'cave_air'
        ]
    }
    blocks['fencelike'] = {
        'values': ['%s_stained_glass_pane' % x for x in COLORS] + [
            'acacia_fence',
            'birch_fence',
            'jungle_fence',
            'mangrove_fence',
            'oak_fence',
            'dark_oak_fence',
            'warped_fence',
            'crimson_fence',
            'spruce_fence',
            'nether_brick_fence',
            'glass_pane',
            'iron_bars',
            'brick_wall',
            'cobblestone_wall',
            'mud_brick_wall',
            'mossy_cobblestone_wall',
            'stone_brick_wall',
            'mossy_stone_brick_wall',
            'end_stone_brick_wall',
            'sandstone_wall',
            'red_sandstone_wall',
            'nether_brick_wall',
            'red_nether_brick_wall',
            'andesite_wall',
            'granite_wall',
            'diorite_wall',
            'prismarine_wall',
            'blackstone_wall',
            'polished_blackstone_wall',
            'polished_blackstone_brick_wall',
            'cobbled_deepslate_wall',
            'polished_deepslate_wall',
            'deepslate_brick_wall',
            'deepslate_tile_wall'
        ]
    }
    blocks['gatelike'] = {
        'values': [
            'acacia_fence_gate',
            'birch_fence_gate',
            'jungle_fence_gate',
            'mangrove_fence_gate',
            'oak_fence_gate',
            'dark_oak_fence_gate',
            'warped_fence_gate',
            'crimson_fence_gate',
            'spruce_fence_gate'
        ]
    }
    blocks['liquid'] = {
        'values': [
            'lava',
            'water'
        ]
    }
    blocks['ore_background'] = {
        'values': [
            'stone',
            'netherrack',
            'deepslate'
        ]
    }
    blocks['ore_blocks'] = {
        'values': [
            'coal_block',
            'iron_block',
            'copper_block',
            'gold_block',
            'diamond_block',
            'lapis_block',
            'redstone_block',
            'emerald_block',
            'quartz_block',
            'netherite_block'
        ]
    }
    blocks['ores'] = {
        'values': [
            'coal_ore',
            'iron_ore',
            'copper_ore',
            'gold_ore',
            'diamond_ore',
            'lapis_ore',
            'redstone_ore',
            'emerald_ore',
            'deepslate_coal_ore',
            'deepslate_iron_ore',
            'deepslate_copper_ore',
            'deepslate_gold_ore',
            'deepslate_diamond_ore',
            'deepslate_lapis_ore',
            'deepslate_redstone_ore',
            'deepslate_emerald_ore',
            'nether_quartz_ore',
            'nether_gold_ore',
            'ancient_debris'
        ]
    }
    blocks['rail'] = {
        'values': [
            'rail',
            'powered_rail',
            'detector_rail',
            'activator_rail'
        ]
    }
    blocks['sand'] = {
        'values': [
            'sand',
            'red_sand',
            'gravel'
        ]
    }
    blocks['soil'] = {
        'values': [
            'grass_block',
            'mycelium',
            'podzol',
            'dirt_path',
            'farmland'
        ]
    }

    blocks['stepable_planks'] = {
        'values': [
            'acacia_planks',
            'birch_planks',
            'jungle_planks',
            'mangrove_planks',
            'oak_planks',
            'dark_oak_planks',
            'spruce_planks',
            'stone',
            'cobblestone',
            'mossy_cobblestone',
            'bricks',
            'stone_bricks',
            'mud_bricks',
            'mossy_stone_bricks',
            'nether_bricks',
            'red_nether_bricks',
            'end_stone_bricks',
            'purpur_block',
            'sandstone',
            'smooth_sandstone',
            'red_sandstone',
            'smooth_red_sandstone',
            'prismarine',
            'prismarine_bricks',
            'dark_prismarine',
            'andesite',
            'polished_andesite',
            'diorite',
            'polished_diorite',
            'granite',
            'polished_granite',
            'blackstone',
            'polished_blackstone',
            'polished_blackstone_bricks',
            'quartz_block',
            'smooth_quartz',
            'warped_planks',
            'crimson_planks',
            'cobbled_deepslate',
            'polished_deepslate',
            'deepslate_bricks',
            'deepslate_tiles',
            'cut_copper',
            'exposed_cut_copper',
            'weathered_cut_copper',
            'oxidized_cut_copper'
        ]
    }
    blocks['stepable_stairs'] = {
        'values': [
            re.sub(r'blocks*', 'stairs',
                   re.sub(r'planks', 'stairs',
                          re.sub(r'(copper|stone$|marine$|ite$|slate$|_quartz$).*', r'\1_stairs',
                                 re.sub(r'(brick|tile)s*', r'\1_stairs', x))))
            for x in blocks['stepable_planks']['values']]
    }
    blocks['stepable_slabs'] = {
        'values': [x.replace('stairs', 'slab') for x in blocks['stepable_stairs']['values']]
    }