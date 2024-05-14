from __future__ import annotations

import math
import random

from pynecraft.base import EAST, NORTH, Nbt, OVERWORLD, SOUTH, WEST, as_facing, d, r, to_id
from pynecraft.commands import Block, CLEAR, Entity, INFINITE, JsonText, RAIN, REPLACE, a, data, e, effect, \
    execute, fill, fillbiome, function, item, kill, particle, playsound, schedule, setblock, summon, weather
from pynecraft.function import BLOCK, ITEM
from pynecraft.simpler import Book, PLAINS, TextDisplay, VILLAGER_BIOMES, VILLAGER_PROFESSIONS, WallSign
from pynecraft.values import ABSORPTION, AMBIENT_ENTITY_EFFECT, ANGRY_VILLAGER, ASH, BASALT_DELTAS, BLINDNESS, \
    BLOCK_MARKER, BUBBLE, BUBBLE_COLUMN_UP, BUBBLE_POP, CAMPFIRE_COSY_SMOKE, CAMPFIRE_SIGNAL_SMOKE, \
    CHERRY_LEAVES, \
    CLOUD, COMPOSTER, CRIMSON_FOREST, CRIMSON_SPORE, CRIT, CURRENT_DOWN, DAMAGE_INDICATOR, DOLPHIN, DRAGON_BREATH, \
    DRIPPING_DRIPSTONE_LAVA, DRIPPING_DRIPSTONE_WATER, DRIPPING_HONEY, DRIPPING_LAVA, DRIPPING_OBSIDIAN_TEAR, \
    DRIPPING_WATER, DUST, DUST_COLOR_TRANSITION, DUST_PILLAR, DUST_PLUME, EFFECT, EGG_CRACK, ELDER_GUARDIAN, \
    ELECTRIC_SPARK, ENCHANT, \
    ENCHANTED_HIT, END_ROD, ENTITY_EFFECT, EXPLOSION, EXPLOSION_EMITTER, FALLING_DRIPSTONE_LAVA, \
    FALLING_DRIPSTONE_WATER, FALLING_DUST, FALLING_HONEY, FALLING_LAVA, FALLING_NECTAR, FALLING_OBSIDIAN_TEAR, \
    FALLING_SPORE_BLOSSOM, FALLING_WATER, FIREWORK, FISHING, FLAME, FLASH, GLOW, GLOW_SQUID_INK, GUST, GUST_DUST, \
    GUST_EMITTER, HAPPY_VILLAGER, HEART, INFESTED, INSTANT_EFFECT, ITEM_COBWEB, ITEM_SLIME, ITEM_SNOWBALL, \
    LANDING_HONEY, LANDING_LAVA, LANDING_OBSIDIAN_TEAR, LARGE_SMOKE, LAVA, MYCELIUM, NAUTILUS, NOTE, OMINOUS_SPAWNING, \
    PARTICLE_GROUP, POOF, PORTAL, RAID_OMEN, RESISTANCE, REVERSE_PORTAL, SCRAPE, SCULK_CHARGE, SCULK_CHARGE_POP, \
    SCULK_SOUL, SHRIEK, SMALL_FLAME, SMALL_GUST, SMOKE, SNEEZE, SNOWFLAKE, SNOWY_TAIGA, SONIC_BOOM, SOUL, \
    SOUL_FIRE_FLAME, SOUL_SAND_VALLEY, SPEED, SPIT, SPLASH, SPORE_BLOSSOM_AIR, SQUID_INK, STRENGTH, SWEEP_ATTACK, \
    TOTEM_OF_UNDYING, TRIAL_OMEN, TRIAL_SPAWNER_DETECTION, TRIAL_SPAWNER_DETECTION_OMINOUS, UNDERWATER, \
    VAULT_CONNECTION, VIBRATION, WARPED_FOREST, WARPED_SPORE, WAX_OFF, WAX_ON, WHITE_ASH, WHITE_SMOKE, WITCH, \
    as_particle
from restworld.rooms import ActionDesc, SignedRoom, Wall, ensure, span
from restworld.world import fast_clock, kill_em, main_clock, restworld, slow_clock


