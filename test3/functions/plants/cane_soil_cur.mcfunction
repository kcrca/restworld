scoreboard players set cane_soil max 10
execute unless score cane_soil funcs matches 0..9 run scoreboard players operation cane_soil funcs %= cane_soil max

execute if score cane_soil funcs matches 0 run setblock ~ ~2 ~1 minecraft:grass_block

execute if score cane_soil funcs matches 1 run setblock ~ ~2 ~1 minecraft:dirt

execute if score cane_soil funcs matches 2 run setblock ~ ~2 ~1 minecraft:coarse_dirt

execute if score cane_soil funcs matches 3 run setblock ~ ~2 ~1 minecraft:podzol

execute if score cane_soil funcs matches 4 run setblock ~ ~2 ~1 minecraft:sand

execute if score cane_soil funcs matches 5 run setblock ~ ~2 ~1 minecraft:red_sand

execute if score cane_soil funcs matches 6 run setblock ~ ~2 ~1 minecraft:sand

execute if score cane_soil funcs matches 7 run setblock ~ ~2 ~1 minecraft:podzol

execute if score cane_soil funcs matches 8 run setblock ~ ~2 ~1 minecraft:coarse_dirt

execute if score cane_soil funcs matches 9 run setblock ~ ~2 ~1 minecraft:dirt
