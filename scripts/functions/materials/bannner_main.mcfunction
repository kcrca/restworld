execute unless score bannner funcs matches 0.. run function bannner_init
scoreboard players add bannner funcs 1
scoreboard players set bannner max 10
execute unless score bannner funcs matches 0..9 run scoreboard players operation bannner funcs %= bannner max

execute if score bannner funcs matches 0 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"",Color:9}]} destroy
execute if score bannner funcs matches 0 run data merge block ~-1 ~2 ~0 {Text2:"\"None\"",Text3:"\"\""}

execute if score bannner funcs matches 0 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"drs",Color:9}]} destroy
execute if score bannner funcs matches 0 run data merge block ~-1 ~2 ~1 {Text2:"\"Down Right Stripe\"",Text3:"\"\""}

execute if score bannner funcs matches 0 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"dls",Color:9}]} destroy
execute if score bannner funcs matches 0 run data merge block ~-1 ~2 ~2 {Text2:"\"Down Left Stripe\"",Text3:"\"\""}

execute if score bannner funcs matches 0 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"cr",Color:9}]} destroy
execute if score bannner funcs matches 0 run data merge block ~-1 ~2 ~3 {Text2:"\"Cross\"",Text3:"\"\""}


execute if score bannner funcs matches 1 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"bs",Color:9}]} destroy
execute if score bannner funcs matches 1 run data merge block ~-1 ~2 ~0 {Text2:"\"Bottom Stripe\"",Text3:"\"\""}

execute if score bannner funcs matches 1 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"ms",Color:9}]} destroy
execute if score bannner funcs matches 1 run data merge block ~-1 ~2 ~1 {Text2:"\"Middle Stripe\"",Text3:"\"\""}

execute if score bannner funcs matches 1 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"ts",Color:9}]} destroy
execute if score bannner funcs matches 1 run data merge block ~-1 ~2 ~2 {Text2:"\"Top Stripe\"",Text3:"\"\""}

execute if score bannner funcs matches 1 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"sc",Color:9}]} destroy
execute if score bannner funcs matches 1 run data merge block ~-1 ~2 ~3 {Text2:"\"Square Cross\"",Text3:"\"\""}


execute if score bannner funcs matches 2 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"ls",Color:9}]} destroy
execute if score bannner funcs matches 2 run data merge block ~-1 ~2 ~0 {Text2:"\"Left Stripe\"",Text3:"\"\""}

execute if score bannner funcs matches 2 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"cs",Color:9}]} destroy
execute if score bannner funcs matches 2 run data merge block ~-1 ~2 ~1 {Text2:"\"Center Stripe\"",Text3:"\"\""}

execute if score bannner funcs matches 2 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"rs",Color:9}]} destroy
execute if score bannner funcs matches 2 run data merge block ~-1 ~2 ~2 {Text2:"\"Right Stripe\"",Text3:"\"\""}

execute if score bannner funcs matches 2 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"ss",Color:9}]} destroy
execute if score bannner funcs matches 2 run data merge block ~-1 ~2 ~3 {Text2:"\"Small Stripes\"",Text3:"\"\""}


execute if score bannner funcs matches 3 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"ld",Color:9}]} destroy
execute if score bannner funcs matches 3 run data merge block ~-1 ~2 ~0 {Text2:"\"Left Diagonal\"",Text3:"\"\""}

execute if score bannner funcs matches 3 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"rud",Color:9}]} destroy
execute if score bannner funcs matches 3 run data merge block ~-1 ~2 ~1 {Text2:"\"Right Upside-Down\"",Text3:"\"Diagonal\""}

execute if score bannner funcs matches 3 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"lud",Color:9}]} destroy
execute if score bannner funcs matches 3 run data merge block ~-1 ~2 ~2 {Text2:"\"Left Upside-Down\"",Text3:"\"Diagonal\""}

execute if score bannner funcs matches 3 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"rd",Color:9}]} destroy
execute if score bannner funcs matches 3 run data merge block ~-1 ~2 ~3 {Text2:"\"Right Diagonal\"",Text3:"\"\""}


execute if score bannner funcs matches 4 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"vh",Color:9}]} destroy
execute if score bannner funcs matches 4 run data merge block ~-1 ~2 ~0 {Text2:"\"Vertical Half\"",Text3:"\"(Left)\""}

execute if score bannner funcs matches 4 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"vhr",Color:9}]} destroy
execute if score bannner funcs matches 4 run data merge block ~-1 ~2 ~1 {Text2:"\"Vertical Half\"",Text3:"\"(Right)\""}

execute if score bannner funcs matches 4 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"hhb",Color:9}]} destroy
execute if score bannner funcs matches 4 run data merge block ~-1 ~2 ~2 {Text2:"\"Horizontal Half\"",Text3:"\"(Bottom)\""}

execute if score bannner funcs matches 4 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"hh",Color:9}]} destroy
execute if score bannner funcs matches 4 run data merge block ~-1 ~2 ~3 {Text2:"\"Horizontal Half\"",Text3:"\"(Top)\""}


