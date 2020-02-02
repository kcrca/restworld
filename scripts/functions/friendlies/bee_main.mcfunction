execute unless score bee funcs matches 0.. run function bee_init
scoreboard players add bee funcs 1
scoreboard players set bee max 4
execute unless score bee funcs matches 0..3 run scoreboard players operation bee funcs %= bee max
    execute if score bee funcs matches 0 run execute at @e[tag=bee_home] run setblock ~2 ~3 ~ beehive[facing=west] replace
    execute if score bee funcs matches 2 run execute at @e[tag=bee_home] run setblock ~2 ~3 ~ bee_nest[facing=west] replace
execute if score bee funcs matches 0 run execute as @e[tag=bee] run data merge entity @s {Anger:0,CustomName:"\"Bee\""}

execute if score bee funcs matches 1 run execute as @e[tag=bee] run data merge entity @s {Anger:100000,CustomName:"\"Angry Bee\""}

execute if score bee funcs matches 2 run execute as @e[tag=bee] run data merge entity @s {Anger:0,CustomName:"\"Bee\""}

execute if score bee funcs matches 3 run execute as @e[tag=bee] run data merge entity @s {Anger:100000,CustomName:"\"Angry Bee\""}
