scoreboard players set walls max 2
execute unless score walls funcs matches 0..1 run scoreboard players operation walls funcs %= walls max

execute if score walls funcs matches 0 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"Cobblestone Wall\"",Text3:"\"Stained Glass\""}
execute if score walls funcs matches 0 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"\"",Text3:"\"Cobblestone Wall\""}



execute if score walls funcs matches 1 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:mossy_cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Mossy Cobblestone Wall\"",Text3:"\"Stained Glass\""}
execute if score walls funcs matches 1 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:mossy_cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Mossy\"",Text3:"\"Cobblestone Wall\""}
