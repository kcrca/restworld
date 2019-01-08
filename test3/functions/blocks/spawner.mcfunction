execute unless score spawner funcs matches 0.. run function spawner_init
scoreboard players add spawner funcs 1
scoreboard players set spawner max 6
execute unless score spawner funcs matches 0..5 run scoreboard players operation spawner funcs %= spawner max

execute if score spawner funcs matches 0 run data merge block ~0 ~3 ~0 {SpawnData:{id:"minecraft:pig"}}
execute if score spawner funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Pig\""}


execute if score spawner funcs matches 1 run data merge block ~0 ~3 ~0 {SpawnData:{id:"minecraft:zombie"}}
execute if score spawner funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Zombie\""}


execute if score spawner funcs matches 2 run data merge block ~0 ~3 ~0 {SpawnData:{id:"minecraft:skeleton"}}
execute if score spawner funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Skeleton\""}


execute if score spawner funcs matches 3 run data merge block ~0 ~3 ~0 {SpawnData:{id:"minecraft:spider"}}
execute if score spawner funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Spider\""}


execute if score spawner funcs matches 4 run data merge block ~0 ~3 ~0 {SpawnData:{id:"minecraft:cave_spider"}}
execute if score spawner funcs matches 4 run data merge block ~0 ~2 ~1 {Text2:"\"Cave Spider\""}


execute if score spawner funcs matches 5 run data merge block ~0 ~3 ~0 {SpawnData:{id:"minecraft:blaze"}}
execute if score spawner funcs matches 5 run data merge block ~0 ~2 ~1 {Text2:"\"Blaze\""}
