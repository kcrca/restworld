tp @e[tag=villager] @e[tag=death,limit=1]



execute unless score villagers funcs matches 0.. run function villagers_init
scoreboard players add villagers funcs 1
scoreboard players set villagers max 2
execute unless score villagers funcs matches 0..1 run scoreboard players operation villagers funcs %= villagers max



execute if score villagers funcs matches 0 run summon minecraft:villager ~0 ~2.3 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,villager,kid],Profession:0,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-2 ~2.3 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,villager,kid],Profession:1,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-4 ~2.3 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,villager,kid],Profession:2,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-6 ~2.3 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,villager,kid],Profession:3,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-8 ~2.3 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,villager,kid],Profession:4,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-10 ~2.3 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,villager,kid],Profession:5,NoAI:True,Silent:True,Rotation:[180f,0f]}


execute if score villagers funcs matches 0 run summon minecraft:villager ~0 ~2.3 ~0 {CustomName:"\"Farmer\"",Tags:[villager,villager],Profession:0,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-2 ~2.3 ~0 {CustomName:"\"Librarian\"",Tags:[villager,villager],Profession:1,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-4 ~2.3 ~0 {CustomName:"\"Priest\"",Tags:[villager,villager],Profession:2,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-6 ~2.3 ~0 {CustomName:"\"Smith\"",Tags:[villager,villager],Profession:3,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-8 ~2.3 ~0 {CustomName:"\"Butcher\"",Tags:[villager,villager],Profession:4,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 0 run summon minecraft:villager ~-10 ~2.3 ~0 {CustomName:"\"Nitwit\"",Tags:[villager,villager],Profession:5,NoAI:True,Silent:True,Rotation:[180f,0f]}




execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~0 ~2.175 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,zombie_villager,kid],Profession:0,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-2 ~2.175 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,zombie_villager,kid],Profession:1,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-4 ~2.175 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,zombie_villager,kid],Profession:2,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-6 ~2.175 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,zombie_villager,kid],Profession:3,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-8 ~2.175 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,zombie_villager,kid],Profession:4,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-10 ~2.175 ~-2 {IsBaby:True,Age:-2147483648,Tags:[villager,zombie_villager,kid],Profession:5,NoAI:True,Silent:True,Rotation:[180f,0f]}


execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~0 ~2.175 ~0 {CustomName:"\"Zombie Farmer\"",Tags:[villager,zombie_villager],Profession:0,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-2 ~2.175 ~0 {CustomName:"\"Zombie Librarian\"",Tags:[villager,zombie_villager],Profession:1,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-4 ~2.175 ~0 {CustomName:"\"Zombie Priest\"",Tags:[villager,zombie_villager],Profession:2,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-6 ~2.175 ~0 {CustomName:"\"Zombie Smith\"",Tags:[villager,zombie_villager],Profession:3,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-8 ~2.175 ~0 {CustomName:"\"Zombie Butcher\"",Tags:[villager,zombie_villager],Profession:4,NoAI:True,Silent:True,Rotation:[180f,0f]}
execute if score villagers funcs matches 1 run summon minecraft:zombie_villager ~-10 ~2.175 ~0 {CustomName:"\"Zombie Nitwit\"",Tags:[villager,zombie_villager],Profession:5,NoAI:True,Silent:True,Rotation:[180f,0f]}
