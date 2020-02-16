execute unless score cauldron funcs matches 0.. run function cauldron_init
scoreboard players add cauldron funcs 1
scoreboard players set cauldron max 4
execute unless score cauldron funcs matches 0..3 run scoreboard players operation cauldron funcs %= cauldron max

execute if score cauldron funcs matches 0 run setblock ~ ~3 ~ cauldron[level=0]
execute if score cauldron funcs matches 0 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 0\"",Text2:"\"Cauldron\""}


execute if score cauldron funcs matches 1 run setblock ~ ~3 ~ cauldron[level=1]
execute if score cauldron funcs matches 1 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 1\"",Text2:"\"Cauldron\""}


execute if score cauldron funcs matches 2 run setblock ~ ~3 ~ cauldron[level=2]
execute if score cauldron funcs matches 2 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 2\"",Text2:"\"Cauldron\""}


execute if score cauldron funcs matches 3 run setblock ~ ~3 ~ cauldron[level=3]
execute if score cauldron funcs matches 3 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 3\"",Text2:"\"Cauldron\""}