def action(which: str, name=None, note=None, also=()):
    return ActionDesc(as_particle(which), name, note, tuple(as_particle(x) for x in also))


# adding action: small_gust (apply wind_charging to mob or villager), item_cobweb (weaving effect), infested (infested),
#       raid_omen, trial_omen
#     oozing effect gives off item_slime particles, use it instead of referring to arena?
# adding to book:
# ignoring:

actions = [
    action(ANGRY_VILLAGER),
    action(ASH),
    action(BLOCK_MARKER),
    action(BUBBLE, 'Bubbles|Currents|Whirlpools', also=(BUBBLE_POP, BUBBLE_COLUMN_UP, CURRENT_DOWN)),
    action(CLOUD, note='Evaporation'),
    action(COMPOSTER),  # Could be in blocks if we added particle
    action(CRIMSON_SPORE),
    action(CRIT),
    action(DAMAGE_INDICATOR),
    action(DOLPHIN),
    action(DRAGON_BREATH),  # Could be in end if we added particle, but it's so _large_
    action(DRIPPING_HONEY, note='Falling, Landing', also=(FALLING_HONEY, LANDING_HONEY)),
    action(DUST_PLUME),
    action(DUST_PILLAR),
    action(EFFECT, 'Effect|(and Entity|Effect)', also=(ENTITY_EFFECT,)),
    action(ELECTRIC_SPARK),  # Could be in redstone if we added particle
    action(ENCHANTED_HIT),
    action(EXPLOSION, also=(EXPLOSION_EMITTER,)),
    action(FALLING_DUST),
    action(FIREWORK, note='and Flash', also=(FLASH,)),
    action(FISHING),
    action(GUST, 'Gust|Gust Emitter|Gust Dust', also=(GUST_DUST, GUST_EMITTER)),
    action(HAPPY_VILLAGER),
    action(HEART),
    action(INFESTED),
    action(INSTANT_EFFECT),
    action(ITEM_COBWEB, note='Weaving Effect'),
    action(ITEM_SNOWBALL),
    action(MYCELIUM),
    action(NAUTILUS, note='with Conduit'),
    action(POOF, note='Small Explosion'),
    action(RAID_OMEN),
    action(RAIN),
    action(SCULK_SOUL, also=(SCULK_CHARGE, SCULK_CHARGE_POP)),
    action(SMALL_GUST, note='Weaving Effect'),
    action(SNEEZE),
    action(SNOWFLAKE, 'Snow'),
    action(SONIC_BOOM),  # Could be in mobs if we added particle
    action(SOUL),
    action(SPLASH),
    action(SQUID_INK, note='and Glow Squid', also=(GLOW, GLOW_SQUID_INK)),
    action(SWEEP_ATTACK),
    action(TOTEM_OF_UNDYING),
    action(TRIAL_OMEN),
    # Removable: Happens in blocks:
    action(TRIAL_SPAWNER_DETECTION, 'Trial Spawner|Detection|(and Ominous)', also=(TRIAL_SPAWNER_DETECTION_OMINOUS,)),
    action(VAULT_CONNECTION, 'Vault Connection|(and Ominous)'),  # Removable: Happens in blocks
    action(WARPED_SPORE),
    action(WAX_ON, 'Wax On / Off', also=(WAX_OFF, SCRAPE)),
    action(WHITE_ASH),
    action(WITCH),
]
actions.sort(key=lambda x: x.sort_key())

# We could put witch squid ink, sonic boom (warden) in mobs...
elsewhere = {
    'Blocks': (END_ROD, CAMPFIRE_COSY_SMOKE, CAMPFIRE_SIGNAL_SMOKE, REVERSE_PORTAL, SHRIEK, DRIPPING_OBSIDIAN_TEAR,
               FALLING_OBSIDIAN_TEAR, LANDING_OBSIDIAN_TEAR, FLAME, SMALL_FLAME, SOUL_FIRE_FLAME, SMOKE, LARGE_SMOKE),
    'Redstone': (DUST, NOTE, VIBRATION),
    'Materials': (
        LAVA, PORTAL, DRIPPING_WATER, FALLING_WATER, DRIPPING_DRIPSTONE_WATER, FALLING_DRIPSTONE_WATER, DRIPPING_LAVA,
        FALLING_LAVA, LANDING_LAVA, DRIPPING_DRIPSTONE_LAVA, FALLING_DRIPSTONE_LAVA),
    'Plants': (SPORE_BLOSSOM_AIR, FALLING_SPORE_BLOSSOM, CHERRY_LEAVES, UNDERWATER),
    'Mobs': (FALLING_NECTAR, EGG_CRACK),
    'Arena': (ITEM_SLIME,),
    'GUI': (ENCHANT,),
}

