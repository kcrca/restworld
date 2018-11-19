



execute unless score chest funcs matches 0.. run function chest_init
scoreboard players add chest funcs 1
execute unless score chest funcs matches 0..1 run scoreboard players set chest funcs 0



execute if score chest funcs matches 0 run setblock ~1 ~2 ~ minecraft:chest[facing=north,type=left]
execute if score chest funcs matches 0 run setblock ~0 ~2 ~ air


execute if score chest funcs matches 1 run setblock ~1 ~2 ~ air
execute if score chest funcs matches 1 run setblock ~0 ~2 ~ minecraft:trapped_chest[facing=north,type=right] 


