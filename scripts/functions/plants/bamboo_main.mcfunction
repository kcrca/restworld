execute unless score bamboo funcs matches 0.. run function bamboo_init
scoreboard players add bamboo funcs 1
scoreboard players set bamboo max 13
execute unless score bamboo funcs matches 0..12 run scoreboard players operation bamboo funcs %= bamboo max
execute if score bamboo funcs matches 0 run setblock ~ ~3 ~ minecraft:bamboo_sapling
execute if score bamboo funcs matches 0 run fill ~ ~8 ~ ~ ~4 ~ minecraft:air

execute if score bamboo funcs matches 1 run fill ~ ~3 ~ ~ ~3 ~ minecraft:bamboo[age=0,leaves=none]
execute if score bamboo funcs matches 1 run fill ~ ~8 ~ ~ ~4 ~ minecraft:air

execute if score bamboo funcs matches 2 run fill ~ ~3 ~ ~ ~4 ~ minecraft:bamboo[age=0,leaves=none]
execute if score bamboo funcs matches 2 run fill ~ ~8 ~ ~ ~5 ~ minecraft:air
execute if score bamboo funcs matches 2 run setblock ~ ~4 ~ minecraft:bamboo[age=0,leaves=small]

execute if score bamboo funcs matches 3 run fill ~ ~3 ~ ~ ~5 ~ minecraft:bamboo[age=0,leaves=none]
execute if score bamboo funcs matches 3 run fill ~ ~8 ~ ~ ~6 ~ minecraft:air
execute if score bamboo funcs matches 3 run setblock ~ ~4 ~ minecraft:bamboo[age=0,leaves=large]
execute if score bamboo funcs matches 3 run setblock ~ ~5 ~ minecraft:bamboo[age=0,leaves=small]

execute if score bamboo funcs matches 4 run fill ~ ~3 ~ ~ ~6 ~ minecraft:bamboo[age=0,leaves=none]
execute if score bamboo funcs matches 4 run fill ~ ~8 ~ ~ ~7 ~ minecraft:air
execute if score bamboo funcs matches 4 run setblock ~ ~5 ~ minecraft:bamboo[age=0,leaves=large]
execute if score bamboo funcs matches 4 run setblock ~ ~6 ~ minecraft:bamboo[age=0,leaves=small]

execute if score bamboo funcs matches 5 run fill ~ ~3 ~ ~ ~7 ~ minecraft:bamboo[age=0,leaves=none]
execute if score bamboo funcs matches 5 run fill ~ ~8 ~ ~ ~8 ~ minecraft:air
execute if score bamboo funcs matches 5 run setblock ~ ~6 ~ minecraft:bamboo[age=0,leaves=large]
execute if score bamboo funcs matches 5 run setblock ~ ~7 ~ minecraft:bamboo[age=0,leaves=small]

execute if score bamboo funcs matches 6 run fill ~ ~3 ~ ~ ~8 ~ minecraft:bamboo[age=0,leaves=none]
execute if score bamboo funcs matches 6 run setblock ~ ~7 ~ minecraft:bamboo[age=0,leaves=large]
execute if score bamboo funcs matches 6 run setblock ~ ~8 ~ minecraft:bamboo[age=0,leaves=small]

execute if score bamboo funcs matches 7 run fill ~ ~3 ~ ~ ~8 ~ minecraft:bamboo[age=1,leaves=none]
execute if score bamboo funcs matches 7 run setblock ~ ~7 ~ minecraft:bamboo[age=1,leaves=large]
execute if score bamboo funcs matches 7 run setblock ~ ~8 ~ minecraft:bamboo[age=1,leaves=small]

execute if score bamboo funcs matches 8 run fill ~ ~3 ~ ~ ~7 ~ minecraft:bamboo[age=1,leaves=none]
execute if score bamboo funcs matches 8 run fill ~ ~8 ~ ~ ~8 ~ minecraft:air
execute if score bamboo funcs matches 8 run setblock ~ ~6 ~ minecraft:bamboo[age=1,leaves=large]
execute if score bamboo funcs matches 8 run setblock ~ ~7 ~ minecraft:bamboo[age=1,leaves=small]

execute if score bamboo funcs matches 9 run fill ~ ~3 ~ ~ ~6 ~ minecraft:bamboo[age=1,leaves=none]
execute if score bamboo funcs matches 9 run fill ~ ~8 ~ ~ ~7 ~ minecraft:air
execute if score bamboo funcs matches 9 run setblock ~ ~5 ~ minecraft:bamboo[age=1,leaves=large]
execute if score bamboo funcs matches 9 run setblock ~ ~6 ~ minecraft:bamboo[age=1,leaves=small]

execute if score bamboo funcs matches 10 run fill ~ ~3 ~ ~ ~5 ~ minecraft:bamboo[age=1,leaves=none]
execute if score bamboo funcs matches 10 run fill ~ ~8 ~ ~ ~6 ~ minecraft:air
execute if score bamboo funcs matches 10 run setblock ~ ~4 ~ minecraft:bamboo[age=1,leaves=large]
execute if score bamboo funcs matches 10 run setblock ~ ~5 ~ minecraft:bamboo[age=1,leaves=small]

execute if score bamboo funcs matches 11 run fill ~ ~3 ~ ~ ~4 ~ minecraft:bamboo[age=1,leaves=none]
execute if score bamboo funcs matches 11 run fill ~ ~8 ~ ~ ~5 ~ minecraft:air
execute if score bamboo funcs matches 11 run setblock ~ ~4 ~ minecraft:bamboo[age=1,leaves=small]

execute if score bamboo funcs matches 12 run fill ~ ~3 ~ ~ ~3 ~ minecraft:bamboo[age=1,leaves=none]
execute if score bamboo funcs matches 12 run fill ~ ~8 ~ ~ ~4 ~ minecraft:air
