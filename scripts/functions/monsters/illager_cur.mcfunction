tp @e[tag=illager] @e[tag=death,limit=1]


scoreboard players set illager max 5
execute unless score illager funcs matches 0..4 run scoreboard players operation illager funcs %= illager max
execute if score illager funcs matches 0 run summon minecraft:vindicator ~-1 ~2 ~0 {Tags:[illager,monsters,monsters,illager,monsters],CustomName:"\"Vindicator\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}


execute if score illager funcs matches 1 run summon minecraft:evoker ~-1 ~2 ~0 {Tags:[illager,monsters,monsters,illager,monsters],CustomName:"\"Evoker\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

    execute if score illager funcs matches 1 run summon minecraft:vex ~1 ~3.5 ~-1 {Tags:[monsters,illager,monsters],LifeTicks:2147483647,CustomName:"\"Vex\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

    execute if score illager funcs matches 1 run summon minecraft:evoker_fangs ~-1 ~3 ~1 {Tags:[monsters,illager,monsters],Warmup:0,CustomName:"\"Evoker Fangs\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}


execute if score illager funcs matches 2 run summon minecraft:pillager ~-1 ~2 ~0 {Tags:[illager,monsters,monsters,illager,monsters],CustomName:"\"Pillager\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}


execute if score illager funcs matches 3 run summon minecraft:pillager ~-1 ~2 ~0 {Tags:[illager,monsters,monsters,illager,monsters],HandItems:[{id:crossbow,Count:1},{}],CustomName:"\"Pillager\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}


execute if score illager funcs matches 4 run summon minecraft:illusioner ~-1 ~2 ~0 {Tags:[illager,monsters,monsters,illager,monsters],CustomName:"\"Illusioner (unused)\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
