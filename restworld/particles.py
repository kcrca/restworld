from __future__ import annotations

import math
import random

from pyker.base import Nbt
from pyker.commands import SOUTH, mc, EAST, WEST, rotated_facing, d, e, r, Block, NORTH, p, OVERWORLD, \
    CLEAR, RAIN, a
from pyker.enums import Particle
from pyker.info import villager_professions
from pyker.simpler import WallSign
from restworld.rooms import SignedRoom, Wall, span, ActionDesc
from restworld.world import restworld, fast_clock, main_clock, slow_clock, kill_em

particles = [
    ActionDesc(Particle.AMBIENT_ENTITY_EFFECT, 'Ambient|Entity|Effect'),
    ActionDesc(Particle.ANGRY_VILLAGER),
    ActionDesc(Particle.ASH),
    ActionDesc(Particle.BARRIER),
    ActionDesc(Particle.BUBBLE, 'Bubbles|Currents|Whirlpools',
               also=(Particle.BUBBLE_POP, Particle.BUBBLE_COLUMN_UP, Particle.CURRENT_DOWN)),
    ActionDesc(Particle.CLOUD, note='Evaporation'),
    ActionDesc(Particle.COMPOSTER),
    ActionDesc(Particle.CRIMSON_SPORE),
    ActionDesc(Particle.CRIT),
    ActionDesc(Particle.DAMAGE_INDICATOR),
    ActionDesc(Particle.DOLPHIN),
    ActionDesc(Particle.DRAGON_BREATH),
    ActionDesc(Particle.DRIPPING_LAVA, note='Falling, Landing', also=(
        Particle.FALLING_LAVA, Particle.LANDING_LAVA, Particle.DRIPPING_DRIPSTONE_LAVA,
        Particle.FALLING_DRIPSTONE_LAVA)),
    ActionDesc(Particle.DRIPPING_WATER, note='Falling',
               also=(Particle.FALLING_WATER, Particle.DRIPPING_DRIPSTONE_WATER, Particle.FALLING_DRIPSTONE_WATER)),
    ActionDesc(Particle.DRIPPING_OBSIDIAN_TEAR, 'Dripping|Obsidian Tear', note='Falling, Landing',
               also=(Particle.FALLING_OBSIDIAN_TEAR, Particle.LANDING_OBSIDIAN_TEAR)),
    ActionDesc(Particle.DRIPPING_HONEY, note='Falling, Landing', also=(Particle.FALLING_HONEY, Particle.LANDING_HONEY)),
    ActionDesc(Particle.DUST, note='Redstone Dust'),
    ActionDesc(Particle.EFFECT),
    ActionDesc(Particle.ELECTRIC_SPARK),
    ActionDesc(Particle.ENCHANT),
    ActionDesc(Particle.ENCHANTED_HIT),
    ActionDesc(Particle.END_ROD),
    ActionDesc(Particle.ENTITY_EFFECT),
    ActionDesc(Particle.EXPLOSION),
    ActionDesc(Particle.EXPLOSION_EMITTER),
    ActionDesc(Particle.FALLING_DUST),
    ActionDesc(Particle.FALLING_NECTAR),
    ActionDesc(Particle.FIREWORK, note='and Flash', also=Particle.FLASH),
    ActionDesc(Particle.FISHING),
    ActionDesc(Particle.FLAME, also=Particle.SOUL_FIRE_FLAME),
    ActionDesc(Particle.HAPPY_VILLAGER),
    ActionDesc(Particle.HEART),
    ActionDesc(Particle.INSTANT_EFFECT),
    ActionDesc(Particle.ITEM_SLIME),
    ActionDesc(Particle.ITEM_SNOWBALL),
    ActionDesc(Particle.LARGE_SMOKE),
    ActionDesc(Particle.LAVA),
    ActionDesc(Particle.LIGHT, also=(Particle.BLOCK_MARKER)),
    ActionDesc(Particle.MYCELIUM),
    ActionDesc(Particle.NAUTILUS, note='with Conduit'),
    ActionDesc(Particle.POOF, note='Small Explosion'),
    ActionDesc(Particle.PORTAL),
    ActionDesc(Particle.VIBRATION, 'Sculk Sensor'),
    ActionDesc(Particle.SCULK_SOUL, also=(Particle.SCULK_CHARGE, Particle.SCULK_CHARGE_POP)),
    ActionDesc(Particle.SHRIEK, 'Shriek'),
    ActionDesc(Particle.SMOKE),
    ActionDesc(Particle.SNEEZE),
    ActionDesc(Particle.RAIN, 'Snow and Rain', also=Particle.SNOWFLAKE),
    ActionDesc(Particle.SOUL),
    ActionDesc(Particle.SPORE_BLOSSOM_AIR, 'Spore Blossom', also=Particle.FALLING_SPORE_BLOSSOM),
    ActionDesc(Particle.SPLASH),
    ActionDesc(Particle.SQUID_INK, note='and Glow Squid', also=(Particle.GLOW, Particle.GLOW_SQUID_INK)),
    ActionDesc(Particle.SWEEP_ATTACK),
    ActionDesc(Particle.TOTEM_OF_UNDYING),
    ActionDesc(Particle.UNDERWATER),
    ActionDesc(Particle.WAX_ON, 'Wax', note='and Copper', also=(Particle.WAX_OFF, Particle.SCRAPE)),
    ActionDesc(Particle.WARPED_SPORE),
    ActionDesc(Particle.WHITE_ASH),
    ActionDesc(Particle.WITCH),
]
unused_particles = {
    Particle.BLOCK,  # This just happens in the game, plus I can't see how to generate it.
    Particle.CAMPFIRE_COSY_SMOKE,  # In block room
    Particle.CAMPFIRE_SIGNAL_SMOKE,  # Same as regular campfire smoke, just goes higher
    Particle.DUST_COLOR_TRANSITION,  # Can the player control its look? AFAICT, it's just when the power level changes?
    Particle.ELDER_GUARDIAN,  # Just the elder guardian face in your face, anbd makes it hard to turn off.
    Particle.ITEM,  # Same as BLOCK
    Particle.NOTE,  # Always shown in the redstone room (as is DUST, FWIW)
    Particle.SPIT,  # Broke at 1.19, can't get the summond spit to move.
}
particles.sort()
# Notes:
#    Maybe spit can be made to work with a live llama hitting a wolf, but the llama must be penned in, etc.
#    Lower priority, easily seen around: DUST, NOTE, UNDERWATER (also not much to see), SPORE_BLOSSOM (right outside
#    the room), PORTAL (which can be seen in Materials).
#
#    Could loop the BLOCK_MARKER types in one thing.
#    Could loop WHITE_ASH, CRIMSON_SPRE, etc.?
#    Could loop various explosions?

