tp @e[tag=skeletal] @e[tag=death,limit=1]




scoreboard players set skeleton max 2
execute unless score skeleton funcs matches 0..1 run scoreboard players operation skeleton funcs %= skeleton max

execute if score skeleton funcs matches 0 run summon minecraft:skeleton ~0.8 ~2 ~0 {Tags:[skeleton,monsters,skeletal,monsters],HandItems:[{id:"minecraft:bow",Count:1b},{}],CustomName:"\"Skeleton\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}

execute if score skeleton funcs matches 1 run summon minecraft:stray ~0.8 ~2 ~0 {Tags:[stray,monsters,skeletal,monsters],HandItems:[{id:"minecraft:bow",Count:1b},{}],CustomName:"\"Stray\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}