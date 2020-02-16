execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=damage_indicator_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[damage_indicator_home,homer,particles_home],NoGravity:true,Small:True,PersistenceRequired:True}
