execute unless score foxes funcs matches 0.. run function foxes_init
scoreboard players add foxes funcs 1
scoreboard players set foxes max 2
execute unless score foxes funcs matches 0..1 run scoreboard players operation foxes funcs %= foxes max
execute if score foxes funcs matches 0 run execute as @e[tag=fox] run data merge entity @s {Type:red,CustomName:"\"Red\""}
execute if score foxes funcs matches 1 run execute as @e[tag=fox] run data merge entity @s {Type:snow,CustomName:"\"Snow\""}
