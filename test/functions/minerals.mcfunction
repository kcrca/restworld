




execute unless score minerals funcs matches 0.. run function minerals_init
scoreboard players add minerals funcs 1
execute unless score minerals funcs matches 0..2 run scoreboard players set minerals funcs 0



execute if score minerals funcs matches 0 run setblock ~ ~3 ~ minecraft:andesite
execute if score minerals funcs matches 0 run data merge block ~-1 ~2 ~ {Text2:"\"Andesite\""}
execute if score minerals funcs matches 0 run setblock ~ ~3 ~2 minecraft:polished_andesite
execute if score minerals funcs matches 0 run data merge block ~-1 ~2 ~2 {Text2:"\"Polished Andesite\""}


execute if score minerals funcs matches 1 run setblock ~ ~3 ~ minecraft:diorite
execute if score minerals funcs matches 1 run data merge block ~-1 ~2 ~ {Text2:"\"Diorite\""}
execute if score minerals funcs matches 1 run setblock ~ ~3 ~2 minecraft:polished_diorite
execute if score minerals funcs matches 1 run data merge block ~-1 ~2 ~2 {Text2:"\"Polished Diorite\""}


execute if score minerals funcs matches 2 run setblock ~ ~3 ~ minecraft:granite
execute if score minerals funcs matches 2 run data merge block ~-1 ~2 ~ {Text2:"\"Granite\""}
execute if score minerals funcs matches 2 run setblock ~ ~3 ~2 minecraft:polished_granite
execute if score minerals funcs matches 2 run data merge block ~-1 ~2 ~2 {Text2:"\"Polished Granite\""}


