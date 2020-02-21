execute positioned ~ ~-4 ~ run kill @e[type=!player,tag=!homer,dx=64,dy=40,dz=64]


execute if score snowy_tundra biome matches 1 run say switching to biome Snowy Tundra

execute at @e[tag=switch_biome_home] run execute if score snowy_tundra biome matches 1 run data merge block ~0 ~1 ~0 {name:"snowy_tundra_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score snowy_tundra biome matches 1 run data merge block ~0 ~1 ~32 {name:"snowy_tundra_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score snowy_tundra biome matches 1 run data merge block ~32 ~1 ~0 {name:"snowy_tundra_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score snowy_tundra biome matches 1 run data merge block ~32 ~1 ~32 {name:"snowy_tundra_4",mode:LOAD}

execute if score ice_spikes biome matches 1 run say switching to biome Ice Spikes

execute at @e[tag=switch_biome_home] run execute if score ice_spikes biome matches 1 run data merge block ~0 ~1 ~0 {name:"ice_spikes_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score ice_spikes biome matches 1 run data merge block ~0 ~1 ~32 {name:"ice_spikes_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score ice_spikes biome matches 1 run data merge block ~32 ~1 ~0 {name:"ice_spikes_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score ice_spikes biome matches 1 run data merge block ~32 ~1 ~32 {name:"ice_spikes_4",mode:LOAD}

execute if score snowy_tiaga biome matches 1 run say switching to biome Snowy Tiaga

execute at @e[tag=switch_biome_home] run execute if score snowy_tiaga biome matches 1 run data merge block ~0 ~1 ~0 {name:"snowy_tiaga_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score snowy_tiaga biome matches 1 run data merge block ~0 ~1 ~32 {name:"snowy_tiaga_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score snowy_tiaga biome matches 1 run data merge block ~32 ~1 ~0 {name:"snowy_tiaga_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score snowy_tiaga biome matches 1 run data merge block ~32 ~1 ~32 {name:"snowy_tiaga_4",mode:LOAD}

execute if score tiaga biome matches 1 run say switching to biome Tiaga

execute at @e[tag=switch_biome_home] run execute if score tiaga biome matches 1 run data merge block ~0 ~1 ~0 {name:"tiaga_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score tiaga biome matches 1 run data merge block ~0 ~1 ~32 {name:"tiaga_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score tiaga biome matches 1 run data merge block ~32 ~1 ~0 {name:"tiaga_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score tiaga biome matches 1 run data merge block ~32 ~1 ~32 {name:"tiaga_4",mode:LOAD}

execute if score stone_shore biome matches 1 run say switching to biome Stone Shore

execute at @e[tag=switch_biome_home] run execute if score stone_shore biome matches 1 run data merge block ~0 ~1 ~0 {name:"stone_shore_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score stone_shore biome matches 1 run data merge block ~0 ~1 ~32 {name:"stone_shore_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score stone_shore biome matches 1 run data merge block ~32 ~1 ~0 {name:"stone_shore_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score stone_shore biome matches 1 run data merge block ~32 ~1 ~32 {name:"stone_shore_4",mode:LOAD}





execute at @e[tag=switch_biome_home] run setblock ~0 ~ ~0 redstone_torch
execute at @e[tag=switch_biome_home] run setblock ~0 ~ ~0 air


execute at @e[tag=switch_biome_home] run setblock ~0 ~ ~32 redstone_torch
execute at @e[tag=switch_biome_home] run setblock ~0 ~ ~32 air


execute at @e[tag=switch_biome_home] run setblock ~32 ~ ~0 redstone_torch
execute at @e[tag=switch_biome_home] run setblock ~32 ~ ~0 air


execute at @e[tag=switch_biome_home] run setblock ~32 ~ ~32 redstone_torch
execute at @e[tag=switch_biome_home] run setblock ~32 ~ ~32 air
