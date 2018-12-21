execute unless score wither_mob funcs matches 0.. run function wither_mob_init
scoreboard players add wither_mob funcs 1
scoreboard players set wither_mob max 3
execute unless score wither_mob funcs matches 0..2 run scoreboard players operation wither_mob funcs %= wither_mob max

execute if score wither_mob funcs matches 0 run data merge entity @e[tag=wither,limit=1] {Health:300,Invul:100}
execute if score wither_mob funcs matches 0 run data merge block ~0 ~2 ~-2 {Text2:"\"Inulverable (New)\""}
execute if score wither_mob funcs matches 1 run data merge entity @e[tag=wither,limit=1] {Health:300,Invul:0}
execute if score wither_mob funcs matches 1 run data merge block ~0 ~2 ~-2 {Text2:"\"Healthy\""}
execute if score wither_mob funcs matches 2 run data merge entity @e[tag=wither,limit=1] {Health:140,Invul:0}
execute if score wither_mob funcs matches 2 run data merge block ~0 ~2 ~-2 {Text2:"\"Armored (Hurt)\""}
