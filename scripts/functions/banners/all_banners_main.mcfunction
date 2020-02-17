setblock ~0 ~3 ~0 air
setblock ~11 ~3 ~11 air

execute unless score all_banners funcs matches 0.. run function all_banners_init
scoreboard players add all_banners funcs 1
scoreboard players set all_banners max 5
execute unless score all_banners funcs matches 0..4 run scoreboard players operation all_banners funcs %= all_banners max

execute if score all_banners funcs matches 0 run setblock ~0.2 ~3 ~0.2 blue_banner[rotation=14]{Patterns:[{Color:0,Pattern:"bri"},{Color:11,Pattern:"hhb"},{Color:15,Pattern:"sc"},{Color:11,Pattern:"sc"},{Color:15,Pattern:"bo"},{Color:11,Pattern:"bo"}]}
execute if score all_banners funcs matches 0 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Tardis\""}
execute if score all_banners funcs matches 0 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by Pikachu\""}

execute if score all_banners funcs matches 0 run setblock ~11.8 ~3 ~11.8 white_banner[rotation=6]{Patterns:[{Color:15,Pattern:"sc"},{Color:0,Pattern:"sc"},{Color:15,Pattern:"flo"},{Color:0,Pattern:"flo"}]}
execute if score all_banners funcs matches 0 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Quartz sculpte\""}
execute if score all_banners funcs matches 0 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by Pikachu\""}


execute if score all_banners funcs matches 1 run setblock ~0.2 ~3 ~0.2 purple_banner[rotation=14]{Patterns:[{Color:2,Pattern:"ss"},{Color:10,Pattern:"bri"},{Color:2,Pattern:"cbo"},{Color:15,Pattern:"bo"}]}
execute if score all_banners funcs matches 1 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Portail du Nether\""}
execute if score all_banners funcs matches 1 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by Akkta\""}

execute if score all_banners funcs matches 1 run setblock ~11.8 ~3 ~11.8 black_banner[rotation=6]{Patterns:[{Color:5,Pattern:"cbo"},{Color:15,Pattern:"rs"},{Color:14,Pattern:"flo"},{Color:5,Pattern:"ms"},{Color:15,Pattern:"tt"},{Color:5,Pattern:"moj"}]}
execute if score all_banners funcs matches 1 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"DRAGON !\""}
execute if score all_banners funcs matches 1 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by kraftime\""}


execute if score all_banners funcs matches 2 run setblock ~0.2 ~3 ~0.2 white_banner[rotation=14]{Patterns:[{Color:15,Pattern:"mr"},{Color:1,Pattern:"cbo"},{Color:1,Pattern:"mc"},{Color:1,Pattern:"cre"},{Color:1,Pattern:"tt"},{Color:1,Pattern:"tts"}]}
execute if score all_banners funcs matches 2 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Fox\""}
execute if score all_banners funcs matches 2 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by mr.crafteur\""}

execute if score all_banners funcs matches 2 run setblock ~11.8 ~3 ~11.8 white_banner[rotation=6]{Patterns:[{Color:15,Pattern:"ts"},{Color:0,Pattern:"sc"},{Color:14,Pattern:"hhb"},{Color:0,Pattern:"bo"},{Color:0,Pattern:"bs"},{Color:4,Pattern:"ms"}]}
execute if score all_banners funcs matches 2 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Poule\""}
execute if score all_banners funcs matches 2 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by mish80\""}


execute if score all_banners funcs matches 3 run setblock ~0.2 ~3 ~0.2 white_banner[rotation=14]{Patterns:[{Color:15,Pattern:"mc"},{Color:0,Pattern:"flo"},{Color:15,Pattern:"tt"},{Color:0,Pattern:"cr"},{Color:15,Pattern:"cbo"},{Color:0,Pattern:"bts"}]}
execute if score all_banners funcs matches 3 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Rabbit\""}
execute if score all_banners funcs matches 3 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by googolplexbyte\""}

execute if score all_banners funcs matches 3 run setblock ~11.8 ~3 ~11.8 black_banner[rotation=6]{Patterns:[{Color:14,Pattern:"gru"},{Color:14,Pattern:"bt"},{Color:0,Pattern:"bts"},{Color:0,Pattern:"tts"}]}
execute if score all_banners funcs matches 3 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Bouche\""}
execute if score all_banners funcs matches 3 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by entonix69\""}


execute if score all_banners funcs matches 4 run setblock ~0.2 ~3 ~0.2 light_blue_banner[rotation=14]{Patterns:[{Color:11,Pattern:"gra"},{Color:0,Pattern:"cbo"},{Color:0,Pattern:"cr"},{Color:0,Pattern:"mc"},{Color:11,Pattern:"flo"},{Color:0,Pattern:"tt"}]}
execute if score all_banners funcs matches 4 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Angel\""}
execute if score all_banners funcs matches 4 run execute as @e[tag=all_banners_home] run execute at @s positioned ~0.2 ~3 ~0.2 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by PK?\""}

execute if score all_banners funcs matches 4 run setblock ~11.8 ~3 ~11.8 lime_banner[rotation=6]{Patterns:[{Color:4,Pattern:"gra"},{Color:3,Pattern:"gru"},{Color:0,Pattern:"cbo"},{Color:0,Pattern:"cr"},{Color:0,Pattern:"mr"},{Color:5,Pattern:"mc"}]}
execute if score all_banners funcs matches 4 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom,distance=..2] run data merge entity @s {CustomName:"\"Like pls ^-^\""}
execute if score all_banners funcs matches 4 run execute as @e[tag=all_banners_home] run execute at @s positioned ~11.8 ~3 ~11.8 as @e[tag=banner_pattern_custom_author,distance=..2] run data merge entity @s {CustomName:"\"by Harmony\""}
