scoreboard players set panes max 18
execute unless score panes funcs matches 0..17 run scoreboard players operation panes funcs %= panes max

execute if score panes funcs matches 0 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:white_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 0 run data merge block ~5 ~2 ~0 {Text2:"\"White\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 1 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:orange_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 1 run data merge block ~5 ~2 ~0 {Text2:"\"Orange\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 2 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:magenta_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 2 run data merge block ~5 ~2 ~0 {Text2:"\"Magenta\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 3 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:light_blue_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 3 run data merge block ~5 ~2 ~0 {Text2:"\"Light Blue\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 4 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:yellow_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 4 run data merge block ~5 ~2 ~0 {Text2:"\"Yellow\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 5 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:lime_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 5 run data merge block ~5 ~2 ~0 {Text2:"\"Lime\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 6 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:pink_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 6 run data merge block ~5 ~2 ~0 {Text2:"\"Pink\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 7 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:gray_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 7 run data merge block ~5 ~2 ~0 {Text2:"\"Gray\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 8 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:light_gray_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 8 run data merge block ~5 ~2 ~0 {Text2:"\"Light Gray\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 9 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:cyan_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 9 run data merge block ~5 ~2 ~0 {Text2:"\"Cyan\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 10 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:purple_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 10 run data merge block ~5 ~2 ~0 {Text2:"\"Purple\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 11 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:blue_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 11 run data merge block ~5 ~2 ~0 {Text2:"\"Blue\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 12 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:brown_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 12 run data merge block ~5 ~2 ~0 {Text2:"\"Brown\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 13 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:green_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 13 run data merge block ~5 ~2 ~0 {Text2:"\"Green\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 14 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:red_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 14 run data merge block ~5 ~2 ~0 {Text2:"\"Red\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 15 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:black_stained_glass_pane replace #v3:fencelike
execute if score panes funcs matches 15 run data merge block ~5 ~2 ~0 {Text2:"\"Black\"",Text3:"\"Stained Glass\""}


execute if score panes funcs matches 16 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:glass_pane replace #v3:fencelike
execute if score panes funcs matches 16 run data merge block ~5 ~2 ~0 {Text2:"\"Glass Pane\"",Text3:"\"\""}


execute if score panes funcs matches 17 run fill ~ ~2 ~ ~6 ~3 ~5 minecraft:iron_bars replace #v3:fencelike
execute if score panes funcs matches 17 run data merge block ~5 ~2 ~0 {Text2:"\"Iron Bars\"",Text3:"\"\""}
