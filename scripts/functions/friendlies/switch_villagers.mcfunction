scoreboard players set which_villagers funcs 0
execute if score cur_villager_group funcs matches 1 run scoreboard players add which_villagers funcs 1
execute if score cur_villager_zombies funcs matches 1 run scoreboard players add which_villagers funcs 2

execute unless score which_villagers funcs = which_villagers_prev funcs run tp @e[tag=villager] @e[tag=death,limit=1]

scoreboard players operation which_villagers_prev funcs = which_villagers funcs
execute if score which_villagers funcs matches 0 at @e[tag=cur_villagers_home] run function v3:friendlies/villager_professions_init
execute if score which_villagers funcs matches 1 at @e[tag=cur_villagers_home] run function v3:friendlies/villager_types_init
execute if score which_villagers funcs matches 2 at @e[tag=cur_villagers_home] run function v3:friendlies/zombie_professions_init
execute if score which_villagers funcs matches 3 at @e[tag=cur_villagers_home] run function v3:friendlies/zombie_types_init

execute if score cur_villager_levels funcs matches 1 run scoreboard players add which_villagers funcs 4
kill @e[tag=cur_villagers_home]
execute if score which_villagers funcs matches 0 at @e[tag=which_villagers_home,limit=1] run summon armor_stand ~ ~ ~1 {Tags:[villager_professions_home,cur_villagers_home],Small:True,NoGravity:True}
execute if score which_villagers funcs matches 1 at @e[tag=which_villagers_home,limit=1] run summon armor_stand ~ ~ ~1 {Tags:[villager_types_home,cur_villagers_home],Small:True,NoGravity:True}
execute if score which_villagers funcs matches 2 at @e[tag=which_villagers_home,limit=1] run summon armor_stand ~ ~ ~1 {Tags:[zombie_professions_home,cur_villagers_home],Small:True,NoGravity:True}
execute if score which_villagers funcs matches 3 at @e[tag=which_villagers_home,limit=1] run summon armor_stand ~ ~ ~1 {Tags:[zombie_types_home,cur_villagers_home],Small:True,NoGravity:True}
execute if score which_villagers funcs matches 4..5 at @e[tag=which_villagers_home,limit=1] run summon armor_stand ~ ~ ~1 {Tags:[villager_levels_home,cur_villagers_home],Small:True,NoGravity:True}
