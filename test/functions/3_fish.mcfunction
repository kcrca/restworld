



execute unless score 3_fish funcs matches 0.. run function 3_fish_init
scoreboard players add 3_fish funcs 1
execute unless score 3_fish funcs matches 0..2 run scoreboard players set 3_fish funcs 0

execute if score 3_fish funcs matches 0 run data merge entity @e[tag=sunstreak,limit=1] {Variant:134217984,CustomName:"\"White-Silver Sunstreak\""}


execute if score 3_fish funcs matches 1 run data merge entity @e[tag=sunstreak,limit=1] {Variant:50790656,CustomName:"\"Gray-Sky SunStreak\""}


execute if score 3_fish funcs matches 2 run data merge entity @e[tag=sunstreak,limit=1] {Variant:118161664,CustomName:"\"Blue-Gray SunStreak\""}


