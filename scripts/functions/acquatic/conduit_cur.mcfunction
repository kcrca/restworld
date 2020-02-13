scoreboard players set conduit max 5
execute unless score conduit funcs matches 0..4 run scoreboard players operation conduit funcs %= conduit max

execute if score conduit funcs matches 0 run fill ~3 ~14 ~3 ~-3 ~12 ~-3 prismarine replace #v3:conduit


execute if score conduit funcs matches 1 run fill ~3 ~14 ~3 ~-3 ~12 ~-3 dark_prismarine replace #v3:conduit


execute if score conduit funcs matches 2 run fill ~3 ~14 ~3 ~-3 ~12 ~-3 prismarine_bricks replace #v3:conduit


execute if score conduit funcs matches 3 run fill ~3 ~14 ~3 ~-3 ~12 ~-3 sea_lantern replace #v3:conduit


execute if score conduit funcs matches 4 run fill ~3 ~14 ~3 ~-3 ~12 ~-3 clay replace #v3:conduit
