from __future__ import annotations

import math
import random

from pynecraft.base import EAST, NORTH, Nbt, OVERWORLD, SOUTH, WEST, d, r, good_facing
from pynecraft.commands import Block, CLEAR, Entity, RAIN, REPLACE, a, data, e, execute, fill, fillbiome, function, \
    item, kill, p, particle, playsound, schedule, setblock, summon, tp, weather
from pynecraft.enums import BiomeId, Particle
from pynecraft.simpler import VILLAGER_BIOMES, VILLAGER_PROFESSIONS, WallSign
from restworld.rooms import ActionDesc, SignedRoom, Wall, span
from restworld.world import fast_clock, kill_em, main_clock, restworld, slow_clock

particles = [
    ActionDesc(Particle.AMBIENT_ENTITY_EFFECT, 'Ambient|Entity|Effect'),
    ActionDesc(Particle.ANGRY_VILLAGER),
    ActionDesc(Particle.ASH),
    ActionDesc(Particle.BUBBLE, 'Bubbles|Currents|Whirlpools',
               also=(Particle.BUBBLE_POP, Particle.BUBBLE_COLUMN_UP, Particle.CURRENT_DOWN)),
    ActionDesc(Particle.CLOUD, note='Evaporation'),
    ActionDesc(Particle.COMPOSTER),
    ActionDesc(Particle.CRIMSON_SPORE),
    ActionDesc(Particle.CRIT),
    ActionDesc(Particle.DAMAGE_INDICATOR),
    ActionDesc(Particle.DOLPHIN),
    ActionDesc(Particle.DRAGON_BREATH),
    ActionDesc(Particle.CHERRY_LEAVES, 'Cherry Leaves'),
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
    ActionDesc(Particle.BLOCK_MARKER),
    ActionDesc(Particle.MYCELIUM),
    ActionDesc(Particle.NAUTILUS, note='with Conduit'),
    ActionDesc(Particle.POOF, note='Small Explosion'),
    ActionDesc(Particle.PORTAL),
    ActionDesc(Particle.VIBRATION, 'Sculk Sensor', note='Vibration'),
    ActionDesc(Particle.SCULK_SOUL, also=(Particle.SCULK_CHARGE, Particle.SCULK_CHARGE_POP)),
    ActionDesc(Particle.SHRIEK, 'Shriek'),
    ActionDesc(Particle.SMOKE),
    ActionDesc(Particle.SNEEZE),
    ActionDesc(Particle.RAIN),
    ActionDesc(Particle.SNOWFLAKE, 'Snow'),
    ActionDesc(Particle.SONIC_BOOM),
    ActionDesc(Particle.SOUL),
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
    Particle.ELDER_GUARDIAN,  # Just the elder guardian face in your face, and makes it hard to turn off.
    Particle.ITEM,  # Same as BLOCK
    Particle.NOTE,  # Always shown in the redstone room (as is DUST, FWIW)
    Particle.SPIT,  # Broke at 1.19, can't get the summoned spit to move.
    Particle.FALLING_NECTAR,  # Shown with the bees in the Friendlies room
    Particle.SPORE_BLOSSOM_AIR, Particle.FALLING_SPORE_BLOSSOM,  # Just outside the room
}
particles.sort(key=lambda x: str(x.enum).replace('|', ' '))
# Notes:
#    Maybe spit can be made to work with a live llama hitting a wolf, but the llama must be penned in, etc.
#
#    Lower priority, easily seen around: DUST, NOTE, UNDERWATER (also not much to see), SPORE_BLOSSOM (right outside
#    the room), MYCELIUM (same), PORTAL (which can be seen in Materials), SCULK_SENSOR (Redstone)
#
#    Could loop the BLOCK_MARKER types in one thing.
#    Could loop WHITE_ASH, CRIMSON_SPORE, etc.?
#    Could loop various explosions?

