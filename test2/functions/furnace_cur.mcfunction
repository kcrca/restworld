execute if score furnace funcs matches 0 run setblock ~ ~3 ~ minecraft:furnace[facing=west,lit=true]
execute if score furnace funcs matches 0 run data merge block ~-1 ~2 ~ {Text3:"\"(lit)\""}




execute if score furnace funcs matches 1 run setblock ~ ~3 ~ minecraft:furnace[facing=west,lit=false]
execute if score furnace funcs matches 1 run data merge block ~-1 ~2 ~ {Text3:"\"\""}