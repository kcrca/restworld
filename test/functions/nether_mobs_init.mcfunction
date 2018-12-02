summon minecraft:ghast ~0 ~6 ~1 {CustomName:"\"Ghast\"",Tags:[],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:blaze ~-4 ~2 ~1.5 {CustomName:"\"Blaze\"",Tags:[],NoAI:True,Silent:True,Rotation:[90f,0f]}

summon minecraft:magma_cube ~ ~2 ~-2 {CustomName:"\"Hopping\"",Size:0}
summon armor_stand ~-4 ~3 ~-1 {Invisible:True,Small:True,Facing:north,Passengers:[{id:magma_cube,CustomName:"\"Magma Cube\"",Tags:[growing],NoAI:True,Silent:True}]}