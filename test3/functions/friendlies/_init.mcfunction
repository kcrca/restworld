scoreboard players add mobs_east funcs 0
scoreboard players add parrot funcs 0
scoreboard players add turtle funcs 0
scoreboard players add turtle_eggs funcs 0

tp @e[tag=friendlies] @e[tag=death,limit=1]


execute at @e[tag=mobs_east_home] run function v3:friendlies/mobs_east_init
execute at @e[tag=parrot_home] run function v3:friendlies/parrot_init
execute at @e[tag=turtle_home] run function v3:friendlies/turtle_init
