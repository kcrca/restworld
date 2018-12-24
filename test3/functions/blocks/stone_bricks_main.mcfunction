execute unless score stone_bricks funcs matches 0.. run function stone_bricks_init
scoreboard players add stone_bricks funcs 1
scoreboard players set stone_bricks max 4
execute unless score stone_bricks funcs matches 0..3 run scoreboard players operation stone_bricks funcs %= stone_bricks max

execute if score stone_bricks funcs matches 0 run setblock ~0 ~3 ~0 minecraft:stone_bricks
execute if score stone_bricks funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Stone Bricks\"",Text3:"\"\"",Text4:"\"\""}


execute if score stone_bricks funcs matches 1 run setblock ~0 ~3 ~0 minecraft:mossy_stone_bricks
execute if score stone_bricks funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Mossy\"",Text3:"\"Stone Bricks\"",Text4:"\"\""}


execute if score stone_bricks funcs matches 2 run setblock ~0 ~3 ~0 minecraft:cracked_stone_bricks
execute if score stone_bricks funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Cracked\"",Text3:"\"Stone Bricks\"",Text4:"\"\""}


execute if score stone_bricks funcs matches 3 run setblock ~0 ~3 ~0 minecraft:chiseled_stone_bricks
execute if score stone_bricks funcs matches 3 run data merge block ~0 ~2 ~-1 {Text2:"\"Chiseled\"",Text3:"\"Stone Bricks\"",Text4:"\"\""}
