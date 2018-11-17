





execute unless score fire funcs matches -1.. run function fire_init
scoreboard players add fire funcs 1
execute unless score fire funcs matches 0..13 run scoreboard players set fire funcs 0



execute if score fire funcs matches 0 run setblock ~ ~3 ~ minecraft:air


execute if score fire funcs matches 1 run setblock ~ ~3 ~ minecraft:fire[east=true]


execute if score fire funcs matches 2 run setblock ~ ~3 ~ minecraft:fire[east=true,north=true]


execute if score fire funcs matches 3 run setblock ~ ~3 ~ minecraft:fire[east=true,north=true]


execute if score fire funcs matches 4 run setblock ~ ~3 ~ minecraft:fire[east=true,west=true]


execute if score fire funcs matches 5 run setblock ~ ~3 ~ minecraft:fire[east=true,west=true,south=true]


execute if score fire funcs matches 6 run setblock ~ ~3 ~ minecraft:fire[east=true,west=true,south=true,north=true]


execute if score fire funcs matches 7 run setblock ~ ~3 ~ minecraft:fire


execute if score fire funcs matches 8 run setblock ~ ~3 ~ minecraft:fire[east=true,west=true,south=true,north=true]


execute if score fire funcs matches 9 run setblock ~ ~3 ~ minecraft:fire[east=true,west=true,south=true]


execute if score fire funcs matches 10 run setblock ~ ~3 ~ minecraft:fire[east=true,west=true]


execute if score fire funcs matches 11 run setblock ~ ~3 ~ minecraft:fire[east=true,north=true]


execute if score fire funcs matches 12 run setblock ~ ~3 ~ minecraft:fire[east=true,north=true]


execute if score fire funcs matches 13 run setblock ~ ~3 ~ minecraft:fire[east=true]


