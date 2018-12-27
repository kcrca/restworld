execute unless entity @e[tag=signer] run summon armor_stand ~ ~2 ~ {Tags:[signer],ArmorItems:[{},{},{},{id:iron_helmet,Count:1}],Rotation:[270f,0f],NoGravity:true}
execute at @e[tag=signer] run data merge block ~ ~ ~-1 {Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function v3:blocks/toggle_expand\"}}"}
execute at @e[tag=signer] run data merge block ~ ~ ~2 {Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function v3:blocks/toggle_expand\"}}"}
execute at @e[tag=signer] run data merge block ~ ~ ~10 {Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function v3:blocks/toggle_expand\"}}"}
execute at @e[tag=signer] run data merge block ~ ~ ~13 {Text1:"{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function v3:blocks/toggle_expand\"}}"}
execute as @e[tag=signer] run execute at @s run tp @s ^ ^ ^3
execute as @e[tag=signer] run execute at @s unless block ^ ^0 ^ minecraft:air run kill @e[tag=signer]
execute as @e[tag=signer] run execute at @s if block ^ ^0 ^ minecraft:air run function v3:blocks/blocks_sign_init
tag @e[tag=frosted_ice_home] add no_expansion
tag @e[tag=cake_home] add no_expansion
tag @e[tag=block_sign_home] add no_expansion
tag @e[tag=expand_home] add no_expansion
