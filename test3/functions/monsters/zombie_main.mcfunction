tp @e[tag=zombieish] @e[tag=death,limit=1]




execute unless score zombie funcs matches 0.. run function zombie_init
scoreboard players add zombie funcs 1
scoreboard players set zombie max 3
execute unless score zombie funcs matches 0..2 run scoreboard players operation zombie funcs %= zombie max

execute if score zombie funcs matches 0 run summon minecraft:zombie ~-1.7 ~2 ~0 {Tags:[zombie,kid,zombieish,monsters],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
execute if score zombie funcs matches 0 run summon minecraft:zombie ~0.2 ~2 ~0 {Tags:[zombie,zombieish,monsters],CustomName:"\"Zombie\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

execute if score zombie funcs matches 1 run summon minecraft:husk ~-1.7 ~2 ~0 {Tags:[husk,kid,zombieish,monsters],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
execute if score zombie funcs matches 1 run summon minecraft:husk ~0.2 ~2 ~0 {Tags:[husk,zombieish,monsters],CustomName:"\"Husk\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

execute if score zombie funcs matches 2 run summon minecraft:drowned ~-1.7 ~2 ~0 {Tags:[drowned,kid,zombieish,monsters],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
execute if score zombie funcs matches 2 run summon minecraft:drowned ~0.2 ~2 ~0 {Tags:[drowned,zombieish,monsters],CustomName:"\"Drowned\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
