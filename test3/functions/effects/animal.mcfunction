execute unless score animal funcs matches 0.. run function animal_init
scoreboard players add animal funcs 1
scoreboard players set animal max 6
execute unless score animal funcs matches 0..5 run scoreboard players operation animal funcs %= animal max

execute if score animal funcs matches 0 run summon minecraft:cow ~0 ~0 ~0 {NoAI:True,Tags:[effecter]}

execute if score animal funcs matches 1 run summon minecraft:pig ~0 ~0 ~0 {NoAI:True,Tags:[effecter]}

execute if score animal funcs matches 2 run summon minecraft:horse ~0 ~0 ~0 {NoAI:True,Tags:[effecter]}

execute if score animal funcs matches 3 run summon minecraft:llama ~0 ~0 ~0 {NoAI:True,Tags:[effecter]}

execute if score animal funcs matches 4 run summon minecraft:sheep ~0 ~0 ~0 {NoAI:True,Tags:[effecter]}

execute if score animal funcs matches 5 run summon minecraft:polar_bear ~0 ~0 ~0 {NoAI:True,Tags:[effecter]}
