execute unless score job_sites_1 funcs matches 0.. run function job_sites_1_init
scoreboard players add job_sites_1 funcs 1
scoreboard players set job_sites_1 max 5
execute unless score job_sites_1 funcs matches 0..4 run scoreboard players operation job_sites_1 funcs %= job_sites_1 max

execute if score job_sites_1 funcs matches 0 run setblock ~ ~3 ~ fletching_table
execute if score job_sites_1 funcs matches 0 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Fletching Table\""}


execute if score job_sites_1 funcs matches 1 run setblock ~ ~3 ~ cartography_table
execute if score job_sites_1 funcs matches 1 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Table\"",Text2:"\"Cartography\""}


execute if score job_sites_1 funcs matches 2 run setblock ~ ~3 ~ smithing_table
execute if score job_sites_1 funcs matches 2 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Smithing Table\""}


execute if score job_sites_1 funcs matches 3 run setblock ~ ~3 ~ loom
execute if score job_sites_1 funcs matches 3 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Loom\""}


execute if score job_sites_1 funcs matches 4 run setblock ~ ~3 ~ stonecutter
execute if score job_sites_1 funcs matches 4 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Stonecutter\""}
