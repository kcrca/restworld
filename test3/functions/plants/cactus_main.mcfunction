execute unless score cactus funcs matches 0.. run function cactus_init
scoreboard players add cactus funcs 1
scoreboard players set cactus max 4
execute unless score cactus funcs matches 0..3 run scoreboard players operation cactus funcs %= cactus max

execute if score cactus funcs matches 0 run setblock ~0 ~4 ~0 minecraft:cactus
execute if score cactus funcs matches 2 run setblock ~0 ~5 ~0 minecraft:air
execute if score cactus funcs matches 1 run setblock ~0 ~5 ~0 minecraft:cactus
execute if score cactus funcs matches 3 run setblock ~0 ~4 ~0 minecraft:air
