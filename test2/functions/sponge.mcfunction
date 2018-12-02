execute unless score sponge funcs matches 0.. run function sponge_init
scoreboard players add sponge funcs 1
execute unless score sponge funcs matches 0..1 run scoreboard players set sponge funcs 0

execute if score sponge funcs matches 0 run setblock ~ ~3 ~ minecraft:sponge
execute if score sponge funcs matches 0 run data merge block ~1 ~2 ~ {Text2:"\"Sponge\""}


execute if score sponge funcs matches 1 run setblock ~ ~3 ~ minecraft:wet_sponge
execute if score sponge funcs matches 1 run data merge block ~1 ~2 ~ {Text2:"\"Wet Sponge\""}