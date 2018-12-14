execute unless score mushrooms funcs matches 0.. run function mushrooms_init
scoreboard players add mushrooms funcs 1
execute unless score mushrooms funcs matches 0..1 run scoreboard players set mushrooms funcs 0
execute if score mushrooms funcs matches 0 run setblock ~ ~3 ~ minecraft:red_mushroom
execute if score mushrooms funcs matches 0 run data merge block ~1 ~2 ~ {Text2:"\"Red Mushroom\""}

execute if score mushrooms funcs matches 1 run setblock ~ ~3 ~ minecraft:brown_mushroom
execute if score mushrooms funcs matches 1 run data merge block ~1 ~2 ~ {Text2:"\"Brown Mushroom\""}
