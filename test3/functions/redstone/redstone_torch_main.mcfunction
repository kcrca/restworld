execute unless score redstone_torch funcs matches 0.. run function redstone_torch_init
scoreboard players add redstone_torch funcs 1
execute unless score redstone_torch funcs matches 0..1 run scoreboard players set redstone_torch funcs 0
execute if score redstone_torch funcs matches 0 run setblock ~-1 ~-1 ~-1 minecraft:redstone_block

execute if score redstone_torch funcs matches 1 run setblock ~-1 ~-1 ~-1 minecraft:air
