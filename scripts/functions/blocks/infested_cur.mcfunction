scoreboard players set infested max 6
execute unless score infested funcs matches 0..5 run scoreboard players operation infested funcs %= infested max

execute if score infested funcs matches 0 run setblock ~0 ~3 ~0 minecraft:infested_chiseled_stone_bricks
execute if score infested funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Infested\"",Text3:"\"Chiseled Stone\"",Text4:"\"Bricks\""}


execute if score infested funcs matches 1 run setblock ~0 ~3 ~0 minecraft:infested_cobblestone
execute if score infested funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Infested\"",Text3:"\"Cobblestone\"",Text4:"\"\""}


execute if score infested funcs matches 2 run setblock ~0 ~3 ~0 minecraft:infested_cracked_stone_bricks
execute if score infested funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Infested\"",Text3:"\"Cracked Stone\"",Text4:"\"Bricks\""}


execute if score infested funcs matches 3 run setblock ~0 ~3 ~0 minecraft:infested_mossy_stone_bricks
execute if score infested funcs matches 3 run data merge block ~0 ~2 ~-1 {Text2:"\"Infested\"",Text3:"\"Mossy Stone\"",Text4:"\"Bricks\""}


execute if score infested funcs matches 4 run setblock ~0 ~3 ~0 minecraft:infested_stone
execute if score infested funcs matches 4 run data merge block ~0 ~2 ~-1 {Text2:"\"Infested\"",Text3:"\"Stone\"",Text4:"\"\""}


execute if score infested funcs matches 5 run setblock ~0 ~3 ~0 minecraft:infested_stone_bricks
execute if score infested funcs matches 5 run data merge block ~0 ~2 ~-1 {Text2:"\"Infested\"",Text3:"\"Stone Bricks\"",Text4:"\"\""}
