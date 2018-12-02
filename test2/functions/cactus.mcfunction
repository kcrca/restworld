execute unless score cactus funcs matches 0.. run function cactus_init
scoreboard players add cactus funcs 1
execute unless score cactus funcs matches 0..3 run scoreboard players set cactus funcs 0
execute if score cactus funcs matches 0 run setblock ~0 ~3 ~1 minecraft:sugar_cane

execute if score cactus funcs matches 0 run setblock ~0 ~4 ~1 minecraft:sugar_cane

execute if score cactus funcs matches 2 run setblock ~0 ~4  ~1 minecraft:air

execute if score cactus funcs matches 2 run setblock ~0 ~3  ~1 minecraft:air