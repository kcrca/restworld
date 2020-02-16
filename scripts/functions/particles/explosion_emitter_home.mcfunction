execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=explosion_emitter_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[explosion_emitter_home,homer,particles_home],NoGravity:true,Small:True,PersistenceRequired:True}
