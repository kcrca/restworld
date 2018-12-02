setblock 0 1 0 redstone_block

execute at @e[tag=starter] run fill ~0 ~5 ~0 ~0 ~5 ~-6 sand
execute at @e[tag=ender] run tp @e[tag=cloner] ~0 ~2 ~0
function allstuff:diy/tick