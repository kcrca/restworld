execute unless score colorings_turned funcs matches 0.. run function colorings_turned_init
scoreboard players add colorings_turned funcs 1
scoreboard players set colorings_turned max 16
execute unless score colorings_turned funcs matches 0..15 run scoreboard players operation colorings_turned funcs %= colorings_turned max

execute if score colorings_turned funcs matches 0 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:white_stained_glass_pane
execute if score colorings_turned funcs matches 0 run setblock ~4 ~4 ~-0 minecraft:white_stained_glass_pane
execute if score colorings_turned funcs matches 0 run setblock ~3 ~3 ~1 minecraft:white_stained_glass
execute if score colorings_turned funcs matches 0 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:white_wool
execute if score colorings_turned funcs matches 0 run setblock ~0 ~3 ~4 minecraft:white_banner[rotation=13]
execute if score colorings_turned funcs matches 0 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:white_carpet
execute if score colorings_turned funcs matches 0 run setblock ~1 ~3 ~7 minecraft:white_concrete
execute if score colorings_turned funcs matches 0 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 0 run setblock ~3 ~3 ~9 minecraft:white_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 0 run setblock ~3 ~3 ~10 minecraft:white_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 0 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:bone_meal},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 0 run setblock ~1 ~5 ~3 minecraft:white_terracotta
execute if score colorings_turned funcs matches 0 run setblock ~1 ~5 ~5 minecraft:white_shulker_box
execute if score colorings_turned funcs matches 0 run setblock ~1 ~5 ~7 minecraft:white_concrete_powder

execute if score colorings_turned funcs matches 0 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 0 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"White\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:16383998}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:16383998}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:16383998}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:16383998}}}]}
execute if score colorings_turned funcs matches 0 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:white_carpet,Count:1},CustomNameVisible:True,CustomName:"\"White\""}


execute if score colorings_turned funcs matches 1 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:orange_stained_glass_pane
execute if score colorings_turned funcs matches 1 run setblock ~4 ~4 ~-0 minecraft:orange_stained_glass_pane
execute if score colorings_turned funcs matches 1 run setblock ~3 ~3 ~1 minecraft:orange_stained_glass
execute if score colorings_turned funcs matches 1 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:orange_wool
execute if score colorings_turned funcs matches 1 run setblock ~0 ~3 ~4 minecraft:orange_banner[rotation=13]
execute if score colorings_turned funcs matches 1 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:orange_carpet
execute if score colorings_turned funcs matches 1 run setblock ~1 ~3 ~7 minecraft:orange_concrete
execute if score colorings_turned funcs matches 1 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 1 run setblock ~3 ~3 ~9 minecraft:orange_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 1 run setblock ~3 ~3 ~10 minecraft:orange_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 1 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:orange_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 1 run setblock ~1 ~5 ~3 minecraft:orange_terracotta
execute if score colorings_turned funcs matches 1 run setblock ~1 ~5 ~5 minecraft:orange_shulker_box
execute if score colorings_turned funcs matches 1 run setblock ~1 ~5 ~7 minecraft:orange_concrete_powder

execute if score colorings_turned funcs matches 1 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 1 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Orange\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:16351261}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:16351261}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:16351261}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:16351261}}}]}
execute if score colorings_turned funcs matches 1 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:orange_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Orange\""}


execute if score colorings_turned funcs matches 2 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:magenta_stained_glass_pane
execute if score colorings_turned funcs matches 2 run setblock ~4 ~4 ~-0 minecraft:magenta_stained_glass_pane
execute if score colorings_turned funcs matches 2 run setblock ~3 ~3 ~1 minecraft:magenta_stained_glass
execute if score colorings_turned funcs matches 2 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:magenta_wool
execute if score colorings_turned funcs matches 2 run setblock ~0 ~3 ~4 minecraft:magenta_banner[rotation=13]
execute if score colorings_turned funcs matches 2 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:magenta_carpet
execute if score colorings_turned funcs matches 2 run setblock ~1 ~3 ~7 minecraft:magenta_concrete
execute if score colorings_turned funcs matches 2 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 2 run setblock ~3 ~3 ~9 minecraft:magenta_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 2 run setblock ~3 ~3 ~10 minecraft:magenta_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 2 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:magenta_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 2 run setblock ~1 ~5 ~3 minecraft:magenta_terracotta
execute if score colorings_turned funcs matches 2 run setblock ~1 ~5 ~5 minecraft:magenta_shulker_box
execute if score colorings_turned funcs matches 2 run setblock ~1 ~5 ~7 minecraft:magenta_concrete_powder

