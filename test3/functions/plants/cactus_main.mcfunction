execute unless score cactus funcs matches 0.. run function cactus_init
scoreboard players add cactus funcs 1
scoreboard players set cactus max 4
execute unless score cactus funcs matches 0..3 run scoreboard players operation cactus funcs %= cactus max

fill ~ ~4 ~ ~ ~6 ~ minecraft:air
execute if score cactus funcs matches 1 run fill ~ ~3 ~ ~ ~4 ~ minecraft:cactus
execute if score cactus funcs matches 2 run fill ~ ~3 ~ ~ ~5 ~ minecraft:cactus
execute if score cactus funcs matches 3 run fill ~ ~3 ~ ~ ~4 ~ minecraft:cactus

kill @e[type=item,distance=..10,nbt={Item:{id:"minecraft:cactus"}}]
