





execute if score weapons funcs matches 0 run data merge entity @e[tag=shovel_stand,limit=1] {HandItems:[{},{id:wooden_shovel,Count:1}]}
execute if score weapons funcs matches 0 run data merge entity @e[tag=hoe_stand,limit=1] {HandItems:[{},{id:wooden_hoe,Count:1}]}

execute if score weapons funcs matches 0 run data merge entity @e[tag=sword_stand,limit=1] {ShowArms:True,ArmorItems:[],HandItems:[{id:wooden_sword,Count:1},{id:shield,Count:1}],CustomName:"\"Wooden\""}

execute if score weapons funcs matches 0 run data merge entity @e[tag=axe_stand,limit=1] {HandItems:[{id:wooden_axe,Count:1}]}
execute if score weapons funcs matches 0 run data merge entity @e[tag=pickaxe_stand,limit=1] {HandItems:[{id:wooden_pickaxe,Count:1}]}

execute if score weapons funcs matches 0 run fill ~-3 ~2 ~1 ~-4 ~2 ~1 minecraft:stone
execute if score weapons funcs matches 0 run setblock ~-3 ~2 ~3 minecraft:cobblestone
execute if score weapons funcs matches 0 run setblock ~-3 ~2 ~-1 minecraft:cobblestone
execute if score weapons funcs matches 0 run setblock ~-4 ~3 ~3 minecraft:cobblestone
execute if score weapons funcs matches 0 run setblock ~-4 ~3 ~1 minecraft:cobblestone
execute if score weapons funcs matches 0 run setblock ~-4 ~3 ~-1 minecraft:cobblestone
execute if score weapons funcs matches 0 run data merge entity @e[tag=source1_frame,limit=1] {Item:{id:cobblestone},Count:1,ItemRotation:0}
execute if score weapons funcs matches 0 run data merge entity @e[tag=source2_frame,limit=1] {Item:{id:stone},Count:1,ItemRotation:0}



execute if score weapons funcs matches 1 run data merge entity @e[tag=shovel_stand,limit=1] {HandItems:[{},{id:stone_shovel,Count:1}]}
execute if score weapons funcs matches 1 run data merge entity @e[tag=hoe_stand,limit=1] {HandItems:[{},{id:stone_hoe,Count:1}]}

execute if score weapons funcs matches 1 run data merge entity @e[tag=sword_stand,limit=1] {ShowArms:True,ArmorItems:[],HandItems:[{id:stone_sword,Count:1},{id:shield,Count:1}],CustomName:"\"Stone\""}

execute if score weapons funcs matches 1 run data merge entity @e[tag=axe_stand,limit=1] {HandItems:[{id:stone_axe,Count:1}]}
execute if score weapons funcs matches 1 run data merge entity @e[tag=pickaxe_stand,limit=1] {HandItems:[{id:stone_pickaxe,Count:1}]}

execute if score weapons funcs matches 1 run fill ~-3 ~2 ~1 ~-4 ~2 ~1 minecraft:oak_wood
execute if score weapons funcs matches 1 run setblock ~-3 ~2 ~3 minecraft:oak_log
execute if score weapons funcs matches 1 run setblock ~-3 ~2 ~-1 minecraft:oak_log
execute if score weapons funcs matches 1 run setblock ~-4 ~3 ~3 minecraft:oak_log
execute if score weapons funcs matches 1 run setblock ~-4 ~3 ~1 minecraft:oak_log
execute if score weapons funcs matches 1 run setblock ~-4 ~3 ~-1 minecraft:oak_log
execute if score weapons funcs matches 1 run data merge entity @e[tag=source1_frame,limit=1] {Item:{id:oak_sapling},Count:1,ItemRotation:0}
execute if score weapons funcs matches 1 run data merge entity @e[tag=source2_frame,limit=1] {Item:{id:oak_planks},Count:1,ItemRotation:0}


execute if score weapons funcs matches 2 run data merge entity @e[tag=armor_horse,limit=1] {ArmorItem:{id:"minecraft:iron_horse_armor",Count:1}}
execute if score weapons funcs matches 2 run data merge entity @e[tag=horse_armor_frame,limit=1] {Item:{id:iron_horse_armor},Count:1,ItemRotation:0}

execute if score weapons funcs matches 2 run data merge entity @e[tag=shovel_stand,limit=1] {HandItems:[{},{id:iron_shovel,Count:1}]}
execute if score weapons funcs matches 2 run data merge entity @e[tag=hoe_stand,limit=1] {HandItems:[{},{id:iron_hoe,Count:1}]}

execute if score weapons funcs matches 2 run data merge entity @e[tag=sword_stand,limit=1] {ArmorItems:[{id:iron_boots,Count:1},{id:iron_leggings,Count:1},{id:iron_chestplate,Count:1},{id:iron_helmet,Count:1}],HandItems:[{id:iron_sword,Count:1},{id:shield,Count:1}],CustomName:"\"Iron\""}

execute if score weapons funcs matches 2 run data merge entity @e[tag=axe_stand,limit=1] {HandItems:[{id:iron_axe,Count:1}]}
execute if score weapons funcs matches 2 run data merge entity @e[tag=pickaxe_stand,limit=1] {HandItems:[{id:iron_pickaxe,Count:1}]}

