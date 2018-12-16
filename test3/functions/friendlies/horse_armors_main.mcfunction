execute unless score horse_armors funcs matches 0.. run function horse_armors_init
scoreboard players add horse_armors funcs 1
scoreboard players set horse_armors max 4
execute unless score horse_armors funcs matches 0..3 run scoreboard players operation horse_armors funcs %= horse_armors max

execute if score horse_armors funcs matches 0 run tp @e[tag=horse] @e[tag=death,limit=1]

execute if score horse_armors funcs matches 0 run execute at @e[tag=horse_home] run function v3:friendlies/horse_init


execute if score horse_armors funcs matches 1 run execute as @e[tag=horse,tag=!kid] run data merge entity @s {ArmorItem:{id:"minecraft:iron_horse_armor",Count:1}}


execute if score horse_armors funcs matches 2 run execute as @e[tag=horse,tag=!kid] run data merge entity @s {ArmorItem:{id:"minecraft:golden_horse_armor",Count:1}}


execute if score horse_armors funcs matches 3 run execute as @e[tag=horse,tag=!kid] run data merge entity @s {ArmorItem:{id:"minecraft:diamond_horse_armor",Count:1}}
