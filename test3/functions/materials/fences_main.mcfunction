execute unless score fences funcs matches 0.. run function fences_init
scoreboard players add fences funcs 1
scoreboard players set fences max 7
execute unless score fences funcs matches 0..6 run scoreboard players operation fences funcs %= fences max

execute if score fences funcs matches 0 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:acacia_fence replace #v3:fencelike
execute if score fences funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"Acacia\"",Text3:"\"Fence\""}



execute if score fences funcs matches 1 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:birch_fence replace #v3:fencelike
execute if score fences funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Birch\"",Text3:"\"Fence\""}



execute if score fences funcs matches 2 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:jungle_fence replace #v3:fencelike
execute if score fences funcs matches 2 run data merge block ~5 ~2 ~0 {Text2:"\"Jungle\"",Text3:"\"Fence\""}



execute if score fences funcs matches 3 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:oak_fence replace #v3:fencelike
execute if score fences funcs matches 3 run data merge block ~5 ~2 ~0 {Text2:"\"Oak\"",Text3:"\"Fence\""}



execute if score fences funcs matches 4 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:dark_oak_fence replace #v3:fencelike
execute if score fences funcs matches 4 run data merge block ~5 ~2 ~0 {Text2:"\"Dark Oak\"",Text3:"\"Fence\""}



execute if score fences funcs matches 5 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:spruce_fence replace #v3:fencelike
execute if score fences funcs matches 5 run data merge block ~5 ~2 ~0 {Text2:"\"Spruce\"",Text3:"\"Fence\""}



execute if score fences funcs matches 6 run fill ~6 ~3 ~5 ~ ~2 ~ minecraft:nether_brick_fence replace #v3:fencelike
execute if score fences funcs matches 6 run data merge block ~5 ~2 ~0 {Text2:"\"Nether Brick\"",Text3:"\"Fence\""}
