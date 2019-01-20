scoreboard players set cage max 2
execute unless score cage funcs matches 0..1 run scoreboard players operation cage funcs %= cage max

execute if score cage funcs matches 0 run execute at @e[tag=crystal_home] run fill ~2 ~9 ~2 ~-2 ~6 ~-2 minecraft:iron_bars hollow
execute if score cage funcs matches 0 run execute at @e[tag=crystal_home] run fill ~1 ~8 ~1 ~-1 ~6 ~-1 minecraft:air
execute if score cage funcs matches 0 run execute at @e[tag=crystal_home] run clone ~2 ~9 ~2 ~-2 ~6 ~-2 ~-2 ~4 ~-2 masked move

execute if score cage funcs matches 1 run execute at @e[tag=crystal_home] run fill ~2 ~7 ~2 ~-2 ~4 ~-2 minecraft:air replace iron_bars
