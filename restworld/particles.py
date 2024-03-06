from __future__ import annotations

import math
import random

from pynecraft.base import EAST, NORTH, Nbt, OVERWORLD, SOUTH, WEST, as_facing, d, r
from pynecraft.commands import Block, CLEAR, Entity, RAIN, REPLACE, a, data, e, execute, fill, fillbiome, function, \
    item, kill, p, particle, playsound, schedule, setblock, summon, tp, weather
from pynecraft.simpler import PLAINS, TextDisplay, VILLAGER_BIOMES, VILLAGER_PROFESSIONS, WallSign
from pynecraft.values import AMBIENT_ENTITY_EFFECT, ANGRY_VILLAGER, ASH, BASALT_DELTAS, BLOCK, BLOCK_MARKER, BUBBLE, \
    BUBBLE_COLUMN_UP, \
    BUBBLE_POP, CAMPFIRE_COSY_SMOKE, CAMPFIRE_SIGNAL_SMOKE, CHERRY_LEAVES, CLOUD, COMPOSTER, CRIMSON_FOREST, \
    CRIMSON_SPORE, CRIT, \
    CURRENT_DOWN, \
    DAMAGE_INDICATOR, DOLPHIN, \
    DRAGON_BREATH, DRIPPING_DRIPSTONE_LAVA, DRIPPING_DRIPSTONE_WATER, DRIPPING_HONEY, DRIPPING_LAVA, \
    DRIPPING_OBSIDIAN_TEAR, \
    DRIPPING_WATER, DUST, DUST_COLOR_TRANSITION, DUST_PLUME, EFFECT, EGG_CRACK, ELDER_GUARDIAN, ELECTRIC_SPARK, ENCHANT, \
    ENCHANTED_HIT, \
    END_ROD, \
    ENTITY_EFFECT, EXPLOSION, EXPLOSION_EMITTER, FALLING_DRIPSTONE_LAVA, \
    FALLING_DRIPSTONE_WATER, FALLING_DUST, FALLING_HONEY, \
    FALLING_LAVA, FALLING_NECTAR, FALLING_OBSIDIAN_TEAR, FALLING_SPORE_BLOSSOM, FALLING_WATER, FIREWORK, FISHING, FLAME, \
    FLASH, GLOW, \
    GLOW_SQUID_INK, GUST, \
    GUST_DUST, \
    GUST_EMITTER, \
    HAPPY_VILLAGER, HEART, INSTANT_EFFECT, ITEM, ITEM_SLIME, ITEM_SNOWBALL, LANDING_HONEY, \
    LANDING_LAVA, LANDING_OBSIDIAN_TEAR, LARGE_SMOKE, LAVA, MYCELIUM, NAUTILUS, NOTE, POOF, PORTAL, \
    REVERSE_PORTAL, \
    SCRAPE, SCULK_CHARGE, SCULK_CHARGE_POP, SCULK_SOUL, SHRIEK, SMALL_FLAME, SMOKE, \
    SNEEZE, SNOWFLAKE, SNOWY_TAIGA, SONIC_BOOM, SOUL, SOUL_FIRE_FLAME, SOUL_SAND_VALLEY, SPIT, SPLASH, \
    SPORE_BLOSSOM_AIR, SQUID_INK, \
    SWEEP_ATTACK, \
    TOTEM_OF_UNDYING, \
    TRIAL_SPAWNER_DETECTION, UNDERWATER, VAULT_CONNECTION, VIBRATION, WARPED_FOREST, WARPED_SPORE, WAX_OFF, WAX_ON, \
    WHITE_ASH, WITCH
from restworld.rooms import ActionDesc, SignedRoom, Wall, span
from restworld.world import fast_clock, kill_em, main_clock, restworld, slow_clock

