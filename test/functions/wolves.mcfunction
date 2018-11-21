

execute unless score wolves funcs matches 0.. run function wolves_init
scoreboard players add wolves funcs 1
execute unless score wolves funcs matches 0..1 run scoreboard players set wolves funcs 0
execute if score wolves funcs matches 0 run execute as @e[tag=wolves] run data merge entity @s {Angry:True}

execute if score wolves funcs matches 1 run execute as @e[tag=wolves] run data merge entity @s {Angry:False}

