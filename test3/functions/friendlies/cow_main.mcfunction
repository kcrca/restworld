tp @e[tag=cowish] @e[tag=death,limit=1]


execute unless score cow funcs matches 0.. run function cow_init
scoreboard players add cow funcs 1
scoreboard players set cow max 2
execute unless score cow funcs matches 0..1 run scoreboard players operation cow funcs %= cow max

execute if score cow funcs matches 0 run function v3:friendlies/do_cow
execute if score cow funcs matches 1 run function v3:friendlies/do_mooshroom