execute if score bannner funcs matches 5 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"bl",Color:9}]} destroy
execute if score bannner funcs matches 5 run data merge block ~-1 ~2 ~0 {Text2:"\"Bottom Left\"",Text3:"\"Corner\""}

execute if score bannner funcs matches 5 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"br",Color:9}]} destroy
execute if score bannner funcs matches 5 run data merge block ~-1 ~2 ~1 {Text2:"\"Bottom Right\"",Text3:"\"Corner\""}

execute if score bannner funcs matches 5 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"tl",Color:9}]} destroy
execute if score bannner funcs matches 5 run data merge block ~-1 ~2 ~2 {Text2:"\"Top Left\"",Text3:"\"Corner\""}

execute if score bannner funcs matches 5 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"tr",Color:9}]} destroy
execute if score bannner funcs matches 5 run data merge block ~-1 ~2 ~3 {Text2:"\"Top Right\"",Text3:"\"Corner\""}


execute if score bannner funcs matches 6 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"bt",Color:9}]} destroy
execute if score bannner funcs matches 6 run data merge block ~-1 ~2 ~0 {Text2:"\"Bottom Triangle\"",Text3:"\"\""}

execute if score bannner funcs matches 6 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"tt",Color:9}]} destroy
execute if score bannner funcs matches 6 run data merge block ~-1 ~2 ~1 {Text2:"\"Top Triangle\"",Text3:"\"\""}

execute if score bannner funcs matches 6 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"bts",Color:9}]} destroy
execute if score bannner funcs matches 6 run data merge block ~-1 ~2 ~2 {Text2:"\"Bottom Triangle\"",Text3:"\"Sawtooth\""}

execute if score bannner funcs matches 6 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"tts",Color:9}]} destroy
execute if score bannner funcs matches 6 run data merge block ~-1 ~2 ~3 {Text2:"\"Top Triangle\"",Text3:"\"Sawtooth\""}


execute if score bannner funcs matches 7 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"mc",Color:9}]} destroy
execute if score bannner funcs matches 7 run data merge block ~-1 ~2 ~0 {Text2:"\"Middle Circle\"",Text3:"\"\""}

execute if score bannner funcs matches 7 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"mr",Color:9}]} destroy
execute if score bannner funcs matches 7 run data merge block ~-1 ~2 ~1 {Text2:"\"Middle Rhombus\"",Text3:"\"\""}

execute if score bannner funcs matches 7 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"bo",Color:9}]} destroy
execute if score bannner funcs matches 7 run data merge block ~-1 ~2 ~2 {Text2:"\"Border\"",Text3:"\"\""}

execute if score bannner funcs matches 7 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"cbo",Color:9}]} destroy
execute if score bannner funcs matches 7 run data merge block ~-1 ~2 ~3 {Text2:"\"Curly Border\"",Text3:"\"\""}


execute if score bannner funcs matches 8 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"gra",Color:9}]} destroy
execute if score bannner funcs matches 8 run data merge block ~-1 ~2 ~0 {Text2:"\"Gradient\"",Text3:"\"\""}

execute if score bannner funcs matches 8 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"gru",Color:9}]} destroy
execute if score bannner funcs matches 8 run data merge block ~-1 ~2 ~1 {Text2:"\"Gradient\"",Text3:"\"Upside-Down\""}

execute if score bannner funcs matches 8 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"cre",Color:9}]} destroy
execute if score bannner funcs matches 8 run data merge block ~-1 ~2 ~2 {Text2:"\"Creeper\"",Text3:"\"\""}

execute if score bannner funcs matches 8 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"bri",Color:9}]} destroy
execute if score bannner funcs matches 8 run data merge block ~-1 ~2 ~3 {Text2:"\"Bick\"",Text3:"\"\""}


execute if score bannner funcs matches 9 run setblock ~0 ~3 ~0 white_banner[rotation=4]{Patterns:[{Pattern:"sku",Color:9}]} destroy
execute if score bannner funcs matches 9 run data merge block ~-1 ~2 ~0 {Text2:"\"Skull\"",Text3:"\"\""}

execute if score bannner funcs matches 9 run setblock ~0 ~3 ~1 white_banner[rotation=4]{Patterns:[{Pattern:"flo",Color:9}]} destroy
execute if score bannner funcs matches 9 run data merge block ~-1 ~2 ~1 {Text2:"\"Flower\"",Text3:"\"\""}

execute if score bannner funcs matches 9 run setblock ~0 ~3 ~2 white_banner[rotation=4]{Patterns:[{Pattern:"moj",Color:9}]} destroy
execute if score bannner funcs matches 9 run data merge block ~-1 ~2 ~2 {Text2:"\"Mojang\"",Text3:"\"\""}

execute if score bannner funcs matches 9 run setblock ~0 ~3 ~3 white_banner[rotation=4]{Patterns:[{Pattern:"glb",Color:9}]} destroy
execute if score bannner funcs matches 9 run data merge block ~-1 ~2 ~3 {Text2:"\"Globe\"",Text3:"\"\""}
