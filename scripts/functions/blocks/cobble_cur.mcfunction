scoreboard players set cobble max 2
execute unless score cobble funcs matches 0..1 run scoreboard players operation cobble funcs %= cobble max

execute if score cobble funcs matches 0 run setblock ~0 ~3 ~0 minecraft:cobblestone
execute if score cobble funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Cobblestone\"",Text3:"\"\"",Text4:"\"\""}


execute if score cobble funcs matches 1 run setblock ~0 ~3 ~0 minecraft:mossy_cobblestone
execute if score cobble funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Mossy\"",Text3:"\"Cobblestone\"",Text4:"\"\""}
