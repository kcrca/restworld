tp @e[tag=spider] @e[tag=death,limit=1]



execute unless score spider funcs matches 0.. run function spider_init
scoreboard players add spider funcs 1
scoreboard players set spider max 2
execute unless score spider funcs matches 0..1 run scoreboard players operation spider funcs %= spider max

execute if score spider funcs matches 0 run summon minecraft:spider ~-0.2 ~2.5 ~0 {Tags:[spider,monsters],CustomName:"\"Spider\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}

execute if score spider funcs matches 1 run summon minecraft:spider ~-0.2 ~2.5 ~0 {Tags:[spider,monsters],Passengers:[{id:"minecraft:skeleton",Tags:[monsters],Rotation:[270f,0f],Facing:east,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Spider\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
