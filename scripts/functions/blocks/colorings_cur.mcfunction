scoreboard players set colorings max 16
execute unless score colorings funcs matches 0..15 run scoreboard players operation colorings funcs %= colorings max

execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_wool replace #v3:wool
execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_carpet replace #v3:carpet
execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_concrete replace #v3:concrete
execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 0 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:white_terracotta replace #v3:terracotta

execute if score colorings funcs matches 0 run data merge block ~-7 ~0 ~3 {name:"restworld:white_terra"}

fill ~-8 ~2 ~3 ~-11 ~2 ~2 air

execute if score colorings funcs matches 0 run setblock ~-8 ~2 ~2 minecraft:white_bed[facing=north,part=head]
execute if score colorings funcs matches 0 run setblock ~-8 ~2 ~3 minecraft:white_bed[facing=north,part=foot]

execute if score colorings funcs matches 0 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:white_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 0 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"White\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:16383998}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:16383998}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:16383998}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:16383998}}}]}
execute if score colorings funcs matches 0 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:16383998}}}}
execute if score colorings funcs matches 0 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:white_carpet,Count:1},CustomNameVisible:True,CustomName:"\"White\""}
execute if score colorings funcs matches 0 run data merge block ~-4 ~2 ~4 {Text2:"\"White\""}


execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_wool replace #v3:wool
execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_carpet replace #v3:carpet
execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_concrete replace #v3:concrete
execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 1 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:orange_terracotta replace #v3:terracotta

execute if score colorings funcs matches 1 run data merge block ~-7 ~0 ~3 {name:"restworld:orange_terra"}


execute if score colorings funcs matches 1 run setblock ~-8 ~2 ~2 minecraft:orange_bed[facing=north,part=head]
execute if score colorings funcs matches 1 run setblock ~-8 ~2 ~3 minecraft:orange_bed[facing=north,part=foot]

execute if score colorings funcs matches 1 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:orange_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 1 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Orange\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:16351261}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:16351261}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:16351261}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:16351261}}}]}
execute if score colorings funcs matches 1 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:16351261}}}}
execute if score colorings funcs matches 1 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:orange_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Orange\""}
execute if score colorings funcs matches 1 run data merge block ~-4 ~2 ~4 {Text2:"\"Orange\""}


execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_wool replace #v3:wool
execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_carpet replace #v3:carpet
execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_concrete replace #v3:concrete
execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 2 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:magenta_terracotta replace #v3:terracotta

execute if score colorings funcs matches 2 run data merge block ~-7 ~0 ~3 {name:"restworld:magenta_terra"}


execute if score colorings funcs matches 2 run setblock ~-8 ~2 ~2 minecraft:magenta_bed[facing=north,part=head]
execute if score colorings funcs matches 2 run setblock ~-8 ~2 ~3 minecraft:magenta_bed[facing=north,part=foot]

execute if score colorings funcs matches 2 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:magenta_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 2 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Magenta\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:13061821}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:13061821}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:13061821}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:13061821}}}]}
execute if score colorings funcs matches 2 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:13061821}}}}
execute if score colorings funcs matches 2 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:magenta_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Magenta\""}
execute if score colorings funcs matches 2 run data merge block ~-4 ~2 ~4 {Text2:"\"Magenta\""}


execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_wool replace #v3:wool
execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_carpet replace #v3:carpet
execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_concrete replace #v3:concrete
execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 3 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_blue_terracotta replace #v3:terracotta

execute if score colorings funcs matches 3 run data merge block ~-7 ~0 ~3 {name:"restworld:light_blue_terra"}


execute if score colorings funcs matches 3 run setblock ~-8 ~2 ~2 minecraft:light_blue_bed[facing=north,part=head]
execute if score colorings funcs matches 3 run setblock ~-8 ~2 ~3 minecraft:light_blue_bed[facing=north,part=foot]

execute if score colorings funcs matches 3 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:light_blue_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 3 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Light Blue\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:3847130}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:3847130}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:3847130}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:3847130}}}]}
execute if score colorings funcs matches 3 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:3847130}}}}
execute if score colorings funcs matches 3 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:light_blue_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Light Blue\""}
execute if score colorings funcs matches 3 run data merge block ~-4 ~2 ~4 {Text2:"\"Light Blue\""}


execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_wool replace #v3:wool
execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_carpet replace #v3:carpet
execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_concrete replace #v3:concrete
execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 4 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:yellow_terracotta replace #v3:terracotta

execute if score colorings funcs matches 4 run data merge block ~-7 ~0 ~3 {name:"restworld:yellow_terra"}


execute if score colorings funcs matches 4 run setblock ~-8 ~2 ~2 minecraft:yellow_bed[facing=north,part=head]
execute if score colorings funcs matches 4 run setblock ~-8 ~2 ~3 minecraft:yellow_bed[facing=north,part=foot]

execute if score colorings funcs matches 4 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:yellow_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 4 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Yellow\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:16701501}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:16701501}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:16701501}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:16701501}}}]}
execute if score colorings funcs matches 4 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:16701501}}}}
execute if score colorings funcs matches 4 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:yellow_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Yellow\""}
execute if score colorings funcs matches 4 run data merge block ~-4 ~2 ~4 {Text2:"\"Yellow\""}


execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_wool replace #v3:wool
execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_carpet replace #v3:carpet
execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_concrete replace #v3:concrete
execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 5 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:lime_terracotta replace #v3:terracotta

execute if score colorings funcs matches 5 run data merge block ~-7 ~0 ~3 {name:"restworld:lime_terra"}


execute if score colorings funcs matches 5 run setblock ~-8 ~2 ~2 minecraft:lime_bed[facing=north,part=head]
execute if score colorings funcs matches 5 run setblock ~-8 ~2 ~3 minecraft:lime_bed[facing=north,part=foot]

execute if score colorings funcs matches 5 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:lime_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 5 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Lime\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:8439583}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:8439583}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:8439583}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:8439583}}}]}
execute if score colorings funcs matches 5 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:8439583}}}}
execute if score colorings funcs matches 5 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:lime_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Lime\""}
execute if score colorings funcs matches 5 run data merge block ~-4 ~2 ~4 {Text2:"\"Lime\""}


execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_wool replace #v3:wool
execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_carpet replace #v3:carpet
execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_concrete replace #v3:concrete
execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 6 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:pink_terracotta replace #v3:terracotta

execute if score colorings funcs matches 6 run data merge block ~-7 ~0 ~3 {name:"restworld:pink_terra"}


execute if score colorings funcs matches 6 run setblock ~-8 ~2 ~2 minecraft:pink_bed[facing=north,part=head]
execute if score colorings funcs matches 6 run setblock ~-8 ~2 ~3 minecraft:pink_bed[facing=north,part=foot]

execute if score colorings funcs matches 6 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:pink_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 6 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Pink\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:15961002}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:15961002}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:15961002}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:15961002}}}]}
execute if score colorings funcs matches 6 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:15961002}}}}
execute if score colorings funcs matches 6 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:pink_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Pink\""}
execute if score colorings funcs matches 6 run data merge block ~-4 ~2 ~4 {Text2:"\"Pink\""}


execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_wool replace #v3:wool
execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_carpet replace #v3:carpet
execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_concrete replace #v3:concrete
execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 7 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:gray_terracotta replace #v3:terracotta

execute if score colorings funcs matches 7 run data merge block ~-7 ~0 ~3 {name:"restworld:gray_terra"}


execute if score colorings funcs matches 7 run setblock ~-8 ~2 ~2 minecraft:gray_bed[facing=north,part=head]
execute if score colorings funcs matches 7 run setblock ~-8 ~2 ~3 minecraft:gray_bed[facing=north,part=foot]

execute if score colorings funcs matches 7 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:gray_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 7 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Gray\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:4673362}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:4673362}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:4673362}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:4673362}}}]}
execute if score colorings funcs matches 7 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:4673362}}}}
execute if score colorings funcs matches 7 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:gray_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Gray\""}
execute if score colorings funcs matches 7 run data merge block ~-4 ~2 ~4 {Text2:"\"Gray\""}


execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_wool replace #v3:wool
execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_carpet replace #v3:carpet
execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_concrete replace #v3:concrete
execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 8 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:light_gray_terracotta replace #v3:terracotta

execute if score colorings funcs matches 8 run data merge block ~-7 ~0 ~3 {name:"restworld:light_gray_terra"}


execute if score colorings funcs matches 8 run setblock ~-8 ~2 ~2 minecraft:light_gray_bed[facing=north,part=head]
execute if score colorings funcs matches 8 run setblock ~-8 ~2 ~3 minecraft:light_gray_bed[facing=north,part=foot]

