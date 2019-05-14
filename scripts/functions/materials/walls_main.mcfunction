execute unless score walls funcs matches 0.. run function walls_init
scoreboard players add walls funcs 1
scoreboard players set walls max 13
execute unless score walls funcs matches 0..12 run scoreboard players operation walls funcs %= walls max

execute if score walls funcs matches 0 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"\"",Text3:"\"Cobblestone Wall\""}



execute if score walls funcs matches 1 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:mossy_cobblestone_wall replace #v3:fencelike
execute if score walls funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Mossy\"",Text3:"\"Cobblestone Wall\""}



execute if score walls funcs matches 2 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:stone_brick_wall replace #v3:fencelike
execute if score walls funcs matches 2 run data merge block ~5 ~2 ~0 {Text2:"\"\"",Text3:"\"Stone Brick Wall\""}



execute if score walls funcs matches 3 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:mossy_stone_brick_wall replace #v3:fencelike
execute if score walls funcs matches 3 run data merge block ~5 ~2 ~0 {Text2:"\"Mossy\"",Text3:"\"Stone Brick Wall\""}



execute if score walls funcs matches 4 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:end_stone_brick_wall replace #v3:fencelike
execute if score walls funcs matches 4 run data merge block ~5 ~2 ~0 {Text2:"\"End\"",Text3:"\"Stone Brick Wall\""}



execute if score walls funcs matches 5 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:sandstone_wall replace #v3:fencelike
execute if score walls funcs matches 5 run data merge block ~5 ~2 ~0 {Text2:"\"\"",Text3:"\"Sandstone Wall\""}



execute if score walls funcs matches 6 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:red_sandstone_wall replace #v3:fencelike
execute if score walls funcs matches 6 run data merge block ~5 ~2 ~0 {Text2:"\"Red\"",Text3:"\"Sandstone Wall\""}



execute if score walls funcs matches 7 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:nether_brick_wall replace #v3:fencelike
execute if score walls funcs matches 7 run data merge block ~5 ~2 ~0 {Text2:"\"\"",Text3:"\"Nether Brick Wall\""}



execute if score walls funcs matches 8 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:red_nether_brick_wall replace #v3:fencelike
execute if score walls funcs matches 8 run data merge block ~5 ~2 ~0 {Text2:"\"Red\"",Text3:"\"Nether Brick Wall\""}



execute if score walls funcs matches 9 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:andesite_wall replace #v3:fencelike
execute if score walls funcs matches 9 run data merge block ~5 ~2 ~0 {Text2:"\"Andesite Wall\"",Text3:"\"\""}



execute if score walls funcs matches 10 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:granite_wall replace #v3:fencelike
execute if score walls funcs matches 10 run data merge block ~5 ~2 ~0 {Text2:"\"Granite Wall\"",Text3:"\"\""}



execute if score walls funcs matches 11 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:diorite_wall replace #v3:fencelike
execute if score walls funcs matches 11 run data merge block ~5 ~2 ~0 {Text2:"\"Diorite Wall\"",Text3:"\"\""}



execute if score walls funcs matches 12 run fill ~6 ~3 ~4 ~0 ~2 ~0 minecraft:prismarine_wall replace #v3:fencelike
execute if score walls funcs matches 12 run data merge block ~5 ~2 ~0 {Text2:"\"Prismarine Wall\"",Text3:"\"\""}
