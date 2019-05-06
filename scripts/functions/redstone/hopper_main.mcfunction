execute unless score hopper funcs matches 0.. run function hopper_init
scoreboard players add hopper funcs 1
scoreboard players set hopper max 2
execute unless score hopper funcs matches 0..1 run scoreboard players operation hopper funcs %= hopper max

execute if score hopper funcs matches 0 run fill ~0 ~2 ~0 ~2 ~2 ~4 minecraft:smooth_sandstone replace minecraft:air
execute if score hopper funcs matches 0 run setblock ~2 ~3 ~2 oak_wall_sign[facing=west]{Text2:"\"Which way are\"",Text3:"\"they pointing?\""}
execute if score hopper funcs matches 1 run fill ~0 ~2 ~0 ~2 ~2 ~4 minecraft:air replace minecraft:smooth_sandstone
execute if score hopper funcs matches 1 run setblock ~2 ~3 ~2 air
