tp @e[tag=material_thing] @e[tag=death,limit=1]



execute if score materials funcs matches 0 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Wooden\"",ArmorItems:[{id:leather_boots,Count:1},{id:leather_leggings,Count:1},{id:leather_chestplate,Count:1},{id:leather_helmet,Count:1}]}
execute if score materials funcs matches 0 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Wooden\"",ArmorItems:[{id:leather_boots,Count:1},{id:leather_leggings,Count:1},{id:leather_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score materials funcs matches 0 run fill ~-3 ~2 ~2 ~-3 ~5 ~2 minecraft:oak_planks
execute if score materials funcs matches 0 run setblock ~4 ~4 ~2 minecraft:oak_planks
execute if score materials funcs matches 0 run
execute if score materials funcs matches 0 run data merge entity @e[tag=armor_boots,limit=1] {Item:{id:leather_boots,Count:1},ItemRotation:0}
execute if score materials funcs matches 0 run data merge entity @e[tag=armor_leggings,limit=1] {Item:{id:leather_leggings,Count:1},ItemRotation:0}
execute if score materials funcs matches 0 run data merge entity @e[tag=armor_chestplate,limit=1] {Item:{id:leather_chestplate,Count:1},ItemRotation:0}
execute if score materials funcs matches 0 run data merge entity @e[tag=armor_helmet,limit=1] {Item:{id:leather_helmet,Count:1},ItemRotation:0}

execute if score materials funcs matches 0 run data merge entity @e[tag=armor_horse_frame,limit=1] {Item:{id:stone,Count:0},ItemRotation:0}
execute if score materials funcs matches 0 run execute if entity @e[tag=armor_horse,distance=..10] run teleport @e[tag=armor_horse] @e[tag=death,limit=1]

execute if score materials funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:wooden_sword,Count:1},{id:shield,Count:1}]}

execute if score materials funcs matches 0 run data merge entity @e[tag=material_0,limit=1] {HandItems:[{}]}
execute if score materials funcs matches 0 run data merge entity @e[tag=material_1,limit=1] {HandItems:[{id:bow,Count:1}]}
execute if score materials funcs matches 0 run data merge entity @e[tag=material_2,limit=1] {HandItems:[{id:wooden_shovel,Count:1}]}
execute if score materials funcs matches 0 run data merge entity @e[tag=material_3,limit=1] {HandItems:[{id:wooden_pickaxe,Count:1}]}
execute if score materials funcs matches 0 run data merge entity @e[tag=material_4,limit=1] {HandItems:[{},{id:wooden_hoe,Count:1}]}
execute if score materials funcs matches 0 run data merge entity @e[tag=material_5,limit=1] {HandItems:[{},{id:wooden_axe,Count:1}]}
execute if score materials funcs matches 0 run data merge entity @e[tag=material_6,limit=1] {HandItems:[{},{id:fishing_rod,Count:1}]}
execute if score materials funcs matches 0 run data merge entity @e[tag=material_7,limit=1] {HandItems:[{},{}]}
execute if score materials funcs matches 0 run data merge block ~-2 ~ ~1 {name:"minecraft:material_wooden"}


execute if score materials funcs matches 1 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Stone\"",ArmorItems:[{id:chainmail_boots,Count:1},{id:chainmail_leggings,Count:1},{id:chainmail_chestplate,Count:1},{id:chainmail_helmet,Count:1}]}
execute if score materials funcs matches 1 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Stone\"",ArmorItems:[{id:chainmail_boots,Count:1},{id:chainmail_leggings,Count:1},{id:chainmail_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score materials funcs matches 1 run fill ~-3 ~2 ~2 ~-3 ~5 ~2 minecraft:stone
execute if score materials funcs matches 1 run setblock ~4 ~4 ~2 minecraft:stone
execute if score materials funcs matches 1 run
execute if score materials funcs matches 1 run data merge entity @e[tag=armor_boots,limit=1] {Item:{id:chainmail_boots,Count:1},ItemRotation:0}
execute if score materials funcs matches 1 run data merge entity @e[tag=armor_leggings,limit=1] {Item:{id:chainmail_leggings,Count:1},ItemRotation:0}
execute if score materials funcs matches 1 run data merge entity @e[tag=armor_chestplate,limit=1] {Item:{id:chainmail_chestplate,Count:1},ItemRotation:0}
execute if score materials funcs matches 1 run data merge entity @e[tag=armor_helmet,limit=1] {Item:{id:chainmail_helmet,Count:1},ItemRotation:0}

execute if score materials funcs matches 1 run data merge entity @e[tag=armor_horse_frame,limit=1] {Item:{id:stone,Count:0},ItemRotation:0}
execute if score materials funcs matches 1 run execute if entity @e[tag=armor_horse,distance=..10] run teleport @e[tag=armor_horse] @e[tag=death,limit=1]

execute if score materials funcs matches 1 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:stone_sword,Count:1},{id:shield,Count:1}]}

