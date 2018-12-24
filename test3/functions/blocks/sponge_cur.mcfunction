scoreboard players set sponge max 2
execute unless score sponge funcs matches 0..1 run scoreboard players operation sponge funcs %= sponge max

execute if score sponge funcs matches 0 run setblock ~0 ~3 ~0 minecraft:sponge
execute if score sponge funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Sponge\"",Text3:"\"\"",Text4:"\"\""}


execute if score sponge funcs matches 1 run setblock ~0 ~3 ~0 minecraft:wet_sponge
execute if score sponge funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Wet Sponge\"",Text3:"\"\"",Text4:"\"\""}
