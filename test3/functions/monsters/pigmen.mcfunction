tp @e[tag=pigman] @e[tag=death,limit=1]




execute unless score pigmen funcs matches 0.. run function pigmen_init
scoreboard players add pigmen funcs 1
scoreboard players set pigmen max 2
execute unless score pigmen funcs matches 0..1 run scoreboard players operation pigmen funcs %= pigmen max

execute if score pigmen funcs matches 0 run summon minecraft:zombie_pigman ~0 ~2 ~-1.6 {Tags:[zombie_pigman,kid,monsters,pigman],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
summon minecraft:zombie_pigman ~0 ~2 ~0.8 {Tags:[zombie_pigman,monsters,pigman],CustomName:"\"Zombie Pigman\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}

execute if score pigmen funcs matches 1 run summon minecraft:chicken ~0 ~2 ~-1.6 {Tags:[chicken,kid,monsters,pigman],Passengers:[{id:"minecraft:zombie_pigman",IsBaby:True,Age:-2147483648,Tags:[monsters],Rotation:[180f,0f],Facing:north,PersistenceRequired:True,NoAI:True,Silent:True}],IsBaby:True,Age:-2147483648,PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}
