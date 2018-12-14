execute unless score redstone_dust funcs matches 0.. run function redstone_dust_init
scoreboard players add redstone_dust funcs 1
execute unless score redstone_dust funcs matches 0..1 run scoreboard players set redstone_dust funcs 0

execute if score redstone_dust funcs matches 0 run fill ~1 ~0 ~1 ~7 ~0 ~7 minecraft:redstone_torch replace minecraft:glass
execute if score redstone_dust funcs matches 1 run fill ~1 ~0 ~1 ~7 ~0 ~7 minecraft:glass replace minecraft:redstone_torch
