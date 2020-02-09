execute unless score trader_llama funcs matches 0.. run function trader_llama_init
scoreboard players add trader_llama funcs 1
scoreboard players set trader_llama max 4
execute unless score trader_llama funcs matches 0..3 run scoreboard players operation trader_llama funcs %= trader_llama max
execute if score trader_llama funcs matches 0 run execute as @e[type=trader_llama] run data modify entity @s Variant set value 0

execute if score trader_llama funcs matches 1 run execute as @e[type=trader_llama] run data modify entity @s Variant set value 1

execute if score trader_llama funcs matches 2 run execute as @e[type=trader_llama] run data modify entity @s Variant set value 2

execute if score trader_llama funcs matches 3 run execute as @e[type=trader_llama] run data modify entity @s Variant set value 3
