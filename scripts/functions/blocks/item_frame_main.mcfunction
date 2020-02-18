execute unless score item_frame funcs matches 0.. run function item_frame_init
scoreboard players add item_frame funcs 1
scoreboard players set item_frame max 8
execute unless score item_frame funcs matches 0..7 run scoreboard players operation item_frame funcs %= item_frame max
execute if score item_frame funcs matches 0 run data merge entity @e[tag=item_frame_as_block,limit=1] {ItemRotation:0}

execute if score item_frame funcs matches 1 run data merge entity @e[tag=item_frame_as_block,limit=1] {ItemRotation:1}

execute if score item_frame funcs matches 2 run data merge entity @e[tag=item_frame_as_block,limit=1] {ItemRotation:2}

execute if score item_frame funcs matches 3 run data merge entity @e[tag=item_frame_as_block,limit=1] {ItemRotation:3}

execute if score item_frame funcs matches 4 run data merge entity @e[tag=item_frame_as_block,limit=1] {ItemRotation:4}

execute if score item_frame funcs matches 5 run data merge entity @e[tag=item_frame_as_block,limit=1] {ItemRotation:5}

execute if score item_frame funcs matches 6 run data merge entity @e[tag=item_frame_as_block,limit=1] {ItemRotation:6}

execute if score item_frame funcs matches 7 run data merge entity @e[tag=item_frame_as_block,limit=1] {ItemRotation:7}