execute if score colorings_turned funcs matches 2 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 2 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Magenta\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:13061821}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:13061821}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:13061821}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:13061821}}}]}
execute if score colorings_turned funcs matches 2 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:magenta_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Magenta\""}


execute if score colorings_turned funcs matches 3 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:light_blue_stained_glass_pane
execute if score colorings_turned funcs matches 3 run setblock ~4 ~4 ~-0 minecraft:light_blue_stained_glass_pane
execute if score colorings_turned funcs matches 3 run setblock ~3 ~3 ~1 minecraft:light_blue_stained_glass
execute if score colorings_turned funcs matches 3 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:light_blue_wool
execute if score colorings_turned funcs matches 3 run setblock ~0 ~3 ~4 minecraft:light_blue_banner[rotation=13]
execute if score colorings_turned funcs matches 3 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:light_blue_carpet
execute if score colorings_turned funcs matches 3 run setblock ~1 ~3 ~7 minecraft:light_blue_concrete
execute if score colorings_turned funcs matches 3 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 3 run setblock ~3 ~3 ~9 minecraft:light_blue_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 3 run setblock ~3 ~3 ~10 minecraft:light_blue_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 3 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:light_blue_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 3 run setblock ~1 ~5 ~3 minecraft:light_blue_terracotta
execute if score colorings_turned funcs matches 3 run setblock ~1 ~5 ~5 minecraft:light_blue_shulker_box
execute if score colorings_turned funcs matches 3 run setblock ~1 ~5 ~7 minecraft:light_blue_concrete_powder

execute if score colorings_turned funcs matches 3 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 3 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Light Blue\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:3847130}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:3847130}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:3847130}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:3847130}}}]}
execute if score colorings_turned funcs matches 3 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:light_blue_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Light Blue\""}


execute if score colorings_turned funcs matches 4 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:yellow_stained_glass_pane
execute if score colorings_turned funcs matches 4 run setblock ~4 ~4 ~-0 minecraft:yellow_stained_glass_pane
execute if score colorings_turned funcs matches 4 run setblock ~3 ~3 ~1 minecraft:yellow_stained_glass
execute if score colorings_turned funcs matches 4 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:yellow_wool
execute if score colorings_turned funcs matches 4 run setblock ~0 ~3 ~4 minecraft:yellow_banner[rotation=13]
execute if score colorings_turned funcs matches 4 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:yellow_carpet
execute if score colorings_turned funcs matches 4 run setblock ~1 ~3 ~7 minecraft:yellow_concrete
execute if score colorings_turned funcs matches 4 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 4 run setblock ~3 ~3 ~9 minecraft:yellow_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 4 run setblock ~3 ~3 ~10 minecraft:yellow_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 4 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:dandelion_yellow},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 4 run setblock ~1 ~5 ~3 minecraft:yellow_terracotta
execute if score colorings_turned funcs matches 4 run setblock ~1 ~5 ~5 minecraft:yellow_shulker_box
execute if score colorings_turned funcs matches 4 run setblock ~1 ~5 ~7 minecraft:yellow_concrete_powder

execute if score colorings_turned funcs matches 4 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 4 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Yellow\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:16701501}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:16701501}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:16701501}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:16701501}}}]}
execute if score colorings_turned funcs matches 4 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:yellow_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Yellow\""}


