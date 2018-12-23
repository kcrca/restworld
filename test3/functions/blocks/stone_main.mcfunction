execute unless score stone funcs matches 0.. run function stone_init
scoreboard players add stone funcs 1
scoreboard players set stone max 4
execute unless score stone funcs matches 0..3 run scoreboard players operation stone funcs %= stone max
execute if score stone funcs matches 0 run setblock ~0 ~3 ~0 minecraft:stone
execute if score stone funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Stone\""}
execute if score stone funcs matches 0 run setblock ~0 ~3 ~3 minecraft:smooth_stone
execute if score stone funcs matches 0 run data merge block ~0 ~2 ~2 {Text2:"\"Smooth Stone\""}

execute if score stone funcs matches 1 run setblock ~0 ~3 ~0 minecraft:andesite
execute if score stone funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Andesite\""}
execute if score stone funcs matches 1 run setblock ~0 ~3 ~3 minecraft:polished_andesite
execute if score stone funcs matches 1 run data merge block ~0 ~2 ~2 {Text2:"\"Polished Andesite\""}

execute if score stone funcs matches 2 run setblock ~0 ~3 ~0 minecraft:diorite
execute if score stone funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Diorite\""}
execute if score stone funcs matches 2 run setblock ~0 ~3 ~3 minecraft:polished_diorite
execute if score stone funcs matches 2 run data merge block ~0 ~2 ~2 {Text2:"\"Polished Diorite\""}

execute if score stone funcs matches 3 run setblock ~0 ~3 ~0 minecraft:granite
execute if score stone funcs matches 3 run data merge block ~0 ~2 ~-1 {Text2:"\"Granite\""}
execute if score stone funcs matches 3 run setblock ~0 ~3 ~3 minecraft:polished_granite
execute if score stone funcs matches 3 run data merge block ~0 ~2 ~2 {Text2:"\"Polished Granite\""}
