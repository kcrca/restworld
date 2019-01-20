execute unless score repeater funcs matches 0.. run function repeater_init
scoreboard players add repeater funcs 1
scoreboard players set repeater max 2
execute unless score repeater funcs matches 0..1 run scoreboard players operation repeater funcs %= repeater max

execute if score repeater funcs matches 0 run fill ~0 ~2 ~-1 ~0 ~2 ~1 minecraft:redstone_block replace minecraft:air
execute if score repeater funcs matches 1 run fill ~0 ~2 ~-1 ~0 ~2 ~1 minecraft:air replace minecraft:redstone_block
