scoreboard players add 2_fish funcs 0
scoreboard players add 3_fish funcs 0
scoreboard players add all_fish funcs 0
scoreboard players add conduit funcs 0
scoreboard players add elder_guardian funcs 0
scoreboard players add fishies funcs 0
scoreboard players add guardian funcs 0
scoreboard players add tropical_fish funcs 0

tp @e[tag=acquatic] @e[tag=death,limit=1]


execute at @e[tag=all_fish_home] run function v3:acquatic/all_fish_init
execute at @e[tag=elder_guardian_home] run function v3:acquatic/elder_guardian_init
execute at @e[tag=fishies_home] run function v3:acquatic/fishies_init
execute at @e[tag=guardian_home] run function v3:acquatic/guardian_init
execute at @e[tag=tropical_fish_home] run function v3:acquatic/tropical_fish_init
