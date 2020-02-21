fill ~9 ~2 ~9 ~0 ~1 ~9 air

setblock ~9 ~1 ~9 oak_wall_sign{Text2:"\"Snowy\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/snowy_signs\"}}"} replace


setblock ~8 ~1 ~9 oak_wall_sign{Text2:"\"Cold\"",Text3:"{\"text\":\"Biomes\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=category_home] positioned ~ ~2 ~ run function v3:biomes/cold_signs\"}}"} replace
