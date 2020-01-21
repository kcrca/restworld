execute unless score villager funcs matches 0.. run function villager_init
scoreboard players add villager funcs 1
scoreboard players set villager max 105
execute unless score villager funcs matches 0..104 run scoreboard players operation villager funcs %= villager max

execute if score villager funcs matches 0 run say villager 0 profession:Nitwit,type:Swamp
execute if score villager funcs matches 0 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Nitwit,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 1 run say villager 1 profession:Butcher,type:Taiga
execute if score villager funcs matches 1 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Butcher,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 2 run say villager 2 profession:Farmer,type:Taiga
execute if score villager funcs matches 2 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Farmer,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 3 run say villager 3 profession:Cleric,type:Taiga
execute if score villager funcs matches 3 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cleric,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 4 run say villager 4 profession:Cartographer,type:Plains
execute if score villager funcs matches 4 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cartographer,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 5 run say villager 5 profession:Toolsmith,type:Jungle
execute if score villager funcs matches 5 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Toolsmith,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 6 run say villager 6 profession:Cartographer,type:Taiga
execute if score villager funcs matches 6 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cartographer,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 7 run say villager 7 profession:Mason,type:Snow
execute if score villager funcs matches 7 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Mason,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 8 run say villager 8 profession:Mason,type:Plains
execute if score villager funcs matches 8 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Mason,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 9 run say villager 9 profession:Butcher,type:Savanna
execute if score villager funcs matches 9 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Butcher,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 10 run say villager 10 profession:Toolsmith,type:Swamp
execute if score villager funcs matches 10 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Toolsmith,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 11 run say villager 11 profession:Fletcher,type:Taiga
execute if score villager funcs matches 11 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fletcher,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 12 run say villager 12 profession:Weaponsmith,type:Jungle
execute if score villager funcs matches 12 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Weaponsmith,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 13 run say villager 13 profession:Cartographer,type:Snow
execute if score villager funcs matches 13 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cartographer,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 14 run say villager 14 profession:Weaponsmith,type:Desert
execute if score villager funcs matches 14 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Weaponsmith,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 15 run say villager 15 profession:Shepherd,type:Savanna
execute if score villager funcs matches 15 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Shepherd,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 16 run say villager 16 profession:Cartographer,type:Savanna
execute if score villager funcs matches 16 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cartographer,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 17 run say villager 17 profession:Armorer,type:Savanna
execute if score villager funcs matches 17 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Armorer,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 18 run say villager 18 profession:Shepherd,type:Plains
execute if score villager funcs matches 18 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Shepherd,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 19 run say villager 19 profession:Weaponsmith,type:Snow
execute if score villager funcs matches 19 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Weaponsmith,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 20 run say villager 20 profession:Librarian,type:Savanna
execute if score villager funcs matches 20 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Librarian,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 21 run say villager 21 profession:Fisherman,type:Plains
execute if score villager funcs matches 21 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fisherman,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 22 run say villager 22 profession:Butcher,type:Desert
execute if score villager funcs matches 22 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Butcher,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 23 run say villager 23 profession:Librarian,type:Jungle
execute if score villager funcs matches 23 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Librarian,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 24 run say villager 24 profession:Leatherworker,type:Desert
execute if score villager funcs matches 24 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Leatherworker,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 25 run say villager 25 profession:Leatherworker,type:Jungle
execute if score villager funcs matches 25 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Leatherworker,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 26 run say villager 26 profession:Armorer,type:Desert
execute if score villager funcs matches 26 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Armorer,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 27 run say villager 27 profession:Weaponsmith,type:Plains
execute if score villager funcs matches 27 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Weaponsmith,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 28 run say villager 28 profession:Leatherworker,type:Taiga
execute if score villager funcs matches 28 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Leatherworker,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 29 run say villager 29 profession:Librarian,type:Snow
execute if score villager funcs matches 29 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Librarian,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 30 run say villager 30 profession:Unemployed,type:Desert
execute if score villager funcs matches 30 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Unemployed,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 31 run say villager 31 profession:Unemployed,type:Snow
execute if score villager funcs matches 31 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Unemployed,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 32 run say villager 32 profession:Shepherd,type:Taiga
execute if score villager funcs matches 32 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Shepherd,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 33 run say villager 33 profession:Weaponsmith,type:Swamp
execute if score villager funcs matches 33 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Weaponsmith,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 34 run say villager 34 profession:Mason,type:Taiga
execute if score villager funcs matches 34 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Mason,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 35 run say villager 35 profession:Fletcher,type:Swamp
execute if score villager funcs matches 35 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fletcher,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 36 run say villager 36 profession:Mason,type:Swamp
execute if score villager funcs matches 36 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Mason,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 37 run say villager 37 profession:Unemployed,type:Taiga
execute if score villager funcs matches 37 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Unemployed,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 38 run say villager 38 profession:Shepherd,type:Swamp
execute if score villager funcs matches 38 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Shepherd,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 39 run say villager 39 profession:Shepherd,type:Desert
execute if score villager funcs matches 39 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Shepherd,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 40 run say villager 40 profession:Nitwit,type:Snow
execute if score villager funcs matches 40 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Nitwit,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 41 run say villager 41 profession:Farmer,type:Swamp
execute if score villager funcs matches 41 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Farmer,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 42 run say villager 42 profession:Farmer,type:Savanna
execute if score villager funcs matches 42 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Farmer,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 43 run say villager 43 profession:Cleric,type:Plains
execute if score villager funcs matches 43 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cleric,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 44 run say villager 44 profession:Fisherman,type:Savanna
execute if score villager funcs matches 44 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fisherman,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 45 run say villager 45 profession:Leatherworker,type:Swamp
execute if score villager funcs matches 45 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Leatherworker,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 46 run say villager 46 profession:Fletcher,type:Desert
execute if score villager funcs matches 46 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fletcher,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 47 run say villager 47 profession:Nitwit,type:Jungle
execute if score villager funcs matches 47 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Nitwit,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 48 run say villager 48 profession:Nitwit,type:Plains
execute if score villager funcs matches 48 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Nitwit,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 49 run say villager 49 profession:Shepherd,type:Snow
execute if score villager funcs matches 49 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Shepherd,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 50 run say villager 50 profession:Cleric,type:Desert
execute if score villager funcs matches 50 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cleric,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 51 run say villager 51 profession:Cartographer,type:Swamp
execute if score villager funcs matches 51 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cartographer,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 52 run say villager 52 profession:Farmer,type:Desert
execute if score villager funcs matches 52 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Farmer,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 53 run say villager 53 profession:Toolsmith,type:Snow
execute if score villager funcs matches 53 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Toolsmith,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 54 run say villager 54 profession:Librarian,type:Desert
execute if score villager funcs matches 54 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Librarian,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 55 run say villager 55 profession:Cartographer,type:Desert
execute if score villager funcs matches 55 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cartographer,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 56 run say villager 56 profession:Nitwit,type:Desert
execute if score villager funcs matches 56 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Nitwit,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 57 run say villager 57 profession:Unemployed,type:Jungle
execute if score villager funcs matches 57 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Unemployed,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 58 run say villager 58 profession:Toolsmith,type:Taiga
execute if score villager funcs matches 58 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Toolsmith,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 59 run say villager 59 profession:Fletcher,type:Savanna
execute if score villager funcs matches 59 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fletcher,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 60 run say villager 60 profession:Armorer,type:Taiga
execute if score villager funcs matches 60 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Armorer,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 61 run say villager 61 profession:Toolsmith,type:Plains
execute if score villager funcs matches 61 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Toolsmith,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 62 run say villager 62 profession:Fletcher,type:Plains
execute if score villager funcs matches 62 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fletcher,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 63 run say villager 63 profession:Librarian,type:Swamp
execute if score villager funcs matches 63 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Librarian,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 64 run say villager 64 profession:Butcher,type:Swamp
execute if score villager funcs matches 64 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Butcher,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 65 run say villager 65 profession:Fisherman,type:Snow
execute if score villager funcs matches 65 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fisherman,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 66 run say villager 66 profession:Fisherman,type:Swamp
execute if score villager funcs matches 66 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fisherman,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 67 run say villager 67 profession:Mason,type:Savanna
execute if score villager funcs matches 67 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Mason,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 68 run say villager 68 profession:Librarian,type:Plains
execute if score villager funcs matches 68 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Librarian,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 69 run say villager 69 profession:Cleric,type:Jungle
execute if score villager funcs matches 69 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cleric,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 70 run say villager 70 profession:Fisherman,type:Jungle
execute if score villager funcs matches 70 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fisherman,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 71 run say villager 71 profession:Armorer,type:Jungle
execute if score villager funcs matches 71 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Armorer,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 72 run say villager 72 profession:Farmer,type:Jungle
execute if score villager funcs matches 72 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Farmer,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 73 run say villager 73 profession:Weaponsmith,type:Savanna
execute if score villager funcs matches 73 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Weaponsmith,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 74 run say villager 74 profession:Nitwit,type:Savanna
execute if score villager funcs matches 74 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Nitwit,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 75 run say villager 75 profession:Cleric,type:Snow
execute if score villager funcs matches 75 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cleric,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 76 run say villager 76 profession:Nitwit,type:Taiga
execute if score villager funcs matches 76 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Nitwit,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 77 run say villager 77 profession:Armorer,type:Plains
execute if score villager funcs matches 77 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Armorer,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 78 run say villager 78 profession:Fletcher,type:Snow
execute if score villager funcs matches 78 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fletcher,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 79 run say villager 79 profession:Mason,type:Desert
execute if score villager funcs matches 79 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Mason,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 80 run say villager 80 profession:Butcher,type:Jungle
execute if score villager funcs matches 80 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Butcher,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 81 run say villager 81 profession:Fisherman,type:Desert
execute if score villager funcs matches 81 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fisherman,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 82 run say villager 82 profession:Toolsmith,type:Savanna
execute if score villager funcs matches 82 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Toolsmith,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 83 run say villager 83 profession:Armorer,type:Snow
execute if score villager funcs matches 83 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Armorer,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 84 run say villager 84 profession:Weaponsmith,type:Taiga
execute if score villager funcs matches 84 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Weaponsmith,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 85 run say villager 85 profession:Armorer,type:Swamp
execute if score villager funcs matches 85 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Armorer,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 86 run say villager 86 profession:Toolsmith,type:Desert
execute if score villager funcs matches 86 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Toolsmith,type:Desert},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 87 run say villager 87 profession:Shepherd,type:Jungle
execute if score villager funcs matches 87 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Shepherd,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 88 run say villager 88 profession:Farmer,type:Snow
execute if score villager funcs matches 88 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Farmer,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 89 run say villager 89 profession:Fisherman,type:Taiga
execute if score villager funcs matches 89 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fisherman,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 90 run say villager 90 profession:Cartographer,type:Jungle
execute if score villager funcs matches 90 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cartographer,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 91 run say villager 91 profession:Fletcher,type:Jungle
execute if score villager funcs matches 91 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Fletcher,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 92 run say villager 92 profession:Cleric,type:Swamp
execute if score villager funcs matches 92 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cleric,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 93 run say villager 93 profession:Farmer,type:Plains
execute if score villager funcs matches 93 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Farmer,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 94 run say villager 94 profession:Leatherworker,type:Snow
execute if score villager funcs matches 94 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Leatherworker,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 95 run say villager 95 profession:Unemployed,type:Swamp
execute if score villager funcs matches 95 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Unemployed,type:Swamp},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 96 run say villager 96 profession:Unemployed,type:Plains
execute if score villager funcs matches 96 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Unemployed,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 97 run say villager 97 profession:Butcher,type:Snow
execute if score villager funcs matches 97 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Butcher,type:Snow},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 98 run say villager 98 profession:Cleric,type:Savanna
execute if score villager funcs matches 98 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Cleric,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 99 run say villager 99 profession:Leatherworker,type:Plains
execute if score villager funcs matches 99 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Leatherworker,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 100 run say villager 100 profession:Unemployed,type:Savanna
execute if score villager funcs matches 100 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Unemployed,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 101 run say villager 101 profession:Butcher,type:Plains
execute if score villager funcs matches 101 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Butcher,type:Plains},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 102 run say villager 102 profession:Leatherworker,type:Savanna
execute if score villager funcs matches 102 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Leatherworker,type:Savanna},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 103 run say villager 103 profession:Librarian,type:Taiga
execute if score villager funcs matches 103 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Librarian,type:Taiga},NoAI:True,Tags:[particler],PersistenceRequired:True}


execute if score villager funcs matches 104 run say villager 104 profession:Mason,type:Jungle
execute if score villager funcs matches 104 run summon minecraft:villager ~0 ~0 ~0 {VillagerData:{profession:Mason,type:Jungle},NoAI:True,Tags:[particler],PersistenceRequired:True}
