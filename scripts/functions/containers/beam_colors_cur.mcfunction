scoreboard players set beam_colors max 17
execute unless score beam_colors funcs matches 0..16 run scoreboard players operation beam_colors funcs %= beam_colors max

execute if score beam_colors funcs matches 0 run setblock ~ ~5 ~ minecraft:white_stained_glass
execute if score beam_colors funcs matches 0 run data merge block ~ ~4 ~-1 {Text2:"\"White\""}


execute if score beam_colors funcs matches 1 run setblock ~ ~5 ~ minecraft:orange_stained_glass
execute if score beam_colors funcs matches 1 run data merge block ~ ~4 ~-1 {Text2:"\"Orange\""}


execute if score beam_colors funcs matches 2 run setblock ~ ~5 ~ minecraft:magenta_stained_glass
execute if score beam_colors funcs matches 2 run data merge block ~ ~4 ~-1 {Text2:"\"Magenta\""}


execute if score beam_colors funcs matches 3 run setblock ~ ~5 ~ minecraft:light_blue_stained_glass
execute if score beam_colors funcs matches 3 run data merge block ~ ~4 ~-1 {Text2:"\"Light Blue\""}


execute if score beam_colors funcs matches 4 run setblock ~ ~5 ~ minecraft:yellow_stained_glass
execute if score beam_colors funcs matches 4 run data merge block ~ ~4 ~-1 {Text2:"\"Yellow\""}


execute if score beam_colors funcs matches 5 run setblock ~ ~5 ~ minecraft:lime_stained_glass
execute if score beam_colors funcs matches 5 run data merge block ~ ~4 ~-1 {Text2:"\"Lime\""}


execute if score beam_colors funcs matches 6 run setblock ~ ~5 ~ minecraft:pink_stained_glass
execute if score beam_colors funcs matches 6 run data merge block ~ ~4 ~-1 {Text2:"\"Pink\""}


execute if score beam_colors funcs matches 7 run setblock ~ ~5 ~ minecraft:gray_stained_glass
execute if score beam_colors funcs matches 7 run data merge block ~ ~4 ~-1 {Text2:"\"Gray\""}


execute if score beam_colors funcs matches 8 run setblock ~ ~5 ~ minecraft:light_gray_stained_glass
execute if score beam_colors funcs matches 8 run data merge block ~ ~4 ~-1 {Text2:"\"Light Gray\""}


execute if score beam_colors funcs matches 9 run setblock ~ ~5 ~ minecraft:cyan_stained_glass
execute if score beam_colors funcs matches 9 run data merge block ~ ~4 ~-1 {Text2:"\"Cyan\""}


execute if score beam_colors funcs matches 10 run setblock ~ ~5 ~ minecraft:purple_stained_glass
execute if score beam_colors funcs matches 10 run data merge block ~ ~4 ~-1 {Text2:"\"Purple\""}


execute if score beam_colors funcs matches 11 run setblock ~ ~5 ~ minecraft:blue_stained_glass
execute if score beam_colors funcs matches 11 run data merge block ~ ~4 ~-1 {Text2:"\"Blue\""}


execute if score beam_colors funcs matches 12 run setblock ~ ~5 ~ minecraft:brown_stained_glass
execute if score beam_colors funcs matches 12 run data merge block ~ ~4 ~-1 {Text2:"\"Brown\""}


execute if score beam_colors funcs matches 13 run setblock ~ ~5 ~ minecraft:green_stained_glass
execute if score beam_colors funcs matches 13 run data merge block ~ ~4 ~-1 {Text2:"\"Green\""}


execute if score beam_colors funcs matches 14 run setblock ~ ~5 ~ minecraft:red_stained_glass
execute if score beam_colors funcs matches 14 run data merge block ~ ~4 ~-1 {Text2:"\"Red\""}


execute if score beam_colors funcs matches 15 run setblock ~ ~5 ~ minecraft:black_stained_glass
execute if score beam_colors funcs matches 15 run data merge block ~ ~4 ~-1 {Text2:"\"Black\""}


execute if score beam_colors funcs matches 16 run setblock ~ ~5 ~ minecraft:glass_pane
execute if score beam_colors funcs matches 16 run data merge block ~ ~4 ~-1 {Text2:"\"Clear\""}
