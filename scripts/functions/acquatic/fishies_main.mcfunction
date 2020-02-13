execute unless score fishies funcs matches 0.. run function fishies_init
scoreboard players add fishies funcs 1
scoreboard players set fishies max 4
execute unless score fishies funcs matches 0..3 run scoreboard players operation fishies funcs %= fishies max

execute if score fishies funcs matches 0 run data merge entity @e[tag=pufferfish,limit=1] {PuffState:0}

execute if score fishies funcs matches 1 run data merge entity @e[tag=pufferfish,limit=1] {PuffState:1}

execute if score fishies funcs matches 2 run data merge entity @e[tag=pufferfish,limit=1] {PuffState:2}

execute if score fishies funcs matches 3 run data merge entity @e[tag=pufferfish,limit=1] {PuffState:1}
