scoreboard players set piston max 2
execute unless score piston funcs matches 0..1 run scoreboard players operation piston funcs %= piston max
execute if score piston funcs matches 0 run setblock ~0 ~2 ~0 minecraft:piston[facing=west]
execute if score piston funcs matches 0 run setblock ~0 ~2 ~1 minecraft:piston[facing=west,extended=true]
execute if score piston funcs matches 0 run setblock ~-1 ~2 ~1 piston_head[facing=west,type=normal]
execute if score piston funcs matches 0 run data merge block ~ ~3 ~ {Text2:"\"Piston\""}

execute if score piston funcs matches 1 run setblock ~0 ~2 ~0 minecraft:sticky_piston[facing=west]
execute if score piston funcs matches 1 run setblock ~0 ~2 ~1 minecraft:sticky_piston[facing=west,extended=true]
execute if score piston funcs matches 1 run setblock ~-1 ~2 ~1 piston_head[facing=west,type=sticky]
execute if score piston funcs matches 1 run data merge block ~ ~3 ~ {Text2:"\"Sticky Piston\""}
