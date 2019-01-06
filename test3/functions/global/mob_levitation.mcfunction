execute unless score mob_levitation funcs matches 0.. run function mob_levitation_init
scoreboard players add mob_levitation funcs 1
scoreboard players set mob_levitation max 2
execute unless score mob_levitation funcs matches 0..1 run scoreboard players operation mob_levitation funcs %= mob_levitation max


execute if score mob_levitation funcs matches 1 run execute at @e[tag=sleeping_bat] run clone ~ ~1 ~ ~ ~1 ~ ~ ~3 ~ replace move
execute if score mob_levitation funcs matches 1 run execute at @e[tag=turtle_eggs_home] run clone ~1 ~2 ~0 ~-2 ~2 ~0 ~-2 ~4 ~0 replace move
execute if score mob_levitation funcs matches 1 run execute at @e[tag=brown_horses,tag=kid] run clone ~2 ~ ~ ~2 ~ ~ ~2 ~2 ~ replace move
execute if score mob_levitation funcs matches 1 run execute as @e[tag=friendlies_home] run data merge entity @s {Invisible:true}
execute if score mob_levitation funcs matches 1 run execute as @e[tag=friendlies_home] run execute at @s run tp @s ~ ~2 ~
execute if score mob_levitation funcs matches 1 run execute as @e[tag=friendlies,tag=!passenger] run execute at @s run tp @s ~ ~2 ~
execute if score mob_levitation funcs matches 1 run execute as @e[tag=monsters_home] run data merge entity @s {Invisible:true}
execute if score mob_levitation funcs matches 1 run execute as @e[tag=monsters_home] run execute at @s run tp @s ~ ~2 ~
execute if score mob_levitation funcs matches 1 run execute as @e[tag=monsters,tag=!passenger] run execute at @s run tp @s ~ ~2 ~
execute if score mob_levitation funcs matches 1 run execute as @e[tag=acquatic_home] run data merge entity @s {Invisible:true}
execute if score mob_levitation funcs matches 1 run execute as @e[tag=acquatic_home] run execute at @s run tp @s ~ ~2 ~
execute if score mob_levitation funcs matches 1 run execute as @e[tag=acquatic,tag=!passenger] run execute at @s run tp @s ~ ~2 ~
execute if score mob_levitation funcs matches 1 run execute as @e[tag=wither_home] run data merge entity @s {Invisible:true}
execute if score mob_levitation funcs matches 1 run execute as @e[tag=wither_home] run execute at @s run tp @s ~ ~2 ~
execute if score mob_levitation funcs matches 1 run execute as @e[tag=wither,tag=!passenger] run execute at @s run tp @s ~ ~2 ~

execute if score mob_levitation funcs matches 0 run execute at @e[tag=sleeping_bat] run clone ~ ~1 ~ ~ ~1 ~ ~ ~-1 ~ replace move
execute if score mob_levitation funcs matches 0 run execute at @e[tag=turtle_eggs_home] run clone ~1 ~4 ~0 ~-2 ~4 ~0 ~-2 ~2 ~0 replace move
execute if score mob_levitation funcs matches 0 run execute at @e[tag=brown_horses,tag=kid] run clone ~2 ~ ~ ~2 ~ ~ ~2 ~-2 ~ replace move
execute if score mob_levitation funcs matches 0 run execute as @e[tag=friendlies_home] run data merge entity @s {Invisible:false}
execute if score mob_levitation funcs matches 0 run execute as @e[tag=friendlies_home] run execute at @s run tp @s ~ ~-2 ~
execute if score mob_levitation funcs matches 0 run execute as @e[tag=friendlies,tag=!passenger] run execute at @s run tp @s ~ ~-2 ~
execute if score mob_levitation funcs matches 0 run execute as @e[tag=monsters_home] run data merge entity @s {Invisible:false}
execute if score mob_levitation funcs matches 0 run execute as @e[tag=monsters_home] run execute at @s run tp @s ~ ~-2 ~
execute if score mob_levitation funcs matches 0 run execute as @e[tag=monsters,tag=!passenger] run execute at @s run tp @s ~ ~-2 ~
execute if score mob_levitation funcs matches 0 run execute as @e[tag=acquatic_home] run data merge entity @s {Invisible:false}
execute if score mob_levitation funcs matches 0 run execute as @e[tag=acquatic_home] run execute at @s run tp @s ~ ~-2 ~
execute if score mob_levitation funcs matches 0 run execute as @e[tag=acquatic,tag=!passenger] run execute at @s run tp @s ~ ~-2 ~
execute if score mob_levitation funcs matches 0 run execute as @e[tag=wither_home] run data merge entity @s {Invisible:false}
execute if score mob_levitation funcs matches 0 run execute as @e[tag=wither_home] run execute at @s run tp @s ~ ~-2 ~
execute if score mob_levitation funcs matches 0 run execute as @e[tag=wither,tag=!passenger] run execute at @s run tp @s ~ ~-2 ~
