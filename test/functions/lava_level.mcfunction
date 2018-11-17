




execute unless score lava_level funcs matches -1.. run function lava_level_init
scoreboard players add lava_level funcs 1
execute unless score lava_level funcs matches 0..1 run scoreboard players set lava_level funcs 0



execute if score lava_level funcs matches 0 run fill ~0 ~2 ~0 ~3 ~2 ~3 minecraft:air


execute if score lava_level funcs matches 1 run fill ~0 ~2 ~0 ~3 ~2 ~3 minecraft:stone_slab
execute if score lava_level funcs matches 1 run fill ~1 ~2 ~1 ~2 ~2 ~2 minecraft:air


