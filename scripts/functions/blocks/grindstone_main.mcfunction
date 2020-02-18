execute unless score grindstone funcs matches 0.. run function grindstone_init
scoreboard players add grindstone funcs 1
scoreboard players set grindstone max 3
execute unless score grindstone funcs matches 0..2 run scoreboard players operation grindstone funcs %= grindstone max

execute if score grindstone funcs matches 0 run setblock ~ ~3 ~ grindstone[face=floor]
execute if score grindstone funcs matches 0 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Face Floor\"",Text2:"\"Grindstone\""}


execute if score grindstone funcs matches 1 run setblock ~ ~3 ~ grindstone[face=wall]
execute if score grindstone funcs matches 1 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Face Wall\"",Text2:"\"Grindstone\""}


execute if score grindstone funcs matches 2 run setblock ~ ~3 ~ grindstone[face=ceiling]
execute if score grindstone funcs matches 2 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Face Ceiling\"",Text2:"\"Grindstone\""}
