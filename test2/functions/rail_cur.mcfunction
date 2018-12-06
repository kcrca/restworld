execute if score rail funcs matches 0 run fill ~1 ~0 ~-1 ~1 ~0 ~-2 minecraft:air
execute if score rail funcs matches 0 run fill ~1 ~2 ~-1 ~2 ~2 ~-1 minecraft:rail[shape=east_west]
execute if score rail funcs matches 0 run setblock ~3 ~3 ~-1 minecraft:rail[shape=east_west]
execute if score rail funcs matches 0 run setblock ~1 ~2 ~-2 minecraft:rail[shape=north_south]
execute if score rail funcs matches 0 run data merge block ~2 ~2 ~-2 {Text2:"\"Rail\"",Text3:"\"\""}

execute if score rail funcs matches 1 run fill ~1 ~0 ~-1 ~1 ~0 ~-2 minecraft:air
execute if score rail funcs matches 1 run fill ~1 ~2 ~-1 ~2 ~2 ~-1 minecraft:powered_rail[shape=east_west]
execute if score rail funcs matches 1 run setblock ~3 ~3 ~-1 minecraft:powered_rail[shape=east_west]
execute if score rail funcs matches 1 run setblock ~1 ~2 ~-2 minecraft:powered_rail[shape=north_south]
execute if score rail funcs matches 1 run data merge block ~2 ~2 ~-2 {Text2:"\"Powered Rail\"",Text3:"\"\""}

execute if score rail funcs matches 2 run data merge block ~2 ~2 ~-2 {Text3:"\"(Powered)\""}
execute if score rail funcs matches 2 run fill ~1 ~0 ~-1 ~1 ~0 ~-2 minecraft:redstone_torch

execute if score rail funcs matches 3 run fill ~1 ~0 ~-1 ~1 ~0 ~-2 minecraft:air
execute if score rail funcs matches 3 run fill ~1 ~2 ~-1 ~2 ~2 ~-1 minecraft:detector_rail[shape=east_west]
execute if score rail funcs matches 3 run setblock ~3 ~3 ~-1 minecraft:detector_rail[shape=east_west]
execute if score rail funcs matches 3 run setblock ~1 ~2 ~-2 minecraft:detector_rail[shape=north_south]
execute if score rail funcs matches 3 run data merge block ~2 ~2 ~-2 {Text2:"\"Detector Rail\"",Text3:"\"\""}

execute if score rail funcs matches 4 run data merge block ~2 ~2 ~-2 {Text3:"\"(Powered)\""}
execute if score rail funcs matches 4 run summon minecart ~2 ~2 ~-1 {Tags:[trigger_minecart]}
execute if score rail funcs matches 4 run summon minecart ~1 ~2 ~-1 {Tags:[trigger_minecart]}
execute if score rail funcs matches 4 run summon minecart ~3 ~3 ~-1 {Tags:[trigger_minecart]}
execute if score rail funcs matches 4 run summon minecart ~1 ~2 ~-2 {Tags:[trigger_minecart]}
execute if score rail funcs matches 4 run setblock ~0 ~0 ~-1 redstone_block

execute if score rail funcs matches 5 run fill ~1 ~0 ~-1 ~1 ~0 ~-2 minecraft:air
execute if score rail funcs matches 5 run fill ~1 ~2 ~-1 ~2 ~2 ~-1 minecraft:activator_rail[shape=east_west]
execute if score rail funcs matches 5 run setblock ~3 ~3 ~-1 minecraft:activator_rail[shape=east_west]
execute if score rail funcs matches 5 run setblock ~1 ~2 ~-2 minecraft:activator_rail[shape=north_south]
execute if score rail funcs matches 5 run data merge block ~2 ~2 ~-2 {Text2:"\"Activator Rail\"",Text3:"\"\""}

execute if score rail funcs matches 6 run data merge block ~2 ~2 ~-2 {Text3:"\"(Powered)\""}
execute if score rail funcs matches 6 run fill ~1 ~0 ~-1 ~1 ~0 ~-2 minecraft:redstone_torch