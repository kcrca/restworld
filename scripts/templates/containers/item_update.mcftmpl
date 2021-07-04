execute unless entity @e[tag=item_ground] at @e[tag=item_home] run summon item ~0 ~3 ~1 {Item:{id:iron_pickaxe,Count:1},Age:-32768,PickupDelay:2147483647,Tags:[item_ground]}
data modify entity @e[tag=item_ground,limit=1] Item set from entity @e[tag=item_src,limit=1] Item
data merge entity @e[tag=item_ground,limit=1] {Age:-32768,PickupDelay:2147483647}

data modify entity @e[tag=item_hands,limit=1] HandItems[0] set from entity @e[tag=item_src,limit=1] Item
data modify entity @e[tag=item_hands,limit=1] HandItems[1] set from entity @e[tag=item_src,limit=1] Item
data remove entity @e[tag=item_hands,limit=1] ArmorItems[3]
execute if score item_head funcs matches 1 run data modify entity @e[tag=item_hands,limit=1] ArmorItems[3] set from entity @e[tag=item_src,limit=1] Item
