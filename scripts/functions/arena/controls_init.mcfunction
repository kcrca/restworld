fill ~-2 ~1 ~1 ~-2 ~0 ~-1 air


setblock ~-2 ~1 ~-1 oak_wall_sign[facing=west]{Text2:"{\"text\":\"Ocean\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_home] positioned ~ ~2 ~ run function v3:arena/toggle_ocean\"}}"} replace


setblock ~-2 ~1 ~0 oak_wall_sign[facing=west]{Text2:"{\"text\":\"Grass\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_home] positioned ~ ~2 ~ run function v3:arena/toggle_grass\"}}"} replace


setblock ~-2 ~1 ~1 oak_wall_sign[facing=west]{Text2:"{\"text\":\"Night\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_home] positioned ~ ~2 ~ run function v3:arena/toggle_night\"}}"} replace


setblock ~-2 ~0 ~-1 oak_wall_sign[facing=west]{Text2:"{\"text\":\"Kill All\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_home] positioned ~ ~2 ~ run function v3:arena/kill_arena\"}}"} replace


setblock ~-2 ~0 ~0 oak_wall_sign[facing=west]{Text2:"{\"text\":\"Go Home\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_home] positioned ~ ~2 ~ run function v3:arena/go_home\"}}"} replace


setblock ~-2 ~0 ~1 oak_wall_sign[facing=west]{Text2:"{\"text\":\"Angry Vindicator\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"execute at @e[tag=arena_home] positioned ~ ~2 ~ run function v3:arena/angry_vindicator\"}}"} replace
