execute unless score command_blocks funcs matches 0.. run function command_blocks_init
scoreboard players add command_blocks funcs 1
scoreboard players set command_blocks max 12
execute unless score command_blocks funcs matches 0..11 run scoreboard players operation command_blocks funcs %= command_blocks max

execute if score command_blocks funcs matches 0 run setblock ~ ~3 ~ minecraft:command_block[facing=west,conditional=true]
execute if score command_blocks funcs matches 0 run data merge block ~ ~2 ~-1 {Text2:"\"\"",Text4:"\"(Conditional)\""}


execute if score command_blocks funcs matches 1 run setblock ~ ~3 ~ minecraft:command_block[facing=west,conditional=false]
execute if score command_blocks funcs matches 1 run data merge block ~ ~2 ~-1 {Text2:"\"\"",Text4:"\"\""}


execute if score command_blocks funcs matches 2 run setblock ~ ~3 ~ minecraft:chain_command_block[facing=west,conditional=false]
execute if score command_blocks funcs matches 2 run data merge block ~ ~2 ~-1 {Text2:"\"Chain\"",Text4:"\"\""}


execute if score command_blocks funcs matches 3 run setblock ~ ~3 ~ minecraft:chain_command_block[facing=west,conditional=true]
execute if score command_blocks funcs matches 3 run data merge block ~ ~2 ~-1 {Text2:"\"Chain\"",Text4:"\"(Conditional)\""}


execute if score command_blocks funcs matches 4 run setblock ~ ~3 ~ minecraft:repeating_command_block[facing=west,conditional=true]
execute if score command_blocks funcs matches 4 run data merge block ~ ~2 ~-1 {Text2:"\"Repeating\"",Text4:"\"(Conditional)\""}


execute if score command_blocks funcs matches 5 run setblock ~ ~3 ~ minecraft:repeating_command_block[facing=west,conditional=false]
execute if score command_blocks funcs matches 5 run data merge block ~ ~2 ~-1 {Text2:"\"Repeating\"",Text4:"\"\""}


execute if score command_blocks funcs matches 6 run setblock ~ ~3 ~ minecraft:command_block[facing=west,conditional=false]
execute if score command_blocks funcs matches 6 run data merge block ~ ~2 ~-1 {Text2:"\"\"",Text4:"\"\""}


execute if score command_blocks funcs matches 7 run setblock ~ ~3 ~ minecraft:command_block[facing=west,conditional=true]
execute if score command_blocks funcs matches 7 run data merge block ~ ~2 ~-1 {Text2:"\"\"",Text4:"\"(Conditional)\""}


execute if score command_blocks funcs matches 8 run setblock ~ ~3 ~ minecraft:chain_command_block[facing=west,conditional=true]
execute if score command_blocks funcs matches 8 run data merge block ~ ~2 ~-1 {Text2:"\"Chain\"",Text4:"\"(Conditional)\""}


execute if score command_blocks funcs matches 9 run setblock ~ ~3 ~ minecraft:chain_command_block[facing=west,conditional=false]
execute if score command_blocks funcs matches 9 run data merge block ~ ~2 ~-1 {Text2:"\"Chain\"",Text4:"\"\""}


execute if score command_blocks funcs matches 10 run setblock ~ ~3 ~ minecraft:repeating_command_block[facing=west,conditional=false]
execute if score command_blocks funcs matches 10 run data merge block ~ ~2 ~-1 {Text2:"\"Repeating\"",Text4:"\"\""}


execute if score command_blocks funcs matches 11 run setblock ~ ~3 ~ minecraft:repeating_command_block[facing=west,conditional=true]
execute if score command_blocks funcs matches 11 run data merge block ~ ~2 ~-1 {Text2:"\"Repeating\"",Text4:"\"(Conditional)\""}
