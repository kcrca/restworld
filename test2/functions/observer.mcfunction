execute unless score observer funcs matches 0.. run function observer_init
scoreboard players add observer funcs 1
execute unless score observer funcs matches 0..1 run scoreboard players set observer funcs 0
execute if score observer funcs matches 0 run setblock ~ ~2 ~ minecraft:observer[powered=true,facing=east]

execute if score observer funcs matches 1 run setblock ~ ~2 ~ minecraft:observer[powered=false,facing=east]