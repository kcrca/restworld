tp @e[tag=villager] @e[tag=death,limit=1]



scoreboard players set villagers max 2
execute unless score villagers funcs matches 0..1 run scoreboard players operation villagers funcs %= villagers max



execute if score villagers funcs matches 0 run summon minecraft:villager ~0 ~2.3 ~-2 {Tags:[villager,kid,villager,friendlies,friendlies],Profession:0,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-2 ~2.3 ~-2 {Tags:[villager,kid,villager,friendlies,friendlies],Profession:1,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-4 ~2.3 ~-2 {Tags:[villager,kid,villager,friendlies,friendlies],Profession:2,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-6 ~2.3 ~-2 {Tags:[villager,kid,villager,friendlies,friendlies],Profession:3,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-8 ~2.3 ~-2 {Tags:[villager,kid,villager,friendlies,friendlies],Profession:4,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-10 ~2.3 ~-2 {Tags:[villager,kid,villager,friendlies,friendlies],Profession:5,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}


execute if score villagers funcs matches 0 run summon minecraft:villager ~0 ~2.3 ~0 {Tags:[villager,villager,friendlies,friendlies],Profession:0,CustomName:"\"Farmer\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-2 ~2.3 ~0 {Tags:[villager,villager,friendlies,friendlies],Profession:1,CustomName:"\"Librarian\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-4 ~2.3 ~0 {Tags:[villager,villager,friendlies,friendlies],Profession:2,CustomName:"\"Priest\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-6 ~2.3 ~0 {Tags:[villager,villager,friendlies,friendlies],Profession:3,CustomName:"\"Smith\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-8 ~2.3 ~0 {Tags:[villager,villager,friendlies,friendlies],Profession:4,CustomName:"\"Butcher\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-10 ~2.3 ~0 {Tags:[villager,villager,friendlies,friendlies],Profession:5,CustomName:"\"Nitwit\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}






execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 0 run summon minecraft:zombie_villager ~0 ~2.175 ~-2 {Tags:[zombie_villager,kid,villager,friendlies,friendlies],Profession:0,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 0 run summon minecraft:zombie_villager ~-2 ~2.175 ~-2 {Tags:[zombie_villager,kid,villager,friendlies,friendlies],Profession:1,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 0 run summon minecraft:zombie_villager ~-4 ~2.175 ~-2 {Tags:[zombie_villager,kid,villager,friendlies,friendlies],Profession:2,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 0 run summon minecraft:zombie_villager ~-6 ~2.175 ~-2 {Tags:[zombie_villager,kid,villager,friendlies,friendlies],Profession:3,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 0 run summon minecraft:zombie_villager ~-8 ~2.175 ~-2 {Tags:[zombie_villager,kid,villager,friendlies,friendlies],Profession:4,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 0 run summon minecraft:zombie_villager ~-10 ~2.175 ~-2 {Tags:[zombie_villager,kid,villager,friendlies,friendlies],Profession:5,IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}



execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 1 run summon minecraft:chicken ~0 ~2.175 ~-2 {Tags:[chicken,villager,friendlies,friendlies],Passengers:[{id:"minecraft:zombie_villager",Profession:0,IsBaby:True,Age:-2147483648,Tags:[zombie_villager,kids],Rotation:[180f,0f],Facing:north,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Chicken\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}

execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 1 run summon minecraft:chicken ~-2 ~2.175 ~-2 {Tags:[chicken,villager,friendlies,friendlies],Passengers:[{id:"minecraft:zombie_villager",Profession:1,IsBaby:True,Age:-2147483648,Tags:[zombie_villager,kids],Rotation:[180f,0f],Facing:north,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Chicken\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}

execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 1 run summon minecraft:chicken ~-4 ~2.175 ~-2 {Tags:[chicken,villager,friendlies,friendlies],Passengers:[{id:"minecraft:zombie_villager",Profession:2,IsBaby:True,Age:-2147483648,Tags:[zombie_villager,kids],Rotation:[180f,0f],Facing:north,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Chicken\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}

execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 1 run summon minecraft:chicken ~-6 ~2.175 ~-2 {Tags:[chicken,villager,friendlies,friendlies],Passengers:[{id:"minecraft:zombie_villager",Profession:3,IsBaby:True,Age:-2147483648,Tags:[zombie_villager,kids],Rotation:[180f,0f],Facing:north,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Chicken\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}

execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 1 run summon minecraft:chicken ~-8 ~2.175 ~-2 {Tags:[chicken,villager,friendlies,friendlies],Passengers:[{id:"minecraft:zombie_villager",Profession:4,IsBaby:True,Age:-2147483648,Tags:[zombie_villager,kids],Rotation:[180f,0f],Facing:north,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Chicken\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}

execute if score villagers funcs matches 1 run execute if score villager_jockeys funcs matches 1 run summon minecraft:chicken ~-10 ~2.175 ~-2 {Tags:[chicken,villager,friendlies,friendlies],Passengers:[{id:"minecraft:zombie_villager",Profession:5,IsBaby:True,Age:-2147483648,Tags:[zombie_villager,kids],Rotation:[180f,0f],Facing:north,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Chicken\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}




execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~0 ~2.175 ~0 {Tags:[zombie_villager,villager,friendlies,friendlies],Profession:0,CustomName:"\"Zombie Farmer\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-2 ~2.175 ~0 {Tags:[zombie_villager,villager,friendlies,friendlies],Profession:1,CustomName:"\"Zombie Librarian\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-4 ~2.175 ~0 {Tags:[zombie_villager,villager,friendlies,friendlies],Profession:2,CustomName:"\"Zombie Priest\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-6 ~2.175 ~0 {Tags:[zombie_villager,villager,friendlies,friendlies],Profession:3,CustomName:"\"Zombie Smith\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-8 ~2.175 ~0 {Tags:[zombie_villager,villager,friendlies,friendlies],Profession:4,CustomName:"\"Zombie Butcher\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-10 ~2.175 ~0 {Tags:[zombie_villager,villager,friendlies,friendlies],Profession:5,CustomName:"\"Zombie Nitwit\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
