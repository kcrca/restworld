scoreboard players set skulls max 5
execute unless score skulls funcs matches 0..4 run scoreboard players operation skulls funcs %= skulls max

execute if score skulls funcs matches 0 run setblock ~ ~3 ~ minecraft:skeleton_skull
execute if score skulls funcs matches 0 run setblock ~ ~3 ~1 minecraft:skeleton_wall_skull
execute if score skulls funcs matches 0 run data merge block ~ ~2 ~-1 {Text2:"\"Skeleton Skull\""}
execute if score skulls funcs matches 0 run data merge block ~ ~2 ~-1 {Text3:"\"\""}


execute if score skulls funcs matches 1 run setblock ~ ~3 ~ minecraft:wither_skeleton_skull
execute if score skulls funcs matches 1 run setblock ~ ~3 ~1 minecraft:wither_skeleton_wall_skull
execute if score skulls funcs matches 1 run data merge block ~ ~2 ~-1 {Text2:"\"Wither Skeleton Skull\""}
execute if score skulls funcs matches 1 run data merge block ~ ~2 ~-1 {Text3:"\"Skull\""}


execute if score skulls funcs matches 2 run setblock ~ ~3 ~ minecraft:player_head
execute if score skulls funcs matches 2 run setblock ~ ~3 ~1 minecraft:player_wall_head
execute if score skulls funcs matches 2 run data merge block ~ ~2 ~-1 {Text2:"\"Player Head\""}
execute if score skulls funcs matches 2 run data merge block ~ ~2 ~-1 {Text3:"\"\""}


execute if score skulls funcs matches 3 run setblock ~ ~3 ~ minecraft:zombie_head
execute if score skulls funcs matches 3 run setblock ~ ~3 ~1 minecraft:zombie_wall_head
execute if score skulls funcs matches 3 run data merge block ~ ~2 ~-1 {Text2:"\"Zombie Head\""}
execute if score skulls funcs matches 3 run data merge block ~ ~2 ~-1 {Text3:"\"\""}


execute if score skulls funcs matches 4 run setblock ~ ~3 ~ minecraft:creeper_head
execute if score skulls funcs matches 4 run setblock ~ ~3 ~1 minecraft:creeper_wall_head
execute if score skulls funcs matches 4 run data merge block ~ ~2 ~-1 {Text2:"\"Creeper Head\""}
execute if score skulls funcs matches 4 run data merge block ~ ~2 ~-1 {Text3:"\"\""}
