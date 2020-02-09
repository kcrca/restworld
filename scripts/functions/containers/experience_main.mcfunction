execute unless score experience funcs matches 0.. run function experience_init
scoreboard players add experience funcs 1
scoreboard players set experience max 13
execute unless score experience funcs matches 0..12 run scoreboard players operation experience funcs %= experience max

execute if score experience funcs matches 0 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:1},Xp:0}


execute if score experience funcs matches 1 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:1},Xp:3}


execute if score experience funcs matches 2 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:1},Xp:6}


execute if score experience funcs matches 3 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:2},Xp:0}


execute if score experience funcs matches 4 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:2},Xp:16}


execute if score experience funcs matches 5 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:2},Xp:33}


execute if score experience funcs matches 6 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:3},Xp:0}


execute if score experience funcs matches 7 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:3},Xp:33}


execute if score experience funcs matches 8 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:3},Xp:66}


execute if score experience funcs matches 9 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:4},Xp:0}


execute if score experience funcs matches 10 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:4},Xp:66}


execute if score experience funcs matches 11 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:4},Xp:133}


execute if score experience funcs matches 12 run data merge entity @e[tag=trading_villager,limit=1] {VillagerData:{level:5},Xp:500}
