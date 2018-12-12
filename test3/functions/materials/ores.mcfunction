execute unless score ores funcs matches 0.. run function ores_init
scoreboard players add ores funcs 1
execute unless score ores funcs matches 0..7 run scoreboard players set ores funcs 0

execute if score ores funcs matches 0 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:redstone_ore replace #v3:ores
execute if score ores funcs matches 0 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:redstone_block replace #v3:ore_blocks
execute if score ores funcs matches 0 run data merge block ~2 ~2 ~3 {Text2:"\"Redstone\""}


execute if score ores funcs matches 1 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:emerald_ore replace #v3:ores
execute if score ores funcs matches 1 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:emerald_block replace #v3:ore_blocks
execute if score ores funcs matches 1 run data merge block ~2 ~2 ~3 {Text2:"\"Emerald\""}


execute if score ores funcs matches 2 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:nether_quartz_ore replace #v3:ores
execute if score ores funcs matches 2 run fill ~4 ~3 ~2 ~0 ~2 ~0 quartz_block replace #v3:ore_blocks
execute if score ores funcs matches 2 run data merge block ~2 ~2 ~3 {Text2:"\"Nether Quartz\""}
execute if score ores funcs matches 2 run fill ~4 ~3 ~2 ~0 ~2 ~0 netherrack replace stone


execute if score ores funcs matches 3 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:gold_ore replace #v3:ores
execute if score ores funcs matches 3 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:gold_block replace #v3:ore_blocks
execute if score ores funcs matches 3 run data merge block ~2 ~2 ~3 {Text2:"\"Gold\""}
execute if score ores funcs matches 3 run fill ~4 ~3 ~2 ~0 ~2 ~0 stone replace netherrack


execute if score ores funcs matches 4 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:iron_ore replace #v3:ores
execute if score ores funcs matches 4 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:iron_block replace #v3:ore_blocks
execute if score ores funcs matches 4 run data merge block ~2 ~2 ~3 {Text2:"\"Iron\""}


execute if score ores funcs matches 5 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:coal_ore replace #v3:ores
execute if score ores funcs matches 5 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:coal_block replace #v3:ore_blocks
execute if score ores funcs matches 5 run data merge block ~2 ~2 ~3 {Text2:"\"Coal\""}


execute if score ores funcs matches 6 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:lapis_ore replace #v3:ores
execute if score ores funcs matches 6 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:lapis_block replace #v3:ore_blocks
execute if score ores funcs matches 6 run data merge block ~2 ~2 ~3 {Text2:"\"Lapis\""}


execute if score ores funcs matches 7 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:diamond_ore replace #v3:ores
execute if score ores funcs matches 7 run fill ~4 ~3 ~2 ~0 ~2 ~0 minecraft:diamond_block replace #v3:ore_blocks
execute if score ores funcs matches 7 run data merge block ~2 ~2 ~3 {Text2:"\"Diamond\""}