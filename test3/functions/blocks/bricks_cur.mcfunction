scoreboard players set bricks max 3
execute unless score bricks funcs matches 0..2 run scoreboard players operation bricks funcs %= bricks max

execute if score bricks funcs matches 0 run setblock ~0 ~3 ~0 minecraft:bricks
execute if score bricks funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Bricks\"",Text3:"\"\"",Text4:"\"\""}


execute if score bricks funcs matches 1 run setblock ~0 ~3 ~0 minecraft:nether_bricks
execute if score bricks funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Nether Bricks\"",Text3:"\"\"",Text4:"\"\""}


execute if score bricks funcs matches 2 run setblock ~0 ~3 ~0 minecraft:red_nether_bricks
execute if score bricks funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Red Nether Bricks\"",Text3:"\"\"",Text4:"\"\""}
