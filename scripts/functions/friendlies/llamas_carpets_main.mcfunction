execute unless score llamas_carpets funcs matches 0.. run function llamas_carpets_init
scoreboard players add llamas_carpets funcs 1
scoreboard players set llamas_carpets max 16
execute unless score llamas_carpets funcs matches 0..15 run scoreboard players operation llamas_carpets funcs %= llamas_carpets max
execute if score llamas_carpets funcs matches 0 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:white_carpet,Count:1}}
execute if score llamas_carpets funcs matches 1 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:orange_carpet,Count:1}}
execute if score llamas_carpets funcs matches 2 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:magenta_carpet,Count:1}}
execute if score llamas_carpets funcs matches 3 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:light_blue_carpet,Count:1}}
execute if score llamas_carpets funcs matches 4 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:yellow_carpet,Count:1}}
execute if score llamas_carpets funcs matches 5 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:lime_carpet,Count:1}}
execute if score llamas_carpets funcs matches 6 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:pink_carpet,Count:1}}
execute if score llamas_carpets funcs matches 7 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:gray_carpet,Count:1}}
execute if score llamas_carpets funcs matches 8 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:light_gray_carpet,Count:1}}
execute if score llamas_carpets funcs matches 9 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:cyan_carpet,Count:1}}
execute if score llamas_carpets funcs matches 10 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:purple_carpet,Count:1}}
execute if score llamas_carpets funcs matches 11 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:blue_carpet,Count:1}}
execute if score llamas_carpets funcs matches 12 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:brown_carpet,Count:1}}
execute if score llamas_carpets funcs matches 13 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:green_carpet,Count:1}}
execute if score llamas_carpets funcs matches 14 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:red_carpet,Count:1}}
execute if score llamas_carpets funcs matches 15 as @e[tag=llama,tag=!kid] run data merge entity @s {DecorItem:{id:black_carpet,Count:1}}
