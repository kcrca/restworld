scoreboard players set pig max 2
execute unless score pig funcs matches 0..1 run scoreboard players operation pig funcs %= pig max

execute if score pig funcs matches 0 run execute as @e[tag=pig,tag=!kid] run data merge entity @s {Saddle:0}
execute if score pig funcs matches 1 run execute as @e[tag=pig,tag=!kid] run data merge entity @s {Saddle:1}
