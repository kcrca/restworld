scoreboard players add cur_villager_zombies funcs 1
scoreboard players operation cur_villager_zombies funcs %= bool max
execute if score cur_villager_zombies funcs matches 1 run scoreboard players set cur_villager_levels funcs 0
function v3:friendlies/switch_villagers
