scoreboard players add cave_spider funcs 0
scoreboard players add creeper funcs 0
scoreboard players add fangs funcs 0
scoreboard players add growing funcs 0
scoreboard players add illager funcs 0
scoreboard players add phantom funcs 0
scoreboard players add silverfish funcs 0
scoreboard players add skeleton funcs 0
scoreboard players add skeleton_horse funcs 0
scoreboard players add slime funcs 0
scoreboard players add spider funcs 0
scoreboard players add witch funcs 0
scoreboard players add zombie funcs 0
scoreboard players add zombie_horse funcs 0
scoreboard players add zombie_jockey funcs 0

tp @e[tag=monsters] @e[tag=death,limit=1]


execute at @e[tag=cave_spider_home] run function v3:monsters/cave_spider_init
execute at @e[tag=creeper_home] run function v3:monsters/creeper_init
execute at @e[tag=illager_home] run function v3:monsters/illager_init
execute at @e[tag=phantom_home] run function v3:monsters/phantom_init
execute at @e[tag=silverfish_home] run function v3:monsters/silverfish_init
execute at @e[tag=skeleton_horse_home] run function v3:monsters/skeleton_horse_init
execute at @e[tag=slime_home] run function v3:monsters/slime_init
execute at @e[tag=spider_home] run function v3:monsters/spider_init
execute at @e[tag=witch_home] run function v3:monsters/witch_init
execute at @e[tag=zombie_horse_home] run function v3:monsters/zombie_horse_init
