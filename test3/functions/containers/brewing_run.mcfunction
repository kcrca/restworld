execute unless score brewing_run funcs matches 0.. run function brewing_run_init
scoreboard players add brewing_run funcs 1
scoreboard players set brewing_run max 2
execute unless score brewing_run funcs matches 0..1 run scoreboard players operation brewing_run funcs %= brewing_run max

execute if score brewing_run funcs matches 0 run function v3:containers/brewing_init
execute if score brewing_run funcs matches 1 run replaceitem block ~ ~2 ~ container.3 minecraft:spider_eye 64
execute if score brewing_run funcs matches 1 run replaceitem block ~ ~2 ~ container.4 minecraft:blaze_powder 64
