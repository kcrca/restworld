execute unless score growing funcs matches 0.. run function growing_init
scoreboard players add growing funcs 1
execute unless score growing funcs matches 0..5 run scoreboard players set growing funcs 0

execute if score growing funcs matches 0 run execute as @e[tag=growing] run data merge entity @s {Size:0}

execute if score growing funcs matches 1 run execute as @e[tag=growing] run data merge entity @s {Size:1}

execute if score growing funcs matches 2 run execute as @e[tag=growing] run data merge entity @s {Size:2}

execute if score growing funcs matches 3 run execute as @e[tag=growing] run data merge entity @s {Size:3}

execute if score growing funcs matches 4 run execute as @e[tag=growing] run data merge entity @s {Size:2}

execute if score growing funcs matches 5 run execute as @e[tag=growing] run data merge entity @s {Size:1}