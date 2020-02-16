execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=min_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[min_home,homer,global_home],NoGravity:true,Small:True,PersistenceRequired:True}
