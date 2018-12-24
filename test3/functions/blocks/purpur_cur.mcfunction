scoreboard players set purpur max 2
execute unless score purpur funcs matches 0..1 run scoreboard players operation purpur funcs %= purpur max

execute if score purpur funcs matches 0 run setblock ~0 ~3 ~0 minecraft:purpur_block
execute if score purpur funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Purpur Block\"",Text3:"\"\"",Text4:"\"\""}


execute if score purpur funcs matches 1 run setblock ~0 ~3 ~0 minecraft:purpur_pillar
execute if score purpur funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Purpur Pillar\"",Text3:"\"\"",Text4:"\"\""}
