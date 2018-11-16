




execute unless score stone funcs matches -1.. run function stone_init
scoreboard players add stone funcs 1
execute unless score stone funcs matches 0..1 run scoreboard players set stone funcs 0



execute if score stone funcs matches 0 run setblock ~ ~3 ~ minecraft:stone
execute if score stone funcs matches 0 run data merge block ~-1 ~2 ~ {Text2:"\"Stone\""}


execute if score stone funcs matches 1 run setblock ~ ~3 ~ minecraft:smooth_stone
execute if score stone funcs matches 1 run data merge block ~-1 ~2 ~ {Text2:"\"Smooth Stone\""}


