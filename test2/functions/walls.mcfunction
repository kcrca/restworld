execute unless score walls funcs matches 0.. run function walls_init
scoreboard players add walls funcs 1
execute unless score walls funcs matches 0..2 run scoreboard players set walls funcs 0

execute if score walls funcs matches 0 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:cobblestone_wall replace #v2:fencelike
execute if score walls funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"Cobblestone Wall\"",Text3:"\"Stained Glass\""}
execute if score walls funcs matches 0 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:cobblestone_wall replace #v2:fencelike
execute if score walls funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"\"",Text3:"\"Cobblestone Wall\""}



execute if score walls funcs matches 1 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:mossy_cobblestone_wall replace #v2:fencelike
execute if score walls funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Mossy Cobblestone Wall\"",Text3:"\"Stained Glass\""}
execute if score walls funcs matches 1 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:mossy_cobblestone_wall replace #v2:fencelike
execute if score walls funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Mossy\"",Text3:"\"Cobblestone Wall\""}



execute if score walls funcs matches 2 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:iron_bars replace #v2:fencelike
execute if score walls funcs matches 2 run data merge block ~5 ~2 ~0 {Text2:"\"Iron Bars\"",Text3:"\"Stained Glass\""}
execute if score walls funcs matches 2 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:iron_bars replace #v2:fencelike
execute if score walls funcs matches 2 run data merge block ~5 ~2 ~0 {Text2:"\"Iron Bars\"",Text3:"\"\""}