scoreboard players set llama max 8
execute unless score llama funcs matches 0..7 run scoreboard players operation llama funcs %= llama max

execute if score llama funcs matches 0 run data merge entity @e[tag=strength_llama,limit=1] {Strength:1}

execute if score llama funcs matches 1 run data merge entity @e[tag=strength_llama,limit=1] {Strength:2}

execute if score llama funcs matches 2 run data merge entity @e[tag=strength_llama,limit=1] {Strength:3}

execute if score llama funcs matches 3 run data merge entity @e[tag=strength_llama,limit=1] {Strength:4}

execute if score llama funcs matches 4 run data merge entity @e[tag=strength_llama,limit=1] {Strength:5}

execute if score llama funcs matches 5 run data merge entity @e[tag=strength_llama,limit=1] {Strength:4}

execute if score llama funcs matches 6 run data merge entity @e[tag=strength_llama,limit=1] {Strength:3}

execute if score llama funcs matches 7 run data merge entity @e[tag=strength_llama,limit=1] {Strength:2}