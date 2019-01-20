scoreboard players add example_painting funcs 0
scoreboard players add lights funcs 0
scoreboard players add mobs_east funcs 0
scoreboard players add mobs_west funcs 0

tp @e[tag=center] @e[tag=death,limit=1]


execute at @e[tag=example_painting_home] run function v3:center/example_painting_init
execute at @e[tag=mobs_east_home] run function v3:center/mobs_east_init
execute at @e[tag=mobs_west_home] run function v3:center/mobs_west_init
