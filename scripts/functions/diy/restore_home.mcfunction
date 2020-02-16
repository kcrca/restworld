execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=restore_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[restore_home,homer,diy_home],NoGravity:true,Small:True,PersistenceRequired:True}
