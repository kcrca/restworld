execute unless score villager funcs matches 0.. run function villager_init
scoreboard players add villager funcs 1
scoreboard players set villager max 6
execute unless score villager funcs matches 0..5 run scoreboard players operation villager funcs %= villager max

execute if score villager funcs matches 0 run summon minecraft:villager ~0 ~0 ~0 {Profession:0,NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 1 run summon minecraft:villager ~0 ~0 ~0 {Profession:1,NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 2 run summon minecraft:villager ~0 ~0 ~0 {Profession:2,NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 3 run summon minecraft:villager ~0 ~0 ~0 {Profession:3,NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 4 run summon minecraft:villager ~0 ~0 ~0 {Profession:4,NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 5 run summon minecraft:villager ~0 ~0 ~0 {Profession:5,NoAI:True,Tags:[effecter],PersistenceRequired:True}