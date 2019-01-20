execute unless score redstone_block funcs matches 0.. run function redstone_block_init
scoreboard players add redstone_block funcs 1
scoreboard players set redstone_block max 2
execute unless score redstone_block funcs matches 0..1 run scoreboard players operation redstone_block funcs %= redstone_block max
execute if score redstone_block funcs matches 0 run setblock ~ ~3 ~ minecraft:redstone_block

execute if score redstone_block funcs matches 1 run setblock ~ ~3 ~ minecraft:air
