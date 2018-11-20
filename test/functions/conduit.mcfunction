



execute unless score conduit funcs matches 0.. run function conduit_init
scoreboard players add conduit funcs 1
execute unless score conduit funcs matches 0..1 run scoreboard players set conduit funcs 0

execute if score conduit funcs matches 0 run fill ~-2 ~4 ~0 ~2 ~6 ~-1 minecraft:dark_prismarine replace minecraft:dirt


execute if score conduit funcs matches 1 run fill ~-2 ~4 ~0 ~2 ~6 ~-1 minecraft:dirt replace minecraft:dark_prismarine


