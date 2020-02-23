fill ~9 ~2 ~9 ~0 ~1 ~9 air

setblock ~9 ~1 ~9 oak_wall_sign{Text2:"\"Snowy\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/snowy_signs\"}}"} replace


setblock ~8 ~1 ~9 oak_wall_sign{Text2:"\"Cold\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/cold_signs\"}}"} replace


setblock ~7 ~1 ~9 oak_wall_sign{Text2:"\"Temperate\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/temperate_signs\"}}"} replace


setblock ~6 ~1 ~9 oak_wall_sign{Text2:"\"The End\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/the_end_signs\"}}"} replace



setblock ~9 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives remove biome\"}}",Text2:"{\"text\":\"The End\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives add biome dummy\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard players set the_end biome 1\"}}",Text4:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run execute at @e[tag=switch_biome_home] run function v3:biomes/switch_biome\"}}"}
setblock ~8 ~2 ~9 birch_wall_sign{Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives remove biome\"}}",Text2:"{\"text\":\"End Island\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard objectives add biome dummy\"}}",Text3:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run scoreboard players set end_island biome 1\"}}",Text4:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=biomes_home] positioned ~ ~2 ~ run execute at @e[tag=switch_biome_home] run function v3:biomes/switch_biome\"}}"}

setblock ~6 ~1 ~9 birch_wall_sign{Text2:"{\"text\":\"The End\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/category\"}}",Text3:"\"Biomes\""}
