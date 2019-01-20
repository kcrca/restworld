scoreboard players set snow_golem max 2
execute unless score snow_golem funcs matches 0..1 run scoreboard players operation snow_golem funcs %= snow_golem max

execute if score snow_golem funcs matches 0 run execute as @e[tag=snow_golem] run data merge entity @s {Pumpkin:1}
execute if score snow_golem funcs matches 1 run execute as @e[tag=snow_golem] run data merge entity @s {Pumpkin:0}
