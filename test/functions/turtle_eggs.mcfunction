


execute unless score turtle_eggs funcs matches 0.. run function turtle_eggs_init
scoreboard players add turtle_eggs funcs 1
execute unless score turtle_eggs funcs matches 0..5 run scoreboard players set turtle_eggs funcs 0
execute if score turtle_eggs funcs matches 0 run setblock ~0 ~2 ~0 minecraft:turtle_egg[eggs=1,hatch=0]
execute if score turtle_eggs funcs matches 0 run setblock ~0 ~2 ~-1 minecraft:turtle_egg[eggs=1,hatch=1]
execute if score turtle_eggs funcs matches 0 run setblock ~0 ~2 ~-2 minecraft:turtle_egg[eggs=1,hatch=2]
execute if score turtle_eggs funcs matches 1 run setblock ~0 ~2 ~0 minecraft:turtle_egg[eggs=2,hatch=0]
execute if score turtle_eggs funcs matches 1 run setblock ~0 ~2 ~-1 minecraft:turtle_egg[eggs=2,hatch=1]
execute if score turtle_eggs funcs matches 1 run setblock ~0 ~2 ~-2 minecraft:turtle_egg[eggs=2,hatch=2]
execute if score turtle_eggs funcs matches 2 run setblock ~0 ~2 ~0 minecraft:turtle_egg[eggs=3,hatch=0]
execute if score turtle_eggs funcs matches 2 run setblock ~0 ~2 ~-1 minecraft:turtle_egg[eggs=3,hatch=1]
execute if score turtle_eggs funcs matches 2 run setblock ~0 ~2 ~-2 minecraft:turtle_egg[eggs=3,hatch=2]
execute if score turtle_eggs funcs matches 3 run setblock ~0 ~2 ~0 minecraft:turtle_egg[eggs=4,hatch=0]
execute if score turtle_eggs funcs matches 3 run setblock ~0 ~2 ~-1 minecraft:turtle_egg[eggs=4,hatch=1]
execute if score turtle_eggs funcs matches 3 run setblock ~0 ~2 ~-2 minecraft:turtle_egg[eggs=4,hatch=2]
execute if score turtle_eggs funcs matches 4 run setblock ~0 ~2 ~0 minecraft:turtle_egg[eggs=3,hatch=0]
execute if score turtle_eggs funcs matches 4 run setblock ~0 ~2 ~-1 minecraft:turtle_egg[eggs=3,hatch=1]
execute if score turtle_eggs funcs matches 4 run setblock ~0 ~2 ~-2 minecraft:turtle_egg[eggs=3,hatch=2]
execute if score turtle_eggs funcs matches 5 run setblock ~0 ~2 ~0 minecraft:turtle_egg[eggs=2,hatch=0]
execute if score turtle_eggs funcs matches 5 run setblock ~0 ~2 ~-1 minecraft:turtle_egg[eggs=2,hatch=1]
execute if score turtle_eggs funcs matches 5 run setblock ~0 ~2 ~-2 minecraft:turtle_egg[eggs=2,hatch=2]