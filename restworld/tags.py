import re

from pynecraft.base import to_id
from pynecraft.commands import COLORS
from pynecraft.function import BLOCK
from pynecraft.info import corals, stems, woods
from restworld.world import restworld


def create():
    colorable = {
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

    blocks = restworld.tags(BLOCK)
    for thing, added in colorable.items():
        blocks[thing] = {
            'values': ['%s_%s' % (c, thing) for c in COLORS]
        }
        if isinstance(added, tuple):
            blocks[thing]['values'].extend(added)
        elif added:
            blocks[thing]['values'].append(added)

    # Things that need clearing out wider than usual for the particle room, so be particular to avoid damaging stuff
    blocks['particles_clear'] = {
        'water', 'barrier', 'structure_void'
    }

    blocks['air'] = {
        'values': [
            'air',
            'cave_air'
        ]
    }
    wood_ids = tuple(to_id(x) for x in woods)
    stem_ids = tuple(to_id(x) for x in stems)
    woodlike_ids = wood_ids + stem_ids
    blocks['fencelike'] = {
        'values': ['%s_stained_glass_pane' % x for x in COLORS] + [f'{x}_fence' for x in woodlike_ids] + [
            'nether_brick_fence',
            '#bars',
            'glass_pane',
            'brick_wall',
            'cobblestone_wall',
            'mud_brick_wall',
            'mossy_cobblestone_wall',
            'resin_brick_wall',
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
    blocks['gatelike'] = {'values': [f'{x}_fence_gate' for x in woodlike_ids]}
    blocks['leaflike'] = {
        'values': ['%s_leaves' % x for x in wood_ids] + [
            'nether_wart_block',
            'warped_wart_block',
        ]
    }
    blocks['woodlike'] = {'values': [f'{x}_wood' for x in wood_ids] + [f'{x}_hyphae' for x in stem_ids]}
    blocks['loglike'] = {'values': [f'{x}_log' for x in wood_ids] + [f'{x}_stem' for x in stem_ids]}
    blocks['leaflike']['values'] = list(filter(lambda x: x != 'bamboo_leaves', blocks['leaflike']['values']))
    blocks['woodlike']['values'] = list(filter(lambda x: x != 'bamboo_wood', blocks['woodlike']['values']))
    sp = blocks['loglike']['values']
    sp[sp.index('bamboo_log')] = 'bamboo_block'
    blocks['stripped_loglike'] = {'values': [f'stripped_{x}' for x in blocks['loglike']['values']]}
    blocks['stripped_woodlike'] = {'values': [f'stripped_{x}' for x in blocks['woodlike']['values']]}

    blocks['saplinglike'] = {
        'values': [
            'acacia_sapling',
            'bamboo_sapling',
            'bamboo',
            'birch_sapling',
            'cherry_sapling',
            'jungle_sapling',
            'mangrove_propagule',
            'oak_sapling',
            'dark_oak_sapling',
            'pale_oak_sapling',
            'spruce_sapling',
            'warped_roots',
            'warped_fungus',
            'crimson_roots',
            'crimson_fungus'
        ]
    }
    coral_ids = tuple(x.lower() for x in corals)
    blocks['coral_fans'] = {'values': [f'{x}_coral_fan' for x in coral_ids]}
    blocks['dead_coral_plants'] = {'values': [f'dead_{x}_coral' for x in coral_ids]}
    blocks['dead_coral_blocks'] = {'values': [f'dead_{x}_coral_block' for x in coral_ids]}
    blocks['dead_coral_fans'] = {'values': [f'dead_{x}_coral_fan' for x in coral_ids]}
    blocks['dead_wall_corals'] = {'values': [f'dead_{x}_coral_wall_fan' for x in coral_ids]}
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
    blocks['falling'] = {
        'values': [
            'sand',
            'suspicious_sand',
            'red_sand',
            'gravel',
            'suspicious_gravel',
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
    blocks['no_model_block'] = {
        'values': [
            '#doors',
            '#beds',
            'sugar_cane',  # must be _next to_ water
            'weeping_vines',  # must be _under_ the right block
            'cactus',  # Must be on falling block (sand)
            'sunflower',  # tall flower
            'peony',  # tall flower
            'rose_bush',  # tall flower
            'lilac',  # tall flower
            'pitcher_plant',  # tall flower
        ]
    }

    def coppers(which):
        return [f'copper_{which}'] + [f'{x}_copper_{which}' for x in ('exposed', 'weathered', 'oxidized')]

    blocks['stepable_planks'] = {
        'values': [
            'acacia_planks',
            'bamboo_planks',
            'bamboo_mosaic_block',
            'birch_planks',
            'cherry_planks',
            'jungle_planks',
            'mangrove_planks',
            'oak_planks',
            'dark_oak_planks',
            'pale_oak_planks',
            'spruce_planks',
            'stone',
            'cobblestone',
            'mossy_cobblestone',
            'bricks',
            'stone_bricks',
            'mud_bricks',
            'mossy_stone_bricks',
            'resin_bricks',
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
            'tuff',
            'tuff_bricks',
            'polished_tuff',
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
    blocks['planks'] = {
        'values': ['#planks', 'bamboo_mosaic']
    }
    blocks['stepable_stairs'] = {
        'values': [
            re.sub(r'blocks*', 'stairs',
                   re.sub(r'planks', 'stairs',
                          re.sub(r'(copper|stone$|tuff$|marine$|ite$|slate$|_quartz$).*', r'\1_stairs',
                                 re.sub(r'(brick|tile)s*', r'\1_stairs', x))))
            for x in blocks['stepable_planks']['values']]
    }
    blocks['stepable_slabs'] = {
        'values': [x.replace('stairs', 'slab') for x in blocks['stepable_stairs']['values']]
    }
    sp = blocks['stepable_planks']['values']
    sp[sp.index('bamboo_mosaic_block')] = 'bamboo_mosaic'
