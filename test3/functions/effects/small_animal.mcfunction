execute unless score small_animal funcs matches 0.. run function small_animal_init
scoreboard players add small_animal funcs 1
scoreboard players set small_animal max 3
execute unless score small_animal funcs matches 0..2 run scoreboard players operation small_animal funcs %= small_animal max

execute if score small_animal funcs matches 0 run summon minecraft:ocelot ~0 ~0 ~0 {CatType:1,NoAI:True,Tags:[effecter]}


execute if score small_animal funcs matches 1 run summon minecraft:horse ~0 ~0 ~0 {CatType:1,NoAI:True,Tags:[effecter]}


execute if score small_animal funcs matches 2 run summon minecraft:llama ~0 ~0 ~0 {CatType:1,NoAI:True,Tags:[effecter]}
