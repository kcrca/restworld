execute at @e[tag=beam_colors_home] run function v3:containers/beam_colors_exit


execute at @e[type=!player] run data merge entity @s {PersistenceRequired:True}
