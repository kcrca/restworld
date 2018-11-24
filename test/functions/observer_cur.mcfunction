


execute if score observer funcs matches 0 run setblock ~ ~4 ~ minecraft:observer[powered=true,facing=west]
execute if score observer funcs matches 0 run data merge block ~1 ~2 ~ {Text3:"\"(Powered)\""}

execute if score observer funcs matches 1 run setblock ~ ~4 ~ minecraft:observer[powered=false,facing=west]
execute if score observer funcs matches 1 run data merge block ~1 ~2 ~ {Text3:"\"\""}


