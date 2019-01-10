scoreboard players set arena_is_night funcs 0
execute at @e[tag=controls_home] unless block ~ ~3 ~ daylight_detector[power=15] run scoreboard players set arena_is_night funcs 1

execute if score arena_is_night funcs matches 0 run time set midnight
execute if score arena_is_night funcs matches 0 at @e[tag=controls_home] run data merge block ~-2 ~1 ~1 {Text3:"\"Off\""}
execute if score arena_is_night funcs matches 1 run time set noon
execute if score arena_is_night funcs matches 1 at @e[tag=controls_home] run data merge block ~-2 ~1 ~1 {Text3:"\"On\""}
