scoreboard players set ore_blocks max 7
execute unless score ore_blocks funcs matches 0..6 run scoreboard players operation ore_blocks funcs %= ore_blocks max

execute if score ore_blocks funcs matches 0 run setblock ~0 ~3 ~0 minecraft:coal_ore
execute if score ore_blocks funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Coal Ore\"",Text3:"\"\"",Text4:"\"\""}

execute if score ore_blocks funcs matches 0 run setblock ~0 ~3 ~3 minecraft:coal_block
execute if score ore_blocks funcs matches 0 run data merge block ~0 ~2 ~2 {Text2:"\"Coal Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score ore_blocks funcs matches 1 run setblock ~0 ~3 ~0 minecraft:iron_ore
execute if score ore_blocks funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Iron Ore\"",Text3:"\"\"",Text4:"\"\""}

execute if score ore_blocks funcs matches 1 run setblock ~0 ~3 ~3 minecraft:iron_block
execute if score ore_blocks funcs matches 1 run data merge block ~0 ~2 ~2 {Text2:"\"Iron Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score ore_blocks funcs matches 2 run setblock ~0 ~3 ~0 minecraft:gold_ore
execute if score ore_blocks funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Gold Ore\"",Text3:"\"\"",Text4:"\"\""}

execute if score ore_blocks funcs matches 2 run setblock ~0 ~3 ~3 minecraft:gold_block
execute if score ore_blocks funcs matches 2 run data merge block ~0 ~2 ~2 {Text2:"\"Gold Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score ore_blocks funcs matches 3 run setblock ~0 ~3 ~0 minecraft:diamond_ore
execute if score ore_blocks funcs matches 3 run data merge block ~0 ~2 ~-1 {Text2:"\"Diamond Ore\"",Text3:"\"\"",Text4:"\"\""}

execute if score ore_blocks funcs matches 3 run setblock ~0 ~3 ~3 minecraft:diamond_block
execute if score ore_blocks funcs matches 3 run data merge block ~0 ~2 ~2 {Text2:"\"Diamond Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score ore_blocks funcs matches 4 run setblock ~0 ~3 ~0 minecraft:lapis_ore
execute if score ore_blocks funcs matches 4 run data merge block ~0 ~2 ~-1 {Text2:"\"Lapis Ore\"",Text3:"\"\"",Text4:"\"\""}

execute if score ore_blocks funcs matches 4 run setblock ~0 ~3 ~3 minecraft:lapis_block
execute if score ore_blocks funcs matches 4 run data merge block ~0 ~2 ~2 {Text2:"\"Lapis Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score ore_blocks funcs matches 5 run setblock ~0 ~3 ~0 minecraft:emerald_ore
execute if score ore_blocks funcs matches 5 run data merge block ~0 ~2 ~-1 {Text2:"\"Emerald Ore\"",Text3:"\"\"",Text4:"\"\""}

execute if score ore_blocks funcs matches 5 run setblock ~0 ~3 ~3 minecraft:emerald_block
execute if score ore_blocks funcs matches 5 run data merge block ~0 ~2 ~2 {Text2:"\"Emerald Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score ore_blocks funcs matches 6 run setblock ~0 ~3 ~0 minecraft:redstone_ore
execute if score ore_blocks funcs matches 6 run data merge block ~0 ~2 ~-1 {Text2:"\"Redstone Ore\"",Text3:"\"\"",Text4:"\"\""}

execute if score ore_blocks funcs matches 6 run setblock ~0 ~3 ~3 minecraft:redstone_block
execute if score ore_blocks funcs matches 6 run data merge block ~0 ~2 ~2 {Text2:"\"Redstone Block\"",Text3:"\"\"",Text4:"\"\""}
