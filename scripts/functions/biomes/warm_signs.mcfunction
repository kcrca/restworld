fill ~9 ~2 ~9 ~0 ~1 ~9 air

setblock ~9 ~1 ~9 oak_wall_sign{Text2:"\"Snowy\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/snowy_signs\"}}"} replace


setblock ~8 ~1 ~9 oak_wall_sign{Text2:"\"Cold\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/cold_signs\"}}"} replace


setblock ~7 ~1 ~9 oak_wall_sign{Text2:"\"Temperate\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/temperate_signs\"}}"} replace


setblock ~6 ~1 ~9 oak_wall_sign{Text2:"\"Warm\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/warm_signs\"}}"} replace


setblock ~5 ~1 ~9 oak_wall_sign{Text2:"\"Ocean\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/ocean_signs\"}}"} replace


setblock ~4 ~1 ~9 oak_wall_sign{Text2:"\"End and Nether\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/end_and_nether_signs\"}}"} replace




setblock ~6 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives remove biome\"}}",Text2:"{\"text\":\"Desert\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives add biome dummy\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard players set desert biome 1\"}}",Text4:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run execute at @e[tag=switch_biome_home] run function v3:biomes/switch_biome\"}}"}
setblock ~5 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives remove biome\"}}",Text2:"{\"text\":\"Savanna\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives add biome dummy\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard players set savanna biome 1\"}}",Text4:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run execute at @e[tag=switch_biome_home] run function v3:biomes/switch_biome\"}}"}
setblock ~4 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives remove biome\"}}",Text2:"{\"text\":\"Badlands\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives add biome dummy\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard players set badlands biome 1\"}}",Text4:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run execute at @e[tag=switch_biome_home] run function v3:biomes/switch_biome\"}}"}

setblock ~6 ~1 ~9 birch_wall_sign{Text2:"{\"text\":\"Warm\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/category\"}}",Text3:"\"Biomes\""}
