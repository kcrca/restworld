



tp @e[tag=minecart_type] @e[tag=death,limit=1]

execute if score minecarts funcs matches 0 run summon minecraft:minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 0 run data merge block ~1 ~2 ~ {Text2:"\"Minecart\"",Text3:"\"\""}

execute if score minecarts funcs matches 1 run summon minecraft:chest_minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 1 run data merge block ~1 ~2 ~ {Text2:"\"Chest\"",Text3:"\"Minecart\""}

execute if score minecarts funcs matches 2 run summon minecraft:furnace_minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 2 run data merge block ~1 ~2 ~ {Text2:"\"Furnace\"",Text3:"\"Minecart\""}

execute if score minecarts funcs matches 3 run summon minecraft:tnt_minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 3 run data merge block ~1 ~2 ~ {Text2:"\"TNT\"",Text3:"\"Minecart\""}

execute if score minecarts funcs matches 4 run summon minecraft:hopper_minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 4 run data merge block ~1 ~2 ~ {Text2:"\"Hopper\"",Text3:"\"Minecart\""}

execute if score minecarts funcs matches 5 run summon minecraft:command_block_minecart ~0 ~3 ~ {Tags:[minecart_type]}
execute if score minecarts funcs matches 5 run data merge block ~1 ~2 ~ {Text2:"\"Command Block\"",Text3:"\"Minecart\""}


