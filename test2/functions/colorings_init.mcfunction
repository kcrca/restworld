execute positioned ~ ~2 ~ run kill @e[dx=-15,dy=5,dz=5,type=!player]
kill @e[tag=colorings_item]

summon minecraft:item_frame ~-6 ~4 ~2 {Facing:3,Tags:[colorings_item_frame],Item:{id:stone,Count:1}}
summon minecraft:armor_stand ~-9 ~2.5 ~2 {Tags:[colorings_armor_stand],Rotation:[-45f,0f]}
summon minecraft:llama ~1.2 ~2.5 ~4 {Tags:[colorings_llama],Variant:1,Tame:True,NoAI:True,Silent:True,Rotation:[160f,0f],Leashed:True,Leash:{X:36,Y:104,Z:-85}}

setblock ~-5 ~4 ~2 minecraft:wall_sign[facing=south]{Text2:"\"Shulker Box\""}

execute positioned ~ ~1 ~ run tag @e[dx=-15,dy=5,dz=5,type=!player] add colorings_item