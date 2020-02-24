fill ~9 ~0 ~9 ~0 ~1 ~9 air



setblock ~9 ~1 ~9 oak_wall_sign{Text2:"\"Temperate\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/temperate_signs\"}}"} replace




setblock ~8 ~1 ~9 oak_wall_sign{Text2:"\"Warm\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/warm_signs\"}}"} replace




setblock ~7 ~1 ~9 oak_wall_sign{Text2:"\"Cold\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/cold_signs\"}}"} replace




setblock ~6 ~1 ~9 oak_wall_sign{Text2:"\"Snowy\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/snowy_signs\"}}"} replace




setblock ~5 ~1 ~9 oak_wall_sign{Text2:"\"Ocean\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/ocean_signs\"}}"} replace




setblock ~4 ~1 ~9 oak_wall_sign{Text2:"\"End and Nether\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/end_and_nether_signs\"}}"} replace




setblock ~3 ~1 ~9 oak_wall_sign{Text2:"\"Structures\"",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/structures_signs\"}}"} replace




setblock ~9 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Plains\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 0\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~8 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Forest\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 1\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~7 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Flower Forest\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 2\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~6 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Birch Forest\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 3\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~5 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Dark Forest\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 4\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~4 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Swamp\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 5\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~3 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Jungle\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 6\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~2 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Mushroom Field\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 7\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}

setblock ~9 ~1 ~9 birch_wall_sign{Text2:"{\"text\":\"Temperate\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/category\"}}",Text3:"\"Biomes\""}
