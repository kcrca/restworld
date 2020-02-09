execute unless score lantern funcs matches 0.. run function lantern_init
scoreboard players add lantern funcs 1
scoreboard players set lantern max 2
execute unless score lantern funcs matches 0..1 run scoreboard players operation lantern funcs %= lantern max

execute if score lantern funcs matches 0 run setblock ~ ~3 ~ lantern[hanging=false]
execute if score lantern funcs matches 0 run setblock ~ ~4 ~ air
execute if score lantern funcs matches 0 run data merge block ~ ~2 ~-1 {Text2:"\"\""}
execute if score lantern funcs matches 1 run setblock ~ ~3 ~ lantern[hanging=true]
execute if score lantern funcs matches 1 run setblock ~ ~4 ~ stone_slab
execute if score lantern funcs matches 1 run data merge block ~ ~2 ~-1 {Text2:"\"Hanging\""}


execute if score lantern funcs matches 0 run setblock ~ ~3 ~ lantern[hanging=false]
execute if score lantern funcs matches 0 run setblock ~ ~4 ~ air
execute if score lantern funcs matches 0 run data merge block ~ ~2 ~-1 {Text2:"\"\""}
execute if score lantern funcs matches 1 run setblock ~ ~3 ~ lantern[hanging=true]
execute if score lantern funcs matches 1 run setblock ~ ~4 ~ stone_slab
execute if score lantern funcs matches 1 run data merge block ~ ~2 ~-1 {Text2:"\"Hanging\""}
