execute unless score holders funcs matches 0.. run function holders_init
scoreboard players add holders funcs 1
scoreboard players set holders max 8
execute unless score holders funcs matches 0..7 run scoreboard players operation holders funcs %= holders max

execute if score holders funcs matches 0 run data merge entity @e[tag=strength_llama,limit=1] {Strength:1}

execute if score holders funcs matches 1 run data merge entity @e[tag=strength_llama,limit=1] {Strength:2}

execute if score holders funcs matches 2 run data merge entity @e[tag=strength_llama,limit=1] {Strength:3}

execute if score holders funcs matches 3 run data merge entity @e[tag=strength_llama,limit=1] {Strength:4}

execute if score holders funcs matches 4 run data merge entity @e[tag=strength_llama,limit=1] {Strength:5}

execute if score holders funcs matches 5 run data merge entity @e[tag=strength_llama,limit=1] {Strength:4}

execute if score holders funcs matches 6 run data merge entity @e[tag=strength_llama,limit=1] {Strength:3}

execute if score holders funcs matches 7 run data merge entity @e[tag=strength_llama,limit=1] {Strength:2}