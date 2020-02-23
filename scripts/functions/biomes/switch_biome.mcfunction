execute positioned ~ ~-4 ~ run kill @e[type=!player,tag=!homer,dx=64,dy=40,dz=64]
fill ~-1 81 ~-1 ~66 87 ~66 air
fill ~-1 88 ~-1 ~66 94 ~66 air


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

execute if score plains biome matches 1 run say switching to biome Plains

execute at @e[tag=switch_biome_home] run execute if score plains biome matches 1 run data merge block ~0 ~1 ~0 {name:"plains_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score plains biome matches 1 run data merge block ~0 ~1 ~32 {name:"plains_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score plains biome matches 1 run data merge block ~32 ~1 ~0 {name:"plains_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score plains biome matches 1 run data merge block ~32 ~1 ~32 {name:"plains_4",mode:LOAD}

execute if score forest biome matches 1 run say switching to biome Forest

execute at @e[tag=switch_biome_home] run execute if score forest biome matches 1 run data merge block ~0 ~1 ~0 {name:"forest_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score forest biome matches 1 run data merge block ~0 ~1 ~32 {name:"forest_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score forest biome matches 1 run data merge block ~32 ~1 ~0 {name:"forest_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score forest biome matches 1 run data merge block ~32 ~1 ~32 {name:"forest_4",mode:LOAD}

execute if score flower_forest biome matches 1 run say switching to biome Flower Forest

execute at @e[tag=switch_biome_home] run execute if score flower_forest biome matches 1 run data merge block ~0 ~1 ~0 {name:"flower_forest_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score flower_forest biome matches 1 run data merge block ~0 ~1 ~32 {name:"flower_forest_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score flower_forest biome matches 1 run data merge block ~32 ~1 ~0 {name:"flower_forest_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score flower_forest biome matches 1 run data merge block ~32 ~1 ~32 {name:"flower_forest_4",mode:LOAD}

execute if score birch_forest biome matches 1 run say switching to biome Birch Forest

execute at @e[tag=switch_biome_home] run execute if score birch_forest biome matches 1 run data merge block ~0 ~1 ~0 {name:"birch_forest_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score birch_forest biome matches 1 run data merge block ~0 ~1 ~32 {name:"birch_forest_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score birch_forest biome matches 1 run data merge block ~32 ~1 ~0 {name:"birch_forest_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score birch_forest biome matches 1 run data merge block ~32 ~1 ~32 {name:"birch_forest_4",mode:LOAD}

execute if score dark_forest biome matches 1 run say switching to biome Dark Forest

execute at @e[tag=switch_biome_home] run execute if score dark_forest biome matches 1 run data merge block ~0 ~1 ~0 {name:"dark_forest_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score dark_forest biome matches 1 run data merge block ~0 ~1 ~32 {name:"dark_forest_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score dark_forest biome matches 1 run data merge block ~32 ~1 ~0 {name:"dark_forest_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score dark_forest biome matches 1 run data merge block ~32 ~1 ~32 {name:"dark_forest_4",mode:LOAD}

execute if score swamp biome matches 1 run say switching to biome Swamp

execute at @e[tag=switch_biome_home] run execute if score swamp biome matches 1 run data merge block ~0 ~1 ~0 {name:"swamp_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score swamp biome matches 1 run data merge block ~0 ~1 ~32 {name:"swamp_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score swamp biome matches 1 run data merge block ~32 ~1 ~0 {name:"swamp_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score swamp biome matches 1 run data merge block ~32 ~1 ~32 {name:"swamp_4",mode:LOAD}

execute if score jungle biome matches 1 run say switching to biome Jungle

execute at @e[tag=switch_biome_home] run execute if score jungle biome matches 1 run data merge block ~0 ~1 ~0 {name:"jungle_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score jungle biome matches 1 run data merge block ~0 ~1 ~32 {name:"jungle_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score jungle biome matches 1 run data merge block ~32 ~1 ~0 {name:"jungle_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score jungle biome matches 1 run data merge block ~32 ~1 ~32 {name:"jungle_4",mode:LOAD}

execute if score mushroom_field biome matches 1 run say switching to biome Mushroom Field

execute at @e[tag=switch_biome_home] run execute if score mushroom_field biome matches 1 run data merge block ~0 ~1 ~0 {name:"mushroom_field_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score mushroom_field biome matches 1 run data merge block ~0 ~1 ~32 {name:"mushroom_field_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score mushroom_field biome matches 1 run data merge block ~32 ~1 ~0 {name:"mushroom_field_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score mushroom_field biome matches 1 run data merge block ~32 ~1 ~32 {name:"mushroom_field_4",mode:LOAD}

execute if score the_end biome matches 1 run say switching to biome The End

execute at @e[tag=switch_biome_home] run execute if score the_end biome matches 1 run data merge block ~0 ~1 ~0 {name:"the_end_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score the_end biome matches 1 run data merge block ~0 ~1 ~32 {name:"the_end_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score the_end biome matches 1 run data merge block ~32 ~1 ~0 {name:"the_end_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score the_end biome matches 1 run data merge block ~32 ~1 ~32 {name:"the_end_4",mode:LOAD}

execute if score end_island biome matches 1 run say switching to biome End Island

execute at @e[tag=switch_biome_home] run execute if score end_island biome matches 1 run data merge block ~0 ~1 ~0 {name:"end_island_1",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score end_island biome matches 1 run data merge block ~0 ~1 ~32 {name:"end_island_2",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score end_island biome matches 1 run data merge block ~32 ~1 ~0 {name:"end_island_3",mode:LOAD}
execute at @e[tag=switch_biome_home] run execute if score end_island biome matches 1 run data merge block ~32 ~1 ~32 {name:"end_island_4",mode:LOAD}





execute at @e[tag=switch_biome_home] run setblock ~0 ~ ~0 redstone_torch
execute at @e[tag=switch_biome_home] run setblock ~0 ~ ~0 air


execute at @e[tag=switch_biome_home] run setblock ~0 ~ ~32 redstone_torch
execute at @e[tag=switch_biome_home] run setblock ~0 ~ ~32 air


execute at @e[tag=switch_biome_home] run setblock ~32 ~ ~0 redstone_torch
execute at @e[tag=switch_biome_home] run setblock ~32 ~ ~0 air


execute at @e[tag=switch_biome_home] run setblock ~32 ~ ~32 redstone_torch
execute at @e[tag=switch_biome_home] run setblock ~32 ~ ~32 air
