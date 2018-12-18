scoreboard players add anvil funcs 0
scoreboard players add beam_colors funcs 0
scoreboard players add brewing funcs 0
scoreboard players add holders funcs 0
scoreboard players add survival funcs 0

tp @e[tag=containers] @e[tag=death,limit=1]


execute at @e[tag=holders_home] run function v3:containers/holders_init
execute at @e[tag=survival_home] run function v3:containers/survival_init
