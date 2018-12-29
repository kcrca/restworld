execute unless score spawner funcs matches 0.. run function spawner_init
scoreboard players add spawner funcs 1
scoreboard players set spawner max 6
execute unless score spawner funcs matches 0..5 run scoreboard players operation spawner funcs %= spawner max

    execute if score spawner funcs matches 0 run setblock ~0 ~3 ~0 minecraft:air
execute if score spawner funcs matches 0 run setblock ~0 ~3 ~0 minecraft:spawner{SpawnData:{id:"minecraft:pig"}} destroy
execute if score spawner funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Pig Spawner\"",Text3:"\"\"",Text4:"\"\""}


    execute if score spawner funcs matches 1 run setblock ~0 ~3 ~0 minecraft:air
execute if score spawner funcs matches 1 run setblock ~0 ~3 ~0 minecraft:spawner{SpawnData:{id:"minecraft:zombie"}} destroy
execute if score spawner funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Zombie Spawner\"",Text3:"\"\"",Text4:"\"\""}


    execute if score spawner funcs matches 2 run setblock ~0 ~3 ~0 minecraft:air
execute if score spawner funcs matches 2 run setblock ~0 ~3 ~0 minecraft:spawner{SpawnData:{id:"minecraft:skeleton"}} destroy
execute if score spawner funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Skeleton Spawner\"",Text3:"\"\"",Text4:"\"\""}


    execute if score spawner funcs matches 3 run setblock ~0 ~3 ~0 minecraft:air
execute if score spawner funcs matches 3 run setblock ~0 ~3 ~0 minecraft:spawner{SpawnData:{id:"minecraft:spider"}} destroy
execute if score spawner funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Spider Spawner\"",Text3:"\"\"",Text4:"\"\""}


    execute if score spawner funcs matches 4 run setblock ~0 ~3 ~0 minecraft:air
execute if score spawner funcs matches 4 run setblock ~0 ~3 ~0 minecraft:spawner{SpawnData:{id:"minecraft:cave_spider"}} destroy
execute if score spawner funcs matches 4 run data merge block ~0 ~2 ~1 {Text2:"\"Cave Spider\"",Text3:"\"Spawner\"",Text4:"\"\""}


    execute if score spawner funcs matches 5 run setblock ~0 ~3 ~0 minecraft:air
execute if score spawner funcs matches 5 run setblock ~0 ~3 ~0 minecraft:spawner{SpawnData:{id:"minecraft:blaze"}} destroy
execute if score spawner funcs matches 5 run data merge block ~0 ~2 ~1 {Text2:"\"Blaze Spawner\"",Text3:"\"\"",Text4:"\"\""}
