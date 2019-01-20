execute unless score ice funcs matches 0.. run function ice_init
scoreboard players add ice funcs 1
scoreboard players set ice max 3
execute unless score ice funcs matches 0..2 run scoreboard players operation ice funcs %= ice max

execute if score ice funcs matches 0 run setblock ~0 ~3 ~0 minecraft:ice
execute if score ice funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Ice\"",Text3:"\"\"",Text4:"\"\""}


execute if score ice funcs matches 1 run setblock ~0 ~3 ~0 minecraft:packed_ice
execute if score ice funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Packed Ice\"",Text3:"\"\"",Text4:"\"\""}


execute if score ice funcs matches 2 run setblock ~0 ~3 ~0 minecraft:blue_ice
execute if score ice funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Blue Ice\"",Text3:"\"\"",Text4:"\"\""}
