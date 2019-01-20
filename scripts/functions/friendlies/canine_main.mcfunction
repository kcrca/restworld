execute unless score canine funcs matches 0.. run function canine_init
scoreboard players add canine funcs 1
scoreboard players set canine max 2
execute unless score canine funcs matches 0..1 run scoreboard players operation canine funcs %= canine max
execute if score canine funcs matches 0 run execute as @e[tag=wolf] run data merge entity @s {Angry:True}

execute if score canine funcs matches 1 run execute as @e[tag=wolf] run data merge entity @s {Angry:False}
