time set noon
execute at @e[tag=daylight_detector_home] run fill ~3 ~8 ~3 ~-3 ~8 ~-3 minecraft:air
scoreboard players set daylight_detector funcs 0
kill @e[tag=daylight_detector_home]
