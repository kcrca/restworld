execute unless score horse funcs matches 0.. run function horse_init
scoreboard players add horse funcs 1
scoreboard players set horse max 5
execute unless score horse funcs matches 0..4 run scoreboard players operation horse funcs %= horse max

execute if score horse funcs matches 0 as @e[tag=white_horses] run data merge entity @s {Variant:0}
execute if score horse funcs matches 0 as @e[tag=creamy_horses] run data merge entity @s {Variant:1}
execute if score horse funcs matches 0 as @e[tag=chestnut_horses] run data merge entity @s {Variant:2}
execute if score horse funcs matches 0 as @e[tag=brown_horses] run data merge entity @s {Variant:3}
execute if score horse funcs matches 0 as @e[tag=black_horses] run data merge entity @s {Variant:4}
execute if score horse funcs matches 0 as @e[tag=gray_horses] run data merge entity @s {Variant:5}
execute if score horse funcs matches 0 as @e[tag=dark_brown_horses] run data merge entity @s {Variant:6}
execute if score horse funcs matches 0 at @e[tag=brown_horses,tag=kid] run data merge block ~2 ~ ~ {Text3:"\"None\""}


execute if score horse funcs matches 1 as @e[tag=white_horses] run data merge entity @s {Variant:256}
execute if score horse funcs matches 1 as @e[tag=creamy_horses] run data merge entity @s {Variant:257}
execute if score horse funcs matches 1 as @e[tag=chestnut_horses] run data merge entity @s {Variant:258}
execute if score horse funcs matches 1 as @e[tag=brown_horses] run data merge entity @s {Variant:259}
execute if score horse funcs matches 1 as @e[tag=black_horses] run data merge entity @s {Variant:260}
execute if score horse funcs matches 1 as @e[tag=gray_horses] run data merge entity @s {Variant:261}
execute if score horse funcs matches 1 as @e[tag=dark_brown_horses] run data merge entity @s {Variant:262}
execute if score horse funcs matches 1 at @e[tag=brown_horses,tag=kid] run data merge block ~2 ~ ~ {Text3:"\"White\""}


execute if score horse funcs matches 2 as @e[tag=white_horses] run data merge entity @s {Variant:512}
execute if score horse funcs matches 2 as @e[tag=creamy_horses] run data merge entity @s {Variant:513}
execute if score horse funcs matches 2 as @e[tag=chestnut_horses] run data merge entity @s {Variant:514}
execute if score horse funcs matches 2 as @e[tag=brown_horses] run data merge entity @s {Variant:515}
execute if score horse funcs matches 2 as @e[tag=black_horses] run data merge entity @s {Variant:516}
execute if score horse funcs matches 2 as @e[tag=gray_horses] run data merge entity @s {Variant:517}
execute if score horse funcs matches 2 as @e[tag=dark_brown_horses] run data merge entity @s {Variant:518}
execute if score horse funcs matches 2 at @e[tag=brown_horses,tag=kid] run data merge block ~2 ~ ~ {Text3:"\"White Field\""}


execute if score horse funcs matches 3 as @e[tag=white_horses] run data merge entity @s {Variant:768}
execute if score horse funcs matches 3 as @e[tag=creamy_horses] run data merge entity @s {Variant:769}
execute if score horse funcs matches 3 as @e[tag=chestnut_horses] run data merge entity @s {Variant:770}
execute if score horse funcs matches 3 as @e[tag=brown_horses] run data merge entity @s {Variant:771}
execute if score horse funcs matches 3 as @e[tag=black_horses] run data merge entity @s {Variant:772}
execute if score horse funcs matches 3 as @e[tag=gray_horses] run data merge entity @s {Variant:773}
execute if score horse funcs matches 3 as @e[tag=dark_brown_horses] run data merge entity @s {Variant:774}
execute if score horse funcs matches 3 at @e[tag=brown_horses,tag=kid] run data merge block ~2 ~ ~ {Text3:"\"White Dots\""}


execute if score horse funcs matches 4 as @e[tag=white_horses] run data merge entity @s {Variant:1024}
execute if score horse funcs matches 4 as @e[tag=creamy_horses] run data merge entity @s {Variant:1025}
execute if score horse funcs matches 4 as @e[tag=chestnut_horses] run data merge entity @s {Variant:1026}
execute if score horse funcs matches 4 as @e[tag=brown_horses] run data merge entity @s {Variant:1027}
execute if score horse funcs matches 4 as @e[tag=black_horses] run data merge entity @s {Variant:1028}
execute if score horse funcs matches 4 as @e[tag=gray_horses] run data merge entity @s {Variant:1029}
execute if score horse funcs matches 4 as @e[tag=dark_brown_horses] run data merge entity @s {Variant:1030}
execute if score horse funcs matches 4 at @e[tag=brown_horses,tag=kid] run data merge block ~2 ~ ~ {Text3:"\"Black Dots\""}
