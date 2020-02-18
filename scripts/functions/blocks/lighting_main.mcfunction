execute unless score lighting funcs matches 0.. run function lighting_init
scoreboard players add lighting funcs 1
scoreboard players set lighting max 2
execute unless score lighting funcs matches 0..1 run scoreboard players operation lighting funcs %= lighting max

execute if score lighting funcs matches 0 run setblock ~0 ~3 ~0 minecraft:glowstone
execute if score lighting funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Glowstone\"",Text3:"\"\"",Text4:"\"\""}


execute if score lighting funcs matches 1 run setblock ~0 ~3 ~0 minecraft:sea_lantern
execute if score lighting funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Sea Lantern\"",Text3:"\"\"",Text4:"\"\""}