villager_data = []
for t in VILLAGER_BIOMES:
    for pro in VILLAGER_PROFESSIONS:
        villager_data.append({'profession': pro.lower(), 'type': t.lower()})
    random.shuffle(villager_data)


def at_center():
    return execute().at(e().tag('particles_action_home')).positioned(r(0, 2, 0)).run('')


def clock(which, delay=0):
    return execute().if_().score(which.time).matches(delay).at(e().tag('particles_action_home')).positioned(
        r(0, 2, 0))


def fast(delay=0):
    return clock(fast_clock, delay)


def main(delay=0):
    return clock(main_clock, delay)


def slow(delay=0):
    return clock(slow_clock, delay)


def exemplar(id, y, nbt=None):
    nbt = Nbt({'Tags': ['particler'], 'Silent': True, 'PersistenceRequired': True}).merge(nbt)
    return summon(id, r(0, y, 0), nbt)


def floor(block):
    return fill(r(-3, -1, -3), r(3, -1, 3), block)


def set_biome(biome):
    return fillbiome(r(-3, 1, -3), r(3, 5, 3), biome)


def room():
    check_for_unused()

    def particle_sign(action_desc, wall):
        dx, _, dz = good_facing(wall.facing).scale(1)
        run_at = execute().at(e().tag('particles_action_home')).positioned(r(0, 2, 0))
        return WallSign(action_desc.sign_text(), (
            run_at.run(setblock(r(0, -4, 0), 'redstone_block')),
            run_at.run(data().merge(r(0, -4, -2), {
                'Command': f'{str(run_at.run(""))} function restworld:particles/{action_desc.enum}_init'})),
            run_at.run(data().merge(r(-1, -2, 0), {
                'Command': f'{str(run_at.run(""))} function restworld:particles/{action_desc.enum}'})),
            setblock(d(-dx, 0, -dz), 'emerald_block')
        ))

    e_wall_used = {5: (1, 2, 5, 6), 4: span(1, 6), 3: span(1, 6), 2: span(1, 6)}
    n_wall_used = {4: span(1, 5), 3: span(1, 5), 2: span(1, 5)}
    w_wall_used = {5: (0, 1, 4, 5), 4: span(0, 5), 3: span(0, 5), 2: span(0, 5)}
    room = SignedRoom('particles', restworld, SOUTH, (None, 'Particles'), particle_sign, particles, (
        Wall(7, EAST, 1, -1, e_wall_used),
        Wall(7, SOUTH, 1, -7, n_wall_used),
        Wall(7, WEST, 7, -7, w_wall_used),
    ))
    room.function('signs_init', home=False).add(function('restworld:particles/signs'))

    room.function('ambient_entity_effect', home=False).add(
        main().run(particle(Particle.AMBIENT_ENTITY_EFFECT, r(0, 0, 0), 0.5, 5, 0.5, 1, 500)))
    room.function('ambient_entity_effect_init', home=False).add(function('restworld:particles/villager'))
    room.function('angry_villager', home=False).add(
        fast().run(particle(Particle.ANGRY_VILLAGER, r(0, 1, 0), 0.5, 0.5, 0.5, 0, 5)))
    room.function('angry_villager_init', home=False).add(function('restworld:particles/villager'))
    room.loop('animal', home=False).loop(lambda step: exemplar(step.elem, 0, {'NoAI': True}), (
        Block('cow'), Block('Pig'), Block('Horse'), Block('Llama'), Block('Sheep'), Block('Polar Bear'), Block('Goat')))
    room.function('ash_init', home=False).add(
        floor('soul_soil'),
        set_biome(BiomeId.SOUL_SAND_VALLEY))
    room.function('barrier', home=False).add(
        main().run(particle(Particle.BLOCK_MARKER, 'barrier', r(0, 2, 0), 0, 0, 0, 0, 1)))
    room.function('light', home=False).add(
        main().run(particle(Particle.BLOCK_MARKER, 'light', r(0, 2, 0), 0, 0, 0, 0, 1)))

    def block_marker_loop(step):
        yield particle(Particle.BLOCK_MARKER, step.elem, r(0, 2, 0))

    room.loop('block_marker_run').loop(block_marker_loop, ('barrier', 'light'))
    room.function('block_marker', home=False).add(
        slow().run(function('restworld:particles/block_marker_run')))
    room.function('bubble_init', home=False).add(
        fill(r(1, -1, 1), r(1, -1, -1), 'magma_block'),
        fill(r(-1, -1, 1), r(-1, -1, -1), 'soul_sand'),
        function('restworld:particles/ocean'))
    room.function('cloud', home=False).add(main().run(particle(Particle.CLOUD, r(0, 1, 0), 0.25, 0.25, 0.25, 0.05, 50)))
    room.function('composter', home=False).add(
        main().run(particle(Particle.COMPOSTER, r(0, 0.9, 0), 0.2, 0.1, 0.2, 1, 12)))
    room.function('composter_init', home=False).add(setblock(r(0, 0, 0), ('composter', {'level': 3})))
    room.function('crimson_spore_init', home=False).add(
        floor('crimson_nylium'),
        set_biome(BiomeId.CRIMSON_FOREST))
    room.function('crit', home=False).add(fast().run(particle(Particle.CRIT, r(0, 1.5, 0), 0.5, 0.5, 0.5, 0, 10)))
    room.function('crit_init', home=False).add(function('restworld:particles/animal'))
    room.function('damage_indicator', home=False).add(
        fast().run(particle(Particle.DAMAGE_INDICATOR, r(0, 1.5, 0), 0.5, 0.5, 0.5, 0, 5)))
    room.function('damage_indicator_init', home=False).add(function('restworld:particles/animal'))
    room.function('dolphin_init', home=False).add(
        fill(r(-3, 0, 5), r(3, 6, 5), 'barrier').replace('air'),
        fill(r(0, 0, 5), r(0, 1, 5), 'air'),
        fill(r(4, 5, 4), r(-4, 5, -4), 'barrier'),
        fill(r(3, 5, 3), r(-3, 5, -3), 'air'),
        fill(r(3, 7, 3), r(-3, 7, -3), 'barrier'),
        function('restworld:particles/ocean'),
        exemplar('dolphin', 1.5),
    )
    room.function('dragon_breath', home=False).add(slow().run(function('restworld:particles/dragon_breath_run')))
    room.function('dragon_breath_init', home=False).add(floor('end_stone'))
    room.function('dragon_breath_run', home=False).add(
        kill(e().tag('particle_dragonball')),
        summon('dragon_fireball', r(0, 4, 4),
               {'power': {0.0, -0.05, -0.05}, 'ExplosionPower': 0, 'Tags': ['particle_dragonball', 'particler']}),
        schedule().function('restworld:particles/dragon_breath_finish', 1, REPLACE),
    )
    room.function('dragon_breath_finish', home=False).add(
        data().merge(e().tag('particle_dragonball').limit(1), {'Motion': [0, -0.5, -0.5]}))
    cherry = room.function('cherry_leaves_init', home=False).add(
        fill(r(2, 4, 2), r(-2, 4, -2), 'cherry_leaves'), floor('grass_block'))
    for x in range(-3, 4):
        for z in range(-3, 4):
            level = random.randint(0, 4)
            if level > 0:
                cherry.add(
                    setblock(r(x, 0, z), ('pink_petals',
                                          {'flower_amount': level,
                                           'facing': ('north', 'east', 'south', 'west')[random.randint(0, 3)]})))
    room.function('dripping_honey_init', home=False).add(
        fill(r(2, 4, 2), r(-2, 4, -2), ('beehive', {'honey_level': 5, 'facing': SOUTH})),
        fill(r(2, 4, -2), r(-2, 4, -2), ('beehive', {'honey_level': 5, 'facing': NORTH})),
        fill(r(2, 4, -1), r(2, 4, 1), ('beehive', {'honey_level': 5, 'facing': EAST})),
        fill(r(-2, 4, -1), r(-2, 4, 1), ('beehive', {'honey_level': 5, 'facing': WEST})),
    )

    def drip_base(dripper):
        return (
            fill(r(3, 5, 3), r(-3, 5, -3), 'structure_void'),
            fill(r(2, 4, 2), r(-2, 4, -2), 'stone'),
            setblock(r(2, 4, 2), 'dripstone_block'),
            setblock(r(-2, 4, 2), 'dripstone_block'),
            setblock(r(2, 4, -2), 'dripstone_block'),
            setblock(r(-2, 4, -2), 'dripstone_block'),
            setblock(r(2, 3, 2), 'pointed_dripstone[thickness=base,vertical_direction=down]'),
            setblock(r(-2, 3, 2), 'pointed_dripstone[thickness=base,vertical_direction=down]'),
            setblock(r(2, 3, -2), 'pointed_dripstone[thickness=base,vertical_direction=down]'),
            setblock(r(-2, 3, -2), 'pointed_dripstone[thickness=base,vertical_direction=down]'),
            fill(r(2, 5, 2), r(-2, 5, -2), dripper),
        )

    room.function('dripping_lava_init', home=False).add(drip_base('lava'))
    room.function('dripping_obsidian_tear_init', home=False).add(fill(r(1, 4, 1), r(-1, 4, -1), 'crying_obsidian'))
    room.function('dripping_water_init', home=False).add(drip_base('water'))
    room.function('dust_init', home=False).add(
        fill(r(2, 0, 2), r(-2, 0, -2), 'redstone_wire'),
        fill(r(1, 0, 1), r(-1, 0, -1), 'air'),
        setblock(r(-1, 0, -2), 'air'),
        setblock(r(-2, 0, -2), 'redstone_block'),
        setblock(r(-2, 0, -1), 'repeater'),
    )
    room.function('effect', home=False).add(fast().run(particle(Particle.EFFECT, r(0, 1, 0), 0.25, 0.5, 0.5, 0.2, 20)))
    room.function('effect_init', home=False).add(exemplar('evoker', 0, {'NoAI': True}))
    room.function('electric_spark', home=False).add(main().run(summon('lightning_bolt', r(0, 1, 0))))
    room.function('electric_spark_init', home=False).add(setblock(r(0, 0, 0), 'lightning_rod'))
    room.function('enchant_init', home=False).add(
        fill(r(2, 0, 1), r(-2, 0, -2), 'bookshelf'),
        fill(r(2, 1, -1), r(-2, 1, -2), 'bookshelf'),
        fill(r(1, 0, 1), r(-1, 1, -1), 'air'),
        setblock(r(0, 0, 0), 'enchanting_table'),
    )
    room.function('enchanted_hit', home=False).add(
        fast().run(particle(Particle.ENCHANTED_HIT, r(0, 1, 0, 0.5), 0.5, 0.5, 0, 15)))
    room.function('enchanted_hit_init', home=False).add(function('restworld:particles/animal'))
    room.function('end_rod_init', home=False).add(
        fill(r(-1, 0, 0), r(1, 0, 0), 'end_rod'),
        fill(r(-1, 2, -2), r(1, 2, -2), ('end_rod', {'facing': SOUTH})))
    room.function('entity_effect', home=False).add(
        main().run(particle(Particle.ENTITY_EFFECT, r(0, 1, 0), 0.25, 0.5, 0.5, 0.2, 80)))
    room.function('entity_effect_init', home=False).add(function('restworld:particles/animal'))
    room.function('explosion', home=False).add(
        main().run(particle(Particle.EXPLOSION, r(0, 1, 0), 0.5, 0.5, 0.5, 2, 8)))
    room.function('explosion_emitter', home=False).add(
        main().run(particle(Particle.EXPLOSION_EMITTER, r(0, 1, 0), 0.5, 0.5, 0.5, 0.2, 1)))
    room.function('falling_dust', home=False).add(main().run(function('restworld:particles/falling_dust_change')))

    def falling_dust_loop(step):
        yield fill(r(-2, 5, -2), r(2, 5, 2), step.elem.id)
        yield particle(Particle.FALLING_DUST, step.elem.id, r(0, 4.9, 0), 1.5, 0, 1.5, 0, 50)

    room.loop('falling_dust_change', home=False).loop(falling_dust_loop, (
        Block('Dragon Egg'), Block('Sand'), Block('Red Sand'), Block('Gravel'), Block('Green Concrete Powder')))
    room.function('falling_dust_init', home=False).add(
        fill(r(-2, 4, -2), r(2, 4, 2), 'barrier'),
        function('restworld:particles/falling_dust_change'))
    room.function('firework', home=False).add(main().run(function('restworld:particles/firework_change')))
    room.loop('firework_change', home=False).loop(
        lambda step: item().replace().block(r(0, 1, 0), 'container.0').with_(Entity('firework_rocket', nbt={
            'Fireworks': {'Explosions': [{'Colors': Nbt.TypedArray('I', (step.elem,)), 'Trail': 1, 'Type': step.i}],
                          'Flight': 0}})), (11743532, 6719955, 14602026, 3887386, 15790320)).add(
        setblock(r(0, 0, 0), 'redstone_torch'),
        setblock(r(0, 0, 0), 'air'))
    room.function('firework_init', home=False).add(setblock(r(0, 1, 0), ('dispenser', {'facing': 'up'})))
    room.function('fishing', home=False).add(fast().run(particle(Particle.FISHING, r(0, 1.5, 0), 0.2, 0, 0.2, 0, 6)))
    room.function('fishing_init', home=False).add(
        fill(r(-3, 0, 4), r(3, 0, 4), 'oak_wall_sign'),
        fill(r(3, 0, 3), r(-3, 0, -3), 'water'))
    room.function('flame_init', home=False).add(
        fill(r(-2, 0, -2), r(-2, 0, 2), 'torch'),
        fill(r(2, 0, -2), r(2, 0, 2), 'soul_torch'),
        setblock(r(0, 0, 0), Block('spawner', nbt={'SpawnData': {'entity': {'id': 'zombie'}}}))
    )
    room.function('happy_villager', home=False).add(
        fast().run(particle(Particle.HAPPY_VILLAGER, r(0, 1, 0), 0.5, 0.5, 0.5, 0, 5)))
    room.function('happy_villager_init', home=False).add(function('restworld:particles/villager'))
    room.function('heart', home=False).add(fast().run(particle(Particle.HEART, r(0, 1.5, 0), 0.5, 0.2, 0.5, 0, 5)))
    room.function('heart_init', home=False).add(function('restworld:particles/small_animal'))
    room.function('instant_effect', home=False).add(
        fast().run(particle(Particle.INSTANT_EFFECT, r(0, 1.5, 0), 0.5, 1, 0.5, 0, 10)))
    room.function('instant_effect_init', home=False).add(function('restworld:particles/animal'))
    room.function('item_slime_init', home=False).add(
        fill(r(-2, 0, -2), r(2, 1, 2), 'barrier'),
        fill(r(-1, 0, -1), r(1, 1, 1), 'air'),
        exemplar('slime', 0, {'Size': 1}),
        tp(p().distance((None, 7)), r(0, 0, -3)).facing(r(0, 0, 5)))
    room.function('item_snowball', home=False).add(
        fast().run(item().replace().block(r(0, 2, -1), 'container.0').with_('snowball', 1)),
        fast().run(setblock(r(0, 3, -1), ('stone_button', {'powered': True, 'face': 'floor'}))),
        fast().run(setblock(r(0, 3, -1), 'air')),
    )
    room.function('item_snowball_init', home=False).add(
        setblock(r(0, 2, -1), ('dispenser', {'facing': SOUTH})),
        fill(r(-1, 2, 4), r(1, 2, 4), 'glass'),
        setblock(r(0, 3, 4), 'glass'))
    room.function('large_smoke_init', home=False).add(setblock(r(0, 0, 0), 'fire'))
    room.function('lava_init', home=False).add(
        fill(r(-2, 0, -2), r(2, 0, 2), 'stone'),
        fill(r(-1, 0, -1), r(1, 0, 1), 'lava'))
    room.function('mycelium_init', home=False).add(floor('mycelium'))
    room.function('nautilus', home=False).add(slow().run(function('restworld:particles/nautilus_change')))
    room.loop('nautilus_change', home=False).loop(
        lambda step: fill(r(-2, 0, -2), r(2, 2, 0), 'prismarine' if step.i == 0 else 'sand'), range(0, 2)).add(
        fill(r(-1, 1, -1), r(1, 2, 0), 'water'),
        setblock(r(0, 2, 0), 'conduit'))
    room.function('nautilus_init', home=False).add(
        function('restworld:particles/ocean'),
        fill(r(-2, 0, -2), r(2, 2, 0), 'prismarine'),
        fill(r(-1, 1, -1), r(1, 2, 0), 'air'),
        setblock(r(0, 2, 0), 'conduit'))
    room.function('note', home=False).add(
        fast().run(setblock(r(0, 0, -1), ('stone_button', {'powered': True, 'facing': NORTH}))),
        fast().run(setblock(r(0, 0, -1), 'air')))
    room.function('note_init', home=False).add(setblock(r(0, 0, 0), 'note_block'))
    room.function('ocean', home=False).add(
        fill(r(-3, 0, 4), r(3, 0, 4), 'structure_void'),
        fill(r(3, 6, 3), r(-3, 6, -3), 'structure_void'),
        fill(r(2, 6, 2), r(-2, 6, -2), 'water'),
        fill(r(2, 0, 2), r(-2, 6, -2), 'water'),
    )
    room.function('particles_clear', home=False).add(
        kill_em(e().tag('particler')),
        fill(r(20, 0, 20), r(-20, 10, -20), 'air').replace('snow'),
        set_biome(BiomeId.PLAINS),
        execute().in_(OVERWORLD).run(weather(CLEAR)))
    room.function('poof', home=False).add(main().run(particle(Particle.POOF, r(0, 1, 0), 0.25, 0.25, 0.25, 0, 30)))
    room.function('portal_init', home=False).add(
        fill(r(-2, 0, -1), r(2, 4, -1), 'obsidian'),
        fill(r(-1, 1, -1), r(1, 3, -1), 'nether_portal'))
    room.function('vibration', home=False).add(main().run(function('restworld:particles/vibration_run')))
    room.function('vibration_init', home=False).add(
        setblock(r(2, 0, 2), ('piston', {'facing': 'up'})),
        setblock(r(2, 1, -2), ('piston', {'facing': 'up'})),
        setblock(r(-2, 2, -2), ('piston', {'facing': 'up'})),
        setblock(r(-2, 3, 2), ('piston', {'facing': 'up'})),
        setblock(r(0, 0, 0), 'sculk_sensor'),
        room.score('sculk_particles').set(0),
    )
    coords = (r(3, 0, 2), r(2, 0, -2), r(-2, 1, -2), r(-2, 2, 2))

    def vibration_loop(step):
        yield setblock(step.elem, 'redstone_torch')
        yield setblock(coords[(step.i - 1 + len(coords)) % len(coords)], 'air')

    room.loop('vibration_run', home=False).loop(vibration_loop, coords)

    room.function('sculk_soul_init', home=False).add(
        setblock(r(0, 0, 0), 'sculk_catalyst'),
    )
    room.function('sculk_soul', home=False).add(
        main().run(fill(r(-1, -1, -1), r(1, -1, 1), 'stone_bricks').replace('sculk')),
        main().run(fill(r(-1, 0, -1), r(1, 0, 1), 'air').replace('sculk_vein')),
        main().run(function('restworld:particles/sculk_soul_show')),
        main(delay=1).run(setblock(r(0, 0, 0), ('sculk_catalyst', {'bloom': True}))),
        main(delay=5).run(function('restworld:particles/sculk_spread')),
        main(delay=9).run(setblock(r(0, 0, 0), ('sculk_catalyst', {'bloom': False}))),
        main(delay=16).run(function('restworld:particles/sculk_pop')),
    )
    room.function('sculk_soul_show', home=False).add(
        particle(Particle.SCULK_SOUL, r(0, 0.5, 2)),
        particle(Particle.SCULK_SOUL, r(-1.5, 0.5, 1)),
        particle(Particle.SCULK_SOUL, r(1, 0.5, -1)))
    sculk_pos = (r(-1, -1, -1), r(0, -1, -1), r(-1, -1, 1), r(0, 0, -1), r(0, 0, 1), r(1, 0, 0))
    spread = room.function('sculk_spread', home=False)
    pop = room.function('sculk_pop', home=False)
    for i, pos in enumerate(sculk_pos):
        block = 'sculk' if str(pos[1]) == '~-1' else ('sculk_vein', {'down': True})
        height = 1.3 if str(pos[1]) == '~-1' else 0.5
        spread.add(particle(Particle.SCULK_CHARGE, random.uniform(-math.pi / 6, +math.pi / 6),
                            (pos[0], pos[1] + height, pos[2])))
        pop.add(
            setblock(pos, block),
            particle(Particle.SCULK_CHARGE_POP, (pos[0], pos[1] + height, pos[2])))
    room.function('shriek', home=False).add(
        slow().run(function('restworld:particles/shriek_out')),
        slow(delay=7 * 8).run(setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True, 'shrieking': False}))))
    room.function('shriek_init', home=False).add(setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True})))
    room.function('shriek_out', home=False).add(
        setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True, 'shrieking': True})),
        function('restworld:particles/shriek_particles'))
    room.function('shriek_particles', home=False).add(
        (particle(Particle.SHRIEK, i * 7, r(0, 1, 0)) for i in range(0, 8)))
    room.loop('small_animal', home=False).loop(lambda step: exemplar(step.elem, 0, {'CatType': 1, 'NoAI': True}),
                                               ('ocelot', 'horse', 'llama'))
    room.function('smoke_init', home=False).add(
        setblock(r(-1, 0, 0), 'torch'),
        setblock(r(0, 0, 0), 'brewing_stand'),
        setblock(r(1, 0, 0), 'soul_torch'))
    room.function('sneeze', home=False).add(
        main().run(particle(Particle.SNEEZE, r(0, 0.25, 1.25), 0.05, 0.05, 0.5, 0.0, 2)),
        main().run(playsound('entity.panda.sneeze', 'neutral', a(), r(0, 0, 0))))
    room.function('sneeze_init', home=False).add(exemplar('panda', 0, {'NoAI': True, 'Age': -2147483648}))
    room.function('rain_init', home=False).add(weather(RAIN))
    room.function('rain_exit', home=False).add(weather(CLEAR))
    room.function('snowflake_init', home=False).add(set_biome(BiomeId.SNOWY_TAIGA), weather(RAIN))
    room.function('snowflake_exit', home=False).add(weather(CLEAR))
    room.function('sonic_boom_init', home=False).add(exemplar('warden', 0, {'NoAI': True}))
    room.function('sonic_boom', home=False).add(main().run(particle(Particle.SONIC_BOOM, r(0, 2, 0.5), 0, 0, 0, 1, 1)))
    room.function('soul', home=False).add(main().run(particle(Particle.SOUL, r(0, 0.75, 0), 0.05, 0, 0.05, 0.05, 4)))
    room.function('soul_init', home=False).add(floor('soul_soil'))
    room.function('spit', home=False).add(fast().run(summon('llama_spit', r(0, 1.6, 0.7),
                                                            {'Motion': [0.0, 0.0, 1.0], 'direction': [0.0, 0.0, 1.0],
                                                             'ExplosionPower': 1})))
    room.function('spit_init', home=False).add(exemplar('llama', 0, {'NoAI': True}))
    room.function('splash', home=False).add(fast().run(particle(Particle.SPLASH, r(0, 1, 0), 0.5, 0.1, 0.5, 1, 50)))
    room.function('splash_init', home=False).add(
        fill(r(-2, 0, -2), r(2, 0, 2), 'stone'),
        fill(r(-1, 0, -1), r(1, 0, 1), 'water'))
    # Currently not done: Low priority (just outside) Making room for separate RAIN and SNOW
    # room.function('spore_blossom_air_init', home=False).add(
    #     setblock(r(0, 4, 0), 'stone'),
    #     setblock(r(0, 3, 0), 'spore_blossom'))
    room.function('squid_ink', home=False).add(main().run(function('restworld:particles/squid_ink_run')))
    room.function('squid_ink_init', home=False).add(function('restworld:particles/ocean'))

    def squid_ink_loop(step):
        yield exemplar(step.elem, 4, {'NoAI': True})
        yield particle(step.elem + '_ink', r(0, 2.8, -0), 0.15, 0.3, 0.15, 0.01, 30)

    room.loop('squid_ink_run', home=False).add(
        kill_em(e().tag('particler'))).loop(
        squid_ink_loop, ('squid', 'glow_squid'))
    room.function('sweep_attack', home=False).add(
        main().run(particle(Particle.SWEEP_ATTACK, r(0, 1, 0), 0.3, 0.2, 0.3, 0, 3)))
    room.function('totem_of_undying', home=False).add(
        main().run(particle(Particle.TOTEM_OF_UNDYING, r(0, 2, 0), 0.5, 1, 0.5, 0.5, 50)))
    room.function('underwater_init', home=False).add(function('restworld:particles/ocean'))
    room.loop('villager', home=False).loop(
        lambda step: exemplar('villager', 0, {'NoAI': True, 'VillagerData': step.elem}),
        villager_data)
    room.function('warped_spore_init', home=False).add(
        floor('warped_nylium'),
        set_biome(BiomeId.WARPED_FOREST))
    room.function('wax_on', home=False).add(main().run(function('restworld:particles/wax_on_run')))
    room.function('wax_on_init', home=False).add(
        setblock(r(0, 0, 0), 'cut_copper'),
        exemplar('armor_stand', 0, {'Invisible': True, 'Small': True, 'CustomNameVisible': True}))

    def wax_on_run_loop(step):
        yield data().merge(e().tag('particler').limit(1),
                           {'CustomName': step.elem, 'CustomNameVisible': len(step.elem) > 0})
        if step.i == 0:
            yield setblock(r(0, 0, 0), 'exposed_cut_copper')
        elif step.i == 1:
            yield particle(Particle.WAX_ON, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)
        elif step.i == 2:
            yield particle(Particle.WAX_OFF, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)
        else:
            yield setblock(r(0, 0, 0), 'cut_copper')
            yield particle(Particle.SCRAPE, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)

    room.loop('wax_on_run', home=False).loop(wax_on_run_loop, ('', 'Wax On', 'Wax Off', 'Scrape'))
    room.function('white_ash_init', home=False).add(
        floor('basalt'),
        set_biome(BiomeId.BASALT_DELTAS))
    room.function('witch', home=False).add(fast().run(particle(Particle.WITCH, r(0, 2.3, 0), 0.3, 0.3, 0.3, 0, 6)))
    room.function('witch_init', home=False).add(exemplar('witch', 0, {'NoAI': True}))

    # Keeping these in case of future need:
    # room.function('falling_nectar_init', home=False).add(exemplar('bee', 2, {'HasNectar': 1, 'NoAI': True}))


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
