scoreboard players add basic funcs 0
scoreboard players add fencelike funcs 0
scoreboard players add fences funcs 0
scoreboard players add ores funcs 0
scoreboard players add panes funcs 0
scoreboard players add walls funcs 0
scoreboard players add wood funcs 0

tp @e[tag=materials] @e[tag=death,limit=1]


execute at @e[tag=basic_home] run function v3:materials/basic_init
execute at @e[tag=fencelike_home] run function v3:materials/fencelike_init
execute at @e[tag=wood_home] run function v3:materials/wood_init
