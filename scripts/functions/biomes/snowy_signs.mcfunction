fill ~9 ~0 ~9 ~0 ~1 ~9 air


setblock ~9 ~1 ~9 oak_wall_sign{Text2:"\"Temperate\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/temperate_signs\"}}"} replace



setblock ~8 ~1 ~9 oak_wall_sign{Text2:"\"Warm\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/warm_signs\"}}"} replace



setblock ~7 ~1 ~9 oak_wall_sign{Text2:"\"Cold\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/cold_signs\"}}"} replace



setblock ~6 ~1 ~9 oak_wall_sign{Text2:"\"Snowy\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/snowy_signs\"}}"} replace



setblock ~5 ~1 ~9 oak_wall_sign{Text2:"\"Ocean\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/ocean_signs\"}}"} replace



setblock ~4 ~1 ~9 oak_wall_sign{Text2:"\"End and Nether\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/end_and_nether_signs\"}}"} replace




setblock ~6 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Snowy Tundra\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 13\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~5 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Ice Spikes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 14\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}
setblock ~4 ~0 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/clear_biome\"}}",Text2:"{\"text\":\"Snowy Tiaga\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run scoreboard players set load_biome funcs 15\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute run execute at @e[tag=biome_loading_home] run function v3:biomes/load_biome_cur\"}}",}

setblock ~6 ~1 ~9 birch_wall_sign{Text2:"{\"text\":\"Snowy\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/category\"}}",Text3:"\"Biomes\""}
