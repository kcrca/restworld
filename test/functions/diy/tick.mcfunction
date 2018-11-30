execute at @e[tag=cloner] run setblock ~0 ~3 ~0 sand
scoreboard players set custom_reset funcs 0
execute at @e[tag=cloner] unless block ~0 ~0 ~-1 air run scoreboard players set custom_reset funcs 1
execute at @e[tag=cloner] if block ~0 ~4 ~-1 air run scoreboard players set custom_reset funcs 1
execute if score custom_reset funcs matches 1 at @e[tag=starter] run tp @e[tag=cloner] ~0 ~2 ~0
execute if score custom_reset funcs matches 0 at @e[tag=cloner] run tp @e[tag=cloner] ^ ^ ^1
execute at @e[tag=cloner] run setblock ~0 ~3 ~0 red_sand
execute at @e[tag=cloner] run clone ~0 ~4 ~0 ~0 ~4 ~0 ~3 ~-2 -37
execute at @e[tag=displayer] run clone ~0 ~-2 ~0 ~0 ~-2 ~0 ~0 ~4 ~0
