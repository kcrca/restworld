scoreboard players set sandstone max 4
execute unless score sandstone funcs matches 0..3 run scoreboard players operation sandstone funcs %= sandstone max

execute if score sandstone funcs matches 0 run setblock ~0 ~3 ~0 minecraft:red_sandstone
execute if score sandstone funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Red Sandstone\"",Text3:"\"\"",Text4:"\"\""}

execute if score sandstone funcs matches 0 run setblock ~3 ~3 ~0 minecraft:sandstone
execute if score sandstone funcs matches 0 run data merge block ~3 ~2 ~1 {Text2:"\"Sandstone\"",Text3:"\"\"",Text4:"\"\""}


execute if score sandstone funcs matches 1 run setblock ~0 ~3 ~0 minecraft:smooth_red_sandstone
execute if score sandstone funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Smooth Red Sandstone\"",Text3:"\"\"",Text4:"\"\""}

execute if score sandstone funcs matches 1 run setblock ~3 ~3 ~0 minecraft:smooth_sandstone
execute if score sandstone funcs matches 1 run data merge block ~3 ~2 ~1 {Text2:"\"Smooth Sandstone\"",Text3:"\"\"",Text4:"\"\""}


execute if score sandstone funcs matches 2 run setblock ~0 ~3 ~0 minecraft:cut_red_sandstone
execute if score sandstone funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Cut Red Sandstone\"",Text3:"\"\"",Text4:"\"\""}

execute if score sandstone funcs matches 2 run setblock ~3 ~3 ~0 minecraft:cut_sandstone
execute if score sandstone funcs matches 2 run data merge block ~3 ~2 ~1 {Text2:"\"Cut Sandstone\"",Text3:"\"\"",Text4:"\"\""}


execute if score sandstone funcs matches 3 run setblock ~0 ~3 ~0 minecraft:chiseled_red_sandstone
execute if score sandstone funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Chiseled Red Sandstone\"",Text3:"\"\"",Text4:"\"\""}

execute if score sandstone funcs matches 3 run setblock ~3 ~3 ~0 minecraft:chiseled_sandstone
execute if score sandstone funcs matches 3 run data merge block ~3 ~2 ~1 {Text2:"\"Chiseled Sandstone\"",Text3:"\"\"",Text4:"\"\""}
