execute unless score villager funcs matches 0.. run function villager_init
scoreboard players add villager funcs 1
scoreboard players set villager max 105
execute unless score villager funcs matches 0..104 run scoreboard players operation villager funcs %= villager max

execute if score villager funcs matches 0 run say villager 0 profession:librarian,type:desert
execute if score villager funcs matches 0 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:librarian,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 1 run say villager 1 profession:nitwit,type:plains
execute if score villager funcs matches 1 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:nitwit,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 2 run say villager 2 profession:butcher,type:savanna
execute if score villager funcs matches 2 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:butcher,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 3 run say villager 3 profession:shepherd,type:desert
execute if score villager funcs matches 3 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:shepherd,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 4 run say villager 4 profession:stonemason,type:snowy
execute if score villager funcs matches 4 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:stonemason,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 5 run say villager 5 profession:armorer,type:taiga
execute if score villager funcs matches 5 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:armorer,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 6 run say villager 6 profession:stonemason,type:desert
execute if score villager funcs matches 6 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:stonemason,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 7 run say villager 7 profession:armorer,type:desert
execute if score villager funcs matches 7 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:armorer,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 8 run say villager 8 profession:unemployed,type:jungle
execute if score villager funcs matches 8 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:unemployed,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 9 run say villager 9 profession:fletcher,type:savanna
execute if score villager funcs matches 9 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fletcher,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 10 run say villager 10 profession:toolsmith,type:snowy
execute if score villager funcs matches 10 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:toolsmith,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 11 run say villager 11 profession:toolsmith,type:plains
execute if score villager funcs matches 11 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:toolsmith,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 12 run say villager 12 profession:shepherd,type:savanna
execute if score villager funcs matches 12 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:shepherd,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 13 run say villager 13 profession:armorer,type:jungle
execute if score villager funcs matches 13 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:armorer,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 14 run say villager 14 profession:toolsmith,type:swamp
execute if score villager funcs matches 14 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:toolsmith,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 15 run say villager 15 profession:fletcher,type:taiga
execute if score villager funcs matches 15 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fletcher,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 16 run say villager 16 profession:nitwit,type:savanna
execute if score villager funcs matches 16 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:nitwit,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 17 run say villager 17 profession:weaponsmith,type:desert
execute if score villager funcs matches 17 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:weaponsmith,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 18 run say villager 18 profession:farmer,type:desert
execute if score villager funcs matches 18 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:farmer,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 19 run say villager 19 profession:fisherman,type:snowy
execute if score villager funcs matches 19 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fisherman,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 20 run say villager 20 profession:cartographer,type:savanna
execute if score villager funcs matches 20 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cartographer,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 21 run say villager 21 profession:cartographer,type:plains
execute if score villager funcs matches 21 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cartographer,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 22 run say villager 22 profession:fisherman,type:savanna
execute if score villager funcs matches 22 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fisherman,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 23 run say villager 23 profession:butcher,type:jungle
execute if score villager funcs matches 23 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:butcher,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 24 run say villager 24 profession:cleric,type:desert
execute if score villager funcs matches 24 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cleric,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 25 run say villager 25 profession:shepherd,type:jungle
execute if score villager funcs matches 25 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:shepherd,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 26 run say villager 26 profession:fisherman,type:taiga
execute if score villager funcs matches 26 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fisherman,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 27 run say villager 27 profession:stonemason,type:taiga
execute if score villager funcs matches 27 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:stonemason,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 28 run say villager 28 profession:leatherworker,type:taiga
execute if score villager funcs matches 28 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:leatherworker,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 29 run say villager 29 profession:farmer,type:plains
execute if score villager funcs matches 29 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:farmer,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 30 run say villager 30 profession:cleric,type:plains
execute if score villager funcs matches 30 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cleric,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 31 run say villager 31 profession:stonemason,type:swamp
execute if score villager funcs matches 31 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:stonemason,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 32 run say villager 32 profession:librarian,type:taiga
execute if score villager funcs matches 32 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:librarian,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 33 run say villager 33 profession:stonemason,type:jungle
execute if score villager funcs matches 33 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:stonemason,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 34 run say villager 34 profession:fisherman,type:plains
execute if score villager funcs matches 34 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fisherman,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 35 run say villager 35 profession:butcher,type:swamp
execute if score villager funcs matches 35 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:butcher,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 36 run say villager 36 profession:weaponsmith,type:plains
execute if score villager funcs matches 36 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:weaponsmith,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 37 run say villager 37 profession:cleric,type:savanna
execute if score villager funcs matches 37 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cleric,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 38 run say villager 38 profession:cartographer,type:jungle
execute if score villager funcs matches 38 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cartographer,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 39 run say villager 39 profession:fisherman,type:jungle
execute if score villager funcs matches 39 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fisherman,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 40 run say villager 40 profession:fletcher,type:plains
execute if score villager funcs matches 40 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fletcher,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 41 run say villager 41 profession:butcher,type:taiga
execute if score villager funcs matches 41 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:butcher,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 42 run say villager 42 profession:nitwit,type:jungle
execute if score villager funcs matches 42 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:nitwit,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 43 run say villager 43 profession:armorer,type:snowy
execute if score villager funcs matches 43 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:armorer,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 44 run say villager 44 profession:butcher,type:plains
execute if score villager funcs matches 44 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:butcher,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 45 run say villager 45 profession:librarian,type:jungle
execute if score villager funcs matches 45 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:librarian,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 46 run say villager 46 profession:toolsmith,type:savanna
execute if score villager funcs matches 46 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:toolsmith,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 47 run say villager 47 profession:cleric,type:taiga
execute if score villager funcs matches 47 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cleric,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 48 run say villager 48 profession:butcher,type:snowy
execute if score villager funcs matches 48 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:butcher,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 49 run say villager 49 profession:librarian,type:savanna
execute if score villager funcs matches 49 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:librarian,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 50 run say villager 50 profession:armorer,type:plains
execute if score villager funcs matches 50 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:armorer,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 51 run say villager 51 profession:leatherworker,type:snowy
execute if score villager funcs matches 51 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:leatherworker,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 52 run say villager 52 profession:shepherd,type:snowy
execute if score villager funcs matches 52 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:shepherd,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 53 run say villager 53 profession:unemployed,type:swamp
execute if score villager funcs matches 53 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:unemployed,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 54 run say villager 54 profession:cartographer,type:desert
execute if score villager funcs matches 54 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cartographer,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 55 run say villager 55 profession:fisherman,type:swamp
execute if score villager funcs matches 55 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fisherman,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 56 run say villager 56 profession:farmer,type:snowy
execute if score villager funcs matches 56 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:farmer,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 57 run say villager 57 profession:fletcher,type:snowy
execute if score villager funcs matches 57 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fletcher,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 58 run say villager 58 profession:nitwit,type:desert
execute if score villager funcs matches 58 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:nitwit,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 59 run say villager 59 profession:weaponsmith,type:savanna
execute if score villager funcs matches 59 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:weaponsmith,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 60 run say villager 60 profession:weaponsmith,type:swamp
execute if score villager funcs matches 60 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:weaponsmith,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 61 run say villager 61 profession:toolsmith,type:desert
execute if score villager funcs matches 61 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:toolsmith,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 62 run say villager 62 profession:stonemason,type:savanna
execute if score villager funcs matches 62 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:stonemason,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 63 run say villager 63 profession:unemployed,type:snowy
execute if score villager funcs matches 63 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:unemployed,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 64 run say villager 64 profession:weaponsmith,type:snowy
execute if score villager funcs matches 64 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:weaponsmith,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 65 run say villager 65 profession:fletcher,type:desert
execute if score villager funcs matches 65 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fletcher,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 66 run say villager 66 profession:unemployed,type:savanna
execute if score villager funcs matches 66 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:unemployed,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 67 run say villager 67 profession:unemployed,type:desert
execute if score villager funcs matches 67 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:unemployed,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 68 run say villager 68 profession:toolsmith,type:taiga
execute if score villager funcs matches 68 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:toolsmith,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 69 run say villager 69 profession:nitwit,type:taiga
execute if score villager funcs matches 69 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:nitwit,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 70 run say villager 70 profession:weaponsmith,type:jungle
execute if score villager funcs matches 70 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:weaponsmith,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 71 run say villager 71 profession:cartographer,type:taiga
execute if score villager funcs matches 71 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cartographer,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 72 run say villager 72 profession:librarian,type:plains
execute if score villager funcs matches 72 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:librarian,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 73 run say villager 73 profession:unemployed,type:taiga
execute if score villager funcs matches 73 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:unemployed,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 74 run say villager 74 profession:weaponsmith,type:taiga
execute if score villager funcs matches 74 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:weaponsmith,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 75 run say villager 75 profession:leatherworker,type:swamp
execute if score villager funcs matches 75 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:leatherworker,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 76 run say villager 76 profession:armorer,type:savanna
execute if score villager funcs matches 76 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:armorer,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 77 run say villager 77 profession:leatherworker,type:savanna
execute if score villager funcs matches 77 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:leatherworker,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 78 run say villager 78 profession:fletcher,type:jungle
execute if score villager funcs matches 78 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fletcher,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 79 run say villager 79 profession:librarian,type:snowy
execute if score villager funcs matches 79 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:librarian,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 80 run say villager 80 profession:fletcher,type:swamp
execute if score villager funcs matches 80 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fletcher,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 81 run say villager 81 profession:cartographer,type:swamp
execute if score villager funcs matches 81 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cartographer,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 82 run say villager 82 profession:shepherd,type:swamp
execute if score villager funcs matches 82 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:shepherd,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 83 run say villager 83 profession:toolsmith,type:jungle
execute if score villager funcs matches 83 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:toolsmith,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 84 run say villager 84 profession:fisherman,type:desert
execute if score villager funcs matches 84 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:fisherman,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 85 run say villager 85 profession:leatherworker,type:plains
execute if score villager funcs matches 85 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:leatherworker,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 86 run say villager 86 profession:leatherworker,type:jungle
execute if score villager funcs matches 86 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:leatherworker,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 87 run say villager 87 profession:leatherworker,type:desert
execute if score villager funcs matches 87 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:leatherworker,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 88 run say villager 88 profession:stonemason,type:plains
execute if score villager funcs matches 88 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:stonemason,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 89 run say villager 89 profession:cleric,type:jungle
execute if score villager funcs matches 89 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cleric,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 90 run say villager 90 profession:librarian,type:swamp
execute if score villager funcs matches 90 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:librarian,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 91 run say villager 91 profession:shepherd,type:plains
execute if score villager funcs matches 91 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:shepherd,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 92 run say villager 92 profession:nitwit,type:snowy
execute if score villager funcs matches 92 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:nitwit,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 93 run say villager 93 profession:cleric,type:swamp
execute if score villager funcs matches 93 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cleric,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 94 run say villager 94 profession:farmer,type:taiga
execute if score villager funcs matches 94 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:farmer,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 95 run say villager 95 profession:armorer,type:swamp
execute if score villager funcs matches 95 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:armorer,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 96 run say villager 96 profession:cartographer,type:snowy
execute if score villager funcs matches 96 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cartographer,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 97 run say villager 97 profession:unemployed,type:plains
execute if score villager funcs matches 97 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:unemployed,type:plains},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 98 run say villager 98 profession:farmer,type:jungle
execute if score villager funcs matches 98 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:farmer,type:jungle},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 99 run say villager 99 profession:farmer,type:savanna
execute if score villager funcs matches 99 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:farmer,type:savanna},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 100 run say villager 100 profession:shepherd,type:taiga
execute if score villager funcs matches 100 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:shepherd,type:taiga},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 101 run say villager 101 profession:cleric,type:snowy
execute if score villager funcs matches 101 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:cleric,type:snowy},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 102 run say villager 102 profession:nitwit,type:swamp
execute if score villager funcs matches 102 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:nitwit,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 103 run say villager 103 profession:farmer,type:swamp
execute if score villager funcs matches 103 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:farmer,type:swamp},NoAI:True,Tags:[effecter],PersistenceRequired:True}


execute if score villager funcs matches 104 run say villager 104 profession:butcher,type:desert
execute if score villager funcs matches 104 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:butcher,type:desert},NoAI:True,Tags:[effecter],PersistenceRequired:True}
