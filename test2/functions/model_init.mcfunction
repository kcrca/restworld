kill @e[tag=modeling]
summon minecraft:armor_stand ~0 ~2.5 ~0 {Tags:[modeler,modeling],Rotation:[270f,0f],ShowArms:True,ArmorItems:[{id:iron_boots,Count:1},{id:iron_leggings,Count:1},{id:iron_chestplate,Count:1},{id:iron_helmet,Count:1}]}
summon minecraft:item_frame ~1 ~4 ~2 {Facing:5,Tags:[model_item_frame,modeling],Item:{id:stone,Count:1}}

setblock ~2 ~3 ~1 magma_block