scoreboard players add fencelike funcs 0
scoreboard players add fences funcs 0
scoreboard players add materials funcs 0
scoreboard players add panes funcs 0
scoreboard players add walls funcs 0
scoreboard players add wood funcs 0

execute at @e[tag=fencelike_home] run function v3:materials/fencelike_init
execute at @e[tag=materials_home] run function v3:materials/materials_init
execute at @e[tag=wood_home] run function v3:materials/wood_init
