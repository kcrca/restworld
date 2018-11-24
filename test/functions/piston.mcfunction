



execute unless score piston funcs matches 0.. run function piston_init
scoreboard players add piston funcs 1
execute unless score piston funcs matches 0..1 run scoreboard players set piston funcs 0
execute if score piston funcs matches 0 run setblock ~ ~3 ~ minecraft:piston[facing=south]
execute if score piston funcs matches 0 run data merge block ~ ~2 ~1 {Text2:"\"Piston\""}
execute if score piston funcs matches 0 run setblock ~-1 ~3 ~1 minecraft:piston_head[facing=south]
execute if score piston funcs matches 0 run setblock ~-1 ~3 ~0 minecraft:piston[facing=south,extended=true]

execute if score piston funcs matches 1 run setblock ~ ~3 ~ minecraft:sticky_piston[facing=south]
execute if score piston funcs matches 1 run data merge block ~ ~2 ~1 {Text2:"\"Sticky Piston\""}
execute if score piston funcs matches 1 run setblock ~-1 ~3 ~1 minecraft:piston_head[facing=south,type=sticky]
execute if score piston funcs matches 1 run setblock ~-1 ~3 ~0 minecraft:sticky_piston[facing=south,extended=true]


