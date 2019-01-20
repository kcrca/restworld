scoreboard players add daylight_detector funcs 0
scoreboard players add dispenser funcs 0
scoreboard players add hopper funcs 0
scoreboard players add lever funcs 0
scoreboard players add minecarts funcs 0
scoreboard players add note_block funcs 0
scoreboard players add observer funcs 0
scoreboard players add piston funcs 0
scoreboard players add pressure_plate funcs 0
scoreboard players add rail funcs 0
scoreboard players add redstone_block funcs 0
scoreboard players add redstone_dust funcs 0
scoreboard players add redstone_lamp funcs 0
scoreboard players add redstone_torch funcs 0
scoreboard players add repeater funcs 0
scoreboard players add wood_power funcs 0

tp @e[tag=redstone] @e[tag=death,limit=1]


execute at @e[tag=dispenser_home] run function v3:redstone/dispenser_init
execute at @e[tag=note_block_home] run function v3:redstone/note_block_init
execute at @e[tag=piston_home] run function v3:redstone/piston_init
