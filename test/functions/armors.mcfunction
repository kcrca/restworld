



execute unless score armors funcs matches 0.. run function armors_init
scoreboard players add armors funcs 1
execute unless score armors funcs matches 0..4 run scoreboard players set armors funcs 0

execute if score armors funcs matches 0 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Leather\"",ArmorItems:[{id:leather_boots,Count:1},{id:leather_leggings,Count:1},{id:leather_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score armors funcs matches 0 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Leather\"",ArmorItems:[{id:leather_boots,Count:1},{id:leather_leggings,Count:1},{id:leather_chestplate,Count:1},{id:leather_helmet,Count:1}]}


execute if score armors funcs matches 1 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Iron\"",ArmorItems:[{id:iron_boots,Count:1},{id:iron_leggings,Count:1},{id:iron_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score armors funcs matches 1 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Iron\"",ArmorItems:[{id:iron_boots,Count:1},{id:iron_leggings,Count:1},{id:iron_chestplate,Count:1},{id:iron_helmet,Count:1}]}


execute if score armors funcs matches 2 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Chainmail\"",ArmorItems:[{id:chainmail_boots,Count:1},{id:chainmail_leggings,Count:1},{id:chainmail_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score armors funcs matches 2 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Chainmail\"",ArmorItems:[{id:chainmail_boots,Count:1},{id:chainmail_leggings,Count:1},{id:chainmail_chestplate,Count:1},{id:chainmail_helmet,Count:1}]}


execute if score armors funcs matches 3 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Golden\"",ArmorItems:[{id:golden_boots,Count:1},{id:golden_leggings,Count:1},{id:golden_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score armors funcs matches 3 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Golden\"",ArmorItems:[{id:golden_boots,Count:1},{id:golden_leggings,Count:1},{id:golden_chestplate,Count:1},{id:golden_helmet,Count:1}]}


execute if score armors funcs matches 4 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Diamond\"",ArmorItems:[{id:diamond_boots,Count:1},{id:diamond_leggings,Count:1},{id:diamond_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score armors funcs matches 4 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Diamond\"",ArmorItems:[{id:diamond_boots,Count:1},{id:diamond_leggings,Count:1},{id:diamond_chestplate,Count:1},{id:diamond_helmet,Count:1}]}


