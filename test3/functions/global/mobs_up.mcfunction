execute at @e[tag=sleeping_bat] run clone ~ ~1 ~ ~ ~1 ~ ~ ~3 ~ replace move
execute at @e[tag=turtle_eggs_home] run clone ~1 ~2 ~0 ~-2 ~2 ~0 ~-2 ~4 ~0 replace move
execute at @e[tag=brown_horses,tag=kid] run clone ~2 ~ ~ ~2 ~ ~ ~2 ~2 ~ replace move
execute as @e[tag=friendlies_home] run data merge entity @s {Invisible:true}
execute as @e[tag=friendlies_home] run execute at @s run tp @s ~ ~2 ~
execute as @e[tag=friendlies,tag=!passenger] run execute at @s run tp @s ~ ~2 ~
execute as @e[tag=monsters_home] run data merge entity @s {Invisible:true}
execute as @e[tag=monsters_home] run execute at @s run tp @s ~ ~2 ~
execute as @e[tag=monsters,tag=!passenger] run execute at @s run tp @s ~ ~2 ~
execute as @e[tag=acquatic_home] run data merge entity @s {Invisible:true}
execute as @e[tag=acquatic_home] run execute at @s run tp @s ~ ~2 ~
execute as @e[tag=acquatic,tag=!passenger] run execute at @s run tp @s ~ ~2 ~
execute as @e[tag=wither_home] run data merge entity @s {Invisible:true}
execute as @e[tag=wither_home] run execute at @s run tp @s ~ ~2 ~
execute as @e[tag=wither,tag=!passenger] run execute at @s run tp @s ~ ~2 ~
