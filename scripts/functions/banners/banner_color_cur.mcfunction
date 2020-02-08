fill ~-2 ~-2 ~-2 ~16 ~16 ~16 air replace #banners


scoreboard players set banner_color max 16
execute unless score banner_color funcs matches 0..15 run scoreboard players operation banner_color funcs %= banner_color max



execute if score banner_color funcs matches 0 run setblock ~1 ~5 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~1 ~3 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~3 ~5 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~3 ~3 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~5 ~5 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~5 ~3 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~7 ~5 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~7 ~3 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~9 ~5 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~9 ~3 ~0 white_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~5 ~1 white_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~3 ~1 white_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~5 ~3 white_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~3 ~3 white_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~5 ~5 white_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~3 ~5 white_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~5 ~7 white_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~3 ~7 white_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~5 ~9 white_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~11 ~3 ~9 white_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~10 ~5 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~10 ~3 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~8 ~5 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~8 ~3 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~6 ~5 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~6 ~3 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~4 ~5 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~4 ~3 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~2 ~5 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~2 ~3 ~11 white_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~5 ~10 white_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~3 ~10 white_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~5 ~8 white_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~3 ~8 white_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~5 ~6 white_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~3 ~6 white_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~5 ~4 white_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~3 ~4 white_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~5 ~2 white_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 0 run setblock ~0 ~3 ~2 white_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 0 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 0




execute if score banner_color funcs matches 1 run setblock ~1 ~5 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~1 ~3 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~3 ~5 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~3 ~3 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~5 ~5 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~5 ~3 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~7 ~5 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~7 ~3 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~9 ~5 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~9 ~3 ~0 orange_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~5 ~1 orange_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~3 ~1 orange_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~5 ~3 orange_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~3 ~3 orange_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~5 ~5 orange_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~3 ~5 orange_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~5 ~7 orange_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~3 ~7 orange_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~5 ~9 orange_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~11 ~3 ~9 orange_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~10 ~5 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~10 ~3 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~8 ~5 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~8 ~3 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~6 ~5 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~6 ~3 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~4 ~5 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~4 ~3 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~2 ~5 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~2 ~3 ~11 orange_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~5 ~10 orange_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~3 ~10 orange_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~5 ~8 orange_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~3 ~8 orange_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~5 ~6 orange_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~3 ~6 orange_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~5 ~4 orange_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~3 ~4 orange_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~5 ~2 orange_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 1 run setblock ~0 ~3 ~2 orange_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 1 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 1




execute if score banner_color funcs matches 2 run setblock ~1 ~5 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~1 ~3 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~3 ~5 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~3 ~3 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~5 ~5 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~5 ~3 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~7 ~5 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~7 ~3 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~9 ~5 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~9 ~3 ~0 magenta_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~5 ~1 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~3 ~1 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~5 ~3 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~3 ~3 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~5 ~5 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~3 ~5 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~5 ~7 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~3 ~7 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~5 ~9 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~11 ~3 ~9 magenta_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~10 ~5 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~10 ~3 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~8 ~5 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~8 ~3 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~6 ~5 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~6 ~3 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~4 ~5 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~4 ~3 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~2 ~5 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~2 ~3 ~11 magenta_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~5 ~10 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~3 ~10 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~5 ~8 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~3 ~8 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~5 ~6 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~3 ~6 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~5 ~4 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~3 ~4 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~5 ~2 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 2 run setblock ~0 ~3 ~2 magenta_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 2 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 2




execute if score banner_color funcs matches 3 run setblock ~1 ~5 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~1 ~3 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~3 ~5 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~3 ~3 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~5 ~5 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~5 ~3 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~7 ~5 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~7 ~3 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~9 ~5 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~9 ~3 ~0 light_blue_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~5 ~1 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~3 ~1 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~5 ~3 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~3 ~3 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~5 ~5 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~3 ~5 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~5 ~7 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~3 ~7 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~5 ~9 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~11 ~3 ~9 light_blue_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~10 ~5 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~10 ~3 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~8 ~5 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~8 ~3 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~6 ~5 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~6 ~3 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~4 ~5 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~4 ~3 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~2 ~5 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~2 ~3 ~11 light_blue_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~5 ~10 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~3 ~10 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~5 ~8 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~3 ~8 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~5 ~6 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~3 ~6 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~5 ~4 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~3 ~4 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~5 ~2 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 3 run setblock ~0 ~3 ~2 light_blue_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 3 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 3




