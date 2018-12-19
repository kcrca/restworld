execute unless score shulker funcs matches 0.. run function shulker_init
scoreboard players add shulker funcs 1
scoreboard players set shulker max 4
execute unless score shulker funcs matches 0..3 run scoreboard players operation shulker funcs %= shulker max
execute if score shulker funcs matches 0 run data merge entity @e[tag=shulker,limit=1] {Peek:0}
execute if score shulker funcs matches 1 run data merge entity @e[tag=shulker,limit=1] {Peek:30}
execute if score shulker funcs matches 2 run data merge entity @e[tag=shulker,limit=1] {Peek:100}
execute if score shulker funcs matches 3 run data merge entity @e[tag=shulker,limit=1] {Peek:30}
