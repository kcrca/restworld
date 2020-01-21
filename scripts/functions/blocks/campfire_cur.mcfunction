scoreboard players set campfire max 2
execute unless score campfire funcs matches 0..1 run scoreboard players operation campfire funcs %= campfire max

execute if score campfire funcs matches 0 run setblock ~0 ~3 ~0 minecraft:campfire[lit=true]
execute if score campfire funcs matches 0 run data merge block ~0 ~2 ~-1 {Text2:"\"Campfire\"",Text3:"\"\"",Text4:"\"\""}


execute if score campfire funcs matches 1 run setblock ~0 ~3 ~0 minecraft:campfire[lit=false]
execute if score campfire funcs matches 1 run data merge block ~0 ~2 ~-1 {Text2:"\"Campfire\"",Text3:"\"\"",Text4:"\"\""}
