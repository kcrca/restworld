scoreboard players set wither max 3
execute unless score wither funcs matches 0..2 run scoreboard players operation wither funcs %= wither max

execute if score wither funcs matches 0 run data merge entity @e[tag=wither,limit=1] {Health:300,Invul:100}
execute if score wither funcs matches 0 run data merge block ~0 ~2 ~-2 {Text2:"\"Inulverable (New)\""}
execute if score wither funcs matches 1 run data merge entity @e[tag=wither,limit=1] {Health:300,Invul:0}
execute if score wither funcs matches 1 run data merge block ~0 ~2 ~-2 {Text2:"\"Healthy\""}
execute if score wither funcs matches 2 run data merge entity @e[tag=wither,limit=1] {Health:140,Invul:0}
execute if score wither funcs matches 2 run data merge block ~0 ~2 ~-2 {Text2:"\"Armored (Hurt)\""}
