kill @e[tag=trader_llama]
summon minecraft:wandering_trader ~2 ~2 ~0 {Tags:[trader_llama,friendlies,friendlies],CustomName:"\"Wandering Trader\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}

summon minecraft:trader_llama ~0 ~2 ~0 {Tags:[trader_llama,friendlies,friendlies],DespawnDelay:2147483647,CustomName:"\"Trader Llama\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[180f,0f]}

setblock ~0 ~2 ~-3 oak_wall_sign[facing=north]
data modify block ~0 ~2 ~-3 Text2 set value "\"Trader Llama\""
