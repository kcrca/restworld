execute at @e[tag=beam_home] run function v3:containers/beam_exit


execute at @e[type=!player] run data merge entity @s {PersistenceRequired:True}
