



execute if score structure_blocks funcs matches 0 run data merge block ~ ~3 ~ {mode:data}
execute if score structure_blocks funcs matches 0 run data merge block ~-1 ~2 ~ {Text2:"\"Data\""}


execute if score structure_blocks funcs matches 1 run data merge block ~ ~3 ~ {mode:save}
execute if score structure_blocks funcs matches 1 run data merge block ~-1 ~2 ~ {Text2:"\"Save\""}


execute if score structure_blocks funcs matches 2 run data merge block ~ ~3 ~ {mode:load}
execute if score structure_blocks funcs matches 2 run data merge block ~-1 ~2 ~ {Text2:"\"Load\""}


execute if score structure_blocks funcs matches 3 run data merge block ~ ~3 ~ {mode:corner}
execute if score structure_blocks funcs matches 3 run data merge block ~-1 ~2 ~ {Text2:"\"Corner\""}


