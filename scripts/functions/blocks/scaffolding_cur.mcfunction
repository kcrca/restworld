scoreboard players set scaffolding max 8
execute unless score scaffolding funcs matches 0..7 run scoreboard players operation scaffolding funcs %= scaffolding max

execute if score scaffolding funcs matches 0 run setblock ~0 ~4 ~0 scaffolding

execute if score scaffolding funcs matches 1 run setblock ~0 ~5 ~0 scaffolding

execute if score scaffolding funcs matches 2 run setblock ~0 ~5 ~-1 scaffolding[distance=1]

execute if score scaffolding funcs matches 3 run setblock ~0 ~5 ~-2 scaffolding[distance=2]

execute if score scaffolding funcs matches 4 run setblock ~0 ~5 ~-2 air

execute if score scaffolding funcs matches 5 run setblock ~0 ~5 ~-1 air

execute if score scaffolding funcs matches 6 run setblock ~0 ~5 ~0 air

execute if score scaffolding funcs matches 7 run setblock ~0 ~4 ~0 air
