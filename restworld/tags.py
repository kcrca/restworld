from itertools import chain

from pynecraft.base import to_id
from pynecraft.commands import COLORS
from pynecraft.function import BLOCK
from pynecraft.info import corals, leaves_for, stems, steppable, woods
from restworld.world import restworld


def create():
    colorable = {
        'banner': None,
        'carpet': None,
        'concrete': None,
        'concrete_powder': None,
        'wool': None,
        'wool_slab': None,
        'wool_stairs': None,
        'candle': 'candle',
        'candle_cake': ('candle_cake', 'cake'),
        'shulker_box': 'shulker_box',
        'stained_glass': 'glass',
        'stained_glass_pane': 'glass_pane',
        'terracotta': 'terracotta'}

    blocks = restworld.tags(BLOCK)
    for thing, added in colorable.items():
        blocks[thing] = {
            'values': [f'{c}_{thing}' for c in COLORS]
        }
        if isinstance(added, tuple):
            blocks[thing]['values'].extend(added)
        elif added:
            blocks[thing]['values'].append(added)

    # Things that need clearing out wider than usual for the particle room, so be particular to avoid damaging stuff
    blocks['particles_clear'] = {
        'water', 'barrier', 'structure_void'
    }

    blocks['chests'] = {'#copper_chests', 'chest'}

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
        'values': [f'{x}_stained_glass_pane' for x in COLORS] + [f'{x}_fence' for x in woodlike_ids] + [
            'nether_brick_fence',
            '#bars',
            'glass_pane',
            '#walls'
        ]
    }
    blocks['gatelike'] = {'values': [f'{x}_fence_gate' for x in woodlike_ids]}
    blocks['leaflike'] = [
        *chain.from_iterable(leaves_for(wood) for wood in wood_ids),
        'nether_wart_block',
        'warped_wart_block',
    ]
    blocks['woodlike'] = {'values': [f'{x}_wood' for x in wood_ids] + [f'{x}_hyphae' for x in stem_ids]}
    blocks['loglike'] = {'values': [f'{x}_log' for x in wood_ids] + [f'{x}_stem' for x in stem_ids]}
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

    # base/stairs/slab derived from pynecraft.steppable; waxed copper excluded (cosmetically
    # identical to unwaxed). The three stay index-aligned since they share one filtered source.
    no_waxing = [s for s in steppable if not s.block.startswith('waxed_')]
    blocks['stepable_blocks'] = {'values': [s.block for s in no_waxing]}
    blocks['stepable_stairs'] = {'values': [s.stairs for s in no_waxing]}
    blocks['stepable_slabs'] = {'values': [s.slab for s in no_waxing]}
    blocks['planks'] = {
        'values': ['#planks', 'bamboo_mosaic']
    }
