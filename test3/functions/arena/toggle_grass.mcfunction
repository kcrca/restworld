scoreboard players set arena_is_grass funcs 0
execute if block ~20 ~-1 ~20 minecraft:grass_block run scoreboard players set arena_is_grass funcs 1

execute if score arena_is_grass funcs matches 0 run fill ~20 ~-1 ~20 ~-20 ~-1 ~-20 grass_block
execute if score arena_is_grass funcs matches 0 at @e[tag=controls_home] run data merge block ~-2 ~1 ~0 {Text3:"\"Off\""}
execute if score arena_is_grass funcs matches 1 run clone ~20 ~-11 ~20 ~-20 ~-11 ~-20 ~-20 ~-1 ~-20
execute if score arena_is_grass funcs matches 1 at @e[tag=controls_home] run data merge block ~-2 ~1 ~0 {Text3:"\"On\""}