execute if score banner_color funcs matches 4 run setblock ~1 ~5 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~1 ~3 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~3 ~5 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~3 ~3 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~5 ~5 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~5 ~3 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~7 ~5 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~7 ~3 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~9 ~5 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~9 ~3 ~0 yellow_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~5 ~1 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~3 ~1 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~5 ~3 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~3 ~3 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~5 ~5 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~3 ~5 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~5 ~7 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~3 ~7 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~5 ~9 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~11 ~3 ~9 yellow_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~10 ~5 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~10 ~3 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~8 ~5 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~8 ~3 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~6 ~5 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~6 ~3 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~4 ~5 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~4 ~3 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~2 ~5 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~2 ~3 ~11 yellow_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~5 ~10 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~3 ~10 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~5 ~8 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~3 ~8 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~5 ~6 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~3 ~6 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~5 ~4 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~3 ~4 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~5 ~2 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 4 run setblock ~0 ~3 ~2 yellow_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 4 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 4




execute if score banner_color funcs matches 5 run setblock ~1 ~5 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~1 ~3 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~3 ~5 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~3 ~3 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~5 ~5 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~5 ~3 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~7 ~5 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~7 ~3 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~9 ~5 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~9 ~3 ~0 lime_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~5 ~1 lime_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~3 ~1 lime_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~5 ~3 lime_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~3 ~3 lime_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~5 ~5 lime_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~3 ~5 lime_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~5 ~7 lime_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~3 ~7 lime_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~5 ~9 lime_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~11 ~3 ~9 lime_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~10 ~5 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~10 ~3 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~8 ~5 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~8 ~3 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~6 ~5 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~6 ~3 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~4 ~5 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~4 ~3 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~2 ~5 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~2 ~3 ~11 lime_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~5 ~10 lime_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~3 ~10 lime_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~5 ~8 lime_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~3 ~8 lime_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~5 ~6 lime_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~3 ~6 lime_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~5 ~4 lime_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~3 ~4 lime_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~5 ~2 lime_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 5 run setblock ~0 ~3 ~2 lime_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 5 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 5




execute if score banner_color funcs matches 6 run setblock ~1 ~5 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~1 ~3 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~3 ~5 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~3 ~3 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~5 ~5 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~5 ~3 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~7 ~5 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~7 ~3 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~9 ~5 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~9 ~3 ~0 pink_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~5 ~1 pink_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~3 ~1 pink_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~5 ~3 pink_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~3 ~3 pink_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~5 ~5 pink_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~3 ~5 pink_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~5 ~7 pink_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~3 ~7 pink_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~5 ~9 pink_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~11 ~3 ~9 pink_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~10 ~5 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~10 ~3 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~8 ~5 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~8 ~3 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~6 ~5 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~6 ~3 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~4 ~5 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~4 ~3 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~2 ~5 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~2 ~3 ~11 pink_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~5 ~10 pink_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~3 ~10 pink_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~5 ~8 pink_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~3 ~8 pink_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~5 ~6 pink_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~3 ~6 pink_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~5 ~4 pink_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~3 ~4 pink_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~5 ~2 pink_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 6 run setblock ~0 ~3 ~2 pink_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 6 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 6




execute if score banner_color funcs matches 7 run setblock ~1 ~5 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~1 ~3 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~3 ~5 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~3 ~3 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~5 ~5 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~5 ~3 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~7 ~5 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~7 ~3 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~9 ~5 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~9 ~3 ~0 gray_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~5 ~1 gray_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~3 ~1 gray_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~5 ~3 gray_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~3 ~3 gray_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~5 ~5 gray_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~3 ~5 gray_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~5 ~7 gray_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~3 ~7 gray_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~5 ~9 gray_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~11 ~3 ~9 gray_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~10 ~5 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~10 ~3 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~8 ~5 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~8 ~3 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~6 ~5 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~6 ~3 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~4 ~5 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~4 ~3 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~2 ~5 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~2 ~3 ~11 gray_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~5 ~10 gray_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~3 ~10 gray_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~5 ~8 gray_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~3 ~8 gray_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~5 ~6 gray_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~3 ~6 gray_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~5 ~4 gray_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~3 ~4 gray_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~5 ~2 gray_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 7 run setblock ~0 ~3 ~2 gray_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 7 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 7




execute if score banner_color funcs matches 8 run setblock ~1 ~5 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~1 ~3 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~3 ~5 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~3 ~3 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~5 ~5 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~5 ~3 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~7 ~5 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~7 ~3 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~9 ~5 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~9 ~3 ~0 light_gray_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~5 ~1 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~3 ~1 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~5 ~3 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~3 ~3 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~5 ~5 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~3 ~5 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~5 ~7 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~3 ~7 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~5 ~9 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~11 ~3 ~9 light_gray_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~10 ~5 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~10 ~3 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~8 ~5 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~8 ~3 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~6 ~5 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~6 ~3 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~4 ~5 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~4 ~3 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~2 ~5 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~2 ~3 ~11 light_gray_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~5 ~10 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~3 ~10 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~5 ~8 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~3 ~8 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~5 ~6 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~3 ~6 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~5 ~4 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~3 ~4 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~5 ~2 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 8 run setblock ~0 ~3 ~2 light_gray_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 8 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 8




