scoreboard players set glazed_1 max 8
execute unless score glazed_1 funcs matches 0..7 run scoreboard players operation glazed_1 funcs %= glazed_1 max

execute if score glazed_1 funcs matches 0 run data merge block ~0 ~0 ~-1 {name:"restworld:white_terra"}
execute if score glazed_1 funcs matches 0 run data merge block ~1 ~2 ~-0 {Text1:"\"White\""}


execute if score glazed_1 funcs matches 1 run data merge block ~0 ~0 ~-1 {name:"restworld:orange_terra"}
execute if score glazed_1 funcs matches 1 run data merge block ~1 ~2 ~-0 {Text1:"\"Orange\""}


execute if score glazed_1 funcs matches 2 run data merge block ~0 ~0 ~-1 {name:"restworld:magenta_terra"}
execute if score glazed_1 funcs matches 2 run data merge block ~1 ~2 ~-0 {Text1:"\"Magenta\""}


execute if score glazed_1 funcs matches 3 run data merge block ~0 ~0 ~-1 {name:"restworld:light_blue_terra"}
execute if score glazed_1 funcs matches 3 run data merge block ~1 ~2 ~-0 {Text1:"\"Light Blue\""}


execute if score glazed_1 funcs matches 4 run data merge block ~0 ~0 ~-1 {name:"restworld:yellow_terra"}
execute if score glazed_1 funcs matches 4 run data merge block ~1 ~2 ~-0 {Text1:"\"Yellow\""}


execute if score glazed_1 funcs matches 5 run data merge block ~0 ~0 ~-1 {name:"restworld:lime_terra"}
execute if score glazed_1 funcs matches 5 run data merge block ~1 ~2 ~-0 {Text1:"\"Lime\""}


execute if score glazed_1 funcs matches 6 run data merge block ~0 ~0 ~-1 {name:"restworld:pink_terra"}
execute if score glazed_1 funcs matches 6 run data merge block ~1 ~2 ~-0 {Text1:"\"Pink\""}


execute if score glazed_1 funcs matches 7 run data merge block ~0 ~0 ~-1 {name:"restworld:gray_terra"}
execute if score glazed_1 funcs matches 7 run data merge block ~1 ~2 ~-0 {Text1:"\"Gray\""}




setblock ~0 ~-1 ~-1 redstone_torch
setblock ~0 ~-1 ~-1 air
