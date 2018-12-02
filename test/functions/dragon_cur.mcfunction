kill @e[type=minecraft:ender_dragon]


execute if score dragon funcs matches 0 run kill @e[type=minecraft:dragon_fireball]
execute if score dragon funcs matches 0 run setblock ~-5 ~4 ~ minecraft:air
execute if score dragon funcs matches 0 run setblock ~-10 ~4 ~ minecraft:air
execute if score dragon funcs matches 0 run setblock ~-14 ~4 ~ minecraft:lever[powered=false,face=floor,facing=west]


execute if score dragon funcs matches 1 run summon minecraft:ender_dragon ~ ~5 ~ {NoAi:True,Silent:True,Rotation:[270f,0f]}
execute if score dragon funcs matches 1 run summon dragon_fireball ~-10 ~5 ~ {direction:[0.0,0.0,0.0],ExplosionPower:0}
execute if score dragon funcs matches 1 run setblock ~-5 ~4 ~ minecraft:wall_sign[facing=west]{Text2:"\"Dragon\""}
execute if score dragon funcs matches 1 run setblock ~-10 ~4 ~ minecraft:wall_sign[facing=west]{Text2:"\"Dragon Fireball\""}
execute if score dragon funcs matches 1 run setblock ~-14 ~4 ~ minecraft:lever[powered=true,face=floor,facing=west]