execute if score banner_color funcs matches 9 run setblock ~1 ~5 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~1 ~3 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~3 ~5 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~3 ~3 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~5 ~5 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~5 ~3 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~7 ~5 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~7 ~3 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~9 ~5 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~9 ~3 ~0 cyan_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~5 ~1 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~3 ~1 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~5 ~3 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~3 ~3 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~5 ~5 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~3 ~5 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~5 ~7 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~3 ~7 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~5 ~9 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~11 ~3 ~9 cyan_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~10 ~5 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~10 ~3 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~8 ~5 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~8 ~3 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~6 ~5 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~6 ~3 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~4 ~5 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~4 ~3 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~2 ~5 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~2 ~3 ~11 cyan_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~5 ~10 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~3 ~10 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~5 ~8 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~3 ~8 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~5 ~6 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~3 ~6 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~5 ~4 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~3 ~4 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~5 ~2 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 9 run setblock ~0 ~3 ~2 cyan_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 9 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 9




execute if score banner_color funcs matches 10 run setblock ~1 ~5 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~1 ~3 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~3 ~5 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~3 ~3 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~5 ~5 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~5 ~3 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~7 ~5 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~7 ~3 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~9 ~5 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~9 ~3 ~0 purple_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~5 ~1 purple_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~3 ~1 purple_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~5 ~3 purple_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~3 ~3 purple_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~5 ~5 purple_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~3 ~5 purple_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~5 ~7 purple_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~3 ~7 purple_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~5 ~9 purple_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~11 ~3 ~9 purple_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~10 ~5 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~10 ~3 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~8 ~5 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~8 ~3 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~6 ~5 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~6 ~3 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~4 ~5 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~4 ~3 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~2 ~5 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~2 ~3 ~11 purple_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~5 ~10 purple_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~3 ~10 purple_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~5 ~8 purple_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~3 ~8 purple_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~5 ~6 purple_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~3 ~6 purple_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~5 ~4 purple_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~3 ~4 purple_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~5 ~2 purple_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 10 run setblock ~0 ~3 ~2 purple_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 10 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 10




execute if score banner_color funcs matches 11 run setblock ~1 ~5 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~1 ~3 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~3 ~5 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~3 ~3 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~5 ~5 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~5 ~3 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~7 ~5 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~7 ~3 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~9 ~5 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~9 ~3 ~0 blue_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~5 ~1 blue_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~3 ~1 blue_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~5 ~3 blue_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~3 ~3 blue_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~5 ~5 blue_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~3 ~5 blue_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~5 ~7 blue_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~3 ~7 blue_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~5 ~9 blue_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~11 ~3 ~9 blue_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~10 ~5 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~10 ~3 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~8 ~5 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~8 ~3 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~6 ~5 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~6 ~3 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~4 ~5 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~4 ~3 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~2 ~5 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~2 ~3 ~11 blue_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~5 ~10 blue_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~3 ~10 blue_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~5 ~8 blue_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~3 ~8 blue_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~5 ~6 blue_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~3 ~6 blue_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~5 ~4 blue_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~3 ~4 blue_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~5 ~2 blue_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 11 run setblock ~0 ~3 ~2 blue_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 11 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 11




execute if score banner_color funcs matches 12 run setblock ~1 ~5 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~1 ~3 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~3 ~5 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~3 ~3 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~5 ~5 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~5 ~3 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~7 ~5 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~7 ~3 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~9 ~5 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~9 ~3 ~0 brown_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~5 ~1 brown_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~3 ~1 brown_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~5 ~3 brown_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~3 ~3 brown_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~5 ~5 brown_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~3 ~5 brown_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~5 ~7 brown_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~3 ~7 brown_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~5 ~9 brown_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~11 ~3 ~9 brown_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~10 ~5 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~10 ~3 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~8 ~5 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~8 ~3 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~6 ~5 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~6 ~3 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~4 ~5 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~4 ~3 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~2 ~5 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~2 ~3 ~11 brown_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~5 ~10 brown_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~3 ~10 brown_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~5 ~8 brown_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~3 ~8 brown_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~5 ~6 brown_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~3 ~6 brown_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~5 ~4 brown_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~3 ~4 brown_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~5 ~2 brown_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 12 run setblock ~0 ~3 ~2 brown_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 12 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 12




