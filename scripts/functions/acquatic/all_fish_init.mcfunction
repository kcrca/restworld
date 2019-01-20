summon minecraft:tropical_fish ~0 ~2.2 ~0 {Tags:[fish0,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~1 {Tags:[fish1,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~2 {Tags:[fish2,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~3 {Tags:[fish3,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~4 {Tags:[fish4,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~5 {Tags:[fish5,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~0 {Tags:[fish6,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~1 {Tags:[fish7,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~2 {Tags:[fish8,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~3 {Tags:[fish9,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~4 {Tags:[fish10,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~5 {Tags:[fish11,acquatic],NoAI:True,Silent:True,Rotation:[90f,0f]}

scoreboard objectives remove fish
scoreboard objectives add fish dummy
scoreboard players set NUM_COLORS fish 16
scoreboard players set body fish 0
scoreboard players set pattern fish 0
scoreboard players set BODY_SCALE fish 65536
scoreboard players set PATTERN_SCALE fish 16777216
