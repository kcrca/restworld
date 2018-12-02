execute unless score frosted_ice funcs matches 0.. run function frosted_ice_init
scoreboard players add frosted_ice funcs 1
execute unless score frosted_ice funcs matches 0..4 run scoreboard players set frosted_ice funcs 0

execute if score frosted_ice funcs matches 0 run setblock ~ ~3 ~ minecraft:water


execute if score frosted_ice funcs matches 1 run setblock ~ ~3 ~ minecraft:frosted_ice[age=0]


execute if score frosted_ice funcs matches 2 run setblock ~ ~3 ~ minecraft:frosted_ice[age=1]


execute if score frosted_ice funcs matches 3 run setblock ~ ~3 ~ minecraft:frosted_ice[age=2]


execute if score frosted_ice funcs matches 4 run setblock ~ ~3 ~ minecraft:frosted_ice[age=3]