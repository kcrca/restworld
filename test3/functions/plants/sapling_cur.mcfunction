scoreboard players set sapling max 2
execute unless score sapling funcs matches 0..1 run scoreboard players operation sapling funcs %= sapling max
execute if score sapling funcs matches 0 run setblock ~0 ~3 ~0 minecraft:acacia_sapling[stage=0]
execute if score sapling funcs matches 0 run setblock ~0 ~3 ~-3 minecraft:birch_sapling[stage=0]
execute if score sapling funcs matches 0 run setblock ~0 ~3 ~-6 minecraft:jungle_sapling[stage=0]
execute if score sapling funcs matches 0 run setblock ~3 ~3 ~0 minecraft:oak_sapling[stage=0]
execute if score sapling funcs matches 0 run setblock ~3 ~3 ~-3 minecraft:dark_oak_sapling[stage=0]
execute if score sapling funcs matches 0 run setblock ~3 ~3 ~-6 minecraft:spruce_sapling[stage=0]

execute if score sapling funcs matches 1 run setblock ~0 ~3 ~0 minecraft:acacia_sapling[stage=1]
execute if score sapling funcs matches 1 run setblock ~0 ~3 ~-3 minecraft:birch_sapling[stage=1]
execute if score sapling funcs matches 1 run setblock ~0 ~3 ~-6 minecraft:jungle_sapling[stage=1]
execute if score sapling funcs matches 1 run setblock ~3 ~3 ~0 minecraft:oak_sapling[stage=1]
execute if score sapling funcs matches 1 run setblock ~3 ~3 ~-3 minecraft:dark_oak_sapling[stage=1]
execute if score sapling funcs matches 1 run setblock ~3 ~3 ~-6 minecraft:spruce_sapling[stage=1]