execute if score colorings funcs matches 8 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:light_gray_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 8 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Light Gray\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:10329495}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:10329495}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:10329495}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:10329495}}}]}
execute if score colorings funcs matches 8 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:10329495}}}}
execute if score colorings funcs matches 8 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:light_gray_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Light Gray\""}
execute if score colorings funcs matches 8 run data merge block ~-4 ~2 ~4 {Text2:"\"Light Gray\""}


execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_wool replace #v3:wool
execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_carpet replace #v3:carpet
execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_concrete replace #v3:concrete
execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 9 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:cyan_terracotta replace #v3:terracotta

execute if score colorings funcs matches 9 run data merge block ~-7 ~0 ~3 {name:"restworld:cyan_terra"}


execute if score colorings funcs matches 9 run setblock ~-8 ~2 ~2 minecraft:cyan_bed[facing=north,part=head]
execute if score colorings funcs matches 9 run setblock ~-8 ~2 ~3 minecraft:cyan_bed[facing=north,part=foot]

execute if score colorings funcs matches 9 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:cyan_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 9 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Cyan\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:1481884}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:1481884}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:1481884}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:1481884}}}]}
execute if score colorings funcs matches 9 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:1481884}}}}
execute if score colorings funcs matches 9 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:cyan_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Cyan\""}
execute if score colorings funcs matches 9 run data merge block ~-4 ~2 ~4 {Text2:"\"Cyan\""}


execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_wool replace #v3:wool
execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_carpet replace #v3:carpet
execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_concrete replace #v3:concrete
execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 10 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:purple_terracotta replace #v3:terracotta

execute if score colorings funcs matches 10 run data merge block ~-7 ~0 ~3 {name:"restworld:purple_terra"}


execute if score colorings funcs matches 10 run setblock ~-8 ~2 ~2 minecraft:purple_bed[facing=north,part=head]
execute if score colorings funcs matches 10 run setblock ~-8 ~2 ~3 minecraft:purple_bed[facing=north,part=foot]

execute if score colorings funcs matches 10 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:purple_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 10 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Purple\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:8991416}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:8991416}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:8991416}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:8991416}}}]}
execute if score colorings funcs matches 10 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:8991416}}}}
execute if score colorings funcs matches 10 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:purple_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Purple\""}
execute if score colorings funcs matches 10 run data merge block ~-4 ~2 ~4 {Text2:"\"Purple\""}


execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_wool replace #v3:wool
execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_carpet replace #v3:carpet
execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_concrete replace #v3:concrete
execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 11 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:blue_terracotta replace #v3:terracotta

execute if score colorings funcs matches 11 run data merge block ~-7 ~0 ~3 {name:"restworld:blue_terra"}


execute if score colorings funcs matches 11 run setblock ~-8 ~2 ~2 minecraft:blue_bed[facing=north,part=head]
execute if score colorings funcs matches 11 run setblock ~-8 ~2 ~3 minecraft:blue_bed[facing=north,part=foot]

execute if score colorings funcs matches 11 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:blue_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 11 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Blue\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:3949738}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:3949738}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:3949738}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:3949738}}}]}
execute if score colorings funcs matches 11 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:3949738}}}}
execute if score colorings funcs matches 11 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:blue_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Blue\""}
execute if score colorings funcs matches 11 run data merge block ~-4 ~2 ~4 {Text2:"\"Blue\""}


execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_wool replace #v3:wool
execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_carpet replace #v3:carpet
execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_concrete replace #v3:concrete
execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 12 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:brown_terracotta replace #v3:terracotta

execute if score colorings funcs matches 12 run data merge block ~-7 ~0 ~3 {name:"restworld:brown_terra"}


execute if score colorings funcs matches 12 run setblock ~-8 ~2 ~2 minecraft:brown_bed[facing=north,part=head]
execute if score colorings funcs matches 12 run setblock ~-8 ~2 ~3 minecraft:brown_bed[facing=north,part=foot]

execute if score colorings funcs matches 12 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:brown_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 12 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Brown\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:8606770}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:8606770}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:8606770}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:8606770}}}]}
execute if score colorings funcs matches 12 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:8606770}}}}
execute if score colorings funcs matches 12 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:brown_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Brown\""}
execute if score colorings funcs matches 12 run data merge block ~-4 ~2 ~4 {Text2:"\"Brown\""}


execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_wool replace #v3:wool
execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_carpet replace #v3:carpet
execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_concrete replace #v3:concrete
execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 13 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:green_terracotta replace #v3:terracotta

execute if score colorings funcs matches 13 run data merge block ~-7 ~0 ~3 {name:"restworld:green_terra"}


execute if score colorings funcs matches 13 run setblock ~-8 ~2 ~2 minecraft:green_bed[facing=north,part=head]
execute if score colorings funcs matches 13 run setblock ~-8 ~2 ~3 minecraft:green_bed[facing=north,part=foot]

execute if score colorings funcs matches 13 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:green_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 13 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Green\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:6192150}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:6192150}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:6192150}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:6192150}}}]}
execute if score colorings funcs matches 13 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:6192150}}}}
execute if score colorings funcs matches 13 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:green_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Green\""}
execute if score colorings funcs matches 13 run data merge block ~-4 ~2 ~4 {Text2:"\"Green\""}


execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_wool replace #v3:wool
execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_carpet replace #v3:carpet
execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_concrete replace #v3:concrete
execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 14 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:red_terracotta replace #v3:terracotta

execute if score colorings funcs matches 14 run data merge block ~-7 ~0 ~3 {name:"restworld:red_terra"}


execute if score colorings funcs matches 14 run setblock ~-8 ~2 ~2 minecraft:red_bed[facing=north,part=head]
execute if score colorings funcs matches 14 run setblock ~-8 ~2 ~3 minecraft:red_bed[facing=north,part=foot]

execute if score colorings funcs matches 14 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:red_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 14 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Red\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:11546150}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:11546150}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:11546150}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:11546150}}}]}
execute if score colorings funcs matches 14 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:11546150}}}}
execute if score colorings funcs matches 14 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:red_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Red\""}
execute if score colorings funcs matches 14 run data merge block ~-4 ~2 ~4 {Text2:"\"Red\""}


execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_stained_glass replace #v3:stained_glass
execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_stained_glass_pane replace #v3:stained_glass_pane
execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_wool replace #v3:wool
execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_banner[rotation=2] replace #v3:banner
execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_shulker_box replace #v3:shulker_box
execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_carpet replace #v3:carpet
execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_concrete replace #v3:concrete
execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_concrete_powder replace #v3:concrete_powder
execute if score colorings funcs matches 15 run fill ~1 ~2 ~5 ~-11 ~4 ~-1 minecraft:black_terracotta replace #v3:terracotta

execute if score colorings funcs matches 15 run data merge block ~-7 ~0 ~3 {name:"restworld:black_terra"}


execute if score colorings funcs matches 15 run setblock ~-8 ~2 ~2 minecraft:black_bed[facing=north,part=head]
execute if score colorings funcs matches 15 run setblock ~-8 ~2 ~3 minecraft:black_bed[facing=north,part=foot]

execute if score colorings funcs matches 15 run data merge entity @e[tag=colorings_item_frame,limit=1] {Item:{id:black_dye},Count:1,ItemRotation:0}

execute if score colorings funcs matches 15 run data merge entity @e[tag=colorings_armor_stand,limit=1] {CustomName:"\"Black\"",CustomNameVisible:True,ArmorItems:[{id:leather_boots,Count:1,tag:{Variant:2,display:{color:1908001}}},{id:leather_leggings,Count:1,tag:{Variant:2,display:{color:1908001}}},{id:leather_chestplate,Count:1,tag:{Variant:2,display:{color:1908001}}},{id:leather_helmet,Count:1,tag:{Variant:2,display:{color:1908001}}}]}
execute if score colorings funcs matches 15 run data merge entity @e[tag=colorings_horse,limit=1] {ArmorItem:{id:leather_horse_armor,Count:1,tag:{display:{color:1908001}}}}
execute if score colorings funcs matches 15 run data merge entity @e[tag=colorings_llama,limit=1] {DecorItem:{id:black_carpet,Count:1},CustomNameVisible:True,CustomName:"\"Black\""}
execute if score colorings funcs matches 15 run data merge block ~-4 ~2 ~4 {Text2:"\"Black\""}
setblock ~-7 ~-1 ~3 minecraft:redstone_torch
setblock ~-7 ~-1 ~3 air
