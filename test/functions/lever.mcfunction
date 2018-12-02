execute unless score lever funcs matches 0.. run function lever_init
scoreboard players add lever funcs 1
execute unless score lever funcs matches 0..1 run scoreboard players set lever funcs 0
execute if score lever funcs matches 0 run setblock ~ ~3 ~ minecraft:lever[powered=false,face=floor]

execute if score lever funcs matches 1 run setblock ~ ~3 ~ minecraft:lever[powered=true,face=floor]