execute unless score composter funcs matches 0.. run function composter_init
scoreboard players add composter funcs 1
scoreboard players set composter max 9
execute unless score composter funcs matches 0..8 run scoreboard players operation composter funcs %= composter max

execute if score composter funcs matches 0 run setblock ~ ~3 ~ composter[level=0]
execute if score composter funcs matches 0 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 0\"",Text2:"\"Composter\""}


execute if score composter funcs matches 1 run setblock ~ ~3 ~ composter[level=1]
execute if score composter funcs matches 1 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 1\"",Text2:"\"Composter\""}


execute if score composter funcs matches 2 run setblock ~ ~3 ~ composter[level=2]
execute if score composter funcs matches 2 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 2\"",Text2:"\"Composter\""}


execute if score composter funcs matches 3 run setblock ~ ~3 ~ composter[level=3]
execute if score composter funcs matches 3 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 3\"",Text2:"\"Composter\""}


execute if score composter funcs matches 4 run setblock ~ ~3 ~ composter[level=4]
execute if score composter funcs matches 4 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 4\"",Text2:"\"Composter\""}


execute if score composter funcs matches 5 run setblock ~ ~3 ~ composter[level=5]
execute if score composter funcs matches 5 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 5\"",Text2:"\"Composter\""}


execute if score composter funcs matches 6 run setblock ~ ~3 ~ composter[level=6]
execute if score composter funcs matches 6 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 6\"",Text2:"\"Composter\""}


execute if score composter funcs matches 7 run setblock ~ ~3 ~ composter[level=7]
execute if score composter funcs matches 7 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 7\"",Text2:"\"Composter\""}


execute if score composter funcs matches 8 run setblock ~ ~3 ~ composter[level=8]
execute if score composter funcs matches 8 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 8\"",Text2:"\"Composter\""}
