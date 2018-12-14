execute if score fast clocks matches 0 at @e[tag=particles_center] positioned ~ ~2 ~ run replaceitem block ~0 ~2 ~-1 container.0 minecraft:snowball 1
execute if score fast clocks matches 0 at @e[tag=particles_center] positioned ~ ~2 ~ run setblock ~0 ~3 ~-1 minecraft:stone_button[powered=true,face=floor]
execute if score fast clocks matches 0 at @e[tag=particles_center] positioned ~ ~2 ~ run setblock ~0 ~3 ~-1 minecraft:air
