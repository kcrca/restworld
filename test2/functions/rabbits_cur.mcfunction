execute if score rabbits funcs matches 0 run execute as @e[tag=rabbits] run data merge entity @s {RabbitType:0,CustomName:"\"Brown\""}

execute if score rabbits funcs matches 1 run execute as @e[tag=rabbits] run data merge entity @s {RabbitType:1,CustomName:"\"White\""}

execute if score rabbits funcs matches 2 run execute as @e[tag=rabbits] run data merge entity @s {RabbitType:2,CustomName:"\"Black\""}

execute if score rabbits funcs matches 3 run execute as @e[tag=rabbits] run data merge entity @s {RabbitType:3,CustomName:"\"Black & White\""}

execute if score rabbits funcs matches 4 run execute as @e[tag=rabbits] run data merge entity @s {RabbitType:4,CustomName:"\"Gold\""}

execute if score rabbits funcs matches 5 run execute as @e[tag=rabbits] run data merge entity @s {RabbitType:5,CustomName:"\"Salt & Pepper\""}

execute if score rabbits funcs matches 6 run execute as @e[tag=rabbits] run data merge entity @s {RabbitType:99,CustomName:"\"Killer Rabbit (unused)\""}