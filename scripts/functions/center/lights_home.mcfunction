execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=lights_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[lights_home,homer,center_home],NoGravity:true,Small:True,PersistenceRequired:True}
