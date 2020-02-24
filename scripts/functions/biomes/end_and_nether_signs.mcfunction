fill ~9 ~0 ~9 ~0 ~1 ~9 air


setblock ~9 ~1 ~9 oak_wall_sign{Text2:"\"Temperate\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/temperate_signs\"}}"} replace



setblock ~8 ~1 ~9 oak_wall_sign{Text2:"\"Warm\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/warm_signs\"}}"} replace



setblock ~7 ~1 ~9 oak_wall_sign{Text2:"\"Cold\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/cold_signs\"}}"} replace



setblock ~6 ~1 ~9 oak_wall_sign{Text2:"\"Snowy\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/snowy_signs\"}}"} replace



setblock ~5 ~1 ~9 oak_wall_sign{Text2:"\"Ocean\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/ocean_signs\"}}"} replace



setblock ~4 ~1 ~9 oak_wall_sign{Text2:"\"End and Nether\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/end_and_nether_signs\"}}"} replace




setblock ~4 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"The End\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 19\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~3 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"End Island\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 20\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~2 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Nether\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 21\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}

setblock ~4 ~1 ~9 birch_wall_sign{Text2:"{\"text\":\"End and Nether\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/category\"}}",Text3:"\"Biomes\""}
