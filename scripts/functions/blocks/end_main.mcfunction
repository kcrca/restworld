execute unless score end funcs matches 0.. run function end_init
scoreboard players add end funcs 1
scoreboard players set end max 2
execute unless score end funcs matches 0..1 run scoreboard players operation end funcs %= end max

execute if score end funcs matches 0 run setblock ~0 ~3 ~0 minecraft:end_stone
execute if score end funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"End Stone\"",Text3:"\"\"",Text4:"\"\""}


execute if score end funcs matches 1 run setblock ~0 ~3 ~0 minecraft:end_stone_bricks
execute if score end funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"End Stone Bricks\"",Text3:"\"\"",Text4:"\"\""}
