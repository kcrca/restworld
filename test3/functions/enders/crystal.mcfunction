kill @e[tag=crystal]
execute unless score crystal funcs matches 0.. run function crystal_init
scoreboard players add crystal funcs 1
scoreboard players set crystal max 2
execute unless score crystal funcs matches 0..1 run scoreboard players operation crystal funcs %= crystal max

execute if score crystal funcs matches 0 run summon end_crystal ~0 ~5.0 ~0 {Tags:[crystal]}
execute if score crystal funcs matches 0 run setblock ~0 ~5 ~0 minecraft:fire
execute if score crystal funcs matches 0 run fill ~-2 ~6 ~-2 ~2 ~10 ~2 minecraft:iron_bars hollow
execute if score crystal funcs matches 0 run fill ~-2 ~6 ~-2 ~6 ~7 ~2 minecraft:air
execute if score crystal funcs matches 0 run clone ~3 ~11 ~2 ~-1 ~9 ~-2 ~-1 ~6 ~-2 masked move
execute if score crystal funcs matches 0 run setblock ~0 ~5 ~0 minecraft:fire

execute if score crystal funcs matches 1 run kill @e[tag=crystal]
execute if score crystal funcs matches 1 run setblock ~0 ~5 ~0 minecraft:air
execute if score crystal funcs matches 1 run fill ~-2 ~6 ~-2 ~2 ~10 ~2 minecraft:air
