scoreboard players set end_portal max 2
execute unless score end_portal funcs matches 0..1 run scoreboard players operation end_portal funcs %= end_portal max

execute if score end_portal funcs matches 0 run fill ~2 ~2 ~1 ~2 ~2 ~-1 end_portal_frame[facing=west,eye=true]
execute if score end_portal funcs matches 0 run fill ~1 ~2 ~2 ~-1 ~2 ~2 end_portal_frame[facing=north,eye=true]
execute if score end_portal funcs matches 0 run fill ~-2 ~2 ~1 ~-2 ~2 ~-1 end_portal_frame[facing=east,eye=true]
execute if score end_portal funcs matches 0 run fill ~1 ~2 ~-2 ~-1 ~2 ~-2 end_portal_frame[facing=south,eye=true]
execute if score end_portal funcs matches 0 run fill ~1 ~2 ~1 ~-1 ~2 ~-1 minecraft:end_portal


execute if score end_portal funcs matches 1 run fill ~2 ~2 ~1 ~2 ~2 ~-1 end_portal_frame[facing=west,eye=false]
execute if score end_portal funcs matches 1 run fill ~1 ~2 ~2 ~-1 ~2 ~2 end_portal_frame[facing=north,eye=false]
execute if score end_portal funcs matches 1 run fill ~-2 ~2 ~1 ~-2 ~2 ~-1 end_portal_frame[facing=east,eye=false]
execute if score end_portal funcs matches 1 run fill ~1 ~2 ~-2 ~-1 ~2 ~-2 end_portal_frame[facing=south,eye=false]
execute if score end_portal funcs matches 1 run fill ~1 ~2 ~1 ~-1 ~2 ~-1 minecraft:air
