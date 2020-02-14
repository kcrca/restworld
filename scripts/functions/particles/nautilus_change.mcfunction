execute unless score nautilus_change funcs matches 0.. run function nautilus_change_init
scoreboard players add nautilus_change funcs 1
scoreboard players set nautilus_change max 2
execute unless score nautilus_change funcs matches 0..1 run scoreboard players operation nautilus_change funcs %= nautilus_change max

execute if score nautilus_change funcs matches 0 run fill ~-2 ~0 ~-2 ~2 ~2 ~0 prismarine


execute if score nautilus_change funcs matches 1 run fill ~-2 ~0 ~-2 ~2 ~2 ~0 sand



fill ~-1 ~1 ~-1 ~1 ~2 ~0 water
setblock ~0 ~2 ~0 conduit
