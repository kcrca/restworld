kill @e[tag=colorings_item]

summon minecraft:item_frame ~-6 ~3 ~2 {Facing:3,Tags:[colorings_item_frame,colorings_item],Item:{id:stone,Count:1}}
summon minecraft:armor_stand ~-9 ~2 ~2 {Tags:[colorings_armor_stand,colorings_item],Rotation:[-45f,0f]}
summon minecraft:horse ~-11.5 ~2 ~4 {Tags:[colorings_horse,colorings_item],ArmorItem:{id:leather_horse_armor,Count:1},Rotation:[-135f,0f],Tame:true,NoAI:true,Silent:true}
summon minecraft:llama ~1.2 ~2 ~4 {Tags:[colorings_llama,colorings_item],Variant:1,Tame:true,NoAI:true,Silent:true,Rotation:[160f,0f],Leashed:true}

setblock ~-5 ~3 ~2 oak_wall_sign[facing=south]
setblock ~-3 ~3 ~2 oak_wall_sign[facing=south]
setblock ~-5 ~3 ~0 oak_wall_sign[facing=south]
data merge block ~-5 ~3 ~2 {Text2:"\"Shulker Box\""}
data merge block ~-3 ~3 ~2 {Text2:"\"Terracotta\""}
data merge block ~-5 ~3 ~0 {Text2:"\"Banner\""}
