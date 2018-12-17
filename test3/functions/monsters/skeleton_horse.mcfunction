tp @e[tag=skeleton_horse,tag=!kid] @e[tag=death,limit=1]



execute unless score skeleton_horse funcs matches 0.. run function skeleton_horse_init
scoreboard players add skeleton_horse funcs 1
scoreboard players set skeleton_horse max 2
execute unless score skeleton_horse funcs matches 0..1 run scoreboard players operation skeleton_horse funcs %= skeleton_horse max

execute if score skeleton_horse funcs matches 0 run summon minecraft:skeleton_horse ~-0.8 ~2 ~0 {Tags:[skeleton_horse,monsters],CustomName:"\"Skeleton Horse\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}

execute if score skeleton_horse funcs matches 1 run summon minecraft:skeleton_horse ~-0.8 ~2 ~0 {Tags:[skeleton_horse,monsters],Passengers:[{id:"minecraft:skeleton",Tags:[monsters],Rotation:[270f,0f],Facing:east,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Skeleton Horse\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}
