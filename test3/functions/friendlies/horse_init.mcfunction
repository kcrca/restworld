summon minecraft:horse ~1.4 ~2 ~0 {IsBaby:True,Age:-2147483648,Tags:[white_horses,horse,friendlies,saddle,kid],Variant:0,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-1.2 ~2 ~0 {CustomName:"\"White\"",Tags:[white_horses,horse,friendlies,saddle],Variant:0,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~1.4 ~2 ~-2 {IsBaby:True,Age:-2147483648,Tags:[creamy_horses,horse,friendlies,saddle,kid],Variant:1,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-1.2 ~2 ~-2 {CustomName:"\"Creamy\"",Tags:[creamy_horses,horse,friendlies,saddle],Variant:1,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~1.4 ~2 ~-4 {IsBaby:True,Age:-2147483648,Tags:[chestnut_horses,horse,friendlies,saddle,kid],Variant:2,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-1.2 ~2 ~-4 {CustomName:"\"Chestnut\"",Tags:[chestnut_horses,horse,friendlies,saddle],Variant:2,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~1.4 ~2 ~-6 {IsBaby:True,Age:-2147483648,Tags:[brown_horses,horse,friendlies,saddle,kid],Variant:3,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-1.2 ~2 ~-6 {CustomName:"\"Brown\"",Tags:[brown_horses,horse,friendlies,saddle],Variant:3,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~1.4 ~2 ~-8 {IsBaby:True,Age:-2147483648,Tags:[black_horses,horse,friendlies,saddle,kid],Variant:4,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-1.2 ~2 ~-8 {CustomName:"\"Black\"",Tags:[black_horses,horse,friendlies,saddle],Variant:4,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~1.4 ~2 ~-10 {IsBaby:True,Age:-2147483648,Tags:[gray_horses,horse,friendlies,saddle,kid],Variant:5,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-1.2 ~2 ~-10 {CustomName:"\"Gray\"",Tags:[gray_horses,horse,friendlies,saddle],Variant:5,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~1.4 ~2 ~-12 {IsBaby:True,Age:-2147483648,Tags:[dark_brown_horses,horse,friendlies,saddle,kid],Variant:6,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-1.2 ~2 ~-12 {CustomName:"\"Dark Brown\"",Tags:[dark_brown_horses,horse,friendlies,saddle],Variant:6,Tame:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
execute at @e[tag=brown_horses,tag=kid] run setblock ~2 ~ ~ minecraft:wall_sign[facing=east]{Text2:"\"Variant:\""} replace
