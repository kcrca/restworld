tp @e[tag=zombieish] @e[tag=death,limit=1]





execute unless score zombie_jockey funcs matches 0.. run function zombie_jockey_init
scoreboard players add zombie_jockey funcs 1
scoreboard players set zombie_jockey max 3
execute unless score zombie_jockey funcs matches 0..2 run scoreboard players operation zombie_jockey funcs %= zombie_jockey max
execute if score zombie_jockey funcs matches 0 run summon minecraft:chicken ~-1.2 ~2 ~0 {Tags:[chicken,kid,zombieish,monsters,monsters],Passengers:[{id:"minecraft:zombie",Tags:[zombie,kid,monsters],IsBaby:True,Age:-2147483648,Rotation:[90f,0f],PersistenceRequired:True,NoAI:True,Silent:True}],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}


execute if score zombie_jockey funcs matches 1 run summon minecraft:chicken ~-1.2 ~2 ~0 {Tags:[chicken,kid,zombieish,monsters,monsters],Passengers:[{id:"minecraft:husk",Tags:[zombie,kid,monsters],IsBaby:True,Age:-2147483648,Rotation:[90f,0f],PersistenceRequired:True,NoAI:True,Silent:True}],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}


execute if score zombie_jockey funcs matches 2 run summon minecraft:chicken ~-1.2 ~2 ~0 {Tags:[chicken,kid,zombieish,monsters,monsters],Passengers:[{id:"minecraft:drowned",Tags:[zombie,kid,monsters],IsBaby:True,Age:-2147483648,Rotation:[90f,0f],PersistenceRequired:True,NoAI:True,Silent:True}],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
