execute unless score nether funcs matches 0.. run function nether_init
scoreboard players add nether funcs 1
scoreboard players set nether max 3
execute unless score nether funcs matches 0..2 run scoreboard players operation nether funcs %= nether max

execute if score nether funcs matches 0 run setblock ~0 ~3 ~0 minecraft:netherrack
execute if score nether funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Netherrack\"",Text3:"\"\"",Text4:"\"\""}


execute if score nether funcs matches 1 run setblock ~0 ~3 ~0 minecraft:gravel
execute if score nether funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Gravel\"",Text3:"\"\"",Text4:"\"\""}


execute if score nether funcs matches 2 run setblock ~0 ~3 ~0 minecraft:magma_block
execute if score nether funcs matches 2 run data merge block ~0 ~2 ~-1 {Text2:"\"Magma Block\"",Text3:"\"\"",Text4:"\"\""}
