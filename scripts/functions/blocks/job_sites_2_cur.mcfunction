scoreboard players set job_sites_2 max 8
execute unless score job_sites_2 funcs matches 0..7 run scoreboard players operation job_sites_2 funcs %= job_sites_2 max

execute if score job_sites_2 funcs matches 0 run setblock ~ ~3 ~ blast_furnace[lit=false]
execute if score job_sites_2 funcs matches 0 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Not Lit\"",Text2:"\"Blast Furnace\""}
execute if score job_sites_2 funcs matches 0 run say Blast Furnace[lit=false]


execute if score job_sites_2 funcs matches 1 run setblock ~ ~3 ~ blast_furnace[lit=true]
execute if score job_sites_2 funcs matches 1 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Lit\"",Text2:"\"Blast Furnace\""}
execute if score job_sites_2 funcs matches 1 run say Blast Furnace[lit=true]


execute if score job_sites_2 funcs matches 2 run setblock ~ ~3 ~ smoker[lit=false]
execute if score job_sites_2 funcs matches 2 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Not Lit\"",Text2:"\"Smoker\""}
execute if score job_sites_2 funcs matches 2 run say Smoker[lit=false]


execute if score job_sites_2 funcs matches 3 run setblock ~ ~3 ~ smoker[lit=true]
execute if score job_sites_2 funcs matches 3 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Lit\"",Text2:"\"Smoker\""}
execute if score job_sites_2 funcs matches 3 run say Smoker[lit=true]


execute if score job_sites_2 funcs matches 4 run setblock ~ ~3 ~ barrel[facing=north,open=true]
execute if score job_sites_2 funcs matches 4 run data merge block ~0 ~2 ~-1 {Text4:"\"Open\"",Text3:"\"Facing North\"",Text2:"\"Barrel\""}
execute if score job_sites_2 funcs matches 4 run say Barrel[facing=north,open=true]


execute if score job_sites_2 funcs matches 5 run setblock ~ ~3 ~ barrel[facing=north,open=false]
execute if score job_sites_2 funcs matches 5 run data merge block ~0 ~2 ~-1 {Text4:"\"Not Open\"",Text3:"\"Facing North\"",Text2:"\"Barrel\""}
execute if score job_sites_2 funcs matches 5 run say Barrel[facing=north,open=false]


execute if score job_sites_2 funcs matches 6 run setblock ~ ~3 ~ lectern[has_book=false]
execute if score job_sites_2 funcs matches 6 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Not Book\"",Text2:"\"Lectern\""}
execute if score job_sites_2 funcs matches 6 run say Lectern[has_book=false]


execute if score job_sites_2 funcs matches 7 run setblock ~ ~3 ~ lectern[has_book=true]
execute if score job_sites_2 funcs matches 7 run data merge block ~0 ~2 ~-1 {Text4:"\"\"",Text3:"\"Book\"",Text2:"\"Lectern\""}
execute if score job_sites_2 funcs matches 7 run say Lectern[has_book=true]
