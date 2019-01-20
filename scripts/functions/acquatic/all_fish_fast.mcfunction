scoreboard players add pattern fish 1
scoreboard players operation pattern fish %= NUM_COLORS fish
execute if score pattern fish matches 0 run scoreboard players add body fish 1
scoreboard players operation body fish %= NUM_COLORS fish
scoreboard players operation base_variant fish = body fish
scoreboard players operation base_variant fish *= BODY_SCALE fish
scoreboard players operation pattern_variant fish = pattern fish
scoreboard players operation pattern_variant fish *= PATTERN_SCALE fish
scoreboard players operation base_variant fish += pattern_variant fish
scoreboard players operation variant fish = base_variant fish
execute store result entity @e[tag=fish0,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players add variant fish 256
execute store result entity @e[tag=fish1,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players add variant fish 256
execute store result entity @e[tag=fish2,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players add variant fish 256
execute store result entity @e[tag=fish3,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players add variant fish 256
execute store result entity @e[tag=fish4,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players add variant fish 256
execute store result entity @e[tag=fish5,limit=1] Variant long 1 run scoreboard players get variant fish

scoreboard players add variant fish 1
execute store result entity @e[tag=fish6,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players remove variant fish 256
execute store result entity @e[tag=fish7,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players remove variant fish 256
execute store result entity @e[tag=fish8,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players remove variant fish 256
execute store result entity @e[tag=fish9,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players remove variant fish 256
execute store result entity @e[tag=fish10,limit=1] Variant long 1 run scoreboard players get variant fish
scoreboard players remove variant fish 256
execute store result entity @e[tag=fish11,limit=1] Variant long 1 run scoreboard players get variant fish
