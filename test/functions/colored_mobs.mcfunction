

execute unless score colored_mobs funcs matches 0.. run function colored_mobs_init
scoreboard players add colored_mobs funcs 1
execute unless score colored_mobs funcs matches 0..15 run scoreboard players set colored_mobs funcs 0
execute if score colored_mobs funcs matches 0 run execute as @e[tag=sheep] run data merge entity @s {Color:576,CustomName:"\"White\""}
execute if score colored_mobs funcs matches 0 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:576}

execute if score colored_mobs funcs matches 1 run execute as @e[tag=sheep] run data merge entity @s {Color:577,CustomName:"\"Orange\""}
execute if score colored_mobs funcs matches 1 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:577}

execute if score colored_mobs funcs matches 2 run execute as @e[tag=sheep] run data merge entity @s {Color:578,CustomName:"\"Magenta\""}
execute if score colored_mobs funcs matches 2 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:578}

execute if score colored_mobs funcs matches 3 run execute as @e[tag=sheep] run data merge entity @s {Color:579,CustomName:"\"Light Blue\""}
execute if score colored_mobs funcs matches 3 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:579}

execute if score colored_mobs funcs matches 4 run execute as @e[tag=sheep] run data merge entity @s {Color:580,CustomName:"\"Yellow\""}
execute if score colored_mobs funcs matches 4 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:580}

execute if score colored_mobs funcs matches 5 run execute as @e[tag=sheep] run data merge entity @s {Color:581,CustomName:"\"Lime\""}
execute if score colored_mobs funcs matches 5 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:581}

execute if score colored_mobs funcs matches 6 run execute as @e[tag=sheep] run data merge entity @s {Color:582,CustomName:"\"Pink\""}
execute if score colored_mobs funcs matches 6 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:582}

execute if score colored_mobs funcs matches 7 run execute as @e[tag=sheep] run data merge entity @s {Color:583,CustomName:"\"Gray\""}
execute if score colored_mobs funcs matches 7 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:583}

execute if score colored_mobs funcs matches 8 run execute as @e[tag=sheep] run data merge entity @s {Color:584,CustomName:"\"Light Gray\""}
execute if score colored_mobs funcs matches 8 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:584}

execute if score colored_mobs funcs matches 9 run execute as @e[tag=sheep] run data merge entity @s {Color:585,CustomName:"\"Cyan\""}
execute if score colored_mobs funcs matches 9 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:585}

execute if score colored_mobs funcs matches 10 run execute as @e[tag=sheep] run data merge entity @s {Color:586,CustomName:"\"Purple\""}
execute if score colored_mobs funcs matches 10 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:586}

execute if score colored_mobs funcs matches 11 run execute as @e[tag=sheep] run data merge entity @s {Color:587,CustomName:"\"Blue\""}
execute if score colored_mobs funcs matches 11 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:587}

execute if score colored_mobs funcs matches 12 run execute as @e[tag=sheep] run data merge entity @s {Color:588,CustomName:"\"Brown\""}
execute if score colored_mobs funcs matches 12 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:588}

execute if score colored_mobs funcs matches 13 run execute as @e[tag=sheep] run data merge entity @s {Color:589,CustomName:"\"Green\""}
execute if score colored_mobs funcs matches 13 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:589}

execute if score colored_mobs funcs matches 14 run execute as @e[tag=sheep] run data merge entity @s {Color:590,CustomName:"\"Red\""}
execute if score colored_mobs funcs matches 14 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:590}

execute if score colored_mobs funcs matches 15 run execute as @e[tag=sheep] run data merge entity @s {Color:591,CustomName:"\"Black\""}
execute if score colored_mobs funcs matches 15 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:591}

