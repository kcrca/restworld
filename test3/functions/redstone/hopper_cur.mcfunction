execute if score hopper funcs matches 0 run fill ~0 ~2 ~0 ~2 ~2 ~4 minecraft:smooth_sandstone replace minecraft:air
execute if score hopper funcs matches 0 run setblock ~2 ~3 ~2 wall_sign[facing=west]{Text2:"\"Which way are\"",Text3:"\"they pointing?\""}
execute if score hopper funcs matches 1 run fill ~0 ~2 ~0 ~2 ~2 ~4 minecraft:air replace minecraft:smooth_sandstone
execute if score hopper funcs matches 1 run setblock ~2 ~3 ~2 air
