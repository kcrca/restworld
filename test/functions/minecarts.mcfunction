



tp @e[tag=minecart_type] @e[tag=death,limit=1]

execute unless score minecarts funcs matches 0.. run function minecarts_init
scoreboard players add minecarts funcs 1
execute unless score minecarts funcs matches 0..5 run scoreboard players set minecarts funcs 0
execute if score minecarts funcs matches 0 run summon minecraft:Minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 0 run data merge block ~1 ~2 ~ {Text2:"\"Minecart\"",Text3:"\"\""}

execute if score minecarts funcs matches 1 run summon minecraft:Chest Minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 1 run data merge block ~1 ~2 ~ {Text2:"\"Chest\"",Text3:"\"Minecart\""}

execute if score minecarts funcs matches 2 run summon minecraft:Furnace Minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 2 run data merge block ~1 ~2 ~ {Text2:"\"Furnace\"",Text3:"\"Minecart\""}

execute if score minecarts funcs matches 3 run summon minecraft:TNT Minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 3 run data merge block ~1 ~2 ~ {Text2:"\"TNT\"",Text3:"\"Minecart\""}

execute if score minecarts funcs matches 4 run summon minecraft:Hopper Minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 4 run data merge block ~1 ~2 ~ {Text2:"\"Hopper\"",Text3:"\"Minecart\""}

execute if score minecarts funcs matches 5 run summon minecraft:Command Block Minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 5 run data merge block ~1 ~2 ~ {Text2:"\"Command Block\"",Text3:"\"Minecart\""}


