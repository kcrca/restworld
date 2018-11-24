



execute unless score potable funcs matches 0.. run function potable_init
scoreboard players add potable funcs 1
execute unless score potable funcs matches 0..20 run scoreboard players set potable funcs 0
execute if score potable funcs matches 0 run setblock ~ ~3 ~ minecraft:potted_acacia_sapling
execute if score potable funcs matches 0 run data merge block ~1 ~2 ~ {Text3:"\"Acacia Sapling\""}

execute if score potable funcs matches 1 run setblock ~ ~3 ~ minecraft:potted_birch_sapling
execute if score potable funcs matches 1 run data merge block ~1 ~2 ~ {Text3:"\"Birch Sapling\""}

execute if score potable funcs matches 2 run setblock ~ ~3 ~ minecraft:potted_jungle_sapling
execute if score potable funcs matches 2 run data merge block ~1 ~2 ~ {Text3:"\"Jungle Sapling\""}

execute if score potable funcs matches 3 run setblock ~ ~3 ~ minecraft:potted_oak_sapling
execute if score potable funcs matches 3 run data merge block ~1 ~2 ~ {Text3:"\"Oak Sapling\""}

execute if score potable funcs matches 4 run setblock ~ ~3 ~ minecraft:potted_dark_oak_sapling
execute if score potable funcs matches 4 run data merge block ~1 ~2 ~ {Text3:"\"Dark Oak Sapling\""}

execute if score potable funcs matches 5 run setblock ~ ~3 ~ minecraft:potted_spruce_sapling
execute if score potable funcs matches 5 run data merge block ~1 ~2 ~ {Text3:"\"Spruce Sapling\""}

execute if score potable funcs matches 6 run setblock ~ ~3 ~ minecraft:potted_red_tulip
execute if score potable funcs matches 6 run data merge block ~1 ~2 ~ {Text3:"\"Red Tulip\""}

execute if score potable funcs matches 7 run setblock ~ ~3 ~ minecraft:potted_orange_tulip
execute if score potable funcs matches 7 run data merge block ~1 ~2 ~ {Text3:"\"Orange Tulip\""}

execute if score potable funcs matches 8 run setblock ~ ~3 ~ minecraft:potted_pink_tulip
execute if score potable funcs matches 8 run data merge block ~1 ~2 ~ {Text3:"\"Pink Tulip\""}

execute if score potable funcs matches 9 run setblock ~ ~3 ~ minecraft:potted_white_tulip
execute if score potable funcs matches 9 run data merge block ~1 ~2 ~ {Text3:"\"White Tulip\""}

execute if score potable funcs matches 10 run setblock ~ ~3 ~ minecraft:potted_allium
execute if score potable funcs matches 10 run data merge block ~1 ~2 ~ {Text3:"\"Allium\""}

execute if score potable funcs matches 11 run setblock ~ ~3 ~ minecraft:potted_azure_bluet
execute if score potable funcs matches 11 run data merge block ~1 ~2 ~ {Text3:"\"Azure Bluet\""}

execute if score potable funcs matches 12 run setblock ~ ~3 ~ minecraft:potted_blue_orchid
execute if score potable funcs matches 12 run data merge block ~1 ~2 ~ {Text3:"\"Blue Orchid\""}

execute if score potable funcs matches 13 run setblock ~ ~3 ~ minecraft:potted_dandelion
execute if score potable funcs matches 13 run data merge block ~1 ~2 ~ {Text3:"\"Dandelion\""}

execute if score potable funcs matches 14 run setblock ~ ~3 ~ minecraft:potted_oxeye_daisy
execute if score potable funcs matches 14 run data merge block ~1 ~2 ~ {Text3:"\"Oxeye Daisy\""}

execute if score potable funcs matches 15 run setblock ~ ~3 ~ minecraft:potted_poppy
execute if score potable funcs matches 15 run data merge block ~1 ~2 ~ {Text3:"\"Poppy\""}

execute if score potable funcs matches 16 run setblock ~ ~3 ~ minecraft:potted_brown_mushroom
execute if score potable funcs matches 16 run data merge block ~1 ~2 ~ {Text3:"\"Brown Mushroom\""}

execute if score potable funcs matches 17 run setblock ~ ~3 ~ minecraft:potted_red_mushroom
execute if score potable funcs matches 17 run data merge block ~1 ~2 ~ {Text3:"\"Red Mushroom\""}

execute if score potable funcs matches 18 run setblock ~ ~3 ~ minecraft:potted_cactus
execute if score potable funcs matches 18 run data merge block ~1 ~2 ~ {Text3:"\"Cactus\""}

execute if score potable funcs matches 19 run setblock ~ ~3 ~ minecraft:potted_dead_bush
execute if score potable funcs matches 19 run data merge block ~1 ~2 ~ {Text3:"\"Dead Bush\""}

execute if score potable funcs matches 20 run setblock ~ ~3 ~ minecraft:potted_fern
execute if score potable funcs matches 20 run data merge block ~1 ~2 ~ {Text3:"\"Fern\""}


