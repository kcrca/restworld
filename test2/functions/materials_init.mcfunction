kill @e[tag=material_static]


summon armor_stand ~ ~1.5 ~ {Tags:[armor_stand,material_static],Rotation:[180f,0f],ShowArms:True}

summon armor_stand ~-0.8 ~1.5 ~ {Tags:[material_4,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True}
summon armor_stand ~0.6 ~1.5 ~ {Tags:[material_3,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True}
summon armor_stand ~-1.5 ~1.5 ~ {Tags:[material_5,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True}
summon armor_stand ~1.3 ~1.5 ~ {Tags:[material_2,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True}
summon armor_stand ~-2.2 ~1.5 ~ {Tags:[material_6,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True}
summon armor_stand ~2.0 ~1.5 ~ {Tags:[material_1,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True}
summon armor_stand ~-2.9 ~1.5 ~ {Tags:[material_7,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True}
summon armor_stand ~2.7 ~1.5 ~ {Tags:[material_0,material_static],Rotation:[180f,0f],ShowArms:True,Invisible:True}

fill ~-3 ~2 ~2 ~-3 ~5 ~2 stone

kill @e[tag=armor_frame]
summon item_frame ~-3 ~2 ~1 {Facing:2,Tags:[armor_boots,armor_frame],Item:{id:stone,Count:1},temRotation:0}
summon item_frame ~-3 ~3 ~1 {Facing:2,Tags:[armor_leggings,armor_frame],Item:{id:jungle_leaves,Count:1},temRotation:0}
summon item_frame ~-3 ~4 ~1 {Facing:2,Tags:[armor_chestplate,armor_frame],Item:{id:acacia_leaves,Count:1},temRotation:0}
summon item_frame ~-3 ~5 ~1 {Facing:2,Tags:[armor_helmet,armor_frame],Item:{id:oak_leaves,Count:1},temRotation:0}
summon item_frame ~4 ~4 ~1 {Facing:2,Tags:[armor_horse_frame,armor_frame],Item:{id:oak_leaves,Count:1},temRotation:0}
function v2:materials_cur