execute if score materials funcs matches 1 run data merge entity @e[tag=material_0,limit=1] {HandItems:[{}]}
execute if score materials funcs matches 1 run data merge entity @e[tag=material_1,limit=1] {HandItems:[{}]}
execute if score materials funcs matches 1 run data merge entity @e[tag=material_2,limit=1] {HandItems:[{id:stone_shovel,Count:1}]}
execute if score materials funcs matches 1 run data merge entity @e[tag=material_3,limit=1] {HandItems:[{id:stone_pickaxe,Count:1}]}
execute if score materials funcs matches 1 run data merge entity @e[tag=material_4,limit=1] {HandItems:[{},{id:stone_hoe,Count:1}]}
execute if score materials funcs matches 1 run data merge entity @e[tag=material_5,limit=1] {HandItems:[{},{id:stone_axe,Count:1}]}
execute if score materials funcs matches 1 run data merge entity @e[tag=material_6,limit=1] {HandItems:[{},{}]}
execute if score materials funcs matches 1 run data merge entity @e[tag=material_7,limit=1] {HandItems:[{},{}]}
execute if score materials funcs matches 1 run data merge block ~-2 ~ ~1 {name:"minecraft:material_stone"}


execute if score materials funcs matches 2 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Iron\"",ArmorItems:[{id:iron_boots,Count:1},{id:iron_leggings,Count:1},{id:iron_chestplate,Count:1},{id:iron_helmet,Count:1}]}
execute if score materials funcs matches 2 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Iron\"",ArmorItems:[{id:iron_boots,Count:1},{id:iron_leggings,Count:1},{id:iron_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score materials funcs matches 2 run fill ~-3 ~2 ~2 ~-3 ~5 ~2 minecraft:iron_block
execute if score materials funcs matches 2 run setblock ~4 ~4 ~2 minecraft:iron_block
execute if score materials funcs matches 2 run
execute if score materials funcs matches 2 run data merge entity @e[tag=armor_boots,limit=1] {Item:{id:iron_boots,Count:1},ItemRotation:0}
execute if score materials funcs matches 2 run data merge entity @e[tag=armor_leggings,limit=1] {Item:{id:iron_leggings,Count:1},ItemRotation:0}
execute if score materials funcs matches 2 run data merge entity @e[tag=armor_chestplate,limit=1] {Item:{id:iron_chestplate,Count:1},ItemRotation:0}
execute if score materials funcs matches 2 run data merge entity @e[tag=armor_helmet,limit=1] {Item:{id:iron_helmet,Count:1},ItemRotation:0}

execute if score materials funcs matches 2 run execute unless entity @e[tag=armor_horse,distance=..10] run summon minecraft:horse ~4.5 ~2 ~0.5 {Variant:1,Tame:True,NoAI:True,Silent:True,Tags:[armor_horse,material_static],Rotation:[180f,0f]}
execute if score materials funcs matches 2 run data merge entity @e[tag=armor_horse,limit=1,sort=nearest] {ArmorItem:{id:iron_horse_armor,Count:1}}
execute if score materials funcs matches 2 run data merge entity @e[tag=armor_horse_frame,limit=1] {Item:{id:iron_horse_armor,Count:1},ItemRotation:0}
execute if score materials funcs matches 2 run execute if score horse_saddle funcs matches 1 run data merge entity @e[tag=armor_horse,limit=1,sort=nearest] {SaddleItem:{id:saddle,Count:1}}

execute if score materials funcs matches 2 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:iron_sword,Count:1},{id:shield,Count:1}]}

