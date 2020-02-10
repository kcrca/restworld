scoreboard players set glazed_2 max 8
execute unless score glazed_2 funcs matches 0..7 run scoreboard players operation glazed_2 funcs %= glazed_2 max

execute if score glazed_2 funcs matches 0 run data merge block ~0 ~0 ~-1 {name:"restworld:light_gray_terra"}
execute if score glazed_2 funcs matches 0 run data merge block ~1 ~2 ~-5 {Text1:"\"Light Gray\""}


execute if score glazed_2 funcs matches 1 run data merge block ~0 ~0 ~-1 {name:"restworld:cyan_terra"}
execute if score glazed_2 funcs matches 1 run data merge block ~1 ~2 ~-5 {Text1:"\"Cyan\""}


execute if score glazed_2 funcs matches 2 run data merge block ~0 ~0 ~-1 {name:"restworld:purple_terra"}
execute if score glazed_2 funcs matches 2 run data merge block ~1 ~2 ~-5 {Text1:"\"Purple\""}


execute if score glazed_2 funcs matches 3 run data merge block ~0 ~0 ~-1 {name:"restworld:blue_terra"}
execute if score glazed_2 funcs matches 3 run data merge block ~1 ~2 ~-5 {Text1:"\"Blue\""}


execute if score glazed_2 funcs matches 4 run data merge block ~0 ~0 ~-1 {name:"restworld:brown_terra"}
execute if score glazed_2 funcs matches 4 run data merge block ~1 ~2 ~-5 {Text1:"\"Brown\""}


execute if score glazed_2 funcs matches 5 run data merge block ~0 ~0 ~-1 {name:"restworld:green_terra"}
execute if score glazed_2 funcs matches 5 run data merge block ~1 ~2 ~-5 {Text1:"\"Green\""}


execute if score glazed_2 funcs matches 6 run data merge block ~0 ~0 ~-1 {name:"restworld:red_terra"}
execute if score glazed_2 funcs matches 6 run data merge block ~1 ~2 ~-5 {Text1:"\"Red\""}


execute if score glazed_2 funcs matches 7 run data merge block ~0 ~0 ~-1 {name:"restworld:black_terra"}
execute if score glazed_2 funcs matches 7 run data merge block ~1 ~2 ~-5 {Text1:"\"Black\""}




setblock ~0 ~-1 ~-1 redstone_torch
setblock ~0 ~-1 ~-1 air