execute if score colorings_turned funcs matches 5 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:lime_stained_glass_pane
execute if score colorings_turned funcs matches 5 run setblock ~4 ~4 ~-0 minecraft:lime_stained_glass_pane
execute if score colorings_turned funcs matches 5 run setblock ~3 ~3 ~1 minecraft:lime_stained_glass
execute if score colorings_turned funcs matches 5 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:lime_wool
execute if score colorings_turned funcs matches 5 run setblock ~0 ~3 ~4 minecraft:lime_banner[rotation=13]
execute if score colorings_turned funcs matches 5 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:lime_carpet
execute if score colorings_turned funcs matches 5 run setblock ~1 ~3 ~7 minecraft:lime_concrete
execute if score colorings_turned funcs matches 5 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 5 run setblock ~3 ~3 ~9 minecraft:lime_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 5 run setblock ~3 ~3 ~10 minecraft:lime_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 5 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:lime_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 5 run setblock ~1 ~5 ~3 minecraft:lime_terracotta
execute if score colorings_turned funcs matches 5 run setblock ~1 ~5 ~5 minecraft:lime_shulker_box
execute if score colorings_turned funcs matches 5 run setblock ~1 ~5 ~7 minecraft:lime_concrete_powder

execute if score colorings_turned funcs matches 5 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 5 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Lime\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:8439583}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:8439583}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:8439583}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:8439583}}}]}
execute if score colorings_turned funcs matches 5 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:lime_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Lime\""}


execute if score colorings_turned funcs matches 6 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:pink_stained_glass_pane
execute if score colorings_turned funcs matches 6 run setblock ~4 ~4 ~-0 minecraft:pink_stained_glass_pane
execute if score colorings_turned funcs matches 6 run setblock ~3 ~3 ~1 minecraft:pink_stained_glass
execute if score colorings_turned funcs matches 6 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:pink_wool
execute if score colorings_turned funcs matches 6 run setblock ~0 ~3 ~4 minecraft:pink_banner[rotation=13]
execute if score colorings_turned funcs matches 6 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:pink_carpet
execute if score colorings_turned funcs matches 6 run setblock ~1 ~3 ~7 minecraft:pink_concrete
execute if score colorings_turned funcs matches 6 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 6 run setblock ~3 ~3 ~9 minecraft:pink_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 6 run setblock ~3 ~3 ~10 minecraft:pink_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 6 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:pink_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 6 run setblock ~1 ~5 ~3 minecraft:pink_terracotta
execute if score colorings_turned funcs matches 6 run setblock ~1 ~5 ~5 minecraft:pink_shulker_box
execute if score colorings_turned funcs matches 6 run setblock ~1 ~5 ~7 minecraft:pink_concrete_powder

execute if score colorings_turned funcs matches 6 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 6 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Pink\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:15961002}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:15961002}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:15961002}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:15961002}}}]}
execute if score colorings_turned funcs matches 6 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:pink_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Pink\""}


execute if score colorings_turned funcs matches 7 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:gray_stained_glass_pane
execute if score colorings_turned funcs matches 7 run setblock ~4 ~4 ~-0 minecraft:gray_stained_glass_pane
execute if score colorings_turned funcs matches 7 run setblock ~3 ~3 ~1 minecraft:gray_stained_glass
execute if score colorings_turned funcs matches 7 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:gray_wool
execute if score colorings_turned funcs matches 7 run setblock ~0 ~3 ~4 minecraft:gray_banner[rotation=13]
execute if score colorings_turned funcs matches 7 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:gray_carpet
execute if score colorings_turned funcs matches 7 run setblock ~1 ~3 ~7 minecraft:gray_concrete
execute if score colorings_turned funcs matches 7 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 7 run setblock ~3 ~3 ~9 minecraft:gray_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 7 run setblock ~3 ~3 ~10 minecraft:gray_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 7 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:gray_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 7 run setblock ~1 ~5 ~3 minecraft:gray_terracotta
execute if score colorings_turned funcs matches 7 run setblock ~1 ~5 ~5 minecraft:gray_shulker_box
execute if score colorings_turned funcs matches 7 run setblock ~1 ~5 ~7 minecraft:gray_concrete_powder

execute if score colorings_turned funcs matches 7 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 7 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Gray\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:4673362}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:4673362}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:4673362}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:4673362}}}]}
execute if score colorings_turned funcs matches 7 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:gray_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Gray\""}


