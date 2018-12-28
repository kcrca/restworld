scoreboard players add tick funcs 0

tp @e[tag=diy] @e[tag=death,limit=1]


execute at @e[tag=tick_home] run function v3:diy/tick_init
