

summon minecraft:tropical_fish ~3 ~2.2 ~0 {Tags:[fish0],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~3 ~2.2 ~1 {Tags:[fish1],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~3 ~2.2 ~2 {Tags:[fish2],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~3 ~2.2 ~3 {Tags:[fish3],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~3 ~2.2 ~4 {Tags:[fish4],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~3 ~2.2 ~5 {Tags:[fish5],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~4 ~2.2 ~0 {Tags:[fish6],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~4 ~2.2 ~1 {Tags:[fish7],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~4 ~2.2 ~2 {Tags:[fish8],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~4 ~2.2 ~3 {Tags:[fish9],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~4 ~2.2 ~4 {Tags:[fish10],NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~4 ~2.2 ~5 {Tags:[fish11],NoAI:True,Silent:True,Rotation:[90f,0f]}

summon minecraft:tropical_fish ~0 ~2.2 ~0 {Tags:[kob],Variant:917504,CustomName:"\"Red-White Kob\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~1 {Tags:[sunstreak],Variant:134217984,CustomName:"\"White-Silver Sunstreak\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~2 {Tags:[gray_red_snooper],Variant:235340288,CustomName:"\"Gray-Red Snooper\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~3 {Tags:[dasher],Variant:117441280,CustomName:"\"White-Gray Dasher\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~4 {Tags:[brinely],Variant:117441536,CustomName:"\"White-Gray Brinely\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~0 ~2.2 ~5 {Tags:[spotty],Variant:67110144,CustomName:"\"White-Yellow Spotter\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~0 {Tags:[flopper],Variant:117899265,CustomName:"\"Gray Flopper\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~1 {Tags:[stripey],Variant:117506305,CustomName:"\"Orange-Gray Stripey\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~2 {Tags:[white_gray_glitter],Variant:117441025,CustomName:"\"White-Gray Glitter\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~3 {Tags:[blockfish],Variant:67764993,CustomName:"\"Plum-Yellow Blockfish\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~4 {Tags:[red_white_betty],Variant:918529,CustomName:"\"Red-White Betty\"",NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:tropical_fish ~1 ~2.2 ~5 {Tags:[clayfish],Variant:234882305,CustomName:"\"White-Red Clayfish\"",NoAI:True,Silent:True,Rotation:[90f,0f]}

scoreboard objectives remove fish
scoreboard objectives add fish dummy
scoreboard players set NUM_COLORS fish 16
scoreboard players set body fish 0
scoreboard players set pattern fish 0
scoreboard players set BODY_SCALE fish 65536
scoreboard players set PATTERN_SCALE fish 16777216
execute at @e[type=armor_stand,name=mob_anchor] as @e[type=!player,dx=-40,dy=10,dz=40] run data merge entity @s {PersistenceRequired:True}
