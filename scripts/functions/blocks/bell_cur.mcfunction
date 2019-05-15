scoreboard players set bell max 4
execute unless score bell funcs matches 0..3 run scoreboard players operation bell funcs %= bell max

execute if score bell funcs matches 0 run setblock ~0 ~3 ~0 bell[attachment=ceiling,facing=north]

execute if score bell funcs matches 0 run setblock ~-1 ~3 ~0 air
execute if score bell funcs matches 0 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 0 run setblock ~0 ~4 ~0 stone_slab

execute if score bell funcs matches 1 run setblock ~-1 ~3 ~0 stone_stairs[facing=east]
execute if score bell funcs matches 1 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 1 run setblock ~0 ~4 ~0 air

execute if score bell funcs matches 2 run setblock ~-1 ~3 ~0 air
execute if score bell funcs matches 2 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 2 run setblock ~0 ~4 ~0 air

execute if score bell funcs matches 3 run setblock ~-1 ~3 ~0 stone_stairs[facing=east]
execute if score bell funcs matches 3 run setblock ~1 ~3 ~0 stone_stairs[facing=west]
execute if score bell funcs matches 3 run setblock ~0 ~4 ~0 air


execute if score bell funcs matches 1 run setblock ~0 ~3 ~0 bell[attachment=single_wall,facing=west]

execute if score bell funcs matches 0 run setblock ~-1 ~3 ~0 air
execute if score bell funcs matches 0 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 0 run setblock ~0 ~4 ~0 stone_slab

execute if score bell funcs matches 1 run setblock ~-1 ~3 ~0 stone_stairs[facing=east]
execute if score bell funcs matches 1 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 1 run setblock ~0 ~4 ~0 air

execute if score bell funcs matches 2 run setblock ~-1 ~3 ~0 air
execute if score bell funcs matches 2 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 2 run setblock ~0 ~4 ~0 air

execute if score bell funcs matches 3 run setblock ~-1 ~3 ~0 stone_stairs[facing=east]
execute if score bell funcs matches 3 run setblock ~1 ~3 ~0 stone_stairs[facing=west]
execute if score bell funcs matches 3 run setblock ~0 ~4 ~0 air


execute if score bell funcs matches 2 run setblock ~0 ~3 ~0 bell[attachment=floor,facing=north]

execute if score bell funcs matches 0 run setblock ~-1 ~3 ~0 air
execute if score bell funcs matches 0 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 0 run setblock ~0 ~4 ~0 stone_slab

execute if score bell funcs matches 1 run setblock ~-1 ~3 ~0 stone_stairs[facing=east]
execute if score bell funcs matches 1 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 1 run setblock ~0 ~4 ~0 air

execute if score bell funcs matches 2 run setblock ~-1 ~3 ~0 air
execute if score bell funcs matches 2 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 2 run setblock ~0 ~4 ~0 air

execute if score bell funcs matches 3 run setblock ~-1 ~3 ~0 stone_stairs[facing=east]
execute if score bell funcs matches 3 run setblock ~1 ~3 ~0 stone_stairs[facing=west]
execute if score bell funcs matches 3 run setblock ~0 ~4 ~0 air


execute if score bell funcs matches 3 run setblock ~0 ~3 ~0 bell[attachment=double_wall,facing=west]

execute if score bell funcs matches 0 run setblock ~-1 ~3 ~0 air
execute if score bell funcs matches 0 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 0 run setblock ~0 ~4 ~0 stone_slab

execute if score bell funcs matches 1 run setblock ~-1 ~3 ~0 stone_stairs[facing=east]
execute if score bell funcs matches 1 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 1 run setblock ~0 ~4 ~0 air

execute if score bell funcs matches 2 run setblock ~-1 ~3 ~0 air
execute if score bell funcs matches 2 run setblock ~1 ~3 ~0 air
execute if score bell funcs matches 2 run setblock ~0 ~4 ~0 air

execute if score bell funcs matches 3 run setblock ~-1 ~3 ~0 stone_stairs[facing=east]
execute if score bell funcs matches 3 run setblock ~1 ~3 ~0 stone_stairs[facing=west]
execute if score bell funcs matches 3 run setblock ~0 ~4 ~0 air
