say foo
kill @e[type=minecraft:ender_dragon]

scoreboard players set dragon max 2
execute unless score dragon funcs matches 0..1 run scoreboard players operation dragon funcs %= dragon max

{when(i)} kill @e[tag=dragon]


execute if score dragon funcs matches 1 run summon minecraft:ender_dragon ~ ~5 ~ {NoAi:True,Silent:True,Rotation:[180f,0f],PersistenceRequired:True,Tags:[dragon]}
execute if score dragon funcs matches 1 run summon dragon_fireball ~-10 ~5 ~ {direction:[0.0,0.0,0.0],ExplosionPower:0,Tags:[dragon]}
