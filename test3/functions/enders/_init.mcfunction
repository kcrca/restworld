scoreboard players add crystal funcs 0
scoreboard players add dragon funcs 0
scoreboard players add end_portal funcs 0

tp @e[tag=enders] @e[tag=death,limit=1]


execute at @e[tag=dragon_home] run function v3:enders/dragon_init
