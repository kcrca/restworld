scoreboard players set 2_fish max 2
execute unless score 2_fish funcs matches 0..1 run scoreboard players operation 2_fish funcs %= 2_fish max

execute if score 2_fish funcs matches 0 run data merge entity @e[tag=kob,limit=1] {Variant:917504,CustomName:"\"Red-White Kob\""}
execute if score 2_fish funcs matches 0 run data merge entity @e[tag=dasher,limit=1] {Variant:117441280,CustomName:"\"White-Gray Dasher\""}
execute if score 2_fish funcs matches 0 run data merge entity @e[tag=brinely,limit=1] {Variant:117441536,CustomName:"\"White-Gray Brinely\""}
execute if score 2_fish funcs matches 0 run data merge entity @e[tag=spotty,limit=1] {Variant:67110144,CustomName:"\"White-Yellow Spotter\""}
execute if score 2_fish funcs matches 0 run data merge entity @e[tag=flopper,limit=1] {Variant:117899265,CustomName:"\"Gray Flopper\""}
execute if score 2_fish funcs matches 0 run data merge entity @e[tag=stripey,limit=1] {Variant:117506305,CustomName:"\"Orange-Gray Stripey\""}
execute if score 2_fish funcs matches 0 run data merge entity @e[tag=blockfish,limit=1] {Variant:67764993,CustomName:"\"Plum-Yellow Blockfish\""}
execute if score 2_fish funcs matches 0 run data merge entity @e[tag=clayfish,limit=1] {Variant:234882305,CustomName:"\"White-Red Clayfish\""}


execute if score 2_fish funcs matches 1 run data merge entity @e[tag=kob,limit=1] {Variant:65536,CustomName:"\"Orange-White Kob\""}
execute if score 2_fish funcs matches 1 run data merge entity @e[tag=dasher,limit=1] {Variant:101253888,CustomName:"\"Teal-Rose Dasher\""}
execute if score 2_fish funcs matches 1 run data merge entity @e[tag=brinely,limit=1] {Variant:50660352,CustomName:"\"Line-Sky Dasher\""}
execute if score 2_fish funcs matches 1 run data merge entity @e[tag=spotty,limit=1] {Variant:50726144,CustomName:"\"Rose-Sky Spotty\""}
execute if score 2_fish funcs matches 1 run data merge entity @e[tag=flopper,limit=1] {Variant:67108865,CustomName:"\"White-Yellow Flopper\""}
execute if score 2_fish funcs matches 1 run data merge entity @e[tag=stripey,limit=1] {Variant:67371265,CustomName:"\"Yellow Stripey\""}
execute if score 2_fish funcs matches 1 run data merge entity @e[tag=blockfish,limit=1] {Variant:918273,CustomName:"\"Red-White Blockfish\""}
execute if score 2_fish funcs matches 1 run data merge entity @e[tag=clayfish,limit=1] {Variant:16778497,CustomName:"\"White-Orange Clayfish\""}
