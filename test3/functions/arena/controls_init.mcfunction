fill ~-2 ~1 ~1 ~-2 ~0 ~-1 air


setblock ~-2 ~1 ~-1 wall_sign[facing=west]{Text2:"{\"text\":\"Ocean\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_mid_home] positioned ~ ~2 ~ run function v3:arena/toggle_ocean\"}}",Text3:"\"Off\""} replace


setblock ~-2 ~1 ~0 wall_sign[facing=west]{Text2:"{\"text\":\"Grass\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_mid_home] positioned ~ ~2 ~ run function v3:arena/toggle_grass\"}}",Text3:"\"Off\""} replace


setblock ~-2 ~1 ~1 wall_sign[facing=west]{Text2:"{\"text\":\"Night\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_mid_home] positioned ~ ~2 ~ run function v3:arena/toggle_night\"}}",Text3:"\"Off\""} replace


setblock ~-2 ~0 ~-1 wall_sign[facing=west]{Text2:"{\"text\":\"Kill All\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_mid_home] positioned ~ ~2 ~ run function v3:arena/kill_arena\"}}",Text3:"\"\""} replace


setblock ~-2 ~0 ~0 wall_sign[facing=west]{Text2:"{\"text\":\"Go Home\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_mid_home] positioned ~ ~2 ~ run function v3:arena/go_home\"}}",Text3:"\"\""} replace


setblock ~-2 ~0 ~1 wall_sign[facing=west]{Text2:"{\"text\":\"Angry Vindicator\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_mid_home] positioned ~ ~2 ~ run function v3:arena/angry_vindicator\"}}",Text3:"\"\""} replace
