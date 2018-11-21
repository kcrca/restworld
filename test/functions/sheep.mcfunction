

execute unless score sheep funcs matches 0.. run function sheep_init
scoreboard players add sheep funcs 1
execute unless score sheep funcs matches 0..15 run scoreboard players set sheep funcs 0
execute if score sheep funcs matches 0 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:0,CustomName:"\"White\""}
execute if score sheep funcs matches 1 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:1,CustomName:"\"Orange\""}
execute if score sheep funcs matches 2 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:2,CustomName:"\"Magenta\""}
execute if score sheep funcs matches 3 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:3,CustomName:"\"Light Blue\""}
execute if score sheep funcs matches 4 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:4,CustomName:"\"Yellow\""}
execute if score sheep funcs matches 5 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:5,CustomName:"\"Lime\""}
execute if score sheep funcs matches 6 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:6,CustomName:"\"Pink\""}
execute if score sheep funcs matches 7 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:7,CustomName:"\"Gray\""}
execute if score sheep funcs matches 8 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:8,CustomName:"\"Light Gray\""}
execute if score sheep funcs matches 9 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:9,CustomName:"\"Cyan\""}
execute if score sheep funcs matches 10 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:10,CustomName:"\"Purple\""}
execute if score sheep funcs matches 11 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:11,CustomName:"\"Blue\""}
execute if score sheep funcs matches 12 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:12,CustomName:"\"Brown\""}
execute if score sheep funcs matches 13 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:13,CustomName:"\"Green\""}
execute if score sheep funcs matches 14 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:14,CustomName:"\"Red\""}
execute if score sheep funcs matches 15 run execute as @e[tag=colored_sheep] run data merge entity @s {Color:15,CustomName:"\"Black\""}
