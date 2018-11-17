




execute unless score pumpkin funcs matches -1.. run function pumpkin_init
scoreboard players add pumpkin funcs 1
execute unless score pumpkin funcs matches 0..2 run scoreboard players set pumpkin funcs 0



execute if score pumpkin funcs matches 0 run setblock ~ ~3 ~ minecraft:pumpkin
execute if score pumpkin funcs matches 0 run data merge block ~1 ~2 ~ {Text2:"\"Pumpkin\""}


execute if score pumpkin funcs matches 1 run setblock ~ ~3 ~ minecraft:carved_pumpkin[facing=east]
execute if score pumpkin funcs matches 1 run data merge block ~1 ~2 ~ {Text2:"\"Carved Pumpkin\""}


execute if score pumpkin funcs matches 2 run setblock ~ ~3 ~ minecraft:jack_o_lantern[facing=east]
execute if score pumpkin funcs matches 2 run data merge block ~1 ~2 ~ {Text2:"\"Jack O' Lantern\""}


