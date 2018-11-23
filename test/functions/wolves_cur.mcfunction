

execute if score wolves funcs matches 0 run execute as @e[tag=wolves] run data merge entity @s {Angry:True}

execute if score wolves funcs matches 1 run execute as @e[tag=wolves] run data merge entity @s {Angry:False}

