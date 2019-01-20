execute unless score ocelot funcs matches 0.. run function ocelot_init
scoreboard players add ocelot funcs 1
scoreboard players set ocelot max 4
execute unless score ocelot funcs matches 0..3 run scoreboard players operation ocelot funcs %= ocelot max
execute if score ocelot funcs matches 0 run execute as @e[tag=ocelot] run data merge entity @s {CatType:0,CustomName:"\"Ocelot\""}
execute if score ocelot funcs matches 1 run execute as @e[tag=ocelot] run data merge entity @s {CatType:1,CustomName:"\"Tuxedo\""}
execute if score ocelot funcs matches 2 run execute as @e[tag=ocelot] run data merge entity @s {CatType:2,CustomName:"\"Tabby\""}
execute if score ocelot funcs matches 3 run execute as @e[tag=ocelot] run data merge entity @s {CatType:3,CustomName:"\"Siamese\""}
