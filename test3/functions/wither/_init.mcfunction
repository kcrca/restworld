scoreboard players add painting funcs 0
scoreboard players add wither funcs 0
scoreboard players add wither_skull funcs 0

tp @e[tag=wither] @e[tag=death,limit=1]


execute at @e[tag=painting_home] run function v3:wither/painting_init
execute at @e[tag=wither_home] run function v3:wither/wither_init
execute at @e[tag=wither_skull_home] run function v3:wither/wither_skull_init
