scoreboard players set cake max 12
execute unless score cake funcs matches 0..11 run scoreboard players operation cake funcs %= cake max

execute if score cake funcs matches 0 run setblock ~ ~3 ~ minecraft:cake[bites=0]
execute if score cake funcs matches 0 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 0\""}

execute if score cake funcs matches 1 run setblock ~ ~3 ~ minecraft:cake[bites=1]
execute if score cake funcs matches 1 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 1\""}

execute if score cake funcs matches 2 run setblock ~ ~3 ~ minecraft:cake[bites=2]
execute if score cake funcs matches 2 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 2\""}

execute if score cake funcs matches 3 run setblock ~ ~3 ~ minecraft:cake[bites=3]
execute if score cake funcs matches 3 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 3\""}

execute if score cake funcs matches 4 run setblock ~ ~3 ~ minecraft:cake[bites=4]
execute if score cake funcs matches 4 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 4\""}

execute if score cake funcs matches 5 run setblock ~ ~3 ~ minecraft:cake[bites=5]
execute if score cake funcs matches 5 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 5\""}

execute if score cake funcs matches 6 run setblock ~ ~3 ~ minecraft:cake[bites=6]
execute if score cake funcs matches 6 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 6\""}

execute if score cake funcs matches 7 run setblock ~ ~3 ~ minecraft:cake[bites=5]
execute if score cake funcs matches 7 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 5\""}

execute if score cake funcs matches 8 run setblock ~ ~3 ~ minecraft:cake[bites=4]
execute if score cake funcs matches 8 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 4\""}

execute if score cake funcs matches 9 run setblock ~ ~3 ~ minecraft:cake[bites=3]
execute if score cake funcs matches 9 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 3\""}

execute if score cake funcs matches 10 run setblock ~ ~3 ~ minecraft:cake[bites=2]
execute if score cake funcs matches 10 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 2\""}

execute if score cake funcs matches 11 run setblock ~ ~3 ~ minecraft:cake[bites=1]
execute if score cake funcs matches 11 run data merge block ~ ~2 ~-1 {Text3:"\"Bites: 1\""}
