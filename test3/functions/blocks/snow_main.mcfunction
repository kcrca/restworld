execute unless score snow funcs matches 0.. run function snow_init
scoreboard players add snow funcs 1
scoreboard players set snow max 14
execute unless score snow funcs matches 0..13 run scoreboard players operation snow funcs %= snow max

execute if score snow funcs matches 0 run setblock ~ ~4 ~ snow[layers=1]

execute if score snow funcs matches 1 run setblock ~ ~4 ~ snow[layers=2]

execute if score snow funcs matches 2 run setblock ~ ~4 ~ snow[layers=3]

execute if score snow funcs matches 3 run setblock ~ ~4 ~ snow[layers=4]

execute if score snow funcs matches 4 run setblock ~ ~4 ~ snow[layers=5]

execute if score snow funcs matches 5 run setblock ~ ~4 ~ snow[layers=6]

execute if score snow funcs matches 6 run setblock ~ ~4 ~ snow[layers=7]

execute if score snow funcs matches 7 run setblock ~ ~4 ~ snow[layers=8]

execute if score snow funcs matches 8 run setblock ~ ~4 ~ snow[layers=7]

execute if score snow funcs matches 9 run setblock ~ ~4 ~ snow[layers=6]

execute if score snow funcs matches 10 run setblock ~ ~4 ~ snow[layers=5]

execute if score snow funcs matches 11 run setblock ~ ~4 ~ snow[layers=4]

execute if score snow funcs matches 12 run setblock ~ ~4 ~ snow[layers=3]

execute if score snow funcs matches 13 run setblock ~ ~4 ~ snow[layers=2]