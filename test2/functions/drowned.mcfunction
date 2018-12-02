execute unless score drowned funcs matches 0.. run function drowned_init
scoreboard players add drowned funcs 1
execute unless score drowned funcs matches 0..1 run scoreboard players set drowned funcs 0
execute if score drowned funcs matches 0 run execute as @e[tag=drowned] run data merge entity @s {HandItems:[{id:trident,Count:0}]}

execute if score drowned funcs matches 1 run execute as @e[tag=drowned] run data merge entity @s {HandItems:[{id:trident,Count:1}]}