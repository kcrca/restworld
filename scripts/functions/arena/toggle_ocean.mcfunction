scoreboard players set arena_is_ocean funcs 0
execute if block ~20 ~16 ~20 minecraft:water run scoreboard players set arena_is_ocean funcs 1

execute if score arena_is_ocean funcs matches 0 run fill ~-20 ~0 ~-20 ~20 ~16 ~20 water replace air
execute if score arena_is_ocean funcs matches 0 at @e[tag=controls_home] run fill ~-3 ~-2 ~-2 ~-3 ~2 ~2 air replace water
execute if score arena_is_ocean funcs matches 0 at @e[tag=controls_home] run data merge block ~-2 ~1 ~-1 {Text3:"\"Off\""}
execute if score arena_is_ocean funcs matches 1 run fill ~-20 ~0 ~-20 ~20 ~16 ~20 air replace water
execute if score arena_is_ocean funcs matches 1 at @e[tag=controls_home] run data merge block ~-2 ~1 ~-1 {Text3:"\"On\""}
execute if score arena_is_ocean funcs matches 0 at @e[tag=controls_home] run fill ~-3 ~-2 ~-2 ~-3 ~2 ~2 water replace air
