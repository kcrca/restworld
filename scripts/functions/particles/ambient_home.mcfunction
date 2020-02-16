execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=ambient_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[ambient_home,homer,particles_home],NoGravity:true,Small:True,PersistenceRequired:True}
