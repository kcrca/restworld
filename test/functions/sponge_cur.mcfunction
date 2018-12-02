execute if score sponge funcs matches 0 run setblock ~ ~3 ~ minecraft:sponge
execute if score sponge funcs matches 0 run data merge block ~1 ~2 ~ {Text2:"\"Sponge\""}


execute if score sponge funcs matches 1 run setblock ~ ~3 ~ minecraft:wet_sponge
execute if score sponge funcs matches 1 run data merge block ~1 ~2 ~ {Text2:"\"Wet Sponge\""}