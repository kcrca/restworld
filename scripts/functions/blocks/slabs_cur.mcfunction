scoreboard players set slabs max 2
execute unless score slabs funcs matches 0..1 run scoreboard players operation slabs funcs %= slabs max

execute if score slabs funcs matches 0 run setblock ~0 ~3 ~0 minecraft:stone_slab
execute if score slabs funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Stone Slab\"",Text3:"\"\"",Text4:"\"\""}


execute if score slabs funcs matches 1 run setblock ~0 ~3 ~0 minecraft:petrified_oak_slab
execute if score slabs funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Petrified Oak Slab\"",Text3:"\"\"",Text4:"\"\""}