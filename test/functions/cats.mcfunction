

execute unless score cats funcs matches 0.. run function cats_init
scoreboard players add cats funcs 1
execute unless score cats funcs matches 0..3 run scoreboard players set cats funcs 0
execute if score cats funcs matches 0 run execute as @e[tag=cats] run data merge entity @s {CatType:0,CustomName:"\"Ocelot\""}
execute if score cats funcs matches 1 run execute as @e[tag=cats] run data merge entity @s {CatType:1,CustomName:"\"Tuxedo\""}
execute if score cats funcs matches 2 run execute as @e[tag=cats] run data merge entity @s {CatType:2,CustomName:"\"Tabby\""}
execute if score cats funcs matches 3 run execute as @e[tag=cats] run data merge entity @s {CatType:3,CustomName:"\"Siamese\""}
