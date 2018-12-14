execute if score walls funcs matches 0 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"Cobblestone Wall\"",Text3:"\"Stained Glass\""}
execute if score walls funcs matches 0 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"\"",Text3:"\"Cobblestone Wall\""}



execute if score walls funcs matches 1 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:mossy_cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Mossy Cobblestone Wall\"",Text3:"\"Stained Glass\""}
execute if score walls funcs matches 1 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:mossy_cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Mossy\"",Text3:"\"Cobblestone Wall\""}
