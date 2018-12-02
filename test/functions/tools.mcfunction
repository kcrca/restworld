execute unless score tools funcs matches 0.. run function tools_init
scoreboard players add tools funcs 1
execute unless score tools funcs matches 0..3 run scoreboard players set tools funcs 0

execute if score tools funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:shears,Count:1},{id:fishing_rod,Count:1}]}


execute if score tools funcs matches 1 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:trident,Count:1},{id:iron_sword,Count:1}]}


execute if score tools funcs matches 2 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:iron_pickaxe,Count:1},{id:iron_axe,Count:1}]}


execute if score tools funcs matches 3 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:iron_shovel,Count:1},{id:iron_hoe,Count:1}]}