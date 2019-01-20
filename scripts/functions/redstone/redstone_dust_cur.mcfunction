scoreboard players set redstone_dust max 2
execute unless score redstone_dust funcs matches 0..1 run scoreboard players operation redstone_dust funcs %= redstone_dust max

execute if score redstone_dust funcs matches 0 run fill ~1 ~0 ~1 ~7 ~0 ~7 minecraft:redstone_torch replace minecraft:glass
execute if score redstone_dust funcs matches 1 run fill ~1 ~0 ~1 ~7 ~0 ~7 minecraft:glass replace minecraft:redstone_torch
