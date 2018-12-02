execute unless score cauldron funcs matches 0.. run function cauldron_init
scoreboard players add cauldron funcs 1
execute unless score cauldron funcs matches 0..5 run scoreboard players set cauldron funcs 0

execute if score cauldron funcs matches 0 run setblock ~ ~2 ~ cauldron[level=0]

execute if score cauldron funcs matches 1 run setblock ~ ~2 ~ cauldron[level=1]

execute if score cauldron funcs matches 2 run setblock ~ ~2 ~ cauldron[level=2]

execute if score cauldron funcs matches 3 run setblock ~ ~2 ~ cauldron[level=3]

execute if score cauldron funcs matches 4 run setblock ~ ~2 ~ cauldron[level=2]

execute if score cauldron funcs matches 5 run setblock ~ ~2 ~ cauldron[level=1]