actions = [
    ActionDesc(AMBIENT_ENTITY_EFFECT, 'Ambient|Entity|Effect'),
    ActionDesc(ANGRY_VILLAGER),
    ActionDesc(ASH),
    ActionDesc(BLOCK_MARKER),
    ActionDesc(BUBBLE, 'Bubbles|Currents|Whirlpools',
               also=(BUBBLE_POP, BUBBLE_COLUMN_UP, CURRENT_DOWN)),
    ActionDesc(CHERRY_LEAVES, 'Cherry Leaves'),
    ActionDesc(CLOUD, note='Evaporation'),
    ActionDesc(COMPOSTER),
    ActionDesc(CRIMSON_SPORE),
    ActionDesc(CRIT),
    ActionDesc(DAMAGE_INDICATOR),
    ActionDesc(DOLPHIN),
    ActionDesc(DRAGON_BREATH),
    ActionDesc(DRIPPING_HONEY, note='Falling, Landing', also=(FALLING_HONEY, LANDING_HONEY)),
    ActionDesc(DRIPPING_LAVA, note='Falling, Landing', also=(
        FALLING_LAVA, LANDING_LAVA, DRIPPING_DRIPSTONE_LAVA, FALLING_DRIPSTONE_LAVA)),
    ActionDesc(DRIPPING_OBSIDIAN_TEAR, 'Dripping|Obsidian Tear', note='Falling, Landing',
               also=(FALLING_OBSIDIAN_TEAR, LANDING_OBSIDIAN_TEAR)),
    ActionDesc(DRIPPING_WATER, note='Falling',
               also=(FALLING_WATER, DRIPPING_DRIPSTONE_WATER, FALLING_DRIPSTONE_WATER)),
    ActionDesc(DUST, note='Redstone Dust'),
    ActionDesc(DUST_PLUME),
    ActionDesc(EFFECT),
    ActionDesc(EGG_CRACK),
    ActionDesc(ELECTRIC_SPARK),
    ActionDesc(ENCHANT),
    ActionDesc(ENCHANTED_HIT),
    ActionDesc(END_ROD),
    ActionDesc(ENTITY_EFFECT),
    ActionDesc(EXPLOSION),
    ActionDesc(EXPLOSION_EMITTER),
    ActionDesc(FALLING_DUST),
    ActionDesc(FIREWORK, note='and Flash', also=FLASH),
    ActionDesc(FLAME, 'Flame, Small Flame|and Smoke',
               also=(SMALL_FLAME, SOUL_FIRE_FLAME, SMOKE)),
    ActionDesc(GUST, 'Gust|Gust Emitter|Gust Dust', also=(GUST_DUST, GUST_EMITTER)),
    ActionDesc(HAPPY_VILLAGER),
    ActionDesc(HEART),
    ActionDesc(INSTANT_EFFECT),
    ActionDesc(ITEM_SLIME),
    ActionDesc(ITEM_SNOWBALL),
    ActionDesc(LARGE_SMOKE),
    ActionDesc(LAVA),
    ActionDesc(MYCELIUM),
    ActionDesc(NAUTILUS, note='with Conduit'),
    ActionDesc(POOF, note='Small Explosion'),
    ActionDesc(PORTAL),
    ActionDesc(RAIN),
    ActionDesc(REVERSE_PORTAL),
    ActionDesc(SCULK_SOUL, also=(SCULK_CHARGE, SCULK_CHARGE_POP)),
    ActionDesc(SHRIEK, 'Shriek'),
    ActionDesc(SNEEZE),
    ActionDesc(SNOWFLAKE, 'Snow'),
    ActionDesc(SONIC_BOOM),
    ActionDesc(SOUL),
    ActionDesc(SPLASH),
    ActionDesc(SQUID_INK, note='and Glow Squid', also=(GLOW, GLOW_SQUID_INK)),
    ActionDesc(SWEEP_ATTACK),
    ActionDesc(TOTEM_OF_UNDYING),
    ActionDesc(TRIAL_SPAWNER_DETECTION),
    ActionDesc(UNDERWATER),
    ActionDesc(VAULT_CONNECTION),
    ActionDesc(VIBRATION, 'Sculk Sensor', note='Vibration'),
    ActionDesc(WARPED_SPORE),
    ActionDesc(WAX_ON, 'Wax', note='and Copper', also=(WAX_OFF, SCRAPE)),
    ActionDesc(WHITE_ASH),
    ActionDesc(WITCH),
]
unused_particles = {
    FISHING,
    BLOCK,  # This just happens in the game, plus I can't see how to generate it.
    CAMPFIRE_COSY_SMOKE,  # In block room
    CAMPFIRE_SIGNAL_SMOKE,  # Same as regular campfire smoke, just goes higher
    DUST_COLOR_TRANSITION,  # Can the player control its look? AFAICT, it's just when the power level changes?
    ELDER_GUARDIAN,  # Just the elder guardian face in your face, and makes it hard to turn off.
    ITEM,  # Same as BLOCK
    NOTE,  # Always shown in the redstone room (as is DUST, FWIW)
    SPIT,  # Broke at 1.19, can't get the summoned spit to move.
    FALLING_NECTAR,  # Shown with the bees in the Friendlies room
    SPORE_BLOSSOM_AIR, FALLING_SPORE_BLOSSOM,  # Just outside the room
}
actions.sort(key=lambda x: x.sort_key())
# Notes:
#    Maybe spit can be made to work with a live llama hitting a wolf, but the llama must be penned in, etc.
#
#    Lower priority, easily seen around: DUST, NOTE, UNDERWATER (also not much to see), SPORE_BLOSSOM (right outside
#    the room), MYCELIUM (same), PORTAL (which can be seen in Materials), SCULK_SENSOR (Redstone)
#
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


