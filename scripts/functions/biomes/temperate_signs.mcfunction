fill ~9 ~2 ~9 ~0 ~1 ~9 air

setblock ~9 ~1 ~9 oak_wall_sign{Text2:"\"Snowy\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/snowy_signs\"}}"} replace


setblock ~8 ~1 ~9 oak_wall_sign{Text2:"\"Cold\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/cold_signs\"}}"} replace


setblock ~7 ~1 ~9 oak_wall_sign{Text2:"\"Temperate\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/temperate_signs\"}}"} replace


setblock ~6 ~1 ~9 oak_wall_sign{Text2:"\"Warm\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/warm_signs\"}}"} replace


setblock ~5 ~1 ~9 oak_wall_sign{Text2:"\"Ocean\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/ocean_signs\"}}"} replace


setblock ~4 ~1 ~9 oak_wall_sign{Text2:"\"End and Nether\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/end_and_nether_signs\"}}"} replace




setblock ~7 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Plains\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 5\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~6 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Forest\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 6\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~5 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Flower Forest\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 7\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~4 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Birch Forest\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 8\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~3 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Dark Forest\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 9\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~2 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Swamp\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 10\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~1 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Jungle\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 11\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~0 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Mushroom Field\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 12\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}

setblock ~7 ~1 ~9 birch_wall_sign{Text2:"{\"text\":\"Temperate\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/category\"}}",Text3:"\"Biomes\""}
