

execute unless score creeper funcs matches 0.. run function creeper_init
scoreboard players add creeper funcs 1
execute unless score creeper funcs matches 0..1 run scoreboard players set creeper funcs 0

execute if score creeper funcs matches 0 run execute as @e[tag=creeper,limit=1] run data merge entity @s {powered:True}


execute if score creeper funcs matches 1 run execute as @e[tag=creeper,limit=1] run data merge entity @s {powered:False}


