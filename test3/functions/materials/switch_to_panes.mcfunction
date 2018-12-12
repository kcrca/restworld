tag @e[tag=walls_home] add fencelike_home
tag @e[tag=panes_home] add fencelike_home
tag @e[tag=fences_home] add fencelike_home
tp @e[tag=fencelike_home] @e[tag=death,limit=1]

execute positioned ~-3 ~-1 ~1 run function v3:materials/panes_home
execute at @e[tag=panes_home] run function v3:materials/panes_cur