kill @e[tag=colorings_item]

summon minecraft:item_frame ~-6 ~4 ~2 {Facing:3,Tags:[colorings_item_frame,colorings_item],Item:{id:stone,Count:1}}
summon minecraft:armor_stand ~-9 ~3 ~2 {Tags:[colorings_armor_stand,colorings_item],Rotation:[-45f,0f]}
summon minecraft:llama ~1.2 ~3 ~4 {Tags:[colorings_llama,colorings_item],Variant:1,Tame:true,NoAI:true,Silent:true,Rotation:[160f,0f],Leashed:true}

setblock ~-5 ~4 ~2 wall_sign[facing=south]{Text2:"\"Shulker Box\""}
setblock ~-3 ~4 ~2 wall_sign[facing=south]{Text2:"\"Terracotta\""}
setblock ~-5 ~4 ~0 wall_sign[facing=south]{Text2:"\"Banner\""}
