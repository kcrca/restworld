scoreboard players set sand max 2
execute unless score sand funcs matches 0..1 run scoreboard players operation sand funcs %= sand max
execute if score sand funcs matches 0 run fill ~0 ~2 ~1 ~-4 ~2 ~0 minecraft:sand replace #v2:sand

execute if score sand funcs matches 1 run fill ~0 ~2 ~1 ~-4 ~2 ~0 minecraft:red_sand replace #v2:sand
