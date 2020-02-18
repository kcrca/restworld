execute unless score wood_blocks funcs matches 0.. run function wood_blocks_init
scoreboard players add wood_blocks funcs 1
scoreboard players set wood_blocks max 6
execute unless score wood_blocks funcs matches 0..5 run scoreboard players operation wood_blocks funcs %= wood_blocks max

execute if score wood_blocks funcs matches 0 run setblock ~0 ~3 ~0 minecraft:acacia_planks
execute if score wood_blocks funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Acacia Planks\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 0 run setblock ~-3 ~3 ~0 minecraft:stripped_acacia_log
execute if score wood_blocks funcs matches 0 run data merge block ~-3 ~2 ~1 {Text2:"\"Stripped\"",Text3:"\"Acacia Log\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 0 run setblock ~0 ~3 ~-3 minecraft:acacia_log
execute if score wood_blocks funcs matches 0 run data merge block ~0 ~2 ~-2 {Text2:"\"Acacia Log\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 0 run setblock ~-3 ~3 ~-3 minecraft:acacia_wood
execute if score wood_blocks funcs matches 0 run data merge block ~-3 ~2 ~-2 {Text2:"\"Acacia Wood\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 0 run setblock ~0 ~3 ~-6 minecraft:acacia_leaves
execute if score wood_blocks funcs matches 0 run data merge block ~0 ~2 ~-5 {Text2:"\"Acacia Leaves\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 0 run setblock ~-3 ~3 ~-6 minecraft:stripped_acacia_wood
execute if score wood_blocks funcs matches 0 run data merge block ~-3 ~2 ~-5 {Text2:"\"Stripped\"",Text3:"\"Acacia Wood\"",Text4:"\"\""}


execute if score wood_blocks funcs matches 1 run setblock ~0 ~3 ~0 minecraft:birch_planks
execute if score wood_blocks funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Birch Planks\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 1 run setblock ~-3 ~3 ~0 minecraft:stripped_birch_log
execute if score wood_blocks funcs matches 1 run data merge block ~-3 ~2 ~1 {Text2:"\"Stripped\"",Text3:"\"Birch Log\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 1 run setblock ~0 ~3 ~-3 minecraft:birch_log
execute if score wood_blocks funcs matches 1 run data merge block ~0 ~2 ~-2 {Text2:"\"Birch Log\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 1 run setblock ~-3 ~3 ~-3 minecraft:birch_wood
execute if score wood_blocks funcs matches 1 run data merge block ~-3 ~2 ~-2 {Text2:"\"Birch Wood\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 1 run setblock ~0 ~3 ~-6 minecraft:birch_leaves
execute if score wood_blocks funcs matches 1 run data merge block ~0 ~2 ~-5 {Text2:"\"Birch Leaves\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 1 run setblock ~-3 ~3 ~-6 minecraft:stripped_birch_wood
execute if score wood_blocks funcs matches 1 run data merge block ~-3 ~2 ~-5 {Text2:"\"Stripped\"",Text3:"\"Birch Wood\"",Text4:"\"\""}


execute if score wood_blocks funcs matches 2 run setblock ~0 ~3 ~0 minecraft:jungle_planks
execute if score wood_blocks funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Jungle Planks\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 2 run setblock ~-3 ~3 ~0 minecraft:stripped_jungle_log
execute if score wood_blocks funcs matches 2 run data merge block ~-3 ~2 ~1 {Text2:"\"Stripped\"",Text3:"\"Jungle Log\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 2 run setblock ~0 ~3 ~-3 minecraft:jungle_log
execute if score wood_blocks funcs matches 2 run data merge block ~0 ~2 ~-2 {Text2:"\"Jungle Log\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 2 run setblock ~-3 ~3 ~-3 minecraft:jungle_wood
execute if score wood_blocks funcs matches 2 run data merge block ~-3 ~2 ~-2 {Text2:"\"Jungle Wood\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 2 run setblock ~0 ~3 ~-6 minecraft:jungle_leaves
execute if score wood_blocks funcs matches 2 run data merge block ~0 ~2 ~-5 {Text2:"\"Jungle Leaves\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 2 run setblock ~-3 ~3 ~-6 minecraft:stripped_jungle_wood
execute if score wood_blocks funcs matches 2 run data merge block ~-3 ~2 ~-5 {Text2:"\"Stripped\"",Text3:"\"Jungle Wood\"",Text4:"\"\""}


execute if score wood_blocks funcs matches 3 run setblock ~0 ~3 ~0 minecraft:oak_planks
execute if score wood_blocks funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Oak Planks\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 3 run setblock ~-3 ~3 ~0 minecraft:stripped_oak_log
execute if score wood_blocks funcs matches 3 run data merge block ~-3 ~2 ~1 {Text2:"\"Stripped\"",Text3:"\"Oak Log\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 3 run setblock ~0 ~3 ~-3 minecraft:oak_log
execute if score wood_blocks funcs matches 3 run data merge block ~0 ~2 ~-2 {Text2:"\"Oak Log\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 3 run setblock ~-3 ~3 ~-3 minecraft:oak_wood
execute if score wood_blocks funcs matches 3 run data merge block ~-3 ~2 ~-2 {Text2:"\"Oak Wood\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 3 run setblock ~0 ~3 ~-6 minecraft:oak_leaves
execute if score wood_blocks funcs matches 3 run data merge block ~0 ~2 ~-5 {Text2:"\"Oak Leaves\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 3 run setblock ~-3 ~3 ~-6 minecraft:stripped_oak_wood
execute if score wood_blocks funcs matches 3 run data merge block ~-3 ~2 ~-5 {Text2:"\"Stripped\"",Text3:"\"Oak Wood\"",Text4:"\"\""}


execute if score wood_blocks funcs matches 4 run setblock ~0 ~3 ~0 minecraft:dark_oak_planks
execute if score wood_blocks funcs matches 4 run data merge block ~0 ~2 ~1 {Text2:"\"Dark Oak Planks\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 4 run setblock ~-3 ~3 ~0 minecraft:stripped_dark_oak_log
execute if score wood_blocks funcs matches 4 run data merge block ~-3 ~2 ~1 {Text2:"\"Stripped\"",Text3:"\"Dark Oak Log\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 4 run setblock ~0 ~3 ~-3 minecraft:dark_oak_log
execute if score wood_blocks funcs matches 4 run data merge block ~0 ~2 ~-2 {Text2:"\"Dark Oak Log\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 4 run setblock ~-3 ~3 ~-3 minecraft:dark_oak_wood
execute if score wood_blocks funcs matches 4 run data merge block ~-3 ~2 ~-2 {Text2:"\"Dark Oak Wood\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 4 run setblock ~0 ~3 ~-6 minecraft:dark_oak_leaves
execute if score wood_blocks funcs matches 4 run data merge block ~0 ~2 ~-5 {Text2:"\"Dark Oak Leaves\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 4 run setblock ~-3 ~3 ~-6 minecraft:stripped_dark_oak_wood
execute if score wood_blocks funcs matches 4 run data merge block ~-3 ~2 ~-5 {Text2:"\"Stripped\"",Text3:"\"Dark Oak Wood\"",Text4:"\"\""}


execute if score wood_blocks funcs matches 5 run setblock ~0 ~3 ~0 minecraft:spruce_planks
execute if score wood_blocks funcs matches 5 run data merge block ~0 ~2 ~1 {Text2:"\"Spruce Planks\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 5 run setblock ~-3 ~3 ~0 minecraft:stripped_spruce_log
execute if score wood_blocks funcs matches 5 run data merge block ~-3 ~2 ~1 {Text2:"\"Stripped\"",Text3:"\"Spruce Log\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 5 run setblock ~0 ~3 ~-3 minecraft:spruce_log
execute if score wood_blocks funcs matches 5 run data merge block ~0 ~2 ~-2 {Text2:"\"Spruce Log\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 5 run setblock ~-3 ~3 ~-3 minecraft:spruce_wood
execute if score wood_blocks funcs matches 5 run data merge block ~-3 ~2 ~-2 {Text2:"\"Spruce Wood\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 5 run setblock ~0 ~3 ~-6 minecraft:spruce_leaves
execute if score wood_blocks funcs matches 5 run data merge block ~0 ~2 ~-5 {Text2:"\"Spruce Leaves\"",Text3:"\"\"",Text4:"\"\""}

execute if score wood_blocks funcs matches 5 run setblock ~-3 ~3 ~-6 minecraft:stripped_spruce_wood
execute if score wood_blocks funcs matches 5 run data merge block ~-3 ~2 ~-5 {Text2:"\"Stripped\"",Text3:"\"Spruce Wood\"",Text4:"\"\""}
