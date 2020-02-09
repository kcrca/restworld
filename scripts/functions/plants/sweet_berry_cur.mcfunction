scoreboard players set sweet_berry max 6
execute unless score sweet_berry funcs matches 0..5 run scoreboard players operation sweet_berry funcs %= sweet_berry max
execute if score sweet_berry funcs matches 0 run setblock ~ ~3 ~ minecraft:sweet_berry_bush[age=0]
execute if score sweet_berry funcs matches 1 run setblock ~ ~3 ~ minecraft:sweet_berry_bush[age=1]
execute if score sweet_berry funcs matches 2 run setblock ~ ~3 ~ minecraft:sweet_berry_bush[age=2]
execute if score sweet_berry funcs matches 3 run setblock ~ ~3 ~ minecraft:sweet_berry_bush[age=3]
execute if score sweet_berry funcs matches 4 run setblock ~ ~3 ~ minecraft:sweet_berry_bush[age=2]
execute if score sweet_berry funcs matches 5 run setblock ~ ~3 ~ minecraft:sweet_berry_bush[age=1]
