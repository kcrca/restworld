scoreboard players set observer max 2
execute unless score observer funcs matches 0..1 run scoreboard players operation observer funcs %= observer max
execute if score observer funcs matches 0 run setblock ~ ~2 ~ minecraft:observer[powered=true,facing=east]

execute if score observer funcs matches 1 run setblock ~ ~2 ~ minecraft:observer[powered=false,facing=east]
