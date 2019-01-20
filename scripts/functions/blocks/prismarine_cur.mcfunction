scoreboard players set prismarine max 3
execute unless score prismarine funcs matches 0..2 run scoreboard players operation prismarine funcs %= prismarine max

execute if score prismarine funcs matches 0 run setblock ~0 ~3 ~0 minecraft:prismarine
execute if score prismarine funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Prismarine\"",Text3:"\"\"",Text4:"\"\""}


execute if score prismarine funcs matches 1 run setblock ~0 ~3 ~0 minecraft:prismarine_bricks
execute if score prismarine funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Prismarine Bricks\"",Text3:"\"\"",Text4:"\"\""}


execute if score prismarine funcs matches 2 run setblock ~0 ~3 ~0 minecraft:dark_prismarine
execute if score prismarine funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Dark Prismarine\"",Text3:"\"\"",Text4:"\"\""}
