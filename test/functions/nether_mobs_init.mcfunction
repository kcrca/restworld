summon minecraft:ghast ~ ~6 ~1 {CustomName:"\"Ghast\"",NoAI:True,Silent:True,Rotation:[90f]}
summon minecraft:blaze ~-4 ~2 ~1.5 {CustomName:"\"Blaze\"",NoAI:True,Silent:True}
summon minecraft:magma_cube ~ ~2 ~-2 {CustomName:"\"Hopping\"",NoAI:True,Silent:True}
summon armor_stand ~-4 ~3 ~-2 {Invisible:True,Small:True,Facing:north,Passengers:[{id:magma_cube,CustomName:"\"Magma Cube\"",Tags:[growing],NoAI:True,Silent:True}]}
