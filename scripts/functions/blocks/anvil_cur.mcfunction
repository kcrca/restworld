scoreboard players set anvil max 3
execute unless score anvil funcs matches 0..2 run scoreboard players operation anvil funcs %= anvil max

execute if score anvil funcs matches 0 run setblock ~0 ~3 ~0 minecraft:anvil[facing=west]
execute if score anvil funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Anvil[facing=west]\"",Text3:"\"\"",Text4:"\"\""}


execute if score anvil funcs matches 1 run setblock ~0 ~3 ~0 minecraft:chipped_anvil[facing=west]
execute if score anvil funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Chipped Anvil[facing=west]\"",Text3:"\"\"",Text4:"\"\""}


execute if score anvil funcs matches 2 run setblock ~0 ~3 ~0 minecraft:damaged_anvil[facing=west]
execute if score anvil funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Damaged Anvil[facing=west]\"",Text3:"\"\"",Text4:"\"\""}
