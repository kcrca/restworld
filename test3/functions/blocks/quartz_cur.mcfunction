scoreboard players set quartz max 4
execute unless score quartz funcs matches 0..3 run scoreboard players operation quartz funcs %= quartz max

execute if score quartz funcs matches 0 run setblock ~0 ~3 ~0 minecraft:quartz_block
execute if score quartz funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Quartz Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score quartz funcs matches 1 run setblock ~0 ~3 ~0 minecraft:smooth_quartz
execute if score quartz funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Smooth Quartz\"",Text3:"\"\"",Text4:"\"\""}


execute if score quartz funcs matches 2 run setblock ~0 ~3 ~0 minecraft:quartz_pillar
execute if score quartz funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Quartz Pillar\"",Text3:"\"\"",Text4:"\"\""}


execute if score quartz funcs matches 3 run setblock ~0 ~3 ~0 minecraft:chiseled_quartz_block
execute if score quartz funcs matches 3 run data merge block ~0 ~2 ~-1 {Text2:"\"Chiseled Quartz Block\"",Text3:"\"\"",Text4:"\"\""}
