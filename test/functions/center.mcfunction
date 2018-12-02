execute if score fast clocks matches 0 run setblock ~0 ~1 ~0 minecraft:redstone_block
execute if score main clocks matches 0 run fill ~1 ~1 ~1 ~-1 ~1 ~-1 minecraft:redstone_block replace minecraft:diamond_block
execute if score slow clocks matches 0 run fill ~2 ~1 ~2 ~-2 ~1 ~-2 minecraft:redstone_block replace minecraft:emerald_block
execute unless blocks ~2 ~-3 ~2 ~-2 ~-3 ~-2 ~-2 ~1 ~-2 masked run clone ~2 ~-3 ~2 ~-2 ~-3 ~-2 ~-2 ~1 ~-2 masked