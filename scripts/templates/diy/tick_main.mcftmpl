execute at @e[tag=diy_cloner] run setblock ~0 ~3 ~0 sand
scoreboard players set custom_reset funcs 0
execute at @e[tag=diy_cloner] unless block ~0 ~0 ~-1 air run scoreboard players set custom_reset funcs 1
execute at @e[tag=diy_cloner] if block ~0 ~4 ~-1 air run scoreboard players set custom_reset funcs 1
execute if score custom_reset funcs matches 1 at @e[tag=diy_starter] run tp @e[tag=diy_cloner] ~0 ~2 ~0
execute if score custom_reset funcs matches 0 at @e[tag=diy_cloner] run tp @e[tag=diy_cloner] ^ ^ ^1
execute at @e[tag=diy_cloner] unless block ~0 ~4 ~0 air run setblock ~0 ~3 ~0 magenta_glazed_terracotta
execute at @e[tag=diy_cloner] run setblock ~0 ~-1 ~0 structure_block{ignoreEntities:true,name:"restworld:singleton",mode:"SAVE",posX:0,posY:5,posZ:0,sizeX:1,sizeY:1,sizeZ:1,showboundingbox:false}
execute at @e[tag=diy_cloner] run setblock ~0 ~-2 ~0 redstone_torch
execute at @e[tag=diy_cloner] run setblock ~0 ~-2 ~0 air
execute at @e[tag=diy_cloner] run setblock ~0 ~-1 ~0 stone
execute at @e[tag=diy_displayer] run setblock ~0 ~-2 ~0 redstone_torch
execute at @e[tag=diy_displayer] run setblock ~0 ~-2 ~0 air
