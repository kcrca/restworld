execute unless score columns funcs matches 0.. run function columns_init
scoreboard players add columns funcs 1
execute unless score columns funcs matches 0..1 run scoreboard players set columns funcs 0

execute if score columns funcs matches 0 run setblock ~ ~2 ~ minecraft:soul_sand
execute if score columns funcs matches 0 run fill ~ ~3 ~ ~ ~7 ~-1 minecraft:bubble_column[drag=false]


execute if score columns funcs matches 1 run setblock ~ ~2 ~ minecraft:magma_block
execute if score columns funcs matches 1 run fill ~ ~3 ~ ~ ~7 ~-1 minecraft:bubble_column[drag=true]