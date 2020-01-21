scoreboard players set bee max 2
execute unless score bee funcs matches 0..1 run scoreboard players operation bee funcs %= bee max
execute if score bee funcs matches 0 run execute as @e[tag=bee] run data merge entity @s {Anger:0}

execute if score bee funcs matches 1 run execute as @e[tag=bee] run data merge entity @s {Anger:100000}