execute if score banner_color funcs matches 13 run setblock ~1 ~5 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~1 ~3 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~3 ~5 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~3 ~3 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~5 ~5 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~5 ~3 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~7 ~5 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~7 ~3 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~9 ~5 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~9 ~3 ~0 green_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~5 ~1 green_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~3 ~1 green_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~5 ~3 green_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~3 ~3 green_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~5 ~5 green_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~3 ~5 green_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~5 ~7 green_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~3 ~7 green_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~5 ~9 green_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~11 ~3 ~9 green_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~10 ~5 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~10 ~3 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~8 ~5 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~8 ~3 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~6 ~5 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~6 ~3 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~4 ~5 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~4 ~3 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~2 ~5 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~2 ~3 ~11 green_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~5 ~10 green_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~3 ~10 green_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~5 ~8 green_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~3 ~8 green_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~5 ~6 green_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~3 ~6 green_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~5 ~4 green_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~3 ~4 green_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~5 ~2 green_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 13 run setblock ~0 ~3 ~2 green_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 13 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 13




execute if score banner_color funcs matches 14 run setblock ~1 ~5 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~1 ~3 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~3 ~5 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~3 ~3 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~5 ~5 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~5 ~3 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~7 ~5 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~7 ~3 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~9 ~5 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~9 ~3 ~0 red_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~5 ~1 red_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~3 ~1 red_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~5 ~3 red_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~3 ~3 red_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~5 ~5 red_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~3 ~5 red_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~5 ~7 red_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~3 ~7 red_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~5 ~9 red_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~11 ~3 ~9 red_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~10 ~5 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~10 ~3 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~8 ~5 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~8 ~3 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~6 ~5 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~6 ~3 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~4 ~5 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~4 ~3 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~2 ~5 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~2 ~3 ~11 red_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~5 ~10 red_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~3 ~10 red_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~5 ~8 red_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~3 ~8 red_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~5 ~6 red_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~3 ~6 red_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~5 ~4 red_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~3 ~4 red_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~5 ~2 red_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 14 run setblock ~0 ~3 ~2 red_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 14 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 14




execute if score banner_color funcs matches 15 run setblock ~1 ~5 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~1 ~3 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~3 ~5 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~3 ~3 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~5 ~5 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~5 ~3 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~7 ~5 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~7 ~3 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~9 ~5 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~9 ~3 ~0 black_wall_banner[facing=south]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~5 ~1 black_wall_banner[facing=west]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~3 ~1 black_wall_banner[facing=west]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~5 ~3 black_wall_banner[facing=west]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~3 ~3 black_wall_banner[facing=west]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~5 ~5 black_wall_banner[facing=west]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~3 ~5 black_wall_banner[facing=west]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~5 ~7 black_wall_banner[facing=west]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~3 ~7 black_wall_banner[facing=west]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~5 ~9 black_wall_banner[facing=west]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~11 ~3 ~9 black_wall_banner[facing=west]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~10 ~5 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~10 ~3 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~8 ~5 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~8 ~3 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~6 ~5 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~6 ~3 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~4 ~5 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~4 ~3 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~2 ~5 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~2 ~3 ~11 black_wall_banner[facing=north]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~5 ~10 black_wall_banner[facing=east]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~3 ~10 black_wall_banner[facing=east]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~5 ~8 black_wall_banner[facing=east]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~3 ~8 black_wall_banner[facing=east]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~5 ~6 black_wall_banner[facing=east]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~3 ~6 black_wall_banner[facing=east]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~5 ~4 black_wall_banner[facing=east]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~3 ~4 black_wall_banner[facing=east]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~5 ~2 black_wall_banner[facing=east]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score banner_color funcs matches 15 run setblock ~0 ~3 ~2 black_wall_banner[facing=east]{Patterns:[{Pattern:"glb",Color:9}]} destroy



execute if score banner_color funcs matches 15 run execute as @e[tag=banner_stand] run data modify entity @s HandItems[1].tag.BlockEntityTag.Base set value 15





execute store result block ~1 ~5 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~1 ~3 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~3 ~5 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~3 ~3 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~5 ~5 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~5 ~3 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~7 ~5 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~7 ~3 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~9 ~5 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~9 ~3 ~0 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~5 ~1 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~3 ~1 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~5 ~3 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~3 ~3 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~5 ~5 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~3 ~5 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~5 ~7 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~3 ~7 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~5 ~9 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~11 ~3 ~9 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~10 ~5 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~10 ~3 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~8 ~5 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~8 ~3 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~6 ~5 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~6 ~3 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~4 ~5 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~4 ~3 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~2 ~5 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~2 ~3 ~11 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~5 ~10 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~3 ~10 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~5 ~8 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~3 ~8 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~5 ~6 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~3 ~6 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~5 ~4 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~3 ~4 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~5 ~2 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
execute store result block ~0 ~3 ~2 Patterns[0].Color int 1 run scoreboard players get banner_ink funcs