execute if score colorings_turned funcs matches 8 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:light_gray_stained_glass_pane
execute if score colorings_turned funcs matches 8 run setblock ~4 ~4 ~-0 minecraft:light_gray_stained_glass_pane
execute if score colorings_turned funcs matches 8 run setblock ~3 ~3 ~1 minecraft:light_gray_stained_glass
execute if score colorings_turned funcs matches 8 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:light_gray_wool
execute if score colorings_turned funcs matches 8 run setblock ~0 ~3 ~4 minecraft:light_gray_banner[rotation=13]
execute if score colorings_turned funcs matches 8 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:light_gray_carpet
execute if score colorings_turned funcs matches 8 run setblock ~1 ~3 ~7 minecraft:light_gray_concrete
execute if score colorings_turned funcs matches 8 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 8 run setblock ~3 ~3 ~9 minecraft:light_gray_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 8 run setblock ~3 ~3 ~10 minecraft:light_gray_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 8 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:light_gray_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 8 run setblock ~1 ~5 ~3 minecraft:light_gray_terracotta
execute if score colorings_turned funcs matches 8 run setblock ~1 ~5 ~5 minecraft:light_gray_shulker_box
execute if score colorings_turned funcs matches 8 run setblock ~1 ~5 ~7 minecraft:light_gray_concrete_powder

execute if score colorings_turned funcs matches 8 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 8 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Light Gray\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:10329495}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:10329495}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:10329495}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:10329495}}}]}
execute if score colorings_turned funcs matches 8 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:light_gray_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Light Gray\""}


execute if score colorings_turned funcs matches 9 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:cyan_stained_glass_pane
execute if score colorings_turned funcs matches 9 run setblock ~4 ~4 ~-0 minecraft:cyan_stained_glass_pane
execute if score colorings_turned funcs matches 9 run setblock ~3 ~3 ~1 minecraft:cyan_stained_glass
execute if score colorings_turned funcs matches 9 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:cyan_wool
execute if score colorings_turned funcs matches 9 run setblock ~0 ~3 ~4 minecraft:cyan_banner[rotation=13]
execute if score colorings_turned funcs matches 9 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:cyan_carpet
execute if score colorings_turned funcs matches 9 run setblock ~1 ~3 ~7 minecraft:cyan_concrete
execute if score colorings_turned funcs matches 9 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 9 run setblock ~3 ~3 ~9 minecraft:cyan_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 9 run setblock ~3 ~3 ~10 minecraft:cyan_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 9 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:cyan_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 9 run setblock ~1 ~5 ~3 minecraft:cyan_terracotta
execute if score colorings_turned funcs matches 9 run setblock ~1 ~5 ~5 minecraft:cyan_shulker_box
execute if score colorings_turned funcs matches 9 run setblock ~1 ~5 ~7 minecraft:cyan_concrete_powder

execute if score colorings_turned funcs matches 9 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 9 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Cyan\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:1481884}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:1481884}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:1481884}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:1481884}}}]}
execute if score colorings_turned funcs matches 9 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:cyan_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Cyan\""}


execute if score colorings_turned funcs matches 10 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:purple_stained_glass_pane
execute if score colorings_turned funcs matches 10 run setblock ~4 ~4 ~-0 minecraft:purple_stained_glass_pane
execute if score colorings_turned funcs matches 10 run setblock ~3 ~3 ~1 minecraft:purple_stained_glass
execute if score colorings_turned funcs matches 10 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:purple_wool
execute if score colorings_turned funcs matches 10 run setblock ~0 ~3 ~4 minecraft:purple_banner[rotation=13]
execute if score colorings_turned funcs matches 10 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:purple_carpet
execute if score colorings_turned funcs matches 10 run setblock ~1 ~3 ~7 minecraft:purple_concrete
execute if score colorings_turned funcs matches 10 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 10 run setblock ~3 ~3 ~9 minecraft:purple_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 10 run setblock ~3 ~3 ~10 minecraft:purple_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 10 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:purple_dye},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 10 run setblock ~1 ~5 ~3 minecraft:purple_terracotta
execute if score colorings_turned funcs matches 10 run setblock ~1 ~5 ~5 minecraft:purple_shulker_box
execute if score colorings_turned funcs matches 10 run setblock ~1 ~5 ~7 minecraft:purple_concrete_powder

