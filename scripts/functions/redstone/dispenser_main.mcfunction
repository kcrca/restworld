execute unless score dispenser funcs matches 0.. run function dispenser_init
scoreboard players add dispenser funcs 1
scoreboard players set dispenser max 2
execute unless score dispenser funcs matches 0..1 run scoreboard players operation dispenser funcs %= dispenser max
execute if score dispenser funcs matches 0 run setblock ~0 ~2 ~0 minecraft:dispenser[facing=up]
execute if score dispenser funcs matches 0 run setblock ~0 ~4 ~0 minecraft:dispenser[facing=west]
execute if score dispenser funcs matches 0 run setblock ~0 ~6 ~0 minecraft:dispenser[facing=down]
execute if score dispenser funcs matches 0 run data merge block ~ ~3 ~ {Text2:"\"Dispenser\""}

execute if score dispenser funcs matches 1 run setblock ~0 ~2 ~0 minecraft:dropper[facing=up]
execute if score dispenser funcs matches 1 run setblock ~0 ~4 ~0 minecraft:dropper[facing=west]
execute if score dispenser funcs matches 1 run setblock ~0 ~6 ~0 minecraft:dropper[facing=down]
execute if score dispenser funcs matches 1 run data merge block ~ ~3 ~ {Text2:"\"Dropper\""}
