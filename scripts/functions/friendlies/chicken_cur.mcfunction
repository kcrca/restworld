scoreboard players set chicken max 2
execute unless score chicken funcs matches 0..1 run scoreboard players operation chicken funcs %= chicken max

execute if score chicken funcs matches 0 as @e[tag=chicken] run data merge entity @s {OnGround:True,EggLayTime:65535}

execute if score chicken funcs matches 1 as @e[tag=chicken] run data merge entity @s {OnGround:False,EggLayTime:65535}
