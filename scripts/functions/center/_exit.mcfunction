execute at @e[tag=lights_home] run function v3:center/lights_exit


execute at @e[type=!player] run data merge entity @s {PersistenceRequired:True}
