scoreboard players set job_sites max 30
execute unless score job_sites funcs matches 0..29 run scoreboard players operation job_sites funcs %= job_sites max

execute if score job_sites funcs matches 0 run setblock ~ ~3 ~ blast_furnace
execute if score job_sites funcs matches 0 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Blast Furnace\""}


execute if score job_sites funcs matches 1 run setblock ~ ~3 ~ smoker
execute if score job_sites funcs matches 1 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Smoker\""}


execute if score job_sites funcs matches 2 run setblock ~ ~3 ~ brewing_stand
execute if score job_sites funcs matches 2 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Brewing Stand\""}


execute if score job_sites funcs matches 3 run setblock ~ ~3 ~ composter[level=0]
execute if score job_sites funcs matches 3 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 0\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 4 run setblock ~ ~3 ~ composter[level=1]
execute if score job_sites funcs matches 4 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 1\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 5 run setblock ~ ~3 ~ composter[level=2]
execute if score job_sites funcs matches 5 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 2\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 6 run setblock ~ ~3 ~ composter[level=3]
execute if score job_sites funcs matches 6 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 3\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 7 run setblock ~ ~3 ~ composter[level=4]
execute if score job_sites funcs matches 7 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 4\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 8 run setblock ~ ~3 ~ composter[level=5]
execute if score job_sites funcs matches 8 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 5\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 9 run setblock ~ ~3 ~ composter[level=6]
execute if score job_sites funcs matches 9 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 6\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 10 run setblock ~ ~3 ~ composter[level=7]
execute if score job_sites funcs matches 10 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 7\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 11 run setblock ~ ~3 ~ composter[level=8]
execute if score job_sites funcs matches 11 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 8\"",Text2:"\"Composter\""}


execute if score job_sites funcs matches 12 run setblock ~ ~3 ~ barrel[facing=up,open=true]
execute if score job_sites funcs matches 12 run data merge block ~0 ~2 ~-1 {Text4:"\"Open\"",Text3:"\"Facing Up\"",Text2:"\"Barrel\""}


execute if score job_sites funcs matches 13 run setblock ~ ~3 ~ barrel[facing=up,open=false]
execute if score job_sites funcs matches 13 run data merge block ~0 ~2 ~-1 {Text4:"\"Not Open\"",Text3:"\"Facing Up\"",Text2:"\"Barrel\""}


execute if score job_sites funcs matches 14 run setblock ~ ~3 ~ barrel[facing=north,open=true]
execute if score job_sites funcs matches 14 run data merge block ~0 ~2 ~-1 {Text4:"\"Open\"",Text3:"\"Facing North\"",Text2:"\"Barrel\""}


execute if score job_sites funcs matches 15 run setblock ~ ~3 ~ barrel[facing=south,open=false]
execute if score job_sites funcs matches 15 run data merge block ~0 ~2 ~-1 {Text4:"\"Not Open\"",Text3:"\"Facing South\"",Text2:"\"Barrel\""}


execute if score job_sites funcs matches 16 run setblock ~ ~3 ~ fletching_table
execute if score job_sites funcs matches 16 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Fletching Table\""}


execute if score job_sites funcs matches 17 run setblock ~ ~3 ~ cartography_table
execute if score job_sites funcs matches 17 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Table\"",Text2:"\"Cartography\""}


execute if score job_sites funcs matches 18 run setblock ~ ~3 ~ smithing_table
execute if score job_sites funcs matches 18 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Smithing Table\""}


execute if score job_sites funcs matches 19 run setblock ~ ~3 ~ cauldron[level=0]
execute if score job_sites funcs matches 19 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 0\"",Text2:"\"Cauldron\""}


execute if score job_sites funcs matches 20 run setblock ~ ~3 ~ cauldron[level=1]
execute if score job_sites funcs matches 20 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 1\"",Text2:"\"Cauldron\""}


execute if score job_sites funcs matches 21 run setblock ~ ~3 ~ cauldron[level=2]
execute if score job_sites funcs matches 21 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 2\"",Text2:"\"Cauldron\""}


execute if score job_sites funcs matches 22 run setblock ~ ~3 ~ cauldron[level=3]
execute if score job_sites funcs matches 22 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Level 3\"",Text2:"\"Cauldron\""}


execute if score job_sites funcs matches 23 run setblock ~ ~3 ~ lectern[has_book=false]
execute if score job_sites funcs matches 23 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Not Book\"",Text2:"\"Lectern\""}


execute if score job_sites funcs matches 24 run setblock ~ ~3 ~ lectern[has_book=true]
execute if score job_sites funcs matches 24 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Book\"",Text2:"\"Lectern\""}


execute if score job_sites funcs matches 25 run setblock ~ ~3 ~ loom
execute if score job_sites funcs matches 25 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Loom\""}


execute if score job_sites funcs matches 26 run setblock ~ ~3 ~ stonecutter
execute if score job_sites funcs matches 26 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"\"",Text2:"\"Stonecutter\""}


execute if score job_sites funcs matches 27 run setblock ~ ~3 ~ grindstone[face=floor]
execute if score job_sites funcs matches 27 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Face Floor\"",Text2:"\"Grindstone\""}


execute if score job_sites funcs matches 28 run setblock ~ ~3 ~ grindstone[face=wall]
execute if score job_sites funcs matches 28 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Face Wall\"",Text2:"\"Grindstone\""}


execute if score job_sites funcs matches 29 run setblock ~ ~3 ~ grindstone[face=ceiling]
execute if score job_sites funcs matches 29 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Face Ceiling\"",Text2:"\"Grindstone\""}
