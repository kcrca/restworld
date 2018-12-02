execute if score topped_blocks funcs matches 0 run setblock ~ ~3 ~ minecraft:grass_path
execute if score topped_blocks funcs matches 0 run data merge block ~1 ~2 ~ {Text1:"\"\"",Text2:"\"Grass Path\""}



execute if score topped_blocks funcs matches 1 run setblock ~ ~3 ~ minecraft:grass_block
execute if score topped_blocks funcs matches 1 run data merge block ~1 ~2 ~ {Text1:"\"\"",Text2:"\"Grass Block\""}



execute if score topped_blocks funcs matches 2 run setblock ~ ~3 ~ minecraft:grass_block[snowy=true]
execute if score topped_blocks funcs matches 2 run data merge block ~1 ~2 ~ {Text1:"\"Snowy\"",Text2:"\"Grass Block\""}



execute if score topped_blocks funcs matches 3 run setblock ~ ~3 ~ minecraft:mycelium
execute if score topped_blocks funcs matches 3 run data merge block ~1 ~2 ~ {Text1:"\"\"",Text2:"\"Mycelium\""}



execute if score topped_blocks funcs matches 4 run setblock ~ ~3 ~ minecraft:podzol
execute if score topped_blocks funcs matches 4 run data merge block ~1 ~2 ~ {Text1:"\"\"",Text2:"\"Podzol\""}