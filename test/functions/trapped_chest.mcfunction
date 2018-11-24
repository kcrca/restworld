



execute unless score trapped_chest funcs matches 0.. run function trapped_chest_init
scoreboard players add trapped_chest funcs 1
execute unless score trapped_chest funcs matches 0..1 run scoreboard players set trapped_chest funcs 0

execute if score trapped_chest funcs matches 0 run setblock ~ ~3 ~ minecraft:chest[facing=south]
execute if score trapped_chest funcs matches 0 run data merge block ~ ~2 ~1 {Text2:"\"Chest\""}


execute if score trapped_chest funcs matches 1 run setblock ~ ~3 ~ minecraft:trapped_chest[facing=south]
execute if score trapped_chest funcs matches 1 run data merge block ~ ~2 ~1 {Text2:"\"Trapped Chest\""}


