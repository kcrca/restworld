execute unless score cane funcs matches 0.. run function cane_init
scoreboard players add cane funcs 1
execute unless score cane funcs matches 0..3 run scoreboard players set cane funcs 0

execute if score cane funcs matches 0 run setblock ~0 ~4 ~0 minecraft:sugar_cane
execute if score cane funcs matches 2 run setblock ~0 ~5 ~0 minecraft:air
execute if score cane funcs matches 1 run setblock ~0 ~5 ~0 minecraft:sugar_cane
execute if score cane funcs matches 3 run setblock ~0 ~4 ~0 minecraft:air