execute if score materials funcs matches 2 run data merge entity @e[tag=material_0,limit=1] {HandItems:[{}]}
execute if score materials funcs matches 2 run data merge entity @e[tag=material_1,limit=1] {HandItems:[{id:flint_and_steel,Count:1}]}
execute if score materials funcs matches 2 run data merge entity @e[tag=material_2,limit=1] {HandItems:[{id:iron_shovel,Count:1}]}
execute if score materials funcs matches 2 run data merge entity @e[tag=material_3,limit=1] {HandItems:[{id:iron_pickaxe,Count:1}]}
execute if score materials funcs matches 2 run data merge entity @e[tag=material_4,limit=1] {HandItems:[{},{id:iron_hoe,Count:1}]}
execute if score materials funcs matches 2 run data merge entity @e[tag=material_5,limit=1] {HandItems:[{},{id:iron_axe,Count:1}]}
execute if score materials funcs matches 2 run data merge entity @e[tag=material_6,limit=1] {HandItems:[{},{id:shears,Count:1}]}
execute if score materials funcs matches 2 run data merge entity @e[tag=material_7,limit=1] {HandItems:[{},{id:compass,Count:1}]}
execute if score materials funcs matches 2 run data merge block ~-2 ~ ~1 {name:"minecraft:material_iron"}


execute if score materials funcs matches 3 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Golden\"",ArmorItems:[{id:golden_boots,Count:1},{id:golden_leggings,Count:1},{id:golden_chestplate,Count:1},{id:golden_helmet,Count:1}]}
execute if score materials funcs matches 3 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Golden\"",ArmorItems:[{id:golden_boots,Count:1},{id:golden_leggings,Count:1},{id:golden_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score materials funcs matches 3 run fill ~-3 ~2 ~2 ~-3 ~5 ~2 minecraft:gold_block
execute if score materials funcs matches 3 run setblock ~4 ~4 ~2 minecraft:gold_block
execute if score materials funcs matches 3 run
execute if score materials funcs matches 3 run data merge entity @e[tag=armor_boots,limit=1] {Item:{id:golden_boots,Count:1},ItemRotation:0}
execute if score materials funcs matches 3 run data merge entity @e[tag=armor_leggings,limit=1] {Item:{id:golden_leggings,Count:1},ItemRotation:0}
execute if score materials funcs matches 3 run data merge entity @e[tag=armor_chestplate,limit=1] {Item:{id:golden_chestplate,Count:1},ItemRotation:0}
execute if score materials funcs matches 3 run data merge entity @e[tag=armor_helmet,limit=1] {Item:{id:golden_helmet,Count:1},ItemRotation:0}

execute if score materials funcs matches 3 run execute unless entity @e[tag=armor_horse,distance=..10] run summon minecraft:horse ~4.5 ~2 ~0.5 {Variant:1,Tame:True,NoAI:True,Silent:True,Tags:[armor_horse,material_static],Rotation:[180f,0f]}
execute if score materials funcs matches 3 run data merge entity @e[tag=armor_horse,limit=1,sort=nearest] {ArmorItem:{id:golden_horse_armor,Count:1}}
execute if score materials funcs matches 3 run data merge entity @e[tag=armor_horse_frame,limit=1] {Item:{id:golden_horse_armor,Count:1},ItemRotation:0}
execute if score materials funcs matches 3 run execute if score horse_saddle funcs matches 1 run data merge entity @e[tag=armor_horse,limit=1,sort=nearest] {SaddleItem:{id:saddle,Count:1}}

execute if score materials funcs matches 3 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:golden_sword,Count:1},{id:shield,Count:1}]}

execute if score materials funcs matches 3 run data merge entity @e[tag=material_0,limit=1] {HandItems:[{}]}
execute if score materials funcs matches 3 run data merge entity @e[tag=material_1,limit=1] {HandItems:[{}]}
execute if score materials funcs matches 3 run data merge entity @e[tag=material_2,limit=1] {HandItems:[{id:golden_shovel,Count:1}]}
execute if score materials funcs matches 3 run data merge entity @e[tag=material_3,limit=1] {HandItems:[{id:golden_pickaxe,Count:1}]}
execute if score materials funcs matches 3 run data merge entity @e[tag=material_4,limit=1] {HandItems:[{},{id:golden_hoe,Count:1}]}
execute if score materials funcs matches 3 run data merge entity @e[tag=material_5,limit=1] {HandItems:[{},{id:golden_axe,Count:1}]}
execute if score materials funcs matches 3 run data merge entity @e[tag=material_6,limit=1] {HandItems:[{},{id:clock,Count:1}]}
execute if score materials funcs matches 3 run data merge entity @e[tag=material_7,limit=1] {HandItems:[{},{}]}
execute if score materials funcs matches 3 run data merge block ~-2 ~ ~1 {name:"minecraft:material_golden"}