execute if score colorings_turned funcs matches 10 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 10 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Purple\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:8991416}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:8991416}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:8991416}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:8991416}}}]}
execute if score colorings_turned funcs matches 10 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:purple_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Purple\""}


execute if score colorings_turned funcs matches 11 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:blue_stained_glass_pane
execute if score colorings_turned funcs matches 11 run setblock ~4 ~4 ~-0 minecraft:blue_stained_glass_pane
execute if score colorings_turned funcs matches 11 run setblock ~3 ~3 ~1 minecraft:blue_stained_glass
execute if score colorings_turned funcs matches 11 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:blue_wool
execute if score colorings_turned funcs matches 11 run setblock ~0 ~3 ~4 minecraft:blue_banner[rotation=13]
execute if score colorings_turned funcs matches 11 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:blue_carpet
execute if score colorings_turned funcs matches 11 run setblock ~1 ~3 ~7 minecraft:blue_concrete
execute if score colorings_turned funcs matches 11 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 11 run setblock ~3 ~3 ~9 minecraft:blue_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 11 run setblock ~3 ~3 ~10 minecraft:blue_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 11 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:lapis_lazuli},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 11 run setblock ~1 ~5 ~3 minecraft:blue_terracotta
execute if score colorings_turned funcs matches 11 run setblock ~1 ~5 ~5 minecraft:blue_shulker_box
execute if score colorings_turned funcs matches 11 run setblock ~1 ~5 ~7 minecraft:blue_concrete_powder

execute if score colorings_turned funcs matches 11 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 11 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Blue\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:3949738}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:3949738}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:3949738}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:3949738}}}]}
execute if score colorings_turned funcs matches 11 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:blue_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Blue\""}


execute if score colorings_turned funcs matches 12 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:brown_stained_glass_pane
execute if score colorings_turned funcs matches 12 run setblock ~4 ~4 ~-0 minecraft:brown_stained_glass_pane
execute if score colorings_turned funcs matches 12 run setblock ~3 ~3 ~1 minecraft:brown_stained_glass
execute if score colorings_turned funcs matches 12 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:brown_wool
execute if score colorings_turned funcs matches 12 run setblock ~0 ~3 ~4 minecraft:brown_banner[rotation=13]
execute if score colorings_turned funcs matches 12 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:brown_carpet
execute if score colorings_turned funcs matches 12 run setblock ~1 ~3 ~7 minecraft:brown_concrete
execute if score colorings_turned funcs matches 12 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 12 run setblock ~3 ~3 ~9 minecraft:brown_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 12 run setblock ~3 ~3 ~10 minecraft:brown_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 12 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 12 run setblock ~1 ~5 ~3 minecraft:brown_terracotta
execute if score colorings_turned funcs matches 12 run setblock ~1 ~5 ~5 minecraft:brown_shulker_box
execute if score colorings_turned funcs matches 12 run setblock ~1 ~5 ~7 minecraft:brown_concrete_powder

execute if score colorings_turned funcs matches 12 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 12 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Brown\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:8606770}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:8606770}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:8606770}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:8606770}}}]}
execute if score colorings_turned funcs matches 12 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:brown_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Brown\""}


execute if score colorings_turned funcs matches 13 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:green_stained_glass_pane
execute if score colorings_turned funcs matches 13 run setblock ~4 ~4 ~-0 minecraft:green_stained_glass_pane
execute if score colorings_turned funcs matches 13 run setblock ~3 ~3 ~1 minecraft:green_stained_glass
execute if score colorings_turned funcs matches 13 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:green_wool
execute if score colorings_turned funcs matches 13 run setblock ~0 ~3 ~4 minecraft:green_banner[rotation=13]
execute if score colorings_turned funcs matches 13 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:green_carpet
execute if score colorings_turned funcs matches 13 run setblock ~1 ~3 ~7 minecraft:green_concrete
execute if score colorings_turned funcs matches 13 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 13 run setblock ~3 ~3 ~9 minecraft:green_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 13 run setblock ~3 ~3 ~10 minecraft:green_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 13 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:cactus_green},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 13 run setblock ~1 ~5 ~3 minecraft:green_terracotta
execute if score colorings_turned funcs matches 13 run setblock ~1 ~5 ~5 minecraft:green_shulker_box
execute if score colorings_turned funcs matches 13 run setblock ~1 ~5 ~7 minecraft:green_concrete_powder

