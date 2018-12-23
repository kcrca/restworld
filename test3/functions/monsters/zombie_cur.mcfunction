scoreboard players add zombie_jockey funcs 0

tp @e[tag=zombieish] @e[tag=death,limit=1]





scoreboard players set zombie max 3
execute unless score zombie funcs matches 0..2 run scoreboard players operation zombie funcs %= zombie max

execute if score zombie_jockey funcs matches 0 run execute if score zombie funcs matches 0 run summon minecraft:zombie ~-1.7 ~2 ~0 {Tags:[zombie,kid,zombieish,monsters,monsters],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
execute if score zombie funcs matches 0 run summon minecraft:zombie ~0.2 ~2 ~0 {Tags:[zombie,zombieish,monsters,monsters],CustomName:"\"Zombie\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

execute if score zombie_jockey funcs matches 1 run execute if score zombie funcs matches 0 run summon minecraft:zombie ~0.2 ~2 ~0 {Tags:[zombie,zombieish,monsters,monsters],CustomName:"\"Zombie\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

execute if score zombie_jockey funcs matches 1 run execute if score zombie funcs matches 0 run summon minecraft:chicken ~-1.7 ~2 ~0 {Tags:[chicken,kid,zombieish,monsters,monsters],Passengers:[{id:"minecraft:zombie",Tags:[zombie,kid,monsters],IsBaby:True,Age:-2147483648,Rotation:[90f,0f],PersistenceRequired:True,NoAI:True,Silent:True}],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}



execute if score zombie_jockey funcs matches 0 run execute if score zombie funcs matches 1 run summon minecraft:husk ~-1.7 ~2 ~0 {Tags:[husk,kid,zombieish,monsters,monsters],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
execute if score zombie funcs matches 1 run summon minecraft:husk ~0.2 ~2 ~0 {Tags:[husk,zombieish,monsters,monsters],CustomName:"\"Husk\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

execute if score zombie_jockey funcs matches 1 run execute if score zombie funcs matches 1 run summon minecraft:husk ~0.2 ~2 ~0 {Tags:[husk,zombieish,monsters,monsters],CustomName:"\"Husk\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

execute if score zombie_jockey funcs matches 1 run execute if score zombie funcs matches 1 run summon minecraft:chicken ~-1.7 ~2 ~0 {Tags:[chicken,kid,zombieish,monsters,monsters],Passengers:[{id:"minecraft:husk",Tags:[zombie,kid,monsters],IsBaby:True,Age:-2147483648,Rotation:[90f,0f],PersistenceRequired:True,NoAI:True,Silent:True}],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}



execute if score zombie_jockey funcs matches 0 run execute if score zombie funcs matches 2 run summon minecraft:drowned ~-1.7 ~2 ~0 {Tags:[drowned,kid,zombieish,monsters,monsters],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
execute if score zombie funcs matches 2 run summon minecraft:drowned ~0.2 ~2 ~0 {Tags:[drowned,zombieish,monsters,monsters],CustomName:"\"Drowned\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

execute if score zombie_jockey funcs matches 1 run execute if score zombie funcs matches 2 run summon minecraft:drowned ~0.2 ~2 ~0 {Tags:[drowned,zombieish,monsters,monsters],CustomName:"\"Drowned\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

execute if score zombie_jockey funcs matches 1 run execute if score zombie funcs matches 2 run summon minecraft:chicken ~-1.7 ~2 ~0 {Tags:[chicken,kid,zombieish,monsters,monsters],Passengers:[{id:"minecraft:drowned",Tags:[zombie,kid,monsters],IsBaby:True,Age:-2147483648,Rotation:[90f,0f],PersistenceRequired:True,NoAI:True,Silent:True}],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
