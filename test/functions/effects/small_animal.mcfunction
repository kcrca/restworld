execute unless score small_animal funcs matches 0.. run function small_animal_init
scoreboard players add small_animal funcs 1
execute unless score small_animal funcs matches 0..2 run scoreboard players set small_animal funcs 0

execute if score small_animal funcs matches 0 run summon minecraft:ocelot ~0 ~0 ~0 {NoAI:True,Silent:True,CatType:1}


execute if score small_animal funcs matches 1 run summon minecraft:horse ~0 ~0 ~0 {NoAI:True,Silent:True,CatType:1}


execute if score small_animal funcs matches 2 run summon minecraft:llama ~0 ~0 ~0 {NoAI:True,Silent:True,CatType:1}