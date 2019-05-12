scoreboard players set villager_types max 16
execute unless score villager_types funcs matches 0..15 run scoreboard players operation villager_types funcs %= villager_types max

execute if score villager_types funcs matches 0 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value armorer
execute if score villager_types funcs matches 0 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 0 run data modify block ~-5 ~2 ~0 Text2 set value "\"Armorer\""


execute if score villager_types funcs matches 1 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value butcher
execute if score villager_types funcs matches 1 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 1 run data modify block ~-5 ~2 ~0 Text2 set value "\"Butcher\""


execute if score villager_types funcs matches 2 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value cartographer
execute if score villager_types funcs matches 2 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 2 run data modify block ~-5 ~2 ~0 Text2 set value "\"Cartographer\""


execute if score villager_types funcs matches 3 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value cleric
execute if score villager_types funcs matches 3 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 3 run data modify block ~-5 ~2 ~0 Text2 set value "\"Cleric\""


execute if score villager_types funcs matches 4 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value farmer
execute if score villager_types funcs matches 4 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 4 run data modify block ~-5 ~2 ~0 Text2 set value "\"Farmer\""


execute if score villager_types funcs matches 5 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value fisherman
execute if score villager_types funcs matches 5 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 5 run data modify block ~-5 ~2 ~0 Text2 set value "\"Fisherman\""


execute if score villager_types funcs matches 6 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value fletcher
execute if score villager_types funcs matches 6 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 6 run data modify block ~-5 ~2 ~0 Text2 set value "\"Fletcher\""


execute if score villager_types funcs matches 7 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value leatherworker
execute if score villager_types funcs matches 7 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 7 run data modify block ~-5 ~2 ~0 Text2 set value "\"Leatherworker\""


execute if score villager_types funcs matches 8 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value librarian
execute if score villager_types funcs matches 8 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 8 run data modify block ~-5 ~2 ~0 Text2 set value "\"Librarian\""


execute if score villager_types funcs matches 9 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value mason
execute if score villager_types funcs matches 9 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 9 run data modify block ~-5 ~2 ~0 Text2 set value "\"Mason\""


execute if score villager_types funcs matches 10 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value nitwit
execute if score villager_types funcs matches 10 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 10 run data modify block ~-5 ~2 ~0 Text2 set value "\"Nitwit\""


execute if score villager_types funcs matches 11 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value shepherd
execute if score villager_types funcs matches 11 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 11 run data modify block ~-5 ~2 ~0 Text2 set value "\"Shepherd\""


execute if score villager_types funcs matches 12 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value toolsmith
execute if score villager_types funcs matches 12 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 12 run data modify block ~-5 ~2 ~0 Text2 set value "\"Toolsmith\""


execute if score villager_types funcs matches 13 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value weaponsmith
execute if score villager_types funcs matches 13 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 13 run data modify block ~-5 ~2 ~0 Text2 set value "\"Weaponsmith\""


execute if score villager_types funcs matches 14 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value unemployed
execute if score villager_types funcs matches 14 run execute as @e[tag=villager] run data modify entity @s Age set value 21474836487
execute if score villager_types funcs matches 14 run data modify block ~-5 ~2 ~0 Text2 set value "\"Unemployed\""


execute if score villager_types funcs matches 15 run execute as @e[tag=zombie_villager,limit=1] run scoreboard players set villager_types funcs 0
execute if score villager_types funcs matches 15 run execute as @e[tag=villager] run data modify entity @s VillagerData.profession set value child
execute if score villager_types funcs matches 15 run execute as @e[tag=villager] run data modify entity @s Age set value -2147483648
execute if score villager_types funcs matches 15 run data modify block ~-5 ~2 ~0 Text2 set value "\"Child\""
