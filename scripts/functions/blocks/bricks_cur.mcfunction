scoreboard players set bricks max 4
execute unless score bricks funcs matches 0..3 run scoreboard players operation bricks funcs %= bricks max

execute if score bricks funcs matches 0 run setblock ~0 ~3 ~0 minecraft:bricks
execute if score bricks funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Bricks\"",Text3:"\"\"",Text4:"\"\""}


execute if score bricks funcs matches 1 run setblock ~0 ~3 ~0 minecraft:nether_bricks
execute if score bricks funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Nether Bricks\"",Text3:"\"\"",Text4:"\"\""}


execute if score bricks funcs matches 2 run setblock ~0 ~3 ~0 minecraft:red_nether_bricks
execute if score bricks funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Red Nether\"",Text3:"\"Bricks\"",Text4:"\"\""}


execute if score bricks funcs matches 3 run setblock ~0 ~3 ~0 minecraft:end_stone_bricks
execute if score bricks funcs matches 3 run data merge block ~0 ~2 ~-1 {Text2:"\"End Stone\"",Text3:"\"Bricks\"",Text4:"\"\""}
