



summon minecraft:horse ~0.5 ~2 ~0 {IsBaby:True,Age:-2147483648,Tags:[white_horses,horse,kid],Variant:0,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-2.5 ~2 ~0 {CustomName:"\"White\"",Tags:[white_horses,horse],Variant:0,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~0.5 ~2 ~-2 {IsBaby:True,Age:-2147483648,Tags:[creamy_horses,horse,kid],Variant:1,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-2.5 ~2 ~-2 {CustomName:"\"Creamy\"",Tags:[creamy_horses,horse],Variant:1,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~0.5 ~2 ~-4 {IsBaby:True,Age:-2147483648,Tags:[chestnut_horses,horse,kid],Variant:2,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-2.5 ~2 ~-4 {CustomName:"\"Chestnut\"",Tags:[chestnut_horses,horse],Variant:2,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~0.5 ~2 ~-6 {IsBaby:True,Age:-2147483648,Tags:[brown_horses,horse,kid],Variant:3,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-2.5 ~2 ~-6 {CustomName:"\"Brown\"",Tags:[brown_horses,horse],Variant:3,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~0.5 ~2 ~-8 {IsBaby:True,Age:-2147483648,Tags:[black_horses,horse,kid],Variant:4,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-2.5 ~2 ~-8 {CustomName:"\"Black\"",Tags:[black_horses,horse],Variant:4,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~0.5 ~2 ~-10 {IsBaby:True,Age:-2147483648,Tags:[gray_horses,horse,kid],Variant:5,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-2.5 ~2 ~-10 {CustomName:"\"Gray\"",Tags:[gray_horses,horse],Variant:5,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~0.5 ~2 ~-12 {IsBaby:True,Age:-2147483648,Tags:[dark_brown_horses,horse,kid],Variant:6,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:horse ~-2.5 ~2 ~-12 {CustomName:"\"Dark Brown\"",Tags:[dark_brown_horses,horse],Variant:6,NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:mule ~0.5 ~2 ~-14 {IsBaby:True,Age:-2147483648,Tags:[mules,mule,kid],NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:mule ~-2.5 ~2 ~-14 {CustomName:"\"Mule\"",Tags:[mules,mule],NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:donkey ~0.5 ~2 ~-16 {IsBaby:True,Age:-2147483648,Tags:[donkeys,donkey,kid],NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:donkey ~-2.5 ~2 ~-16 {CustomName:"\"Donkey\"",Tags:[donkeys,donkey],NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:skeleton_horse ~0.5 ~2 ~-18 {IsBaby:True,Age:-2147483648,Tags:[skeleton_horses,skeleton_horse,kid],NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:skeleton_horse ~-2.5 ~2 ~-18 {CustomName:"\"Skeleton Horse\"",Tags:[skeleton_horses,skeleton_horse],NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:zombie_horse ~0.5 ~2 ~-20 {IsBaby:True,Age:-2147483648,Tags:[zombie_horses,zombie_horse,kid],NoAI:True,Silent:True,Rotation:[270f,0f]}
summon minecraft:zombie_horse ~-2.5 ~2 ~-20 {CustomName:"\"Zombie Horse\"",Tags:[zombie_horses,zombie_horse],NoAI:True,Silent:True,Rotation:[270f,0f]}
execute at @e[tag=brown_horses,tag=kid] run setblock ~1 ~ ~ minecraft:wall_sign[facing=east]{Text2:"\"Variant:\""} replace
