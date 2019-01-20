scoreboard players set music max 2
execute unless score music funcs matches 0..1 run scoreboard players operation music funcs %= music max

execute if score music funcs matches 0 run setblock ~0 ~3 ~0 minecraft:note_block
execute if score music funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Note Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score music funcs matches 1 run setblock ~0 ~3 ~0 minecraft:jukebox
execute if score music funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Jukebox\"",Text3:"\"\"",Text4:"\"\""}
