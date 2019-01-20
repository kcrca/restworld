execute unless score growing funcs matches 0.. run function growing_init
scoreboard players add growing funcs 1
scoreboard players set growing max 4
execute unless score growing funcs matches 0..3 run scoreboard players operation growing funcs %= growing max

execute if score growing funcs matches 0 run execute as @e[tag=growing] run data merge entity @s {Size:0}

execute if score growing funcs matches 1 run execute as @e[tag=growing] run data merge entity @s {Size:1}

execute if score growing funcs matches 2 run execute as @e[tag=growing] run data merge entity @s {Size:3}

execute if score growing funcs matches 3 run execute as @e[tag=growing] run data merge entity @s {Size:1}
