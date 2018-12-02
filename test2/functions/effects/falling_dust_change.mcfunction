execute unless score falling_dust_change funcs matches 0.. run function falling_dust_change_init
scoreboard players add falling_dust_change funcs 1
execute unless score falling_dust_change funcs matches 0..3 run scoreboard players set falling_dust_change funcs 0

execute if score falling_dust_change funcs matches 0 run fill ~-2 ~5 ~-2 ~2 ~5 ~2 minecraft:sand
execute if score falling_dust_change funcs matches 0 run particle minecraft:falling_dust minecraft:sand ~ ~3 ~ 0.8 0 0.8 0 50


execute if score falling_dust_change funcs matches 1 run fill ~-2 ~5 ~-2 ~2 ~5 ~2 minecraft:red_sand
execute if score falling_dust_change funcs matches 1 run particle minecraft:falling_dust minecraft:red_sand ~ ~3 ~ 0.8 0 0.8 0 50


execute if score falling_dust_change funcs matches 2 run fill ~-2 ~5 ~-2 ~2 ~5 ~2 minecraft:gravel
execute if score falling_dust_change funcs matches 2 run particle minecraft:falling_dust minecraft:gravel ~ ~3 ~ 0.8 0 0.8 0 50


execute if score falling_dust_change funcs matches 3 run fill ~-2 ~5 ~-2 ~2 ~5 ~2 minecraft:cyan_concrete_powder
execute if score falling_dust_change funcs matches 3 run particle minecraft:falling_dust minecraft:cyan_concrete_powder ~ ~3 ~ 0.8 0 0.8 0 50