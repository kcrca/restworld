execute at @e[tag=blocks_home,tag=!no_expansion] run data merge block ~ ~2 ~-1 {Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function v3:blocks/toggle_expand\"}}"}
execute at @e[tag=blocks_home,tag=!no_expansion] run data merge block ~ ~2 ~1 {Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function v3:blocks/toggle_expand\"}}"}

execute at @e[tag=blocks_home,tag=no_expansion] run data merge block ~ ~2 ~-1 {Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"say Sorry, cannot expand this block\"}}"}
execute at @e[tag=blocks_home,tag=no_expansion] run data merge block ~ ~2 ~1 {Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"say Sorry, cannot expand this block\"}}"}
