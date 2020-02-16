execute positioned ~ ~1 ~ run kill @e[distance=..0.5]
kill @e[tag=daylight_detector_setup_home]
summon minecraft:armor_stand ~ ~0.5 ~ {Tags:[daylight_detector_setup_home,homer,redstone_home],NoGravity:true,Small:True,PersistenceRequired:True}
