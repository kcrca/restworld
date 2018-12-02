execute if score columns funcs matches 0 run setblock ~ ~2 ~ minecraft:soul_sand
execute if score columns funcs matches 0 run fill ~ ~3 ~ ~ ~7 ~-1 minecraft:bubble_column[drag=false]


execute if score columns funcs matches 1 run setblock ~ ~2 ~ minecraft:magma_block
execute if score columns funcs matches 1 run fill ~ ~3 ~ ~ ~7 ~-1 minecraft:bubble_column[drag=true]