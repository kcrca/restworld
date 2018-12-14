execute unless score brewing funcs matches 0.. run function brewing_init
scoreboard players add brewing funcs 1
execute unless score brewing funcs matches 0..7 run scoreboard players set brewing funcs 0

execute if score brewing funcs matches 0 run replaceitem block ~ ~2 ~ container.0 minecraft:air
execute if score brewing funcs matches 0 run replaceitem block ~ ~2 ~ container.1 minecraft:air
execute if score brewing funcs matches 0 run replaceitem block ~ ~2 ~ container.2 minecraft:air


execute if score brewing funcs matches 1 run replaceitem block ~ ~2 ~ container.0 minecraft:potion{Potion:"minecraft:water"} 1
execute if score brewing funcs matches 1 run replaceitem block ~ ~2 ~ container.1 minecraft:air
execute if score brewing funcs matches 1 run replaceitem block ~ ~2 ~ container.2 minecraft:air


execute if score brewing funcs matches 2 run replaceitem block ~ ~2 ~ container.0 minecraft:air
execute if score brewing funcs matches 2 run replaceitem block ~ ~2 ~ container.1 minecraft:potion{Potion:"minecraft:water"} 1
execute if score brewing funcs matches 2 run replaceitem block ~ ~2 ~ container.2 minecraft:air


execute if score brewing funcs matches 3 run replaceitem block ~ ~2 ~ container.0 minecraft:air
execute if score brewing funcs matches 3 run replaceitem block ~ ~2 ~ container.1 minecraft:air
execute if score brewing funcs matches 3 run replaceitem block ~ ~2 ~ container.2 minecraft:potion{Potion:"minecraft:water"} 1


execute if score brewing funcs matches 4 run replaceitem block ~ ~2 ~ container.0 minecraft:potion{Potion:"minecraft:water"} 1
execute if score brewing funcs matches 4 run replaceitem block ~ ~2 ~ container.1 minecraft:air
execute if score brewing funcs matches 4 run replaceitem block ~ ~2 ~ container.2 minecraft:potion{Potion:"minecraft:water"} 1


execute if score brewing funcs matches 5 run replaceitem block ~ ~2 ~ container.0 minecraft:air
execute if score brewing funcs matches 5 run replaceitem block ~ ~2 ~ container.1 minecraft:potion{Potion:"minecraft:water"} 1
execute if score brewing funcs matches 5 run replaceitem block ~ ~2 ~ container.2 minecraft:potion{Potion:"minecraft:water"} 1


execute if score brewing funcs matches 6 run replaceitem block ~ ~2 ~ container.0 minecraft:potion{Potion:"minecraft:water"} 1
execute if score brewing funcs matches 6 run replaceitem block ~ ~2 ~ container.1 minecraft:potion{Potion:"minecraft:water"} 1
execute if score brewing funcs matches 6 run replaceitem block ~ ~2 ~ container.2 minecraft:air


execute if score brewing funcs matches 7 run replaceitem block ~ ~2 ~ container.0 minecraft:potion{Potion:"minecraft:water"} 1
execute if score brewing funcs matches 7 run replaceitem block ~ ~2 ~ container.1 minecraft:potion{Potion:"minecraft:water"} 1
execute if score brewing funcs matches 7 run replaceitem block ~ ~2 ~ container.2 minecraft:potion{Potion:"minecraft:water"} 1
