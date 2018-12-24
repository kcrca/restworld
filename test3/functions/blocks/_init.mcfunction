scoreboard players add bricks funcs 0
scoreboard players add cake funcs 0
scoreboard players add cobble funcs 0
scoreboard players add command_blocks funcs 0
scoreboard players add dirt funcs 0
scoreboard players add end funcs 0
scoreboard players add frosted_ice funcs 0
scoreboard players add ice funcs 0
scoreboard players add music funcs 0
scoreboard players add nether funcs 0
scoreboard players add ores funcs 0
scoreboard players add prismarine funcs 0
scoreboard players add pumpkin funcs 0
scoreboard players add purpur funcs 0
scoreboard players add quartz funcs 0
scoreboard players add sandstone funcs 0
scoreboard players add skulls funcs 0
scoreboard players add soil funcs 0
scoreboard players add sponge funcs 0
scoreboard players add stone funcs 0
scoreboard players add stone_bricks funcs 0
scoreboard players add structure_blocks funcs 0
scoreboard players add wood_blocks funcs 0

tp @e[tag=blocks] @e[tag=death,limit=1]


execute at @e[tag=cake_home] run function v3:blocks/cake_init
execute at @e[tag=command_blocks_home] run function v3:blocks/command_blocks_init
execute at @e[tag=structure_blocks_home] run function v3:blocks/structure_blocks_init
