

teleport @e[tag=villager] @e[tag=death,limit=1]


execute unless score villagers funcs matches 0.. run function villagers_init
scoreboard players add villagers funcs 1
execute unless score villagers funcs matches 0..1 run scoreboard players set villagers funcs 0



execute if score villagers funcs matches 0 run summon minecraft:villager ~0 ~2 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:0,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-2 ~2 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:1,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-4 ~2 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:2,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-6 ~2 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:3,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-8 ~2 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:4,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-10 ~2 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:5,NoAI:True,Silent:True,Rotation:[0f,0f]}


execute if score villagers funcs matches 0 run summon minecraft:villager ~0 ~2 ~-2 {CustomName:"\"Farmer\"",Tags:[villager],Profession:0,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-2 ~2 ~-2 {CustomName:"\"Librarian\"",Tags:[villager],Profession:1,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-4 ~2 ~-2 {CustomName:"\"Priest\"",Tags:[villager],Profession:2,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-6 ~2 ~-2 {CustomName:"\"Smith\"",Tags:[villager],Profession:3,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-8 ~2 ~-2 {CustomName:"\"Butcher\"",Tags:[villager],Profession:4,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-10 ~2 ~-2 {CustomName:"\"Nitwit\"",Tags:[villager],Profession:5,NoAI:True,Silent:True,Rotation:[0f,0f]}




execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~0 ~1.875 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:0,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-2 ~1.875 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:1,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-4 ~1.875 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:2,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-6 ~1.875 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:3,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-8 ~1.875 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:4,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-10 ~1.875 ~0 {IsBaby:True,Age:-2147483648,Tags:[villager,kid],Profession:5,NoAI:True,Silent:True,Rotation:[0f,0f]}


execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~0 ~1.875 ~-2 {CustomName:"\"Zombie Farmer\"",Tags:[villager],Profession:0,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-2 ~1.875 ~-2 {CustomName:"\"Zombie Librarian\"",Tags:[villager],Profession:1,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-4 ~1.875 ~-2 {CustomName:"\"Zombie Priest\"",Tags:[villager],Profession:2,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-6 ~1.875 ~-2 {CustomName:"\"Zombie Smith\"",Tags:[villager],Profession:3,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-8 ~1.875 ~-2 {CustomName:"\"Zombie Butcher\"",Tags:[villager],Profession:4,NoAI:True,Silent:True,Rotation:[0f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-10 ~1.875 ~-2 {CustomName:"\"Zombie Nitwit\"",Tags:[villager],Profession:5,NoAI:True,Silent:True,Rotation:[0f,0f]}


