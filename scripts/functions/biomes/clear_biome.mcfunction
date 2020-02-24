execute positioned ~ ~-5 ~ run kill @e[type=!player,tag=!homer,dx=64,dy=45,dz=64]
fill ~-2 ~-4 ~-2 ~-1 ~42 ~66 air replace #v3:liquid
fill ~-2 ~-4 ~-2 ~66 ~42 ~-1 air replace #v3:liquid
fill ~-2 ~-4 ~65 ~65 ~42 ~64 air replace #v3:liquid
fill ~64 ~-4 ~-2 ~65 ~42 ~65 air replace #v3:liquid



data merge block ~0 ~1 ~0 {name:"air",mode:LOAD}


data merge block ~0 ~1 ~32 {name:"air",mode:LOAD}


data merge block ~32 ~1 ~0 {name:"air",mode:LOAD}


data merge block ~32 ~1 ~32 {name:"air",mode:LOAD}




setblock ~0 ~ ~0 redstone_torch
setblock ~0 ~ ~0 air

setblock ~0 ~ ~32 redstone_torch
setblock ~0 ~ ~32 air

setblock ~32 ~ ~0 redstone_torch
setblock ~32 ~ ~0 air

setblock ~32 ~ ~32 redstone_torch
setblock ~32 ~ ~32 air


execute positioned ~ ~-5 ~ run kill @e[type=item,dx=64,dy=45,dz=64,nbt={OnGround:True}]
