scoreboard players set structure_blocks max 4
execute unless score structure_blocks funcs matches 0..3 run scoreboard players operation structure_blocks funcs %= structure_blocks max

execute if score structure_blocks funcs matches 0 run data merge block ~ ~3 ~ {mode:data}
execute if score structure_blocks funcs matches 0 run data merge block ~ ~2 ~1 {Text2:"\"Data\""}


execute if score structure_blocks funcs matches 1 run data merge block ~ ~3 ~ {mode:save}
execute if score structure_blocks funcs matches 1 run data merge block ~ ~2 ~1 {Text2:"\"Save\""}


execute if score structure_blocks funcs matches 2 run data merge block ~ ~3 ~ {mode:load}
execute if score structure_blocks funcs matches 2 run data merge block ~ ~2 ~1 {Text2:"\"Load\""}


execute if score structure_blocks funcs matches 3 run data merge block ~ ~3 ~ {mode:corner}
execute if score structure_blocks funcs matches 3 run data merge block ~ ~2 ~1 {Text2:"\"Corner\""}
