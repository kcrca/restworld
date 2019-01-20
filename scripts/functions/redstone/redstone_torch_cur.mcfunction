scoreboard players set redstone_torch max 2
execute unless score redstone_torch funcs matches 0..1 run scoreboard players operation redstone_torch funcs %= redstone_torch max
execute if score redstone_torch funcs matches 0 run setblock ~-1 ~-1 ~-1 minecraft:redstone_block

execute if score redstone_torch funcs matches 1 run setblock ~-1 ~-1 ~-1 minecraft:air
