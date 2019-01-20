execute unless score redstone_lamp funcs matches 0.. run function redstone_lamp_init
scoreboard players add redstone_lamp funcs 1
scoreboard players set redstone_lamp max 2
execute unless score redstone_lamp funcs matches 0..1 run scoreboard players operation redstone_lamp funcs %= redstone_lamp max

execute if score redstone_lamp funcs matches 0 run setblock ~0 ~0 ~-1 minecraft:redstone_torch
execute if score redstone_lamp funcs matches 1 run setblock ~0 ~0 ~-1 minecraft:air
