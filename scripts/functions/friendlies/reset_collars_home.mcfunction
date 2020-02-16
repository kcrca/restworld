execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=reset_collars_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[reset_collars_home,homer,friendlies_home],NoGravity:true,Small:True,PersistenceRequired:True}
