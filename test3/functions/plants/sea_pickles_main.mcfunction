execute unless score sea_pickles funcs matches 0.. run function sea_pickles_init
scoreboard players add sea_pickles funcs 1
scoreboard players set sea_pickles max 4
execute unless score sea_pickles funcs matches 0..3 run scoreboard players operation sea_pickles funcs %= sea_pickles max
execute if score sea_pickles funcs matches 0 run setblock ~ ~3 ~ minecraft:sea_pickle[pickles=1]
execute if score sea_pickles funcs matches 0 run setblock ~ ~3 ~2 minecraft:sea_pickle[waterlogged=false,pickles=1]
execute if score sea_pickles funcs matches 1 run setblock ~ ~3 ~ minecraft:sea_pickle[pickles=2]
execute if score sea_pickles funcs matches 1 run setblock ~ ~3 ~2 minecraft:sea_pickle[waterlogged=false,pickles=2]
execute if score sea_pickles funcs matches 2 run setblock ~ ~3 ~ minecraft:sea_pickle[pickles=3]
execute if score sea_pickles funcs matches 2 run setblock ~ ~3 ~2 minecraft:sea_pickle[waterlogged=false,pickles=3]
execute if score sea_pickles funcs matches 3 run setblock ~ ~3 ~ minecraft:sea_pickle[pickles=2]
execute if score sea_pickles funcs matches 3 run setblock ~ ~3 ~2 minecraft:sea_pickle[waterlogged=false,pickles=2]