execute if score colorings_turned funcs matches 13 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 13 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Green\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:6192150}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:6192150}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:6192150}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:6192150}}}]}
execute if score colorings_turned funcs matches 13 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:green_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Green\""}


execute if score colorings_turned funcs matches 14 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:red_stained_glass_pane
execute if score colorings_turned funcs matches 14 run setblock ~4 ~4 ~-0 minecraft:red_stained_glass_pane
execute if score colorings_turned funcs matches 14 run setblock ~3 ~3 ~1 minecraft:red_stained_glass
execute if score colorings_turned funcs matches 14 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:red_wool
execute if score colorings_turned funcs matches 14 run setblock ~0 ~3 ~4 minecraft:red_banner[rotation=13]
execute if score colorings_turned funcs matches 14 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:red_carpet
execute if score colorings_turned funcs matches 14 run setblock ~1 ~3 ~7 minecraft:red_concrete
execute if score colorings_turned funcs matches 14 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 14 run setblock ~3 ~3 ~9 minecraft:red_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 14 run setblock ~3 ~3 ~10 minecraft:red_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 14 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:rose_red},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 14 run setblock ~1 ~5 ~3 minecraft:red_terracotta
execute if score colorings_turned funcs matches 14 run setblock ~1 ~5 ~5 minecraft:red_shulker_box
execute if score colorings_turned funcs matches 14 run setblock ~1 ~5 ~7 minecraft:red_concrete_powder

execute if score colorings_turned funcs matches 14 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 14 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Red\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:11546150}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:11546150}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:11546150}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:11546150}}}]}
execute if score colorings_turned funcs matches 14 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:red_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Red\""}


execute if score colorings_turned funcs matches 15 run fill ~4 ~3 ~-0 ~4 ~3 ~1 minecraft:black_stained_glass_pane
execute if score colorings_turned funcs matches 15 run setblock ~4 ~4 ~-0 minecraft:black_stained_glass_pane
execute if score colorings_turned funcs matches 15 run setblock ~3 ~3 ~1 minecraft:black_stained_glass
execute if score colorings_turned funcs matches 15 run fill ~1 ~3 ~2 ~0 ~3 ~3 minecraft:black_wool
execute if score colorings_turned funcs matches 15 run setblock ~0 ~3 ~4 minecraft:black_banner[rotation=13]
execute if score colorings_turned funcs matches 15 run fill ~1 ~3 ~4 ~1 ~3 ~6 minecraft:black_carpet
execute if score colorings_turned funcs matches 15 run setblock ~1 ~3 ~7 minecraft:black_concrete
execute if score colorings_turned funcs matches 15 run fill ~3 ~3 ~9 ~3 ~3 ~10 minecraft:air
execute if score colorings_turned funcs matches 15 run setblock ~3 ~3 ~9 minecraft:black_bed[facing=south,part=foot]
execute if score colorings_turned funcs matches 15 run setblock ~3 ~3 ~10 minecraft:black_bed[facing=south,part=head]

execute if score colorings_turned funcs matches 15 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:ink_sac},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 15 run setblock ~1 ~5 ~3 minecraft:black_terracotta
execute if score colorings_turned funcs matches 15 run setblock ~1 ~5 ~5 minecraft:black_shulker_box
execute if score colorings_turned funcs matches 15 run setblock ~1 ~5 ~7 minecraft:black_concrete_powder

execute if score colorings_turned funcs matches 15 run data merge entity @e[tag=colorings_armor_stand,limit=1] {Item:{id:cocoa_beans},Count:1,ItemRotation:0}

execute if score colorings_turned funcs matches 15 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Black\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:1908001}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:1908001}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:1908001}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:1908001}}}]}
execute if score colorings_turned funcs matches 15 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:black_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Black\""}