execute unless score redstone_block funcs matches 0.. run function redstone_block_init
scoreboard players add redstone_block funcs 1
execute unless score redstone_block funcs matches 0..1 run scoreboard players set redstone_block funcs 0
execute if score redstone_block funcs matches 0 run setblock ~ ~3 ~ minecraft:redstone_block

execute if score redstone_block funcs matches 1 run setblock ~ ~3 ~ minecraft:air
