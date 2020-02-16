execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=pressure_plate_add_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[pressure_plate_add_home,homer,redstone_home],NoGravity:true,Small:True,PersistenceRequired:True}
