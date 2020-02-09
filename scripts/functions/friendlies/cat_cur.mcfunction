scoreboard players set cat max 11
execute unless score cat funcs matches 0..10 run scoreboard players operation cat funcs %= cat max
execute if score cat funcs matches 0 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:0,CustomName:"\"Tabby\"",Owner:dummy}

execute if score cat funcs matches 1 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:1,CustomName:"\"Tuxedo\"",Owner:dummy}

execute if score cat funcs matches 2 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:2,CustomName:"\"Red\"",Owner:dummy}

execute if score cat funcs matches 3 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:3,CustomName:"\"Siamese\"",Owner:dummy}

execute if score cat funcs matches 4 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:4,CustomName:"\"British Shorthair\"",Owner:dummy}

execute if score cat funcs matches 5 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:5,CustomName:"\"Calico\"",Owner:dummy}

execute if score cat funcs matches 6 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:6,CustomName:"\"Persian\"",Owner:dummy}

execute if score cat funcs matches 7 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:7,CustomName:"\"Ragdoll\"",Owner:dummy}

execute if score cat funcs matches 8 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:8,CustomName:"\"White\"",Owner:dummy}

execute if score cat funcs matches 9 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:9,CustomName:"\"Jellie\"",Owner:dummy}

execute if score cat funcs matches 10 run execute as @e[tag=cat,tag=collared] run data merge entity @s {CatType:10,CustomName:"\"Black\"",Owner:dummy}
