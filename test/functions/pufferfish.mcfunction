


execute unless score pufferfish funcs matches 0.. run function pufferfish_init
scoreboard players add pufferfish funcs 1
execute unless score pufferfish funcs matches 0..2 run scoreboard players set pufferfish funcs 0
execute if score pufferfish funcs matches 0 run execute as @e[tag=pufferfish] run data merge entity @s {PuffState:0,Age:-2000}

execute if score pufferfish funcs matches 1 run execute as @e[tag=pufferfish] run data merge entity @s {PuffState:1,Age:-2000}

execute if score pufferfish funcs matches 2 run execute as @e[tag=pufferfish] run data merge entity @s {PuffState:2,Age:-2000}

