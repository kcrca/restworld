execute unless score chest funcs matches 0.. run function chest_init
scoreboard players add chest funcs 1
scoreboard players set chest max 4
execute unless score chest funcs matches 0..3 run scoreboard players operation chest funcs %= chest max

execute if score chest funcs matches 0 run setblock ~0 ~3 ~0 minecraft:chest[facing=south]
execute if score chest funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"\"",Text3:"\"Chest\""}
execute if score chest funcs matches 0 run setblock ~-1 ~3 ~0 air


execute if score chest funcs matches 1 run setblock ~0 ~3 ~0 minecraft:trapped_chest[facing=south]
execute if score chest funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Trapped\"",Text3:"\"Chest\""}
execute if score chest funcs matches 1 run setblock ~-1 ~3 ~0 air


execute if score chest funcs matches 2 run setblock ~0 ~3 ~0 minecraft:chest[type=left,facing=south]
execute if score chest funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"\"",Text3:"\"Double Chest\""}
execute if score chest funcs matches 2 run setblock ~-1 ~3 ~0 minecraft:chest[type=right,facing=south]


execute if score chest funcs matches 3 run setblock ~0 ~3 ~0 minecraft:trapped_chest[type=left,facing=south]
execute if score chest funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Trapped\"",Text3:"\"Double Chest\""}
execute if score chest funcs matches 3 run setblock ~-1 ~3 ~0 minecraft:trapped_chest[type=right,facing=south]