villager_types = ('Desert', 'Jungle', 'Plains', 'Savanna', 'Snow', 'Swamp', 'Taiga')
villager_data = []
for t in villager_types:
    for pro in villager_professions:
        villager_data.append({'profession': pro.lower(), 'type': t.lower()})
    random.shuffle(villager_data)


def at_center():
    return mc.execute().at(e().tag('particles_action_home')).positioned(r(0, 2, 0)).run()


def clock(which, delay=0):
    return mc.execute().if_().score(which.time).matches(delay).at(e().tag('particles_action_home')).positioned(
        r(0, 2, 0)).run()


def fast(delay=0):
    return clock(fast_clock, delay)


def main(delay=0):
    return clock(main_clock, delay)


def slow(delay=0):
    return clock(slow_clock, delay)


def summon(id, y, nbt=None):
    nbt = Nbt({'Tags': ['particler']}).merge(nbt)
    return mc.summon(id, r(0, y, 0), nbt)


def floor(block):
    return mc.fill(r(-3, -1, -3), r(3, -1, 3), block)


def room():
    check_for_unused()

    def particle_sign(action_desc, wall):
        dx, _, dz = rotated_facing(wall.facing).scale(1)
        run_at = mc.execute().at(e().tag('particles_action_home')).positioned(r(0, 2, 0)).run()
        return WallSign(action_desc.sign_text(), (
            run_at.setblock(r(0, -4, 0), 'redstone_block'),
            run_at.data().merge(r(0, -4, -2), {
                'Command': f'{str(run_at)} function restworld:particles/{action_desc.enum}_init'}),
            run_at.data().merge(r(-1, -2, 0),
                                {'Command': f'{str(run_at)} function restworld:particles/{action_desc.enum}'}),
            mc.setblock(d(-dx, 0, -dz), 'emerald_block')
        ))

    e_wall_used = {5: (1, 2, 5, 6), 4: span(1, 6), 3: span(1, 6), 2: span(1, 6)}
    n_wall_used = {4: span(1, 5), 3: span(1, 5), 2: span(1, 5)}
    w_wall_used = {5: (0, 1, 4, 5), 4: span(0, 5), 3: span(0, 5), 2: span(0, 5)}
    room = SignedRoom('particles', restworld, SOUTH, (None, 'Particles'), particle_sign, particles, (
        Wall(7, EAST, 1, -1, e_wall_used),
        Wall(7, SOUTH, 1, -7, n_wall_used),
        Wall(7, WEST, 7, -7, w_wall_used),
    ))
    room.function('signs_init').add(mc.function('restworld:particles/signs'))

    room.function('ambient_entity_effect', home=False).add(
        main().particle(Particle.AMBIENT_ENTITY_EFFECT, r(0, 0, 0), 0.5, 5, 0.5, 1, 500))
    room.function('ambient_entity_effect_init').add(mc.function('restworld:particles/villager'))
    room.function('angry_villager', home=False).add(
        fast().particle(Particle.ANGRY_VILLAGER, r(0, 1, 0), 0.5, 0.5, 0.5, 0, 5))
    room.function('angry_villager_init').add(mc.function('restworld:particles/villager'))
    room.loop('animal').loop(lambda step: summon(step.elem, 0, {'NoAI': True}), (
        Block('cow'), Block('Pig'), Block('Horse'), Block('Llama'), Block('Sheep'), Block('Polar Bear'), Block('Goat')))
    room.function('ash', home=False).add(fast().particle(Particle.ASH, r(0, 5, 0), 1, 0, 1, 1, 30))
    room.function('ash_init', home=False).add(floor('soul_soil'))
    room.function('barrier', home=False).add(
        main().particle(Particle.BLOCK_MARKER, 'barrier', r(0, 2, 0), 0, 0, 0, 0, 1))
    room.function('bubble_init', home=False).add(
        mc.fill(r(1, -1, 1), r(1, -1, -1), 'magma_block'),
        mc.fill(r(-1, -1, 1), r(-1, -1, -1), 'soul_sand'),
        mc.function('restworld:particles/ocean'))
    room.function('cloud', home=False).add(main().particle(Particle.CLOUD, r(0, 1, 0), 0.25, 0.25, 0.25, 0.05, 50))
    room.function('composter', home=False).add(main().particle(Particle.COMPOSTER, r(0, 0.9, 0), 0.2, 0.1, 0.2, 1, 12))
    room.function('composter_init', home=False).add(mc.setblock(r(0, 0, 0), ('composter', {'level': 3})))
    room.function('crimson_spore', home=False).add(
        fast().particle(Particle.CRIMSON_SPORE, r(0, 2, 0), 1, 0, 1, 0.0, 25))
    room.function('crimson_spore_init', home=False).add(floor('crimson_nylium'))
    room.function('crit', home=False).add(fast().particle(Particle.CRIT, r(0, 1.5, 0), 0.5, 0.5, 0.5, 0, 10))
    room.function('crit_init').add(mc.function('restworld:particles/animal'))
    room.function('damage_indicator', home=False).add(
        fast().particle(Particle.DAMAGE_INDICATOR, r(0, 1.5, 0), 0.5, 0.5, 0.5, 0, 5))
    room.function('damage_indicator_init').add(mc.function('restworld:particles/animal'))
    room.function('dolphin_init', home=False).add(
        mc.fill(r(-3, 0, 5), r(3, 6, 5), 'barrier').replace('air'),
        mc.fill(r(0, 0, 5), r(0, 1, 5), 'air'),
        mc.fill(r(4, 5, 4), r(-4, 5, -4), 'barrier'),
        mc.fill(r(3, 5, 3), r(-3, 5, -3), 'air'),
        mc.fill(r(3, 7, 3), r(-3, 7, -3), 'barrier'),
        mc.function('restworld:particles/ocean'),
        summon('dolphin', 1.5),
    )
    room.function('dragon_breath', home=False).add(slow().function('restworld:particles/dragon_breath_run'))
    room.function('dragon_breath_init', home=False).add(room.score('dragon_breath_run').set(-1))
    room.function('dragon_breath_run', home=False).add(
        mc.kill(e().tag('particle_dragonball')),
        mc.summon('dragon_fireball', r(0, 4, 4),
                  {'direction': {0.0, 0.0, 0.0}, 'power': {0.0, -0.05, -0.05}, 'ExplosionPower': 0,
                   'Tags': ['particle_dragonball', 'particler']}),
    )
    room.function('dripping_honey_init', home=False).add(
        mc.fill(r(2, 3, 2), r(-2, 3, -2), ('beehive', {'honey_level': 5, 'facing': SOUTH})),
        mc.fill(r(2, 3, -2), r(-2, 3, -2), ('beehive', {'honey_level': 5, 'facing': NORTH})),
        mc.fill(r(2, 3, -1), r(2, 3, 1), ('beehive', {'honey_level': 5, 'facing': EAST})),
        mc.fill(r(-2, 3, -1), r(-2, 3, 1), ('beehive', {'honey_level': 5, 'facing': WEST})),
    )

    def drip_base(dripper):
        return (
            mc.fill(r(3, 5, 3), r(-3, 5, -3), 'structure_void'),
            mc.fill(r(2, 4, 2), r(-2, 4, -2), 'stone'),
            mc.setblock(r(2, 4, 2), 'dripstone_block'),
            mc.setblock(r(-2, 4, 2), 'dripstone_block'),
            mc.setblock(r(2, 4, -2), 'dripstone_block'),
            mc.setblock(r(-2, 4, -2), 'dripstone_block'),
            mc.setblock(r(2, 3, 2), 'pointed_dripstone[thickness=base,vertical_direction=down]'),
            mc.setblock(r(-2, 3, 2), 'pointed_dripstone[thickness=base,vertical_direction=down]'),
            mc.setblock(r(2, 3, -2), 'pointed_dripstone[thickness=base,vertical_direction=down]'),
            mc.setblock(r(-2, 3, -2), 'pointed_dripstone[thickness=base,vertical_direction=down]'),
            mc.fill(r(2, 5, 2), r(-2, 5, -2), dripper),
        )

    room.function('dripping_lava_init', home=False).add(drip_base('lava'))
    room.function('dripping_obsidian_tear_init', home=False).add(mc.fill(r(1, 4, 1), r(-1, 4, -1), 'crying_obsidian'))
    room.function('dripping_water_init', home=False).add(drip_base('water'))
    room.function('dust_init', home=False).add(
        mc.fill(r(2, 0, 2), r(-2, 0, -2), 'redstone_wire'),
        mc.fill(r(1, 0, 1), r(-1, 0, -1), 'air'),
        mc.setblock(r(-1, 0, -2), 'air'),
        mc.setblock(r(-2, 0, -2), 'redstone_block'),
        mc.setblock(r(-2, 0, -1), 'repeater'),
    )
    room.function('effect', home=False).add(fast().particle(Particle.EFFECT, r(0, 1, 0), 0.25, 0.5, 0.5, 0.2, 20))
    room.function('effect_init', home=False).add(summon('evoker', 0, {'NoAI': True}))
    room.function('electric_spark', home=False).add(main().summon('lightning_bolt', r(0, 1, 0)))
    room.function('electric_spark_init', home=False).add(mc.setblock(r(0, 0, 0), 'lightning_rod'))
    room.function('enchant_init', home=False).add(
        mc.fill(r(2, 0, 1), r(-2, 0, -2), 'bookshelf'),
        mc.fill(r(2, 1, -1), r(-2, 1, -2), 'bookshelf'),
        mc.fill(r(1, 0, 1), r(-1, 1, -1), 'air'),
        mc.setblock(r(0, 0, 0), 'enchanting_table'),
    )
    room.function('enchanted_hit', home=False).add(
        fast().particle(Particle.ENCHANTED_HIT, r(0, 1, 0, 0.5), 0.5, 0.5, 0, 15))
    room.function('enchanted_hit_init').add(mc.function('restworld:particles/animal'))
    room.function('end_rod_init', home=False).add(
        mc.fill(r(-1, 0, 0), r(1, 0, 0), 'end_rod'),
        mc.fill(r(-1, 2, -2), r(1, 2, -2), ('end_rod', {'facing': SOUTH})))
    room.function('entity_effect', home=False).add(
        main().particle(Particle.ENTITY_EFFECT, r(0, 1, 0), 0.25, 0.5, 0.5, 0.2, 80))
    room.function('entity_effect_init').add(mc.function('restworld:particles/animal'))
    room.function('explosion', home=False).add(main().particle(Particle.EXPLOSION, r(0, 1, 0), 0.5, 0.5, 0.5, 2, 8))
    room.function('explosion_emitter', home=False).add(
        main().particle(Particle.EXPLOSION_EMITTER, r(0, 1, 0), 0.5, 0.5, 0.5, 0.2, 1))
    room.function('falling_dust', home=False).add(main().function('restworld:particles/falling_dust_change'))

    def falling_dust_loop(step):
        yield mc.fill(r(-2, 5, -2), r(2, 5, 2), step.elem.id)
        yield mc.particle(Particle.FALLING_DUST, step.elem.id, r(0, 4.9, 0), 1.5, 0, 1.5, 0, 50)

    room.loop('falling_dust_change').loop(falling_dust_loop, (
        Block('Dragon Egg'), Block('Sand'), Block('Red Sand'), Block('Gravel'), Block('Green Concrete Powder')))
    room.function('falling_dust_init', home=False).add(
        mc.fill(r(-2, 4, -2), r(2, 4, 2), 'barrier'),
        mc.function('restworld:particles/falling_dust_change'))
    room.function('falling_nectar_init', home=False).add(summon('bee', 2, {'HasNectar': 1, 'NoAI': True}))
    room.function('firework', home=False).add(main().function('restworld:particles/fireworks_change'))
    room.loop('firework_change').loop(
        lambda step: mc.item().replace().block(r(0, 1, 0), 'container.0').with_('firework_rocket' + str(Nbt({
            'Fireworks': {'Explosions': [{'Colors': f'[I;{step.elem:d}]', 'Trail': 1, 'Type': step.i}],
                          'Flight': 0}})).replace('"', '')), (11743532, 6719955, 14602026, 3887386, 15790320)).add(
        mc.setblock(r(0, 0, 0), 'redstone_torch'),
        mc.setblock(r(0, 0, 0), 'air'))
    room.function('firework_init', home=False).add(mc.setblock(r(0, 1, 0), ('dispenser', {'facing': 'up'})))
    room.function('fishing', home=False).add(fast().particle(Particle.FISHING, r(0, 1.5, 0), 0.2, 0, 0.2, 0, 6))
    room.function('fishing_init', home=False).add(
        mc.fill(r(-3, 0, 4), r(3, 0, 4), 'oak_wall_sign'),
        mc.fill(r(3, 0, 3), r(-3, 0, -3), 'water'))
    room.function('flame_init', home=False).add(
        mc.fill(r(-2, 0, -2), r(-2, 0, 2), 'torch'),
        mc.fill(r(2, 0, -2), r(2, 0, 2), 'soul_torch'),
        mc.setblock(r(0, 0, 0), 'spawner')
    )
    room.function('happy_villager', home=False).add(
        fast().particle(Particle.HAPPY_VILLAGER, r(0, 1, 0), 0.5, 0.5, 0.5, 0, 5))
    room.function('happy_villager_init').add(mc.function('restworld:particles/villager'))
    room.function('heart', home=False).add(fast().particle(Particle.HEART, r(0, 1.5, 0), 0.5, 0.2, 0.5, 0, 5))
    room.function('heart_init').add(mc.function('restworld:particles/small_animal'))
    room.function('instant_effect', home=False).add(
        fast().particle(Particle.INSTANT_EFFECT, r(0, 1.5, 0), 0.5, 1, 0.5, 0, 10))
    room.function('instant_effect_init').add(mc.function('restworld:particles/animal'))
    room.function('item_slime_init', home=False).add(
        mc.fill(r(-2, 0, -2), r(2, 1, 2), 'barrier'),
        mc.fill(r(-1, 0, -1), r(1, 1, 1), 'air'),
        summon('slime', 0, {'Size': 1}),
        mc.tp(p().distance((None, 7)), r(0, 0, -3)).facing(r(0, 0, 5)))
    room.function('item_snowball', home=False).add(
        fast().item().replace().block(r(0, 2, -1), 'container.0').with_('snowball', 1),
        fast().setblock(r(0, 3, -1), ('stone_button', {'powered': True, 'face': 'floor'})),
        fast().setblock(r(0, 3, -1), 'air'),
    )
    room.function('item_snowball_init', home=False).add(
        mc.setblock(r(0, 2, -1), ('dispenser', {'facing': SOUTH})),
        mc.fill(r(-1, 2, 4), r(1, 2, 4), 'glass'),
        mc.setblock(r(0, 3, 4), 'glass'))
    room.function('large_smoke_init', home=False).add(mc.setblock(r(0, 0, 0), 'fire'))
    room.function('lava_init', home=False).add(
        mc.fill(r(-2, 0, -2), r(2, 0, 2), 'stone'),
        mc.fill(r(-1, 0, -1), r(1, 0, 1), 'lava'))
    room.function('light', home=False).add(main().particle(Particle.BLOCK_MARKER, 'light', r(0, 2, 0), 0, 0, 0, 0, 1))
    room.function('mycelium_init', home=False).add(floor('mycelium'))
    room.function('nautilus', home=False).add(slow().function('restworld:particles/nautilus_change'))
    room.loop('nautilus_change').loop(
        lambda step: mc.fill(r(-2, 0, -2), r(2, 2, 0), 'prismarine' if step.i == 0 else 'sand'), range(0, 2)).add(
        mc.fill(r(-1, 1, -1), r(1, 2, 0), 'water'),
        mc.setblock(r(0, 2, 0), 'conduit'))
    room.function('nautilus_init', home=False).add(
        mc.function('restworld:particles/ocean'),
        mc.fill(r(-2, 0, -2), r(2, 2, 0), 'prismarine'),
        mc.fill(r(-1, 1, -1), r(1, 2, 0), 'air'),
        mc.setblock(r(0, 2, 0), 'conduit'))
    room.function('note', home=False).add(
        fast().setblock(r(0, 0, -1), ('stone_button', {'powered': True, 'facing': NORTH})),
        fast().setblock(r(0, 0, -1), 'air'))
    room.function('note_init', home=False).add(mc.setblock(r(0, 0, 0), 'note_block'))
    room.function('ocean', home=False).add(
        mc.fill(r(-3, 0, 4), r(3, 0, 4), 'structure_void'),
        mc.fill(r(3, 6, 3), r(-3, 6, -3), 'structure_void'),
        mc.fill(r(2, 6, 2), r(-2, 6, -2), 'water'),
        mc.fill(r(2, 0, 2), r(-2, 6, -2), 'water'),
    )
    room.function('particles_clear', home=False).add(
        kill_em(e().tag('particler')),
        mc.fill(r(20, 0, 20), r(-20, 10, -20), 'air').replace('snow'),
        mc.execute().in_(OVERWORLD).run().weather(CLEAR))
    room.function('poof', home=False).add(main().particle(Particle.POOF, r(0, 1, 0), 0.25, 0.25, 0.25, 0, 30))
    room.function('portal_init', home=False).add(
        mc.fill(r(-2, 0, -1), r(2, 4, -1), 'obsidian'),
        mc.fill(r(-1, 1, -1), r(1, 3, -1), 'nether_portal'))
    room.function('vibration', home=False).add(fast().function('restworld:particles/vibration_run'))
    room.function('vibration_init', home=False).add(
        mc.setblock(r(2, 0, 2), ('piston', {'facing': 'up'})),
        mc.setblock(r(2, 1, -2), ('piston', {'facing': 'up'})),
        mc.setblock(r(-2, 2, -2), ('piston', {'facing': 'up'})),
        mc.setblock(r(-2, 3, 2), ('piston', {'facing': 'up'})),
        mc.setblock(r(0, 0, 0), 'sculk_sensor'),
        room.score('sculk_particles').set(0),
    )
    coords = (r(3, 0, 2), r(2, 0, -2), r(-2, 1, -2), r(-2, 2, 2))

    def vibration_loop(step):
        yield mc.setblock(step.elem, 'redstone_torch')
        yield mc.setblock(coords[(step.i - 1 + len(coords)) % len(coords)], 'air')

    room.loop('vibration_run').loop(vibration_loop, coords)

    room.function('sculk_soul_init', home=False).add(
        mc.setblock(r(0, 0, 0), 'sculk_catalyst'),
    )
    room.function('sculk_soul', home=False).add(
        main().fill(r(-1, -1, -1), r(1, -1, 1), 'stone_bricks').replace('sculk'),
        main().fill(r(-1, 0, -1), r(1, 0, 1), 'air').replace('sculk_vein'),
        main().function('restworld:particles/sculk_soul_show'),
        main(delay=1).setblock(r(0, 0, 0), ('sculk_catalyst', {'bloom': True})),
        main(delay=5).function('restworld:particles/sculk_spread'),
        main(delay=9).setblock(r(0, 0, 0), ('sculk_catalyst', {'bloom': False})),
        main(delay=16).function('restworld:particles/sculk_pop'),
    )
    room.function('sculk_soul_show', home=False).add(
        mc.particle(Particle.SCULK_SOUL, r(0, 0.5, 2)),
        mc.particle(Particle.SCULK_SOUL, r(-1.5, 0.5, 1)),
        mc.particle(Particle.SCULK_SOUL, r(1, 0.5, -1)))
    sculk_pos = (r(-1, -1, -1), r(0, -1, -1), r(-1, -1, 1), r(0, 0, -1), r(0, 0, 1), r(1, 0, 0))
    spread = room.function('sculk_spread', home=False)
    pop = room.function('sculk_pop', home=False)
    for i, pos in enumerate(sculk_pos):
        block = 'sculk' if str(pos[1]) == '~-1' else ('sculk_vein', {'down': True})
        height = 1.3 if str(pos[1]) == '~-1' else 0.5
        spread.add(mc.particle(Particle.SCULK_CHARGE, random.uniform(-math.pi / 6, +math.pi / 6),
                               (pos[0], pos[1] + height, pos[2])))
        pop.add(
            mc.setblock(pos, block),
            mc.particle(Particle.SCULK_CHARGE_POP, (pos[0], pos[1] + height, pos[2])))
    room.function('shriek', home=False).add(
        slow().function('restworld:particles/shriek_out'),
        slow(delay=7 * 8).setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True, 'shrieking': False})))
    room.function('shriek_init', home=False).add(mc.setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True})))
    room.function('shriek_out', home=False).add(
        mc.setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True, 'shrieking': True})),
        mc.function('restworld:particles/shriek_particles'))
    room.function('shriek_particles', home=False).add(
        (mc.particle(Particle.SHRIEK, i * 7, r(0, 1, 0)) for i in range(0, 8)))
    room.loop('small_animal').loop(lambda step: summon(step.elem, 0, {'CatType': 1, 'NoAI': True}),
                                   ('ocelot', 'horse', 'llama'))
    room.function('smoke_init', home=False).add(
        mc.setblock(r(-1, 0, 0), 'torch'),
        mc.setblock(r(0, 0, 0), 'brewing_stand'),
        mc.setblock(r(1, 0, 0), 'soul_torch'))
    room.function('sneeze', home=False).add(
        main().particle(Particle.SNEEZE, r(0, 0.25, 1.25), 0.05, 0.05, 0.5, 0.0, 2),
        main().playsound('entity.panda.sneeze', 'neutral', a(), r(0, 0, 0)))
    room.function('sneeze_init', home=False).add(summon('panda', 0, {'NoAI': True, 'Age': -2147483648}))
    room.function('rain_init', home=False).add(mc.weather(RAIN))
    room.function('rain_exit', home=False).add(mc.weather(CLEAR))
    room.function('soul', home=False).add(main().particle(Particle.SOUL, r(0, 0.75, 0), 0.05, 0, 0.05, 0.05, 4))
    room.function('soul_init', home=False).add(floor('soul_soil'))
    room.function('spit', home=False).add(fast().summon('llama_spit', r(0, 1.6, 0.7),
                                                        {'Motion': [0.0, 0.0, 1.0], 'direction': [0.0, 0.0, 1.0],
                                                         'ExplosionPower': 1}))
    room.function('spit_init', home=False).add(summon('llama', 0, {'NoAI': True}))
    room.function('splash', home=False).add(fast().particle(Particle.SPLASH, r(0, 1, 0), 0.5, 0.1, 0.5, 1, 50))
    room.function('splash_init', home=False).add(
        mc.fill(r(-2, 0, -2), r(2, 0, 2), 'stone'),
        mc.fill(r(-1, 0, -1), r(1, 0, 1), 'water'))
    room.function('spore_blossom_air_init', home=False).add(
        mc.setblock(r(0, 4, 0), 'stone'),
        mc.setblock(r(0, 3, 0), 'spore_blossom'))
    room.function('squid_ink', home=False).add(main().function('restworld:particles/squid_ink_run'))
    room.function('squid_ink_init').add(mc.function('restworld:particles/ocean'))

    def squid_ink_loop(step):
        yield summon(step.elem, 4, {'NoAI': True})
        yield mc.particle(step.elem + '_ink', r(0, 2.8, -0), 0.15, 0.3, 0.15, 0.01, 30)

    room.loop('squid_ink_run').add(
        kill_em(e().tag('particler'))).loop(
        squid_ink_loop, ('squid', 'glow_squid'))
    room.function('sweep_attack', home=False).add(
        main().particle(Particle.SWEEP_ATTACK, r(0, 1, 0), 0.3, 0.2, 0.3, 0, 3))
    room.function('totem_of_undying', home=False).add(
        main().particle(Particle.TOTEM_OF_UNDYING, r(0, 2, 0), 0.5, 1, 0.5, 0.5, 50))
    room.function('underwater_init').add(mc.function('restworld:particles/ocean'))
    room.loop('villager').loop(lambda step: summon('villager', 0, {'NoAI': True, 'VillagerData': step.elem}),
                               villager_data)
    room.function('warped_spore', home=False).add(
        fast().particle(Particle.WARPED_SPORE, r(0, 2, 0), 1, 0, 1, 0.0, 25))
    room.function('warped_spore_init', home=False).add(floor('warped_nylium'))
    room.function('wax_on', home=False).add(main().function('restworld:particles/wax_on_run'))
    room.function('wax_on_init', home=False).add(
        mc.setblock(r(0, 0, 0), 'cut_copper'),
        summon('armor_stand', 0, {'Invisible': True, 'Small': True, 'CustomNameVisible': True}))

    def wax_on_run_loop(step):
        yield mc.data().merge(e().tag('particler').limit(1),
                              {'CustomName': step.elem, 'CustomNameVisible': len(step.elem) > 0})
        if step.i == 0:
            yield mc.setblock(r(0, 0, 0), 'exposed_cut_copper')
        elif step.i == 1:
            yield mc.particle(Particle.WAX_ON, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)
        elif step.i == 2:
            yield mc.particle(Particle.WAX_OFF, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)
        else:
            yield mc.setblock(r(0, 0, 0), 'cut_copper')
            yield mc.particle(Particle.SCRAPE, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)

    room.loop('wax_on_run').loop(wax_on_run_loop, ('', 'Wax On', 'Wax Off', 'Scrape'))
    room.function('white_ash', home=False).add(fast().particle(Particle.WHITE_ASH, r(0, 5, 0), 1, 0, 1, 1, 30))
    room.function('white_ash_init', home=False).add(floor('basalt'))
    room.function('witch', home=False).add(fast().particle(Particle.WITCH, r(0, 2.3, 0), 0.3, 0.3, 0.3, 0, 6))
    room.function('witch_init', home=False).add(summon('witch', 0, {'NoAI': True}))


def check_for_unused():
    # Check for unexpectedly unhandled particles
    used = set()
    for p in particles:
        used.add(p.enum)
        for a in p.also:
            used.add(a)
    avail = set(x for x in Particle) - unused_particles
    unused = tuple(sorted((str(x) for x in (avail - used))))
    if unused:
        raise ValueError(f'Unused particles: {unused}')
