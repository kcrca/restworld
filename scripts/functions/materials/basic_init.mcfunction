tp @e[tag=material_static] @e[tag=death,limit=1]

summon armor_stand ~ ~2.0 ~ {CustomNameVisible:True,Tags:[armor_stand,material_static],Rotation:[180f,0f],ShowArms:True}

summon armor_stand ~-0.8 ~2.0 ~ {Tags:[material_4,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True,NoGravity:True}
summon armor_stand ~0.6 ~2.0 ~ {Tags:[material_3,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True,NoGravity:True}
summon armor_stand ~-1.5 ~2.0 ~ {Tags:[material_5,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True,NoGravity:True}
summon armor_stand ~1.3 ~2.0 ~ {Tags:[material_2,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True,NoGravity:True}
summon armor_stand ~-2.2 ~2.0 ~ {Tags:[material_6,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True,NoGravity:True}
summon armor_stand ~2.0 ~2.0 ~ {Tags:[material_1,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True,NoGravity:True}
summon armor_stand ~-2.9 ~2.0 ~ {Tags:[material_7,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True,NoGravity:True}
summon armor_stand ~2.7 ~2.0 ~ {Tags:[material_0,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True,NoGravity:True}

fill ~-3 ~2 ~2 ~-3 ~5 ~2 stone

tp @e[tag=armor_frame] @e[tag=death,limit=1]

summon item_frame ~-3 ~2 ~1 {Facing:2,Tags:[armor_boots,armor_frame],Item:{id:stone,Count:1},temRotation:0}
summon item_frame ~-3 ~3 ~1 {Facing:2,Tags:[armor_leggings,armor_frame],Item:{id:jungle_leaves,Count:1},temRotation:0}
summon item_frame ~-3 ~4 ~1 {Facing:2,Tags:[armor_chestplate,armor_frame],Item:{id:acacia_leaves,Count:1},temRotation:0}
summon item_frame ~-3 ~5 ~1 {Facing:2,Tags:[armor_helmet,armor_frame],Item:{id:oak_leaves,Count:1},temRotation:0}
summon item_frame ~4 ~4 ~1 {Facing:2,Tags:[armor_horse_frame,armor_frame],Item:{id:oak_leaves,Count:1},temRotation:0}
function v3:materials/materials_cur
