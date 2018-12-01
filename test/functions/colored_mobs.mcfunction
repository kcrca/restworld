

execute unless score colored_mobs funcs matches 0.. run function colored_mobs_init
scoreboard players add colored_mobs funcs 1
execute unless score colored_mobs funcs matches 0..15 run scoreboard players set colored_mobs funcs 0
execute if score colored_mobs funcs matches 0 run execute as @e[tag=sheep] run data merge entity @s {Color:640,CustomName:"\"White\""}
execute if score colored_mobs funcs matches 0 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:640}

execute if score colored_mobs funcs matches 1 run execute as @e[tag=sheep] run data merge entity @s {Color:641,CustomName:"\"Orange\""}
execute if score colored_mobs funcs matches 1 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:641}

execute if score colored_mobs funcs matches 2 run execute as @e[tag=sheep] run data merge entity @s {Color:642,CustomName:"\"Magenta\""}
execute if score colored_mobs funcs matches 2 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:642}

execute if score colored_mobs funcs matches 3 run execute as @e[tag=sheep] run data merge entity @s {Color:643,CustomName:"\"Light Blue\""}
execute if score colored_mobs funcs matches 3 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:643}

execute if score colored_mobs funcs matches 4 run execute as @e[tag=sheep] run data merge entity @s {Color:644,CustomName:"\"Yellow\""}
execute if score colored_mobs funcs matches 4 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:644}

execute if score colored_mobs funcs matches 5 run execute as @e[tag=sheep] run data merge entity @s {Color:645,CustomName:"\"Lime\""}
execute if score colored_mobs funcs matches 5 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:645}

execute if score colored_mobs funcs matches 6 run execute as @e[tag=sheep] run data merge entity @s {Color:646,CustomName:"\"Pink\""}
execute if score colored_mobs funcs matches 6 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:646}

execute if score colored_mobs funcs matches 7 run execute as @e[tag=sheep] run data merge entity @s {Color:647,CustomName:"\"Gray\""}
execute if score colored_mobs funcs matches 7 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:647}

execute if score colored_mobs funcs matches 8 run execute as @e[tag=sheep] run data merge entity @s {Color:648,CustomName:"\"Light Gray\""}
execute if score colored_mobs funcs matches 8 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:648}

execute if score colored_mobs funcs matches 9 run execute as @e[tag=sheep] run data merge entity @s {Color:649,CustomName:"\"Cyan\""}
execute if score colored_mobs funcs matches 9 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:649}

execute if score colored_mobs funcs matches 10 run execute as @e[tag=sheep] run data merge entity @s {Color:650,CustomName:"\"Purple\""}
execute if score colored_mobs funcs matches 10 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:650}

execute if score colored_mobs funcs matches 11 run execute as @e[tag=sheep] run data merge entity @s {Color:651,CustomName:"\"Blue\""}
execute if score colored_mobs funcs matches 11 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:651}

execute if score colored_mobs funcs matches 12 run execute as @e[tag=sheep] run data merge entity @s {Color:652,CustomName:"\"Brown\""}
execute if score colored_mobs funcs matches 12 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:652}

execute if score colored_mobs funcs matches 13 run execute as @e[tag=sheep] run data merge entity @s {Color:653,CustomName:"\"Green\""}
execute if score colored_mobs funcs matches 13 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:653}

execute if score colored_mobs funcs matches 14 run execute as @e[tag=sheep] run data merge entity @s {Color:654,CustomName:"\"Red\""}
execute if score colored_mobs funcs matches 14 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:654}

execute if score colored_mobs funcs matches 15 run execute as @e[tag=sheep] run data merge entity @s {Color:655,CustomName:"\"Black\""}
execute if score colored_mobs funcs matches 15 run execute as @e[tag=dogs] run data merge entity @s {CollarColor:655}

