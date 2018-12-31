execute unless score grow funcs matches 0.. run function grow_init
scoreboard players add grow funcs 1
scoreboard players set grow max 4
execute unless score grow funcs matches 0..3 run scoreboard players operation grow funcs %= grow max


execute unless score grow funcs matches 3 run clone ~6 ~2 ~13 ~0 ~-8 ~-1 ~-5 ~-8 ~-1 replace force
execute unless score grow funcs matches 3 run fill ~1 ~-1 ~9 ~-3 ~-1 ~3 air
execute if score grow funcs matches 3 run say Memory at maximum size
execute if score grow funcs matches 3 run scoreboard players set grow funcs 2
