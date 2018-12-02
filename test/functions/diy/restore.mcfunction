setblock ~0 ~-2 ~0 structure_block{ignoreEntities:true,name:"minecraft:sequence",mode:"SAVE",posX:0,posY:4,posZ:-6,sizeX:1,sizeY:1,sizeZ:7,showboundingbox:false}
setblock ~0 ~-4 ~0 redstone_torch
setblock ~0 ~-4 ~0 air
setblock ~0 ~-2 ~0 stone
execute at @e[tag=starter] run setblock ~ ~-2 ~ redstone_torch
execute at @e[tag=starter] run setblock ~ ~-2 ~ air