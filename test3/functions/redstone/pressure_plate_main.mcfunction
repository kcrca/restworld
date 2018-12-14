execute unless score pressure_plate funcs matches 0.. run function pressure_plate_init
scoreboard players add pressure_plate funcs 1
scoreboard players set pressure_plate max 16
execute unless score pressure_plate funcs matches 0..15 run scoreboard players operation pressure_plate funcs %= pressure_plate max

execute if score pressure_plate funcs matches 0 run kill @e[tag=plate_items]
execute if score pressure_plate funcs matches 1..15 run function v3:redstone/pressure_plate_add
