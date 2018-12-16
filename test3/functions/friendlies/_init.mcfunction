scoreboard players add canine funcs 0
scoreboard players add chicken funcs 0
scoreboard players add colored_mobs funcs 0
scoreboard players add cow funcs 0
scoreboard players add horse funcs 0
scoreboard players add horse_armors funcs 0
scoreboard players add horselike funcs 0
scoreboard players add iron_golem funcs 0
scoreboard players add llamas_carpets funcs 0
scoreboard players add mobs_east funcs 0
scoreboard players add ocelot funcs 0
scoreboard players add parrot funcs 0
scoreboard players add pig funcs 0
scoreboard players add polar_bear funcs 0
scoreboard players add rabbits funcs 0
scoreboard players add sheep funcs 0
scoreboard players add snow_golem funcs 0
scoreboard players add turtle funcs 0
scoreboard players add turtle_eggs funcs 0
scoreboard players add villagers funcs 0

tp @e[tag=friendlies] @e[tag=death,limit=1]


execute at @e[tag=canine_home] run function v3:friendlies/canine_init
execute at @e[tag=chicken_home] run function v3:friendlies/chicken_init
execute at @e[tag=horse_home] run function v3:friendlies/horse_init
execute at @e[tag=horselike_home] run function v3:friendlies/horselike_init
execute at @e[tag=iron_golem_home] run function v3:friendlies/iron_golem_init
execute at @e[tag=mobs_east_home] run function v3:friendlies/mobs_east_init
execute at @e[tag=ocelot_home] run function v3:friendlies/ocelot_init
execute at @e[tag=parrot_home] run function v3:friendlies/parrot_init
execute at @e[tag=pig_home] run function v3:friendlies/pig_init
execute at @e[tag=polar_bear_home] run function v3:friendlies/polar_bear_init
execute at @e[tag=sheep_home] run function v3:friendlies/sheep_init
execute at @e[tag=snow_golem_home] run function v3:friendlies/snow_golem_init
execute at @e[tag=turtle_home] run function v3:friendlies/turtle_init
