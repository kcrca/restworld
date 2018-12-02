execute unless score sand funcs matches 0.. run function sand_init
scoreboard players add sand funcs 1
execute unless score sand funcs matches 0..1 run scoreboard players set sand funcs 0
execute if score sand funcs matches 0 run fill ~0 ~2 ~1 ~-4 ~2 ~0 minecraft:sand replace #allstuff:sand

execute if score sand funcs matches 1 run fill ~0 ~2 ~1 ~-4 ~2 ~0 minecraft:red_sand replace #allstuff:sand