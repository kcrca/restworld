scoreboard players set pumpkin max 3
execute unless score pumpkin funcs matches 0..2 run scoreboard players operation pumpkin funcs %= pumpkin max

execute if score pumpkin funcs matches 0 run setblock ~0 ~3 ~0 minecraft:pumpkin
execute if score pumpkin funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Pumpkin\"",Text3:"\"\"",Text4:"\"\""}


execute if score pumpkin funcs matches 1 run setblock ~0 ~3 ~0 minecraft:carved_pumpkin[facing=south]
execute if score pumpkin funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Carved Pumpkin\"",Text3:"\"\"",Text4:"\"\""}


execute if score pumpkin funcs matches 2 run setblock ~0 ~3 ~0 minecraft:jack_o_lantern[facing=south]
execute if score pumpkin funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Jack O Lantern\"",Text3:"\"\"",Text4:"\"\""}
