execute positioned ~ ~-3 ~ run function v3:global/min_home

kill @e[tag=homer,tag=!min_home]

execute at @e[tag=min_home] run fill ~ 99 ~ ~144 99 ~160 birch_log replace redstone_block

execute at @e[tag=min_home] run fill ~ 99 ~ ~144 99 ~160 redstone_block replace dried_kelp_block
execute at @e[tag=min_home] run fill ~ 99 ~ ~144 99 ~160 dried_kelp_block replace redstone_block
execute at @e[tag=min_home] run fill ~ 100 ~ ~144 100 ~160 redstone_block replace pumpkin
execute at @e[tag=min_home] run fill ~ 100 ~ ~144 100 ~160 pumpkin replace redstone_block

execute at @e[tag=min_home] run fill ~ 99 ~ ~144 99 ~160 redstone_block replace birch_log

function v3:_cur
