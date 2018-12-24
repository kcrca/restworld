scoreboard players set frosted_ice max 5
execute unless score frosted_ice funcs matches 0..4 run scoreboard players operation frosted_ice funcs %= frosted_ice max

execute if score frosted_ice funcs matches 0 run setblock ~0 ~3 ~0 minecraft:water
execute if score frosted_ice funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Water\"",Text3:"\"\"",Text4:"\"\""}


execute if score frosted_ice funcs matches 1 run setblock ~0 ~3 ~0 minecraft:frosted_ice[age=0]
execute if score frosted_ice funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Frosted Ice\"",Text3:"\"\"",Text4:"\"\""}


execute if score frosted_ice funcs matches 2 run setblock ~0 ~3 ~0 minecraft:frosted_ice[age=1]
execute if score frosted_ice funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Frosted Ice\"",Text3:"\"\"",Text4:"\"\""}


execute if score frosted_ice funcs matches 3 run setblock ~0 ~3 ~0 minecraft:frosted_ice[age=2]
execute if score frosted_ice funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Frosted Ice\"",Text3:"\"\"",Text4:"\"\""}


execute if score frosted_ice funcs matches 4 run setblock ~0 ~3 ~0 minecraft:frosted_ice[age=3]
execute if score frosted_ice funcs matches 4 run data merge block ~0 ~2 ~1 {Text2:"\"Frosted Ice\"",Text3:"\"\"",Text4:"\"\""}



execute if score frosted_ice funcs matches 0 run setblock ~1 ~3 ~0 wall_sign[facing=east]
execute if score frosted_ice funcs matches 0 run setblock ~-1 ~3 ~0 wall_sign[facing=west]
execute if score frosted_ice funcs matches 0 run setblock ~0 ~3 ~1 wall_sign[facing=south]
execute if score frosted_ice funcs matches 0 run setblock ~0 ~3 ~-1 wall_sign[facing=north]
execute unless score frosted_ice funcs matches 0 run setblock ~1 ~3 ~0 air
execute unless score frosted_ice funcs matches 0 run setblock ~-1 ~3 ~0 air
execute unless score frosted_ice funcs matches 0 run setblock ~0 ~3 ~1 air
execute unless score frosted_ice funcs matches 0 run setblock ~0 ~3 ~-1 air
execute if score frosted_ice funcs matches 0 run data merge block ~0 ~2 ~1 {Text3:"\"\""}
execute if score frosted_ice funcs matches 1 run data merge block ~0 ~2 ~1 {Text3:"\"Age: 1\""}
execute if score frosted_ice funcs matches 2 run data merge block ~0 ~2 ~1 {Text3:"\"Age: 2\""}
execute if score frosted_ice funcs matches 3 run data merge block ~0 ~2 ~1 {Text3:"\"Age: 3\""}
execute if score frosted_ice funcs matches 4 run data merge block ~0 ~2 ~1 {Text3:"\"Age: 4\""}