def exemplar(id, y, nbt=None, z=0):
    nbt = Nbt({'Tags': ['particler'], 'Silent': True, 'PersistenceRequired': True}).merge(nbt)
    return summon(id, r(0, y, z), nbt)


def floor(block):
    return fill(r(-3, -1, -3), r(3, -1, 3), block)


def set_biome(biome):
    return fillbiome(r(-3, 1, -3), r(3, 5, 3), biome)


def room():
    check_for_unused()

    def particle_sign(action_desc: ActionDesc, wall):
        dx, _, dz = as_facing(wall.facing).scale(1)
        run_at = execute().at(e().tag('particles_action_home')).positioned(r(0, 2, 0))
        return WallSign(action_desc.sign_text(), (
            run_at.run(setblock(r(0, -4, 0), 'redstone_block')),
            run_at.run(data().merge(r(0, -4, -2), {
                'Command': f'{str(run_at.run(""))} function restworld:particles/{action_desc.func()}_init'})),
            run_at.run(data().merge(r(-1, -2, 0), {
                'Command': f'{str(run_at.run(""))} function restworld:particles/{action_desc.func()}'})),
            setblock(d(-dx, 0, -dz), 'emerald_block')
        ))

    e_wall_used = {5: span(1, 6), 4: span(1, 6), 3: span(1, 6), 2: span(1, 6)}
    n_wall_used = {4: span(1, 5), 3: span(1, 5), 2: span(1, 5)}
    w_wall_used = {5: span(0, 5), 4: span(0, 5), 3: span(0, 5), 2: span(0, 5)}
    room = SignedRoom('particles', restworld, SOUTH, (None, 'Particles'), particle_sign, actions, (
        Wall(7, EAST, 1, -1, e_wall_used),
        Wall(7, SOUTH, 1, -7, n_wall_used),
        Wall(7, WEST, 7, -7, w_wall_used),
    ))
    room.function('signs_init', home=False).add(function('restworld:particles/signs'))

    room.function('ambient_entity_effect', home=False).add(
        main().run(particle(AMBIENT_ENTITY_EFFECT, r(0, 0, 0), 0.5, 5, 0.5, 1, 500)))
    room.function('ambient_entity_effect_init', home=False).add(function('restworld:particles/villager'))
    room.function('angry_villager', home=False).add(
        fast().run(particle(ANGRY_VILLAGER, r(0, 1, 0), 0.5, 0.5, 0.5, 0, 5)))
    room.function('angry_villager_init', home=False).add(function('restworld:particles/villager'))
    room.loop('animal', home=False).loop(lambda step: exemplar(step.elem, 0, {'NoAI': True}), (
        Block('cow'), Block('Pig'), Block('Horse'), Block('Llama'), Block('Sheep'), Block('Polar Bear'), Block('Goat')))
    room.function('ash_init', home=False).add(
        floor('soul_soil'),
        set_biome(SOUL_SAND_VALLEY))

    def block_marker_loop(step):
        yield particle(BLOCK_MARKER, step.elem, r(0, 2, 0))

    room.loop('block_marker_run').loop(block_marker_loop, ('barrier', 'light'))
    room.function('block_marker', home=False).add(
        slow().run(function('restworld:particles/block_marker_run')))
    room.function('bubble_init', home=False).add(
        fill(r(1, -1, 1), r(1, -1, -1), 'magma_block'),
        fill(r(-1, -1, 1), r(-1, -1, -1), 'soul_sand'),
        function('restworld:particles/ocean'))
    room.function('cloud', home=False).add(main().run(particle(CLOUD, r(0, 1, 0), 0.25, 0.25, 0.25, 0.05, 50)))
    room.function('composter', home=False).add(
        main().run(particle(COMPOSTER, r(0, 0.9, 0), 0.2, 0.1, 0.2, 1, 12)))
    room.function('composter_init', home=False).add(setblock(r(0, 0, 0), ('composter', {'level': 3})))
    room.function('crimson_spore_init', home=False).add(
        floor('crimson_nylium'),
        set_biome(CRIMSON_FOREST))
    room.function('crit', home=False).add(fast().run(particle(CRIT, r(0, 1.5, 0), 0.5, 0.5, 0.5, 0, 10)))
    room.function('crit_init', home=False).add(function('restworld:particles/animal'))
    room.function('damage_indicator', home=False).add(
        fast().run(particle(DAMAGE_INDICATOR, r(0, 1.5, 0), 0.5, 0.5, 0.5, 0, 5)))
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
                cherry.add(setblock(r(x, 0, z), ('pink_petals',
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
    room.function('dust_plume_init', home=False).add(
        exemplar(TextDisplay('Put Something in the Pot', {'line_width': 50, 'billboard': 'vertical'}).scale(0.5), 2),
        setblock(r(0, 0, 0), 'decorated_pot')
    )
    room.function('effect', home=False).add(fast().run(particle(EFFECT, r(0, 1, 0), 0.25, 0.5, 0.5, 0.2, 20)))
    room.function('effect_init', home=False).add(exemplar('evoker', 0, {'NoAI': True}))
    room.function('egg_crack_init', home=False).add(floor('moss_block'))
    room.function('egg_crack', home=False).add(main().run(
        setblock(r(0, 0, 0), 'air'),
        setblock(r(0, 0, 0), 'sniffer_egg')))
    room.function('electric_spark', home=False).add(main().run(summon('lightning_bolt', r(0, 1, 0))))
    room.function('electric_spark_init', home=False).add(setblock(r(0, 0, 0), 'lightning_rod'))
    room.function('enchant_init', home=False).add(
        fill(r(2, 0, 1), r(-2, 0, -2), 'bookshelf'),
        fill(r(2, 1, -1), r(-2, 1, -2), 'bookshelf'),
        fill(r(1, 0, 1), r(-1, 1, -1), 'air'),
        setblock(r(0, 0, 0), 'enchanting_table'),
    )
    room.function('enchanted_hit', home=False).add(
        fast().run(particle(ENCHANTED_HIT, r(0, 1, 0, 0.5), 0.5, 0.5, 0, 15)))
    room.function('enchanted_hit_init', home=False).add(function('restworld:particles/animal'))
    room.function('end_rod_init', home=False).add(
        fill(r(-1, 0, 0), r(1, 0, 0), 'end_rod'),
        fill(r(-1, 2, -2), r(1, 2, -2), ('end_rod', {'facing': SOUTH})))
    room.function('entity_effect', home=False).add(
        main().run(particle(ENTITY_EFFECT, r(0, 1, 0), 0.25, 0.5, 0.5, 0.2, 80)))
    room.function('entity_effect_init', home=False).add(function('restworld:particles/animal'))
    room.function('explosion', home=False).add(
        main().run(particle(EXPLOSION, r(0, 1, 0), 0.5, 0.5, 0.5, 2, 8)))
    room.function('explosion_emitter', home=False).add(
        main().run(particle(EXPLOSION_EMITTER, r(0, 1, 0), 0.5, 0.5, 0.5, 0.2, 1)))
    room.function('falling_dust', home=False).add(main().run(function('restworld:particles/falling_dust_change')))

    def falling_dust_loop(step):
        yield fill(r(-2, 5, -2), r(2, 5, 2), step.elem.id)
        yield particle(FALLING_DUST, step.elem.id, r(0, 4.9, 0), 1.5, 0, 1.5, 0, 50)

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
    room.function('fishing', home=False).add(fast().run(particle(FISHING, r(0, 1.5, 0), 0.2, 0, 0.2, 0, 6)))
    room.function('fishing_init', home=False).add(
        fill(r(-3, 0, 4), r(3, 0, 4), 'oak_wall_sign'),
        fill(r(3, 0, 3), r(-3, 0, -3), 'water'))
    room.function('flame_init', home=False).add(
        fill(r(-2, 0, -2), r(-2, 0, 2), 'torch'),
        fill(r(2, 0, -2), r(2, 0, 2), 'soul_torch'),
        setblock(r(0, 0, 0), Block('spawner', nbt={'SpawnData': {'entity': {'id': 'zombie'}}}))
    )
    room.function('gust_init', home=False).add(
        setblock(r(0, 2, -1), ('dispenser', {'facing': SOUTH})),
        fill(r(-1, 2, 4), r(1, 2, 4), 'glass'),
        setblock(r(0, 3, 4), 'glass'))
    room.function('gust', home=False).add(
        main().run(item().replace().block(r(0, 2, -1), 'container.0').with_('wind_charge', 1)),
        main().run(setblock(r(0, 3, -1), ('stone_button', {'powered': True, 'face': 'floor'}))),
        main().run(setblock(r(0, 3, -1), 'air')),
    )
    room.function('happy_villager', home=False).add(
        fast().run(particle(HAPPY_VILLAGER, r(0, 1, 0), 0.5, 0.5, 0.5, 0, 5)))
    room.function('happy_villager_init', home=False).add(function('restworld:particles/villager'))
    room.function('heart', home=False).add(fast().run(particle(HEART, r(0, 1.5, 0), 0.5, 0.2, 0.5, 0, 5)))
    room.function('heart_init', home=False).add(function('restworld:particles/small_animal'))
    room.function('instant_effect', home=False).add(
        fast().run(particle(INSTANT_EFFECT, r(0, 1.5, 0), 0.5, 1, 0.5, 0, 10)))
    room.function('instant_effect_init', home=False).add(function('restworld:particles/animal'))
    room.function('item_slime_init', home=False).add(
        fill(r(-2, 0, -2), r(2, 1, 2), 'barrier'),
        fill(r(-1, 0, -1), r(1, 1, 1), 'air'),
        exemplar('slime', 0, {'Size': 1}),
        tp(p().distance((None, 7)), r(0, 0, -3)).facing(r(0, 0, 5)))
    room.function('item_snowball', home=False).add(
        fast().run(item().replace().block(r(0, 2, -1), 'container.0').with_('snowball', 1)),
        # fast().run(setblock(r(0, 3, -1), ('stone_button', {'powered': True, 'face': 'floor'}))),
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
        set_biome(PLAINS),
        execute().in_(OVERWORLD).run(weather(CLEAR)))
    room.function('poof', home=False).add(main().run(particle(POOF, r(0, 1, 0), 0.25, 0.25, 0.25, 0, 30)))
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
        particle(SCULK_SOUL, r(0, 0.5, 2)),
        particle(SCULK_SOUL, r(-1.5, 0.5, 1)),
        particle(SCULK_SOUL, r(1, 0.5, -1)))
    sculk_pos = (r(-1, -1, -1), r(0, -1, -1), r(-1, -1, 1), r(0, 0, -1), r(0, 0, 1), r(1, 0, 0))
    spread = room.function('sculk_spread', home=False)
    pop = room.function('sculk_pop', home=False)
    for i, pos in enumerate(sculk_pos):
        block = 'sculk' if str(pos[1]) == '~-1' else ('sculk_vein', {'down': True})
        height = 1.3 if str(pos[1]) == '~-1' else 0.5
        spread.add(particle(SCULK_CHARGE, random.uniform(-math.pi / 6, +math.pi / 6),
                            (pos[0], pos[1] + height, pos[2])))
        pop.add(
            setblock(pos, block),
            particle(SCULK_CHARGE_POP, (pos[0], pos[1] + height, pos[2])))
    room.function('shriek', home=False).add(
        slow().run(function('restworld:particles/shriek_out')),
        slow(delay=7 * 8).run(setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True, 'shrieking': False}))))
    room.function('shriek_init', home=False).add(setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True})))
    room.function('shriek_out', home=False).add(
        setblock(r(0, 0, 0), ('sculk_shrieker', {'can_summon': True, 'shrieking': True})),
        function('restworld:particles/shriek_particles'))
    room.function('shriek_particles', home=False).add(
        (particle(SHRIEK, i * 7, r(0, 1, 0)) for i in range(0, 8)))
    room.loop('small_animal', home=False).loop(lambda step: exemplar(step.elem, 0, {'CatType': 1, 'NoAI': True}),
                                               ('ocelot', 'horse', 'llama'))
    room.function('smoke_init', home=False).add(
        setblock(r(-1, 0, 0), 'torch'),
        setblock(r(0, 0, 0), 'brewing_stand'),
        setblock(r(1, 0, 0), 'soul_torch'))
    room.function('sneeze', home=False).add(
        main().run(particle(SNEEZE, r(0, 0.25, 1.25), 0.05, 0.05, 0.5, 0.0, 2)),
        main().run(playsound('entity.panda.sneeze', 'neutral', a(), r(0, 0, 0))))
    room.function('sneeze_init', home=False).add(exemplar('panda', 0, {'NoAI': True, 'Age': -2147483648}))
    room.function('rain_init', home=False).add(weather(RAIN))
    room.function('rain_exit', home=False).add(weather(CLEAR))
    room.function('snowflake_init', home=False).add(set_biome(SNOWY_TAIGA), weather(RAIN))
    room.function('snowflake_exit', home=False).add(weather(CLEAR))
    room.function('sonic_boom_init', home=False).add(exemplar('warden', 0, {'NoAI': True}))
    room.function('sonic_boom', home=False).add(main().run(particle(SONIC_BOOM, r(0, 2, 0.5), 0, 0, 0, 1, 1)))
    room.function('soul', home=False).add(main().run(particle(SOUL, r(0, 0.75, 0), 0.05, 0, 0.05, 0.05, 4)))
    room.function('soul_init', home=False).add(floor('soul_soil'))
    room.function('spit', home=False).add(fast().run(summon('llama_spit', r(0, 1.6, 0.7),
                                                            {'Motion': [0.0, 0.0, 1.0], 'direction': [0.0, 0.0, 1.0],
                                                             'ExplosionPower': 1})))
    room.function('spit_init', home=False).add(exemplar('llama', 0, {'NoAI': True}))
    room.function('splash', home=False).add(fast().run(particle(SPLASH, r(0, 1, 0), 0.5, 0.1, 0.5, 1, 50)))
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
        main().run(particle(SWEEP_ATTACK, r(0, 1, 0), 0.3, 0.2, 0.3, 0, 3)))
    room.function('trial_spawner_detection_init', home=False).add(setblock(r(0, 0, 0), 'trial_spawner'))
    room.function('trial_spawner_detection', home=False).add(
        particle(TRIAL_SPAWNER_DETECTION, r(0, 0.5, 0), 0.25, 0.25, 0.25, 0, 1))
    room.function('totem_of_undying', home=False).add(
        main().run(particle(TOTEM_OF_UNDYING, r(0, 2, 0), 0.5, 1, 0.5, 0.5, 50)))
    room.function('underwater_init', home=False).add(function('restworld:particles/ocean'))
    room.function('vault_connection_init', home=False).add(setblock(r(0, 0, 0), 'vault'))
    room.loop('villager', home=False).loop(
        lambda step: exemplar('villager', 0, {'NoAI': True, 'VillagerData': step.elem}),
        villager_data)
    room.function('warped_spore_init', home=False).add(
        floor('warped_nylium'),
        set_biome(WARPED_FOREST))
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
            yield particle(WAX_ON, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)
        elif step.i == 2:
            yield particle(WAX_OFF, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)
        else:
            yield setblock(r(0, 0, 0), 'cut_copper')
            yield particle(SCRAPE, r(0, 0.5, 0), 0.5, 0.5, 0.5, 0, 10)

    room.loop('wax_on_run', home=False).loop(wax_on_run_loop, ('', 'Wax On', 'Wax Off', 'Scrape'))
    room.function('white_ash_init', home=False).add(
        floor('basalt'),
        set_biome(BASALT_DELTAS))
    room.function('witch', home=False).add(fast().run(particle(WITCH, r(0, 2.3, 0), 0.3, 0.3, 0.3, 0, 6)))
    room.function('witch_init', home=False).add(exemplar('witch', 0, {'NoAI': True}))

    # Keeping these in case of future need:
    # room.function('falling_nectar_init', home=False).add(exemplar('bee', 2, {'HasNectar': 1, 'NoAI': True}))


def check_for_unused():
    # Check for unexpectedly unhandled particles
    used = set()
    for p in actions:
        used.add(p.enum)
        for a in p.also:
            used.add(a)
    avail = set(x.enum for x in actions) - unused_particles
    unused = tuple(sorted((str(x) for x in (avail - used))))
    if unused:
        raise ValueError(f'Unused particles: {unused}')
