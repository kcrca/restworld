execute at @e[tag=wither_home] run function v3:wither/wither_exit


execute at @e[type=!player] run data merge entity @s {PersistenceRequired:True}
