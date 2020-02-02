tp @e[tag=villager] @e[tag=death,limit=1]




summon minecraft:villager ~-2 ~2 ~-2 {Tags:[villager,friendlies,types,friendlies],VillagerData:{type:desert},CustomName:"\"Desert\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:villager ~-2 ~2 ~0 {Tags:[villager,friendlies,types,friendlies],VillagerData:{type:jungle},CustomName:"\"Jungle\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:villager ~-2 ~2 ~2 {Tags:[villager,friendlies,types,friendlies],VillagerData:{type:plains},CustomName:"\"Plains\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
    

summon minecraft:villager ~0 ~2 ~-3 {Tags:[villager,friendlies,types,friendlies],VillagerData:{type:savanna},CustomName:"\"Savanna\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:villager ~0 ~2 ~-1 {Tags:[villager,friendlies,types,friendlies],VillagerData:{type:snow},CustomName:"\"Snow\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:villager ~0 ~2 ~1 {Tags:[villager,friendlies,types,friendlies],VillagerData:{type:swamp},CustomName:"\"Swamp\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:villager ~0 ~2 ~3 {Tags:[villager,friendlies,types,friendlies],VillagerData:{type:taiga},CustomName:"\"Taiga\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

function v3:friendlies/villager_types_cur

setblock ~-5 ~2 ~0 oak_wall_sign[facing=west]
data modify block ~-5 ~2 ~0 Text3 set value "\"Villagers\""
