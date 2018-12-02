execute unless score anvil funcs matches 0.. run function anvil_init
scoreboard players add anvil funcs 1
execute unless score anvil funcs matches 0..3 run scoreboard players set anvil funcs 0

execute if score anvil funcs matches 0 run setblock ~ ~3 ~ minecraft:anvil

execute if score anvil funcs matches 1 run setblock ~ ~3 ~ minecraft:chipped_anvil

execute if score anvil funcs matches 2 run setblock ~ ~3 ~ minecraft:damaged_anvil

execute if score anvil funcs matches 3 run setblock ~ ~3 ~ minecraft:chipped_anvil