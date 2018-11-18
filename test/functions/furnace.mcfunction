




execute unless score furnace funcs matches 0.. run function furnace_init
scoreboard players add furnace funcs 1
execute unless score furnace funcs matches 0..1 run scoreboard players set furnace funcs 0




execute if score furnace funcs matches 0 run setblock ~ ~3 ~ minecraft:furnace[facing=west,lit=true]
execute if score furnace funcs matches 0 run data merge block ~-1 ~2 ~-1 {Text3:"\"(lit)\""}




execute if score furnace funcs matches 1 run setblock ~ ~3 ~ minecraft:furnace[facing=west,lit=false]
execute if score furnace funcs matches 1 run data merge block ~-1 ~2 ~-1 {Text3:"\"\""}



