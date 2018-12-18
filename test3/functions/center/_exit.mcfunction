execute at @e[tag=center_home] run function v3:center/center_exit


execute at @e[type=!player] run data merge entity @s {PersistenceRequired:True}
