tp @e[tag=cowish] @e[tag=death,limit=1]





execute unless score cow funcs matches 0.. run function cow_init
scoreboard players add cow funcs 1
scoreboard players set cow max 2
execute unless score cow funcs matches 0..1 run scoreboard players operation cow funcs %= cow max

execute if score cow funcs matches 0 run summon minecraft:cow ~1.4 ~2 ~0 {Tags:[cow,kid,friendlies,cowish,friendlies],IsBaby:True,Age:-2147483648,CustomName:"\"Cow\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
execute if score cow funcs matches 0 run summon minecraft:cow ~-1.2 ~2 ~0 {Tags:[cow,friendlies,cowish,friendlies],CustomName:"\"Cow\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}

execute if score cow funcs matches 1 run summon minecraft:mooshroom ~1.4 ~2 ~0 {Tags:[mooshroom,kid,friendlies,cowish,friendlies],IsBaby:True,Age:-2147483648,CustomName:"\"MooShroom\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
execute if score cow funcs matches 1 run summon minecraft:mooshroom ~-1.2 ~2 ~0 {Tags:[mooshroom,friendlies,cowish,friendlies],CustomName:"\"MooShroom\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
