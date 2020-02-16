kill @e[tag=colorings_item]
say hi

summon minecraft:item_frame ~-4.5 ~4 ~0.5 {Facing:3,Tags:[colorings_item_frame,colorings_item],Item:{id:stone,Count:1}}
summon minecraft:horse ~-10.2 ~2 ~4.8 {Tags:[colorings_horse,colorings_item],ArmorItem:{id:leather_horse_armor,Count:1},Rotation:[-155f,0f],Tame:true,NoAI:true,Silent:true}
summon minecraft:armor_stand ~-0.1 ~2 ~3 {Tags:[colorings_armor_stand,colorings_item],Rotation:[45f,0f]}
summon minecraft:llama ~1.2 ~2 ~5 {Tags:[colorings_llama,colorings_item],Variant:1,Tame:true,NoAI:true,Silent:true,Rotation:[160f,0f],Leashed:true}

setblock ~-1 ~3 ~1 oak_wall_sign[facing=south]{Text2:"\"Terracotta\""} destroy
setblock ~-3 ~3 ~1 oak_wall_sign[facing=south]{Text2:"\"Shulker Box\""} destroy
setblock ~-5 ~3 ~1 oak_wall_sign[facing=south]{Text2:"\"Concrete\""} destroy
setblock ~-7 ~3 ~1 oak_wall_sign[facing=south]{Text2:"\"Glass\""} destroy

setblock ~-4 ~2 ~4 oak_wall_sign[facing=south]
