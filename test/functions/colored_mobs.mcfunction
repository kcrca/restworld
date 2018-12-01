

execute unless score colored_mobs funcs matches 0.. run function colored_mobs_init
scoreboard players add colored_mobs funcs 1
execute unless score colored_mobs funcs matches 0..15 run scoreboard players set colored_mobs funcs 0
execute if score colored_mobs funcs matches 0 run execute as @e[tag=sheep] run data merge entity @s {Color:608,CustomName:"\"White\""}
execute if score colored_mobs funcs matches 0 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:608}

execute if score colored_mobs funcs matches 1 run execute as @e[tag=sheep] run data merge entity @s {Color:609,CustomName:"\"Orange\""}
execute if score colored_mobs funcs matches 1 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:609}

execute if score colored_mobs funcs matches 2 run execute as @e[tag=sheep] run data merge entity @s {Color:610,CustomName:"\"Magenta\""}
execute if score colored_mobs funcs matches 2 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:610}

execute if score colored_mobs funcs matches 3 run execute as @e[tag=sheep] run data merge entity @s {Color:611,CustomName:"\"Light Blue\""}
execute if score colored_mobs funcs matches 3 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:611}

execute if score colored_mobs funcs matches 4 run execute as @e[tag=sheep] run data merge entity @s {Color:612,CustomName:"\"Yellow\""}
execute if score colored_mobs funcs matches 4 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:612}

execute if score colored_mobs funcs matches 5 run execute as @e[tag=sheep] run data merge entity @s {Color:613,CustomName:"\"Lime\""}
execute if score colored_mobs funcs matches 5 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:613}

execute if score colored_mobs funcs matches 6 run execute as @e[tag=sheep] run data merge entity @s {Color:614,CustomName:"\"Pink\""}
execute if score colored_mobs funcs matches 6 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:614}

execute if score colored_mobs funcs matches 7 run execute as @e[tag=sheep] run data merge entity @s {Color:615,CustomName:"\"Gray\""}
execute if score colored_mobs funcs matches 7 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:615}

execute if score colored_mobs funcs matches 8 run execute as @e[tag=sheep] run data merge entity @s {Color:616,CustomName:"\"Light Gray\""}
execute if score colored_mobs funcs matches 8 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:616}

execute if score colored_mobs funcs matches 9 run execute as @e[tag=sheep] run data merge entity @s {Color:617,CustomName:"\"Cyan\""}
execute if score colored_mobs funcs matches 9 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:617}

execute if score colored_mobs funcs matches 10 run execute as @e[tag=sheep] run data merge entity @s {Color:618,CustomName:"\"Purple\""}
execute if score colored_mobs funcs matches 10 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:618}

execute if score colored_mobs funcs matches 11 run execute as @e[tag=sheep] run data merge entity @s {Color:619,CustomName:"\"Blue\""}
execute if score colored_mobs funcs matches 11 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:619}

execute if score colored_mobs funcs matches 12 run execute as @e[tag=sheep] run data merge entity @s {Color:620,CustomName:"\"Brown\""}
execute if score colored_mobs funcs matches 12 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:620}

execute if score colored_mobs funcs matches 13 run execute as @e[tag=sheep] run data merge entity @s {Color:621,CustomName:"\"Green\""}
execute if score colored_mobs funcs matches 13 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:621}

execute if score colored_mobs funcs matches 14 run execute as @e[tag=sheep] run data merge entity @s {Color:622,CustomName:"\"Red\""}
execute if score colored_mobs funcs matches 14 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:622}

execute if score colored_mobs funcs matches 15 run execute as @e[tag=sheep] run data merge entity @s {Color:623,CustomName:"\"Black\""}
execute if score colored_mobs funcs matches 15 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:623}