execute if score materials funcs matches 4 if score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Diamond\"",ArmorItems:[{id:diamond_boots,Count:1},{id:diamond_leggings,Count:1},{id:diamond_chestplate,Count:1},{id:diamond_helmet,Count:1}]}
execute if score materials funcs matches 4 unless score turtle_helmet funcs matches 0 run data merge entity @e[tag=armor_stand,limit=1] {CustomName:"\"Diamond\"",ArmorItems:[{id:diamond_boots,Count:1},{id:diamond_leggings,Count:1},{id:diamond_chestplate,Count:1},{id:turtle_helmet,Count:1}]}
execute if score materials funcs matches 4 run fill ~-3 ~2 ~2 ~-3 ~5 ~2 minecraft:diamond_block
execute if score materials funcs matches 4 run setblock ~4 ~4 ~2 minecraft:diamond_block
execute if score materials funcs matches 4 run
execute if score materials funcs matches 4 run data merge entity @e[tag=armor_boots,limit=1] {Item:{id:diamond_boots,Count:1},ItemRotation:0}
execute if score materials funcs matches 4 run data merge entity @e[tag=armor_leggings,limit=1] {Item:{id:diamond_leggings,Count:1},ItemRotation:0}
execute if score materials funcs matches 4 run data merge entity @e[tag=armor_chestplate,limit=1] {Item:{id:diamond_chestplate,Count:1},ItemRotation:0}
execute if score materials funcs matches 4 run data merge entity @e[tag=armor_helmet,limit=1] {Item:{id:diamond_helmet,Count:1},ItemRotation:0}

execute if score materials funcs matches 4 run execute unless entity @e[tag=armor_horse,distance=..10] run summon minecraft:horse ~4.5 ~2 ~0.5 {Variant:1,Tame:True,NoAI:True,Silent:True,Tags:[armor_horse,material_static],Rotation:[180f,0f]}
execute if score materials funcs matches 4 run data merge entity @e[tag=armor_horse,limit=1,sort=nearest] {ArmorItem:{id:diamond_horse_armor,Count:1}}
execute if score materials funcs matches 4 run data merge entity @e[tag=armor_horse_frame,limit=1] {Item:{id:diamond_horse_armor,Count:1},ItemRotation:0}
execute if score materials funcs matches 4 run execute if score horse_saddle funcs matches 1 run data merge entity @e[tag=armor_horse,limit=1,sort=nearest] {SaddleItem:{id:saddle,Count:1}}

execute if score materials funcs matches 4 run data merge entity @e[tag=armor_stand,limit=1] {HandItems:[{id:diamond_sword,Count:1},{id:shield,Count:1}]}

execute if score materials funcs matches 4 run data merge entity @e[tag=material_0,limit=1] {HandItems:[{}]}
execute if score materials funcs matches 4 run data merge entity @e[tag=material_1,limit=1] {HandItems:[{}]}
execute if score materials funcs matches 4 run data merge entity @e[tag=material_2,limit=1] {HandItems:[{id:diamond_shovel,Count:1}]}
execute if score materials funcs matches 4 run data merge entity @e[tag=material_3,limit=1] {HandItems:[{id:diamond_pickaxe,Count:1}]}
execute if score materials funcs matches 4 run data merge entity @e[tag=material_4,limit=1] {HandItems:[{},{id:diamond_hoe,Count:1}]}
execute if score materials funcs matches 4 run data merge entity @e[tag=material_5,limit=1] {HandItems:[{},{id:diamond_axe,Count:1}]}
execute if score materials funcs matches 4 run data merge entity @e[tag=material_6,limit=1] {HandItems:[{},{}]}
execute if score materials funcs matches 4 run data merge entity @e[tag=material_7,limit=1] {HandItems:[{},{}]}
execute if score materials funcs matches 4 run data merge block ~-2 ~ ~1 {name:"minecraft:material_diamond"}
