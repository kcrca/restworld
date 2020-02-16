kill @e[tag=colorings_item]

summon minecraft:item_frame ~-4.5 ~4 ~0.5 {Facing:3,Tags:[colorings_item_frame,colorings_item],Item:{id:stone,Count:1}}
summon minecraft:horse ~-10.7 ~2 ~4.8 {Tags:[colorings_horse,colorings_item],ArmorItem:{id:leather_horse_armor,Count:1},Rotation:[-155f,0f],Tame:true,NoAI:true,Silent:true}
summon minecraft:armor_stand ~-0.1 ~2 ~3 {Tags:[colorings_armor_stand,colorings_item],Rotation:[45f,0f]}
summon minecraft:llama ~1.2 ~2 ~5 {Tags:[colorings_llama,colorings_item],Variant:1,Tame:true,NoAI:true,Silent:true,Rotation:[160f,0f],Leashed:true}

setblock ~-1 ~3 ~1 oak_wall_sign[facing=south]{Text2:"\"Terracotta\""} destroy
setblock ~-3 ~3 ~1 oak_wall_sign[facing=south]{Text2:"\"Shulker Box\""} destroy
setblock ~-5 ~3 ~1 oak_wall_sign[facing=south]{Text2:"\"Concrete\""} destroy
setblock ~-7 ~3 ~1 oak_wall_sign[facing=south]{Text2:"\"Glass\""} destroy





setblock ~-11 ~2 ~2 acacia_sign[rotation=14]{Text2:"\"Acacia\"",Text3:"\"With Text Colored\"",Text4:"\"Black\""} destroy

setblock ~-10 ~2 ~1 birch_sign[rotation=14]{Text2:"\"Birch\"",Text3:"\"With Text Colored\"",Text4:"\"Black\""} destroy

setblock ~-9 ~2 ~0 jungle_sign[rotation=14]{Text2:"\"Jungle\"",Text3:"\"With Text Colored\"",Text4:"\"Black\""} destroy

setblock ~-11 ~3 ~2 oak_sign[rotation=14]{Text2:"\"Oak\"",Text3:"\"With Text Colored\"",Text4:"\"Black\""} destroy

setblock ~-10 ~3 ~1 dark_oak_sign[rotation=14]{Text2:"\"Dark Oak\"",Text3:"\"With Text Colored\"",Text4:"\"Black\""} destroy

setblock ~-9 ~3 ~0 spruce_sign[rotation=14]{Text2:"\"Spruce\"",Text3:"\"With Text Colored\"",Text4:"\"Black\""} destroy


setblock ~-4 ~2 ~4 oak_wall_sign[facing=south]
