tp @e[tag=skeleton_horse,tag=!kid] @e[tag=death,limit=1]



execute unless score skeleton_horse funcs matches 0.. run function skeleton_horse_init
scoreboard players add skeleton_horse funcs 1
scoreboard players set skeleton_horse max 2
execute unless score skeleton_horse funcs matches 0..1 run scoreboard players operation skeleton_horse funcs %= skeleton_horse max

execute if score skeleton_horse funcs matches 0 run summon minecraft:skeleton_horse ~-0.8 ~2 ~0 {Tags:[skeleton_horse,monsters,monsters],CustomName:"\"Skeleton Horse\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}

execute if score skeleton_horse funcs matches 1 run summon minecraft:skeleton_horse ~-0.8 ~2 ~0 {Tags:[skeleton_horse,monsters,monsters],NoGravity:true,Passengers:[{id:"minecraft:skeleton",ArmorItems:[{},{},{},{id:"minecraft:iron_helmet",Count:1,tag:{RepairCost:1,Enchantments:[{lvl:3,id:"minecraft:unbreaking"}]}}],HandItems:[{id:"minecraft:bow",Count:1b,tag:{RepairCost:1,Enchantments:[{lvl:3s,id:"minecraft:unbreaking"}]}},{}],Tags:[monsters,passenger],Rotation:[270f,0f],Facing:east,PersistenceRequired:True,NoAI:True,Silent:True}],CustomName:"\"Skeleton Horse\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[270f,0f]}