execute if score weapons funcs matches 2 run fill ~-3 ~2 ~1 ~-4 ~2 ~1 minecraft:iron_block
execute if score weapons funcs matches 2 run setblock ~-3 ~2 ~3 minecraft:iron_ore
execute if score weapons funcs matches 2 run setblock ~-3 ~2 ~-1 minecraft:iron_ore
execute if score weapons funcs matches 2 run setblock ~-4 ~3 ~3 minecraft:iron_ore
execute if score weapons funcs matches 2 run setblock ~-4 ~3 ~1 minecraft:iron_ore
execute if score weapons funcs matches 2 run setblock ~-4 ~3 ~-1 minecraft:iron_ore
execute if score weapons funcs matches 2 run data merge entity @e[tag=source1_frame,limit=1] {Item:{id:iron_nugget},Count:1,ItemRotation:0}
execute if score weapons funcs matches 2 run data merge entity @e[tag=source2_frame,limit=1] {Item:{id:iron_ingot},Count:1,ItemRotation:0}


execute if score weapons funcs matches 3 run data merge entity @e[tag=armor_horse,limit=1] {ArmorItem:{id:"minecraft:golden_horse_armor",Count:1}}
execute if score weapons funcs matches 3 run data merge entity @e[tag=horse_armor_frame,limit=1] {Item:{id:golden_horse_armor},Count:1,ItemRotation:0}

execute if score weapons funcs matches 3 run data merge entity @e[tag=shovel_stand,limit=1] {HandItems:[{},{id:golden_shovel,Count:1}]}
execute if score weapons funcs matches 3 run data merge entity @e[tag=hoe_stand,limit=1] {HandItems:[{},{id:golden_hoe,Count:1}]}

execute if score weapons funcs matches 3 run data merge entity @e[tag=sword_stand,limit=1] {ArmorItems:[{id:golden_boots,Count:1},{id:golden_leggings,Count:1},{id:golden_chestplate,Count:1},{id:golden_helmet,Count:1}],HandItems:[{id:golden_sword,Count:1},{id:shield,Count:1}],CustomName:"\"Golden\""}

execute if score weapons funcs matches 3 run data merge entity @e[tag=axe_stand,limit=1] {HandItems:[{id:golden_axe,Count:1}]}
execute if score weapons funcs matches 3 run data merge entity @e[tag=pickaxe_stand,limit=1] {HandItems:[{id:golden_pickaxe,Count:1}]}

execute if score weapons funcs matches 3 run fill ~-3 ~2 ~1 ~-4 ~2 ~1 minecraft:gold_block
execute if score weapons funcs matches 3 run setblock ~-3 ~2 ~3 minecraft:gold_ore
execute if score weapons funcs matches 3 run setblock ~-3 ~2 ~-1 minecraft:gold_ore
execute if score weapons funcs matches 3 run setblock ~-4 ~3 ~3 minecraft:gold_ore
execute if score weapons funcs matches 3 run setblock ~-4 ~3 ~1 minecraft:gold_ore
execute if score weapons funcs matches 3 run setblock ~-4 ~3 ~-1 minecraft:gold_ore
execute if score weapons funcs matches 3 run data merge entity @e[tag=source1_frame,limit=1] {Item:{id:gold_nugget},Count:1,ItemRotation:0}
execute if score weapons funcs matches 3 run data merge entity @e[tag=source2_frame,limit=1] {Item:{id:gold_ingot},Count:1,ItemRotation:0}


execute if score weapons funcs matches 4 run data merge entity @e[tag=armor_horse,limit=1] {ArmorItem:{id:"minecraft:diamond_horse_armor",Count:1}}
execute if score weapons funcs matches 4 run data merge entity @e[tag=horse_armor_frame,limit=1] {Item:{id:diamond_horse_armor},Count:1,ItemRotation:0}

execute if score weapons funcs matches 4 run data merge entity @e[tag=shovel_stand,limit=1] {HandItems:[{},{id:diamond_shovel,Count:1}]}
execute if score weapons funcs matches 4 run data merge entity @e[tag=hoe_stand,limit=1] {HandItems:[{},{id:diamond_hoe,Count:1}]}

execute if score weapons funcs matches 4 run data merge entity @e[tag=sword_stand,limit=1] {ArmorItems:[{id:diamond_boots,Count:1},{id:diamond_leggings,Count:1},{id:diamond_chestplate,Count:1},{id:diamond_helmet,Count:1}],HandItems:[{id:diamond_sword,Count:1},{id:shield,Count:1}],CustomName:"\"Diamond\""}

execute if score weapons funcs matches 4 run data merge entity @e[tag=axe_stand,limit=1] {HandItems:[{id:diamond_axe,Count:1}]}
execute if score weapons funcs matches 4 run data merge entity @e[tag=pickaxe_stand,limit=1] {HandItems:[{id:diamond_pickaxe,Count:1}]}

execute if score weapons funcs matches 4 run fill ~-3 ~2 ~1 ~-4 ~2 ~1 minecraft:diamond_block
execute if score weapons funcs matches 4 run setblock ~-3 ~2 ~3 minecraft:diamond_ore
execute if score weapons funcs matches 4 run setblock ~-3 ~2 ~-1 minecraft:diamond_ore
execute if score weapons funcs matches 4 run setblock ~-4 ~3 ~3 minecraft:diamond_ore
execute if score weapons funcs matches 4 run setblock ~-4 ~3 ~1 minecraft:diamond_ore
execute if score weapons funcs matches 4 run setblock ~-4 ~3 ~-1 minecraft:diamond_ore
execute if score weapons funcs matches 4 run data merge entity @e[tag=source1_frame,limit=1] {Item:{id:diamond},Count:1,ItemRotation:0}
execute if score weapons funcs matches 4 run data merge entity @e[tag=source2_frame,limit=1] {Item:{id:diamond},Count:1,ItemRotation:0}


