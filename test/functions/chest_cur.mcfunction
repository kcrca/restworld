execute if score chest funcs matches 0 run setblock ~1 ~2 ~ minecraft:chest[facing=north,type=left]
execute if score chest funcs matches 0 run setblock ~0 ~2 ~ air


execute if score chest funcs matches 1 run setblock ~1 ~2 ~ air
execute if score chest funcs matches 1 run setblock ~0 ~2 ~ minecraft:trapped_chest[facing=north,type=right]