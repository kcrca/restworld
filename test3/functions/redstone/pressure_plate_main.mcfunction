execute unless score pressure_plate funcs matches 0.. run function pressure_plate_init
scoreboard players add pressure_plate funcs 1
execute unless score pressure_plate funcs matches 0..15 run scoreboard players set pressure_plate funcs 0

execute if score pressure_plate funcs matches 0 run kill @e[tag=plate_items]
execute if score pressure_plate funcs matches 1..15 run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}
execute if score pressure_plate funcs matches 1..15 if score plate_heavy funcs matches 1.. run summon item ~0 ~3 ~ {Item:{id:iron_pickaxe,Count:1},PickupDelay:2147483647,Tags:[plate_items]}