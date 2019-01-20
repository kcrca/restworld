execute unless score frosted_ice funcs matches 0.. run function frosted_ice_init
scoreboard players add frosted_ice funcs 1
scoreboard players set frosted_ice max 4
execute unless score frosted_ice funcs matches 0..3 run scoreboard players operation frosted_ice funcs %= frosted_ice max

execute if score frosted_ice funcs matches 0 run setblock ~0 ~3 ~0 minecraft:frosted_ice[age=0]
execute if score frosted_ice funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Frosted Ice\"",Text3:"\"\"",Text4:"\"\""}


execute if score frosted_ice funcs matches 1 run setblock ~0 ~3 ~0 minecraft:frosted_ice[age=1]
execute if score frosted_ice funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Frosted Ice\"",Text3:"\"\"",Text4:"\"\""}


execute if score frosted_ice funcs matches 2 run setblock ~0 ~3 ~0 minecraft:frosted_ice[age=2]
execute if score frosted_ice funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Frosted Ice\"",Text3:"\"\"",Text4:"\"\""}


execute if score frosted_ice funcs matches 3 run setblock ~0 ~3 ~0 minecraft:frosted_ice[age=3]
execute if score frosted_ice funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Frosted Ice\"",Text3:"\"\"",Text4:"\"\""}



execute if score frosted_ice funcs matches 0 run data merge block ~0 ~2 ~1 {Text3:"\"Age: 1\""}
execute if score frosted_ice funcs matches 1 run data merge block ~0 ~2 ~1 {Text3:"\"Age: 2\""}
execute if score frosted_ice funcs matches 2 run data merge block ~0 ~2 ~1 {Text3:"\"Age: 3\""}
execute if score frosted_ice funcs matches 3 run data merge block ~0 ~2 ~1 {Text3:"\"Age: 4\""}
