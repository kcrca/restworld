execute if score trapped_chest funcs matches 0 run setblock ~ ~3 ~ minecraft:chest[facing=south]
execute if score trapped_chest funcs matches 0 run data merge block ~ ~2 ~1 {Text2:"\"Chest\""}


execute if score trapped_chest funcs matches 1 run setblock ~ ~3 ~ minecraft:trapped_chest[facing=south]
execute if score trapped_chest funcs matches 1 run data merge block ~ ~2 ~1 {Text2:"\"Trapped Chest\""}