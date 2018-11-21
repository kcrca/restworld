



execute unless score 3_firsh funcs matches 0.. run function 3_firsh_init
scoreboard players add 3_firsh funcs 1
execute unless score 3_firsh funcs matches 0..2 run scoreboard players set 3_firsh funcs 0

execute if score 3_firsh funcs matches 0 run data merge entity @e[tag=sunstreak,limit=1] {Variant:134217984,CustomName:"\"White-Silver Sunstreak\""}


execute if score 3_firsh funcs matches 1 run data merge entity @e[tag=sunstreak,limit=1] {Variant:50790656,CustomName:"\"Gray-Sky SunStreak\""}


execute if score 3_firsh funcs matches 2 run data merge entity @e[tag=sunstreak,limit=1] {Variant:118161664,CustomName:"\"Blue-Gray SunStreak\""}


