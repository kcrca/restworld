scoreboard players set coral max 5
execute unless score coral funcs matches 0..4 run scoreboard players operation coral funcs %= coral max
execute if score coral funcs matches 0 run fill ~0 ~2 ~0 ~0 ~2 ~1 minecraft:brain_coral_block
execute if score coral funcs matches 0 run setblock ~0 ~3 ~0 minecraft:brain_coral
execute if score coral funcs matches 0 run setblock ~0 ~3 ~1 minecraft:brain_coral_fan
execute if score coral funcs matches 0 run setblock ~-1 ~2 ~1 minecraft:brain_coral_wall_fan[facing=west]

execute if score coral funcs matches 0 run setblock ~0 ~2 ~2 minecraft:wall_sign[facing=west,waterlogged=false]{Text2:"\"Brain Coral\""}

execute if score coral funcs matches 0 run fill ~0 ~2 ~3 ~0 ~2 ~4 minecraft:dead_brain_coral_block
execute if score coral funcs matches 0 run setblock ~0 ~3 ~3 minecraft:dead_brain_coral
execute if score coral funcs matches 0 run setblock ~0 ~3 ~4 minecraft:dead_brain_coral_fan
execute if score coral funcs matches 0 run setblock ~-1 ~2 ~3 minecraft:dead_brain_coral_wall_fan[facing=west]

execute if score coral funcs matches 1 run fill ~0 ~2 ~0 ~0 ~2 ~1 minecraft:bubble_coral_block
execute if score coral funcs matches 1 run setblock ~0 ~3 ~0 minecraft:bubble_coral
execute if score coral funcs matches 1 run setblock ~0 ~3 ~1 minecraft:bubble_coral_fan
execute if score coral funcs matches 1 run setblock ~-1 ~2 ~1 minecraft:bubble_coral_wall_fan[facing=west]

execute if score coral funcs matches 1 run setblock ~0 ~2 ~2 minecraft:wall_sign[facing=west,waterlogged=false]{Text2:"\"Bubble Coral\""}

execute if score coral funcs matches 1 run fill ~0 ~2 ~3 ~0 ~2 ~4 minecraft:dead_bubble_coral_block
execute if score coral funcs matches 1 run setblock ~0 ~3 ~3 minecraft:dead_bubble_coral
execute if score coral funcs matches 1 run setblock ~0 ~3 ~4 minecraft:dead_bubble_coral_fan
execute if score coral funcs matches 1 run setblock ~-1 ~2 ~3 minecraft:dead_bubble_coral_wall_fan[facing=west]

execute if score coral funcs matches 2 run fill ~0 ~2 ~0 ~0 ~2 ~1 minecraft:fire_coral_block
execute if score coral funcs matches 2 run setblock ~0 ~3 ~0 minecraft:fire_coral
execute if score coral funcs matches 2 run setblock ~0 ~3 ~1 minecraft:fire_coral_fan
execute if score coral funcs matches 2 run setblock ~-1 ~2 ~1 minecraft:fire_coral_wall_fan[facing=west]

execute if score coral funcs matches 2 run setblock ~0 ~2 ~2 minecraft:wall_sign[facing=west,waterlogged=false]{Text2:"\"Fire Coral\""}

execute if score coral funcs matches 2 run fill ~0 ~2 ~3 ~0 ~2 ~4 minecraft:dead_fire_coral_block
execute if score coral funcs matches 2 run setblock ~0 ~3 ~3 minecraft:dead_fire_coral
execute if score coral funcs matches 2 run setblock ~0 ~3 ~4 minecraft:dead_fire_coral_fan
execute if score coral funcs matches 2 run setblock ~-1 ~2 ~3 minecraft:dead_fire_coral_wall_fan[facing=west]

execute if score coral funcs matches 3 run fill ~0 ~2 ~0 ~0 ~2 ~1 minecraft:horn_coral_block
execute if score coral funcs matches 3 run setblock ~0 ~3 ~0 minecraft:horn_coral
execute if score coral funcs matches 3 run setblock ~0 ~3 ~1 minecraft:horn_coral_fan
execute if score coral funcs matches 3 run setblock ~-1 ~2 ~1 minecraft:horn_coral_wall_fan[facing=west]

execute if score coral funcs matches 3 run setblock ~0 ~2 ~2 minecraft:wall_sign[facing=west,waterlogged=false]{Text2:"\"Horn Coral\""}

execute if score coral funcs matches 3 run fill ~0 ~2 ~3 ~0 ~2 ~4 minecraft:dead_horn_coral_block
execute if score coral funcs matches 3 run setblock ~0 ~3 ~3 minecraft:dead_horn_coral
execute if score coral funcs matches 3 run setblock ~0 ~3 ~4 minecraft:dead_horn_coral_fan
execute if score coral funcs matches 3 run setblock ~-1 ~2 ~3 minecraft:dead_horn_coral_wall_fan[facing=west]

execute if score coral funcs matches 4 run fill ~0 ~2 ~0 ~0 ~2 ~1 minecraft:tube_coral_block
execute if score coral funcs matches 4 run setblock ~0 ~3 ~0 minecraft:tube_coral
execute if score coral funcs matches 4 run setblock ~0 ~3 ~1 minecraft:tube_coral_fan
execute if score coral funcs matches 4 run setblock ~-1 ~2 ~1 minecraft:tube_coral_wall_fan[facing=west]

execute if score coral funcs matches 4 run setblock ~0 ~2 ~2 minecraft:wall_sign[facing=west,waterlogged=false]{Text2:"\"Tube Coral\""}

execute if score coral funcs matches 4 run fill ~0 ~2 ~3 ~0 ~2 ~4 minecraft:dead_tube_coral_block
execute if score coral funcs matches 4 run setblock ~0 ~3 ~3 minecraft:dead_tube_coral
execute if score coral funcs matches 4 run setblock ~0 ~3 ~4 minecraft:dead_tube_coral_fan
execute if score coral funcs matches 4 run setblock ~-1 ~2 ~3 minecraft:dead_tube_coral_wall_fan[facing=west]
