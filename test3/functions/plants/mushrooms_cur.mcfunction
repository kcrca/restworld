execute if score mushrooms funcs matches 0 run setblock ~ ~3 ~ minecraft:red_mushroom
execute if score mushrooms funcs matches 0 run data merge block ~1 ~2 ~ {Text2:"\"Red Mushroom\""}

execute if score mushrooms funcs matches 1 run setblock ~ ~3 ~ minecraft:brown_mushroom
execute if score mushrooms funcs matches 1 run data merge block ~1 ~2 ~ {Text2:"\"Brown Mushroom\""}