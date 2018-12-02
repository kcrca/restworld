execute if score creeper funcs matches 0 run execute as @e[tag=creeper,limit=1] run data merge entity @s {powered:True}


execute if score creeper funcs matches 1 run execute as @e[tag=creeper,limit=1] run data merge entity @s {powered:False}