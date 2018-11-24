


execute unless score observer funcs matches 0.. run function observer_init
scoreboard players add observer funcs 1
execute unless score observer funcs matches 0..1 run scoreboard players set observer funcs 0
execute if score observer funcs matches 0 run setblock ~ ~4 ~ minecraft:observer[powered=true,facing=west]
execute if score observer funcs matches 0 run data merge block ~1 ~2 ~ {Text3:"\"(Powered)\""}

execute if score observer funcs matches 1 run setblock ~ ~4 ~ minecraft:observer[powered=false,facing=west]
execute if score observer funcs matches 1 run data merge block ~1 ~2 ~ {Text3:"\"\""}


