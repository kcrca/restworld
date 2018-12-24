scoreboard players set dirt max 2
execute unless score dirt funcs matches 0..1 run scoreboard players operation dirt funcs %= dirt max

execute if score dirt funcs matches 0 run setblock ~0 ~3 ~0 minecraft:dirt
execute if score dirt funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Dirt\"",Text3:"\"\"",Text4:"\"\""}


execute if score dirt funcs matches 1 run setblock ~0 ~3 ~0 minecraft:coarse_dirt
execute if score dirt funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Coarse Dirt\"",Text3:"\"\"",Text4:"\"\""}
