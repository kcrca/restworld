kill @e[type=minecraft:ender_dragon]
summon minecraft:ender_dragon ~ ~5 ~-5 {NoAi:True,Silent:True,Rotation:[0f,0f],Tags:[ender]}
summon dragon_fireball ~ ~5 ~-15 {direction:[0.0,0.0,0.0],ExplosionPower:0,Tags:[ender]}
setblock ~ ~2 ~-5 wall_sign{Text2:"\"Ender Dragon\""}
setblock ~ ~2 ~-15 wall_sign{Text2:"\"Dragon Fireball\""}
