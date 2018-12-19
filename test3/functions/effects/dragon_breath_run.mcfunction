execute unless score dragon_breath_run funcs matches 0.. run function dragon_breath_run_init
scoreboard players add dragon_breath_run funcs 1
scoreboard players set dragon_breath_run max 48
execute unless score dragon_breath_run funcs matches 0..47 run scoreboard players operation dragon_breath_run funcs %= dragon_breath_run max

execute if score dragon_breath_run funcs matches 0 run summon minecraft:dragon_fireball ~0 ~1 ~0 {direction:[0.0,-0.3,0.0],ExplosionPower:1}
