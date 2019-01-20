execute unless score soil funcs matches 0.. run function soil_init
scoreboard players add soil funcs 1
scoreboard players set soil max 4
execute unless score soil funcs matches 0..3 run scoreboard players operation soil funcs %= soil max

execute if score soil funcs matches 0 run setblock ~0 ~3 ~0 minecraft:grass_block
execute if score soil funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Grass Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score soil funcs matches 1 run setblock ~0 ~3 ~0 minecraft:podzol
execute if score soil funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Podzol\"",Text3:"\"\"",Text4:"\"\""}


execute if score soil funcs matches 2 run setblock ~0 ~3 ~0 minecraft:mycelium
execute if score soil funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Mycelium\"",Text3:"\"\"",Text4:"\"\""}


execute if score soil funcs matches 3 run setblock ~0 ~3 ~0 minecraft:grass_path
execute if score soil funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Grass Path\"",Text3:"\"\"",Text4:"\"\""}
