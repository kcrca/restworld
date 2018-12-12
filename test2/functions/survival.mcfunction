data merge block ~-6 ~6 ~0 {Items:[{Slot:0,id:lapis_lazuli,Count:64},{Slot:1,id:book,Count:64}]}


execute unless score survival funcs matches 0.. run function survival_init
scoreboard players add survival funcs 1
execute unless score survival funcs matches 0..3 run scoreboard players set survival funcs 0

execute if score survival funcs matches 0 run xp set @p 0 levels


execute if score survival funcs matches 1 run xp set @p 9 levels


execute if score survival funcs matches 2 run xp set @p 20 levels


execute if score survival funcs matches 3 run xp set @p 30 levels