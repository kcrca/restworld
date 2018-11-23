



execute if score structure_blocks funcs matches 0 run data merge block ~ ~3 ~ {mode:DATA}
execute if score structure_blocks funcs matches 0 run data merge block ~-1 ~2 ~ {Text2:"\"Data\""}


execute if score structure_blocks funcs matches 1 run data merge block ~ ~3 ~ {mode:SAVE}
execute if score structure_blocks funcs matches 1 run data merge block ~-1 ~2 ~ {Text2:"\"Save\""}


execute if score structure_blocks funcs matches 2 run data merge block ~ ~3 ~ {mode:LOAD}
execute if score structure_blocks funcs matches 2 run data merge block ~-1 ~2 ~ {Text2:"\"Load\""}


execute if score structure_blocks funcs matches 3 run data merge block ~ ~3 ~ {mode:CORNER}
execute if score structure_blocks funcs matches 3 run data merge block ~-1 ~2 ~ {Text2:"\"Corner\""}


