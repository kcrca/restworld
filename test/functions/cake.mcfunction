





execute unless score cake funcs matches -1.. run function cake_init
scoreboard players add cake funcs 1
execute unless score cake funcs matches 0..11 run scoreboard players set cake funcs 0



execute if score cake funcs matches 0 run setblock ~ ~3 ~ cake[bites=0]


execute if score cake funcs matches 1 run setblock ~ ~3 ~ cake[bites=1]


execute if score cake funcs matches 2 run setblock ~ ~3 ~ cake[bites=2]


execute if score cake funcs matches 3 run setblock ~ ~3 ~ cake[bites=3]


execute if score cake funcs matches 4 run setblock ~ ~3 ~ cake[bites=4]


execute if score cake funcs matches 5 run setblock ~ ~3 ~ cake[bites=5]


execute if score cake funcs matches 6 run setblock ~ ~3 ~ cake[bites=6]


execute if score cake funcs matches 7 run setblock ~ ~3 ~ cake[bites=5]


execute if score cake funcs matches 8 run setblock ~ ~3 ~ cake[bites=4]


execute if score cake funcs matches 9 run setblock ~ ~3 ~ cake[bites=3]


execute if score cake funcs matches 10 run setblock ~ ~3 ~ cake[bites=2]


execute if score cake funcs matches 11 run setblock ~ ~3 ~ cake[bites=1]


