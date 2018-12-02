execute unless score cane_soil funcs matches 0.. run function cane_soil_init
scoreboard players add cane_soil funcs 1
execute unless score cane_soil funcs matches 0..9 run scoreboard players set cane_soil funcs 0

execute if score cane_soil funcs matches 0 run setblock ~ ~2 ~ minecraft:grass_block

execute if score cane_soil funcs matches 1 run setblock ~ ~2 ~ minecraft:dirt

execute if score cane_soil funcs matches 2 run setblock ~ ~2 ~ minecraft:coarse_dirt

execute if score cane_soil funcs matches 3 run setblock ~ ~2 ~ minecraft:podzol

execute if score cane_soil funcs matches 4 run setblock ~ ~2 ~ minecraft:sand

execute if score cane_soil funcs matches 5 run setblock ~ ~2 ~ minecraft:red_sand

execute if score cane_soil funcs matches 6 run setblock ~ ~2 ~ minecraft:sand

execute if score cane_soil funcs matches 7 run setblock ~ ~2 ~ minecraft:podzol

execute if score cane_soil funcs matches 8 run setblock ~ ~2 ~ minecraft:coarse_dirt

execute if score cane_soil funcs matches 9 run setblock ~ ~2 ~ minecraft:dirt