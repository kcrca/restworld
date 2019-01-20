scoreboard players set wood_power max 14
execute unless score wood_power funcs matches 0..13 run scoreboard players operation wood_power funcs %= wood_power max

execute if score wood_power funcs matches 0 run setblock ~1 ~2 ~-1 minecraft:stone_pressure_plate[powered=false]
execute if score wood_power funcs matches 0 run setblock ~1 ~3 ~0 minecraft:stone_button[facing=east,powered=false]
execute if score wood_power funcs matches 0 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 0 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 0 run data merge block ~1 ~2 ~0 {Text2:"\"Stone\"",Text3:"\"\""}


execute if score wood_power funcs matches 1 run setblock ~1 ~2 ~-1 minecraft:stone_pressure_plate[powered=true]
execute if score wood_power funcs matches 1 run setblock ~1 ~3 ~0 minecraft:stone_button[facing=east,powered=true]
execute if score wood_power funcs matches 1 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 1 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 1 run data merge block ~1 ~2 ~0 {Text2:"\"Stone\"",Text3:"\"(Powered)\""}


execute if score wood_power funcs matches 2 run setblock ~1 ~2 ~-1 minecraft:acacia_pressure_plate[powered=false]
execute if score wood_power funcs matches 2 run setblock ~1 ~3 ~0 minecraft:acacia_button[facing=east,powered=false]
execute if score wood_power funcs matches 2 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 2 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 2 run data merge block ~1 ~2 ~0 {Text2:"\"Acacia\"",Text3:"\"\""}


execute if score wood_power funcs matches 3 run setblock ~1 ~2 ~-1 minecraft:acacia_pressure_plate[powered=true]
execute if score wood_power funcs matches 3 run setblock ~1 ~3 ~0 minecraft:acacia_button[facing=east,powered=true]
execute if score wood_power funcs matches 3 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 3 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 3 run data merge block ~1 ~2 ~0 {Text2:"\"Acacia\"",Text3:"\"(Powered)\""}


execute if score wood_power funcs matches 4 run setblock ~1 ~2 ~-1 minecraft:birch_pressure_plate[powered=false]
execute if score wood_power funcs matches 4 run setblock ~1 ~3 ~0 minecraft:birch_button[facing=east,powered=false]
execute if score wood_power funcs matches 4 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 4 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 4 run data merge block ~1 ~2 ~0 {Text2:"\"Birch\"",Text3:"\"\""}


execute if score wood_power funcs matches 5 run setblock ~1 ~2 ~-1 minecraft:birch_pressure_plate[powered=true]
execute if score wood_power funcs matches 5 run setblock ~1 ~3 ~0 minecraft:birch_button[facing=east,powered=true]
execute if score wood_power funcs matches 5 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 5 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 5 run data merge block ~1 ~2 ~0 {Text2:"\"Birch\"",Text3:"\"(Powered)\""}


execute if score wood_power funcs matches 6 run setblock ~1 ~2 ~-1 minecraft:jungle_pressure_plate[powered=false]
execute if score wood_power funcs matches 6 run setblock ~1 ~3 ~0 minecraft:jungle_button[facing=east,powered=false]
execute if score wood_power funcs matches 6 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 6 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 6 run data merge block ~1 ~2 ~0 {Text2:"\"Jungle\"",Text3:"\"\""}


execute if score wood_power funcs matches 7 run setblock ~1 ~2 ~-1 minecraft:jungle_pressure_plate[powered=true]
execute if score wood_power funcs matches 7 run setblock ~1 ~3 ~0 minecraft:jungle_button[facing=east,powered=true]
execute if score wood_power funcs matches 7 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 7 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 7 run data merge block ~1 ~2 ~0 {Text2:"\"Jungle\"",Text3:"\"(Powered)\""}


execute if score wood_power funcs matches 8 run setblock ~1 ~2 ~-1 minecraft:oak_pressure_plate[powered=false]
execute if score wood_power funcs matches 8 run setblock ~1 ~3 ~0 minecraft:oak_button[facing=east,powered=false]
execute if score wood_power funcs matches 8 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 8 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 8 run data merge block ~1 ~2 ~0 {Text2:"\"Oak\"",Text3:"\"\""}


execute if score wood_power funcs matches 9 run setblock ~1 ~2 ~-1 minecraft:oak_pressure_plate[powered=true]
execute if score wood_power funcs matches 9 run setblock ~1 ~3 ~0 minecraft:oak_button[facing=east,powered=true]
execute if score wood_power funcs matches 9 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 9 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 9 run data merge block ~1 ~2 ~0 {Text2:"\"Oak\"",Text3:"\"(Powered)\""}


execute if score wood_power funcs matches 10 run setblock ~1 ~2 ~-1 minecraft:dark_oak_pressure_plate[powered=false]
execute if score wood_power funcs matches 10 run setblock ~1 ~3 ~0 minecraft:dark_oak_button[facing=east,powered=false]
execute if score wood_power funcs matches 10 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 10 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 10 run data merge block ~1 ~2 ~0 {Text2:"\"Dark Oak\"",Text3:"\"\""}


execute if score wood_power funcs matches 11 run setblock ~1 ~2 ~-1 minecraft:dark_oak_pressure_plate[powered=true]
execute if score wood_power funcs matches 11 run setblock ~1 ~3 ~0 minecraft:dark_oak_button[facing=east,powered=true]
execute if score wood_power funcs matches 11 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 11 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 11 run data merge block ~1 ~2 ~0 {Text2:"\"Dark Oak\"",Text3:"\"(Powered)\""}


execute if score wood_power funcs matches 12 run setblock ~1 ~2 ~-1 minecraft:spruce_pressure_plate[powered=false]
execute if score wood_power funcs matches 12 run setblock ~1 ~3 ~0 minecraft:spruce_button[facing=east,powered=false]
execute if score wood_power funcs matches 12 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 12 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=false]
execute if score wood_power funcs matches 12 run data merge block ~1 ~2 ~0 {Text2:"\"Spruce\"",Text3:"\"\""}


execute if score wood_power funcs matches 13 run setblock ~1 ~2 ~-1 minecraft:spruce_pressure_plate[powered=true]
execute if score wood_power funcs matches 13 run setblock ~1 ~3 ~0 minecraft:spruce_button[facing=east,powered=true]
execute if score wood_power funcs matches 13 run setblock ~0 ~3 ~0 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 13 run setblock ~0 ~2 ~-1 minecraft:redstone_lamp[lit=true]
execute if score wood_power funcs matches 13 run data merge block ~1 ~2 ~0 {Text2:"\"Spruce\"",Text3:"\"(Powered)\""}
