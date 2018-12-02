kill @e[type=minecraft:item_frame,distance=..8]
summon minecraft:item_frame ~4 ~3 ~-2 {Facing:4}

kill @e[type=minecraft:armor_stand,distance=..8]
summon minecraft:armor_stand ~2.9 ~1.5 ~-5 {HandItems:[{},{id:stick,Count:1}],Invisible:True}
summon minecraft:armor_stand ~2.2 ~1.5 ~-5 {HandItems:[{},{id:wooden_shovel,Count:1}],Invisible:True}
summon minecraft:armor_stand ~1.3 ~1.5 ~-5 {ShowArms:True,HandItems:[{},{id:wooden_hoe,Count:1}],Invisible:True}
summon minecraft:armor_stand ~0.3 ~1.5 ~-5 {ShowArms:True,HandItems:[{id:wooden_sword,Count:1},{id:shield,Count:1}]}
summon minecraft:armor_stand ~-0.5 ~1.5 ~-5 {HandItems:[{id:wooden_axe,Count:1},{}],Invisible:True}
summon minecraft:armor_stand ~-1.3 ~1.5 ~-5 {HandItems:[{id:wooden_pickaxe,Count:1},{}],Invisible:True}
summon minecraft:armor_stand ~-2.1 ~1.5 ~-5 {HandItems:[{id:fishing_rod,Count:1},{}],Invisible:True}