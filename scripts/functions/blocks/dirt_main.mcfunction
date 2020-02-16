execute unless score dirt funcs matches 0.. run function dirt_init
scoreboard players add dirt funcs 1
scoreboard players set dirt max 3
execute unless score dirt funcs matches 0..2 run scoreboard players operation dirt funcs %= dirt max

execute if score dirt funcs matches 0 run setblock ~0 ~3 ~0 minecraft:dirt
execute if score dirt funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Dirt\"",Text3:"\"\"",Text4:"\"\""}


execute if score dirt funcs matches 1 run setblock ~0 ~3 ~0 minecraft:coarse_dirt
execute if score dirt funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Coarse Dirt\"",Text3:"\"\"",Text4:"\"\""}


execute if score dirt funcs matches 2 run setblock ~0 ~3 ~0 minecraft:clay
execute if score dirt funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Clay\"",Text3:"\"\"",Text4:"\"\""}