hover = {
    CAMPFIRE_SIGNAL_SMOKE: 'Same as regular smoke, it just goes higher',
    REVERSE_PORTAL: 'Above respawn anchor',
    SHRIEK: 'Sculk shrieker',
    FLAME: 'Fire',
    LARGE_SMOKE: 'Fire',
    SMALL_FLAME: 'Torches',
    NOTE: 'Power the note block',
    VIBRATION: 'Push buttons near sculk sensor',
    UNDERWATER: 'Go inside the water',
    EGG_CRACK: 'Turtle eggs',
    FALLING_NECTAR: 'Bees',
    ITEM_SLIME: 'Slime battle, under the bouncing slimes',
    ENCHANT: 'Enchanting table',
}

unused_particles = {
    AMBIENT_ENTITY_EFFECT,  # Being removed at 1.21 I think
    BLOCK,  # This just happens in the game, plus I can't see how to generate it.
    DUST_COLOR_TRANSITION,  # Can the player control its look? AFAICT, it's just when the power level changes?
    ELDER_GUARDIAN,  # Just the elder guardian face in your face, and makes it hard to turn off.
    ITEM,  # Same as BLOCK
    OMINOUS_SPAWNING,  # Appeared in 24w13a, but no obvious use
    SPIT,  # Broke at 1.19, can't get the summoned spit to move.
    WHITE_SMOKE,  # Appeared in 24w13a, but no obvious use
}
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
        action_desc.which = as_particle(action_desc.which)
        run_at = execute().at(e().tag('particles_action_home')).positioned(r(0, 2, 0))
        return WallSign(action_desc.sign_text(), (
            run_at.run(setblock(r(0, -4, 0), 'redstone_block')),
            run_at.run(data().merge(r(0, -4, -2), {
                'Command': f'{str(run_at.run(""))} function restworld:particles/{action_desc.func()}_init'})),
            run_at.run(data().merge(r(-1, -2, 0), {
                'Command': f'{str(run_at.run(""))} function restworld:particles/{action_desc.func()}'})),
            setblock(d(-dx, 0, -dz), 'emerald_block')
        ))

    n_wall_used = {4: span(1, 5), 3: span(1, 5), 2: (1, 2, 4, 5)}
    e_wall_used = {5: span(2, 4), 4: span(1, 5), 3: span(1, 5), 2: span(1, 5)}
    w_wall_used = {5: span(2, 4), 4: span(1, 5), 3: span(1, 5), 2: span(1, 5)}
    room = SignedRoom('particles', restworld, SOUTH, (None, 'Particles'), particle_sign, actions, (
        Wall(7, EAST, 1, -1, e_wall_used),
        Wall(7, SOUTH, 1, -7, n_wall_used),
        Wall(7, WEST, 7, -7, w_wall_used),
    ))
    room.function('signs_init', home=False).add(function('restworld:particles/signs'))
    particler = e().tag('particler')

    animal = room.loop('animal', home=False).loop(lambda step: exemplar(step.elem, 0, {'NoAI': True}), (
        Entity('Cow'), Entity('Pig'), Entity('Horse', {'Variant': 257}), Entity('Llama', {'Variant': 2}),
        Entity('Sheep', {'Color': 9}), Entity('Polar Bear'), Entity('Goat')))
    villager = room.loop('villager', home=False).loop(
        lambda step: exemplar('villager', 0, {'NoAI': True, 'VillagerData': step.elem}),
        villager_data)
    ocean = room.function('ocean', home=False).add(
        fill(r(-3, 0, 4), r(3, 0, 4), 'structure_void'),
        fill(r(3, 6, 3), r(-3, 6, -3), 'structure_void'),
        fill(r(2, 6, 2), r(-2, 6, -2), 'water'),
        fill(r(2, 0, 2), r(-2, 6, -2), 'water'),
    )
    small_animal = room.loop('small_animal', home=False).loop(
        lambda step: exemplar(step.elem, 0, {'CatType': 1, 'NoAI': True}),
        ('ocelot', 'horse', 'llama'))

    def show_effect(particle_name, effect_name):
        room.function(f'{particle_name}_init', home=False).add(
            exemplar('rabbit', 1, {'NoAI': True}),
            effect().give(particler, effect_name, INFINITE))

    show_effect(as_particle(INFESTED), 'infested')
    show_effect(as_particle(RAID_OMEN), 'raid_omen')
    show_effect(as_particle(TRIAL_OMEN), 'trial_omen')
    show_effect(as_particle(SMALL_GUST), 'wind_charged')
    show_effect(as_particle(ITEM_COBWEB), 'weaving')

    room.function('angry_villager', home=False).add(
        fast().run(particle(ANGRY_VILLAGER, r(0, 1, 0), (0.5, 0.5, 0.5), 0, 5)))
    room.function('angry_villager_init', home=False).add(function(villager))
    room.function('ash_init', home=False).add(
        floor('soul_soil'),
        set_biome(SOUL_SAND_VALLEY))

    def block_marker_loop(step):
        yield particle(Entity(BLOCK_MARKER, {'block_state': step.elem}), r(0, 2, 0))

    block_marker_run = room.loop('block_marker_run', home=False).loop(block_marker_loop, ('barrier', 'light'))
    room.function('block_marker', home=False).add(
        slow().run(function(block_marker_run)))
    room.function('bubble_init', home=False).add(
        fill(r(1, -1, 1), r(1, -1, -1), 'magma_block'),
        fill(r(-1, -1, 1), r(-1, -1, -1), 'soul_sand'),
        function(ocean))
    room.function('cloud', home=False).add(main().run(particle(CLOUD, r(0, 1, 0), (0.25, 0.25, 0.25), 0.05, 10)))
    room.function('composter', home=False).add(
        main().run(particle(COMPOSTER, r(0, 0.9, 0), (0.2, 0.1, 0.2), 1, 12)))
    room.function('composter_init', home=False).add(setblock(r(0, 0, 0), ('composter', {'level': 3})))
    room.function('crimson_spore_init', home=False).add(
        floor('crimson_nylium'),
        set_biome(CRIMSON_FOREST))
    room.function('crit', home=False).add(fast().run(particle(CRIT, r(0, 1.5, 0), (0.5, 0.5, 0.5), 0, 10)))
    room.function('crit_init', home=False).add(function(animal))
    room.function('damage_indicator', home=False).add(
        fast().run(particle(DAMAGE_INDICATOR, r(0, 1.5, 0), (0.5, 0.5, 0.5), 0, 5)))
    room.function('damage_indicator_init', home=False).add(function(animal))
    room.function('dolphin_init', home=False).add(
        fill(r(-3, 0, 5), r(3, 6, 5), 'barrier').replace('air'),
        fill(r(0, 0, 5), r(0, 1, 5), 'air'),
        fill(r(4, 5, 4), r(-4, 5, -4), 'barrier'),
        fill(r(3, 5, 3), r(-3, 5, -3), 'air'),
        fill(r(3, 7, 3), r(-3, 7, -3), 'barrier'),
        function(ocean),
        exemplar('dolphin', 1.5),
    )
    room.function('dragon_breath_init', home=False).add(floor('end_stone'))
    dragon_breath_finish = room.function('dragon_breath_finish', home=False).add(
        data().merge(e().tag('particle_dragonball').limit(1), {'Motion': [0, -0.5, -0.5]}))
    dragon_breath_run = room.function('dragon_breath_run', home=False).add(
        kill(e().tag('particle_dragonball')),
        summon('dragon_fireball', r(0, 4, 4),
               {'power': {0.0, -0.05, -0.05}, 'ExplosionPower': 0, 'Tags': ['particle_dragonball', 'particler']}),
        schedule().function(dragon_breath_finish, 1, REPLACE),
    )
    room.function('dragon_breath', home=False).add(slow().run(function(dragon_breath_run)))
    room.function('dripping_honey_init', home=False).add(
        fill(r(2, 4, 2), r(-2, 4, -2), ('beehive', {'honey_level': 5, 'facing': SOUTH})),
        fill(r(2, 4, -2), r(-2, 4, -2), ('beehive', {'honey_level': 5, 'facing': NORTH})),
        fill(r(2, 4, -1), r(2, 4, 1), ('beehive', {'honey_level': 5, 'facing': EAST})),
        fill(r(-2, 4, -1), r(-2, 4, 1), ('beehive', {'honey_level': 5, 'facing': WEST})),
    )
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
    dust_pillar_change = room.loop('dust_pillar_change', home=False).loop(
        lambda step:  (
            floor(step.elem),
            particle(Entity(DUST_PILLAR, {'block_state': step.elem}), r(0, 0, 0), (0.5, 0, 0.5), 0, 50)),
        ('stone', 'grass_block', 'sandstone'))
    room.function('dust_pillar', home=False).add(main().run(function(dust_pillar_change)))
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
        fast().run(particle(ENCHANTED_HIT, r(0, 1, 0, 0.5), (0.5, 0.5, 0), 15)))
    room.function('enchanted_hit_init', home=False).add(function(animal))

    def effect_loop(step):
        yield effect().clear(particler.limit(1))
        yield effect().give(particler.limit(1), step.elem, INFINITE)

    effect_change = room.loop('effect_change', home=False).loop(
        effect_loop, (SPEED, STRENGTH, ABSORPTION, RESISTANCE, BLINDNESS))
    room.function('effect', home=False).add(main().run(function(effect_change)))
    room.function('effect_init', home=False).add(function(animal))
    room.function('explosion', home=False).add(
        main().run(particle(EXPLOSION, r(0, 1, 0), (0.5, 0.5, 0.5), 2, 8)))
    room.function('explosion_emitter', home=False).add(
        main().run(particle(EXPLOSION_EMITTER, r(0, 1, 0), (0.5, 0.5, 0.5), 0.2, 1)))

    def falling_dust_loop(step):
        id = to_id(step.elem)
        yield fill(r(-2, 5, -2), r(2, 5, 2), id)
        yield particle(Entity(FALLING_DUST, {'block_state': id}), r(0, 4.9, 0), (1.5, 0, 1.5), 0, 50)

    falling_dust_change = room.loop('falling_dust_change', home=False).loop(falling_dust_loop, (
        'Dragon Egg', 'Sand', 'Red Sand', 'Gravel', 'Green Concrete Powder'))
    room.function('falling_dust_init', home=False).add(
        fill(r(-2, 4, -2), r(2, 4, 2), 'barrier'),
        function(falling_dust_change))
    room.function('falling_dust', home=False).add(main().run(function(falling_dust_change)))

    def fireworks_loop(step):
        color, shape = step.elem
        ent = Entity('firework_rocket', components={"minecraft:fireworks": {
            'explosions': [{'colors': Nbt.TypedArray('I', (color,)), 'has_trail': True, 'shape': shape}],
            'flight_duration': 0}})
        yield item().replace().block(r(0, 1, 0), 'container.0').with_(ent)

    firework_change = room.loop('firework_change', home=False).loop(
        fireworks_loop, ((11743532, 'large_ball'), (6719955, 'star'), (14602026, 'creeper'), (3887386, 'burst'),
                         (15790320, 'small_ball'))).add(
        setblock(r(0, 0, 0), 'redstone_torch'),
        setblock(r(0, 0, 0), 'air'))
    room.function('firework', home=False).add(main().run(function(firework_change)))
    room.function('firework_init', home=False).add(setblock(r(0, 1, 0), ('dispenser', {'facing': 'up'})))
    room.function('fishing', home=False).add(fast().run(particle(FISHING, r(0, 1.5, 0), (0.2, 0, 0.2), 0, 6)))
    room.function('fishing_init', home=False).add(
        fill(r(-3, 0, 4), r(3, 0, 4), 'oak_wall_sign'),
        fill(r(3, 0, 3), r(-3, 0, -3), 'water'))
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
        fast().run(particle(HAPPY_VILLAGER, r(0, 1, 0), (0.5, 0.5, 0.5), 0, 5)))
    room.function('happy_villager_init', home=False).add(function(villager))
    room.function('heart', home=False).add(fast().run(particle(HEART, r(0, 1.5, 0), (0.5, 0.2, 0.5), 0, 5)))
    room.function('heart_init', home=False).add(function(small_animal))
    room.function('instant_effect', home=False).add(
        fast().run(particle(INSTANT_EFFECT, r(0, 1.5, 0), (0.5, 1, 0.5), 0, 10)))
    room.function('instant_effect_init', home=False).add(function(animal))
    room.function('item_snowball', home=False).add(
        fast().run(item().replace().block(r(0, 2, -1), 'container.0').with_('snowball', 1)),
        fast().run(setblock(r(0, 3, -1), ('stone_button', {'powered': True, 'face': 'floor'}))),
        fast().run(setblock(r(0, 3, -1), 'air')),
    )
    room.function('item_snowball_init', home=False).add(
        setblock(r(0, 2, -1), ('dispenser', {'facing': SOUTH})),
        fill(r(-1, 2, 4), r(1, 2, 4), 'glass'),
        setblock(r(0, 3, 4), 'glass'))
    room.function('mycelium_init', home=False).add(floor('mycelium'))
    nautilus_change = room.loop('nautilus_change', home=False).loop(
        lambda step: fill(r(-2, 0, -2), r(2, 2, 0), 'prismarine' if step.i == 0 else 'sand'), range(0, 2)).add(
        fill(r(-1, 1, -1), r(1, 2, 0), 'water'),
        setblock(r(0, 2, 0), 'conduit'))
    room.function('nautilus', home=False).add(slow().run(function(nautilus_change)))
    room.function('nautilus_init', home=False).add(
        function(ocean),
        fill(r(-2, 0, -2), r(2, 2, 0), 'prismarine'),
        fill(r(-1, 1, -1), r(1, 2, 0), 'air'),
        setblock(r(0, 2, 0), 'conduit'))
    room.function('particles_clear', home=False).add(
        kill_em(particler),
        kill(e().type('area_effect_cloud').distance((None, 10))),
        fill(r(20, 0, 20), r(-20, 10, -20), 'air').replace('snow'),
        set_biome(PLAINS),
        execute().in_(OVERWORLD).run(weather(CLEAR)))
    room.function('poof', home=False).add(main().run(particle(POOF, r(0, 1, 0), (0.25, 0.25, 0.25), 0, 15)))
    room.function('portal_init', home=False).add(
        fill(r(-2, 0, -1), r(2, 4, -1), 'obsidian'),
        fill(r(-1, 1, -1), r(1, 3, -1), 'nether_portal'))
    room.function('sculk_soul_init', home=False).add(
        setblock(r(0, 0, 0), 'sculk_catalyst'),
    )
    sculk_soul_show = room.function('sculk_soul_show', home=False).add(
        particle(SCULK_SOUL, r(0, 0.5, 2)),
        particle(SCULK_SOUL, r(-1.5, 0.5, 1)),
        particle(SCULK_SOUL, r(1, 0.5, -1)))
    skulk_spread = room.function('sculk_spread', home=False)
    sculk_pos = (r(-1, -1, -1), r(0, -1, -1), r(-1, -1, 1), r(0, 0, -1), r(0, 0, 1), r(1, 0, 0))
    sculk_pop = room.function('sculk_pop', home=False)
    for i, pos in enumerate(sculk_pos):
        block = 'sculk' if str(pos[1]) == '~-1' else ('sculk_vein', {'down': True})
        height = 1.3 if str(pos[1]) == '~-1' else 0.5
        skulk_spread.add(particle(Entity(SCULK_CHARGE, {'roll': random.uniform(-math.pi / 6, +math.pi / 6)}),
                                  (pos[0], pos[1] + height, pos[2])))
        sculk_pop.add(
            setblock(pos, block),
            particle(SCULK_CHARGE_POP, (pos[0], pos[1] + height, pos[2])))
    room.function('sculk_soul', home=False).add(
        main().run(fill(r(-1, -1, -1), r(1, -1, 1), 'stone_bricks').replace('sculk')),
        main().run(fill(r(-1, 0, -1), r(1, 0, 1), 'air').replace('sculk_vein')),
        main().run(function(sculk_soul_show)),
        main(delay=1).run(setblock(r(0, 0, 0), ('sculk_catalyst', {'bloom': True}))),
        main(delay=5).run(function(skulk_spread)),
        main(delay=9).run(setblock(r(0, 0, 0), ('sculk_catalyst', {'bloom': False}))),
        main(delay=16).run(function(sculk_pop)),
    )
    room.function('sneeze', home=False).add(
        main().run(particle(SNEEZE, r(0, 0.25, 1.25), (0.05, 0.05, 0.5), 0.0, 2)),
        main().run(playsound('entity.panda.sneeze', 'neutral', a(), r(0, 0, 0))))
    room.function('sneeze_init', home=False).add(exemplar('panda', 0, {'NoAI': True, 'Age': -2147483648}))
    room.function('rain_init', home=False).add(weather(RAIN))
    room.function('rain_exit', home=False).add(weather(CLEAR))
    room.function('snowflake_init', home=False).add(set_biome(SNOWY_TAIGA), weather(RAIN))
    room.function('snowflake_exit', home=False).add(weather(CLEAR))
    room.function('sonic_boom_init', home=False).add(exemplar('warden', 0, {'NoAI': True}))
    room.function('sonic_boom', home=False).add(main().run(particle(SONIC_BOOM, r(0, 2, 0.5), (0, 0, 0), 1, 1)))
    room.function('soul', home=False).add(fast().run(particle(SOUL, r(0, 0.75, 0), (0.05, 0, 0.05), 0.0, 4)))
    room.function('soul_init', home=False).add(floor('soul_soil'))
    room.function('spit', home=False).add(fast().run(summon('llama_spit', r(0, 1.6, 0.7),
                                                            {'Motion': [0.0, 0.0, 1.0], 'direction': [0.0, 0.0, 1.0],
                                                             'ExplosionPower': 1})))
    room.function('spit_init', home=False).add(exemplar('llama', 0, {'NoAI': True}))
    room.function('splash', home=False).add(fast().run(particle(SPLASH, r(0, 1, 0), (0.5, 0.1, 0.5), 1, 50)))
    room.function('splash_init', home=False).add(
        fill(r(-2, 0, -2), r(2, 0, 2), 'stone'),
        fill(r(-1, 0, -1), r(1, 0, 1), 'water'))
    room.function('squid_ink_init', home=False).add(function(ocean))

    def squid_ink_loop(step):
        yield exemplar(step.elem, 4, {'NoAI': True})
        yield particle(step.elem + '_ink', r(0, 2.8, -0), (0.15, 0.3, 0.15), 0.01, 30)

    squid_ink_run = room.loop('squid_ink_run', home=False).add(
        kill_em(particler)).loop(
        squid_ink_loop, ('squid', 'glow_squid'))
    room.function('squid_ink', home=False).add(main().run(function(squid_ink_run)))
    room.function('sweep_attack', home=False).add(
        main().run(particle(SWEEP_ATTACK, r(0, 1, 0), (0.3, 0.2, 0.3), 0, 3)))
    room.function('trial_spawner_detection_init', home=False).add(
        setblock(r(-1, 0, 0), 'trial_spawner'),
        setblock(r(1, 0, 0), ('trial_spawner', {'ominous': True})))
    room.function('trial_spawner_detection', home=False).add(
        main().run(
            particle(TRIAL_SPAWNER_DETECTION, r(-1, 0.75, 0), (0.25, 0.0, 0.25), 0, 25),
            particle(TRIAL_SPAWNER_DETECTION_OMINOUS, r(1, 0.75, 0), (0.25, 0.0, 0.25), 0, 25)))
    room.function('totem_of_undying', home=False).add(
        main().run(particle(TOTEM_OF_UNDYING, r(0, 2, 0), (0.5, 1, 0.5), 0.5, 50)))
    room.function('vault_connection_init', home=False).add(
        setblock(r(-1, 0, 0), 'vault'),
        setblock(r(1, 0, 0), ('vault', {'ominous': True})))
    room.function('warped_spore_init', home=False).add(
        floor('warped_nylium'),
        set_biome(WARPED_FOREST))
    room.function('wax_on_init', home=False).add(
        setblock(r(0, 0, 0), 'cut_copper'),
        exemplar('text_display', 1.5),
    )

    def wax_on_run_loop(step):
        yield data().modify(particler.limit(1), 'text').set().value(JsonText.text(step.elem))
        if step.i == 0:
            yield setblock(r(0, 0, 0), 'exposed_cut_copper')
        elif step.i == 1:
            yield setblock(r(0, 0, 0), 'waxed_exposed_cut_copper')
            yield particle(WAX_ON, r(0, 0.5, 0), (0.5, 0.5, 0.5), 0, 10)
        elif step.i == 2:
            yield setblock(r(0, 0, 0), 'exposed_cut_copper')
            yield particle(WAX_OFF, r(0, 0.5, 0), (0.5, 0.5, 0.5), 0, 10)
        else:
            yield setblock(r(0, 0, 0), 'cut_copper')
            yield particle(SCRAPE, r(0, 0.5, 0), (0.5, 0.5, 0.5), 0, 10)

    wax_on_run = room.loop('wax_on_run', home=False).loop(wax_on_run_loop, ('', 'Wax On', 'Wax Off', 'Scrape'))
    room.function('wax_on', home=False).add(main().run(function(wax_on_run)))
    room.function('white_ash_init', home=False).add(
        floor('basalt'),
        set_biome(BASALT_DELTAS))
    room.function('witch', home=False).add(fast().run(particle(WITCH, r(0, 2.3, 0), (0.3, 0.3, 0.3), 0, 6)))
    room.function('witch_init', home=False).add(exemplar('witch', 0, {'NoAI': True}))

    book = Book()
    book.sign_book('Particle Book', 'RestWorld', 'Particles in the world')
    book.add(JsonText.text('\\n\\nParticles in the World\\n\\n').italic())
    book.add(JsonText.text('Many particles are shown in the rest of this world. '
                           'This room is focused on those that aren\'t. '
                           'This book lists where those other particles are by room.').plain())
    page_break = ('Materials', 'Blocks', 'Plants', 'Arena')
    for k, v in elsewhere.items():
        if k in page_break:
            book.next_page()
        else:
            book.add(r'\n\n')
        book.add(JsonText.text(f'{k} Room:\\n').plain().bold())
        first = True
        for p in sorted(v):
            if not first:
                book.add(JsonText(', ').bold(False))
            else:
                first = False
            text = JsonText(as_particle(p).capitalize().replace('_', ' ')).bold(False)
            if p in hover:
                text = text.hover_event().show_text(hover[p])
            book.add(text)
        book.add(JsonText('.').bold(False))
    room.function('particle_book', home=False).add(
        ensure(r(1, 2, -4), Block('lectern', {'facing': SOUTH, 'has_book': True}),
               nbt=book.as_item())
    )


def check_for_unused():
    # Check for unexpectedly unhandled particles
    used = set()
    for p in actions:
        used.add(p.which)
        used.update(set(p.also))
        continue
    for v in elsewhere.values():
        values = set(as_particle(x) for x in v)
        both = values.intersection(used)
        if both:
            raise ValueError(f'{both} in both elsewhere and actions')
        used.update(values)
        continue
    both = used.intersection(unused_particles)
    if both:
        raise ValueError(f'{both} in both unused and actions+elsewhere')
    given = used.union(unused_particles)
    all_particles = set(as_particle(x) for x in PARTICLE_GROUP)
    not_given = all_particles - given
    if not_given:
        raise ValueError(f'Unused particles: {not_given}')
