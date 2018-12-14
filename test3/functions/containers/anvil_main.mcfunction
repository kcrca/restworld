execute unless score anvil funcs matches 0.. run function anvil_init
scoreboard players add anvil funcs 1
scoreboard players set anvil max 4
execute unless score anvil funcs matches 0..3 run scoreboard players operation anvil funcs %= anvil max

execute if score anvil funcs matches 0 run setblock ~ ~2 ~ minecraft:anvil

execute if score anvil funcs matches 1 run setblock ~ ~2 ~ minecraft:chipped_anvil

execute if score anvil funcs matches 2 run setblock ~ ~2 ~ minecraft:damaged_anvil

execute if score anvil funcs matches 3 run setblock ~ ~2 ~ minecraft:chipped_anvil
