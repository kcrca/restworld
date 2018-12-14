scoreboard players set cane max 4
execute unless score cane funcs matches 0..3 run scoreboard players operation cane funcs %= cane max

fill ~ ~4 ~ ~ ~6 ~ minecraft:air
execute if score cane funcs matches 1 run fill ~ ~3 ~ ~ ~4 ~ minecraft:sugar_cane
execute if score cane funcs matches 2 run fill ~ ~3 ~ ~ ~5 ~ minecraft:sugar_cane
execute if score cane funcs matches 3 run fill ~ ~3 ~ ~ ~4 ~ minecraft:sugar_cane

kill @e[type=item,distance=..10,nbt={Item:{id:"minecraft:sugar_cane"}}]
