execute unless score load_biome funcs matches 0.. run function load_biome_init
scoreboard players add load_biome funcs 1
scoreboard players set load_biome max 24
execute unless score load_biome funcs matches 0..23 run scoreboard players operation load_biome funcs %= load_biome max
execute if score load_biome funcs matches 0 run say Switching to biome Plains

execute if score load_biome funcs matches 0 run data merge block ~0 ~1 ~0 {name:"plains_1",mode:LOAD}

execute if score load_biome funcs matches 0 run data merge block ~0 ~1 ~32 {name:"plains_2",mode:LOAD}

execute if score load_biome funcs matches 0 run data merge block ~32 ~1 ~0 {name:"plains_3",mode:LOAD}

execute if score load_biome funcs matches 0 run data merge block ~32 ~1 ~32 {name:"plains_4",mode:LOAD}


execute if score load_biome funcs matches 1 run say Switching to biome Forest

execute if score load_biome funcs matches 1 run data merge block ~0 ~1 ~0 {name:"forest_1",mode:LOAD}

execute if score load_biome funcs matches 1 run data merge block ~0 ~1 ~32 {name:"forest_2",mode:LOAD}

execute if score load_biome funcs matches 1 run data merge block ~32 ~1 ~0 {name:"forest_3",mode:LOAD}

execute if score load_biome funcs matches 1 run data merge block ~32 ~1 ~32 {name:"forest_4",mode:LOAD}


execute if score load_biome funcs matches 2 run say Switching to biome Flower Forest

execute if score load_biome funcs matches 2 run data merge block ~0 ~1 ~0 {name:"flower_forest_1",mode:LOAD}

execute if score load_biome funcs matches 2 run data merge block ~0 ~1 ~32 {name:"flower_forest_2",mode:LOAD}

execute if score load_biome funcs matches 2 run data merge block ~32 ~1 ~0 {name:"flower_forest_3",mode:LOAD}

execute if score load_biome funcs matches 2 run data merge block ~32 ~1 ~32 {name:"flower_forest_4",mode:LOAD}


execute if score load_biome funcs matches 3 run say Switching to biome Birch Forest

execute if score load_biome funcs matches 3 run data merge block ~0 ~1 ~0 {name:"birch_forest_1",mode:LOAD}

execute if score load_biome funcs matches 3 run data merge block ~0 ~1 ~32 {name:"birch_forest_2",mode:LOAD}

execute if score load_biome funcs matches 3 run data merge block ~32 ~1 ~0 {name:"birch_forest_3",mode:LOAD}

execute if score load_biome funcs matches 3 run data merge block ~32 ~1 ~32 {name:"birch_forest_4",mode:LOAD}


execute if score load_biome funcs matches 4 run say Switching to biome Dark Forest

execute if score load_biome funcs matches 4 run data merge block ~0 ~1 ~0 {name:"dark_forest_1",mode:LOAD}

execute if score load_biome funcs matches 4 run data merge block ~0 ~1 ~32 {name:"dark_forest_2",mode:LOAD}

execute if score load_biome funcs matches 4 run data merge block ~32 ~1 ~0 {name:"dark_forest_3",mode:LOAD}

execute if score load_biome funcs matches 4 run data merge block ~32 ~1 ~32 {name:"dark_forest_4",mode:LOAD}


execute if score load_biome funcs matches 5 run say Switching to biome Swamp

execute if score load_biome funcs matches 5 run data merge block ~0 ~1 ~0 {name:"swamp_1",mode:LOAD}

execute if score load_biome funcs matches 5 run data merge block ~0 ~1 ~32 {name:"swamp_2",mode:LOAD}

execute if score load_biome funcs matches 5 run data merge block ~32 ~1 ~0 {name:"swamp_3",mode:LOAD}

execute if score load_biome funcs matches 5 run data merge block ~32 ~1 ~32 {name:"swamp_4",mode:LOAD}


execute if score load_biome funcs matches 6 run say Switching to biome Jungle

execute if score load_biome funcs matches 6 run data merge block ~0 ~1 ~0 {name:"jungle_1",mode:LOAD}

execute if score load_biome funcs matches 6 run data merge block ~0 ~1 ~32 {name:"jungle_2",mode:LOAD}

execute if score load_biome funcs matches 6 run data merge block ~32 ~1 ~0 {name:"jungle_3",mode:LOAD}

execute if score load_biome funcs matches 6 run data merge block ~32 ~1 ~32 {name:"jungle_4",mode:LOAD}


execute if score load_biome funcs matches 7 run say Switching to biome Mushroom Field

execute if score load_biome funcs matches 7 run data merge block ~0 ~1 ~0 {name:"mushroom_field_1",mode:LOAD}

execute if score load_biome funcs matches 7 run data merge block ~0 ~1 ~32 {name:"mushroom_field_2",mode:LOAD}

execute if score load_biome funcs matches 7 run data merge block ~32 ~1 ~0 {name:"mushroom_field_3",mode:LOAD}

execute if score load_biome funcs matches 7 run data merge block ~32 ~1 ~32 {name:"mushroom_field_4",mode:LOAD}


execute if score load_biome funcs matches 8 run say Switching to biome Desert

execute if score load_biome funcs matches 8 run data merge block ~0 ~1 ~0 {name:"desert_1",mode:LOAD}

execute if score load_biome funcs matches 8 run data merge block ~0 ~1 ~32 {name:"desert_2",mode:LOAD}

execute if score load_biome funcs matches 8 run data merge block ~32 ~1 ~0 {name:"desert_3",mode:LOAD}

execute if score load_biome funcs matches 8 run data merge block ~32 ~1 ~32 {name:"desert_4",mode:LOAD}


execute if score load_biome funcs matches 9 run say Switching to biome Savanna

execute if score load_biome funcs matches 9 run data merge block ~0 ~1 ~0 {name:"savanna_1",mode:LOAD}

execute if score load_biome funcs matches 9 run data merge block ~0 ~1 ~32 {name:"savanna_2",mode:LOAD}

execute if score load_biome funcs matches 9 run data merge block ~32 ~1 ~0 {name:"savanna_3",mode:LOAD}

execute if score load_biome funcs matches 9 run data merge block ~32 ~1 ~32 {name:"savanna_4",mode:LOAD}


execute if score load_biome funcs matches 10 run say Switching to biome Badlands

execute if score load_biome funcs matches 10 run data merge block ~0 ~1 ~0 {name:"badlands_1",mode:LOAD}

execute if score load_biome funcs matches 10 run data merge block ~0 ~1 ~32 {name:"badlands_2",mode:LOAD}

execute if score load_biome funcs matches 10 run data merge block ~32 ~1 ~0 {name:"badlands_3",mode:LOAD}

execute if score load_biome funcs matches 10 run data merge block ~32 ~1 ~32 {name:"badlands_4",mode:LOAD}


execute if score load_biome funcs matches 11 run say Switching to biome Tiaga

execute if score load_biome funcs matches 11 run data merge block ~0 ~1 ~0 {name:"tiaga_1",mode:LOAD}

execute if score load_biome funcs matches 11 run data merge block ~0 ~1 ~32 {name:"tiaga_2",mode:LOAD}

execute if score load_biome funcs matches 11 run data merge block ~32 ~1 ~0 {name:"tiaga_3",mode:LOAD}

execute if score load_biome funcs matches 11 run data merge block ~32 ~1 ~32 {name:"tiaga_4",mode:LOAD}


execute if score load_biome funcs matches 12 run say Switching to biome Stone Shore

execute if score load_biome funcs matches 12 run data merge block ~0 ~1 ~0 {name:"stone_shore_1",mode:LOAD}

execute if score load_biome funcs matches 12 run data merge block ~0 ~1 ~32 {name:"stone_shore_2",mode:LOAD}

execute if score load_biome funcs matches 12 run data merge block ~32 ~1 ~0 {name:"stone_shore_3",mode:LOAD}

execute if score load_biome funcs matches 12 run data merge block ~32 ~1 ~32 {name:"stone_shore_4",mode:LOAD}


execute if score load_biome funcs matches 13 run say Switching to biome Snowy Tundra

execute if score load_biome funcs matches 13 run data merge block ~0 ~1 ~0 {name:"snowy_tundra_1",mode:LOAD}

execute if score load_biome funcs matches 13 run data merge block ~0 ~1 ~32 {name:"snowy_tundra_2",mode:LOAD}

execute if score load_biome funcs matches 13 run data merge block ~32 ~1 ~0 {name:"snowy_tundra_3",mode:LOAD}

execute if score load_biome funcs matches 13 run data merge block ~32 ~1 ~32 {name:"snowy_tundra_4",mode:LOAD}


execute if score load_biome funcs matches 14 run say Switching to biome Ice Spikes

execute if score load_biome funcs matches 14 run data merge block ~0 ~1 ~0 {name:"ice_spikes_1",mode:LOAD}

execute if score load_biome funcs matches 14 run data merge block ~0 ~1 ~32 {name:"ice_spikes_2",mode:LOAD}

execute if score load_biome funcs matches 14 run data merge block ~32 ~1 ~0 {name:"ice_spikes_3",mode:LOAD}

execute if score load_biome funcs matches 14 run data merge block ~32 ~1 ~32 {name:"ice_spikes_4",mode:LOAD}


execute if score load_biome funcs matches 15 run say Switching to biome Snowy Tiaga

execute if score load_biome funcs matches 15 run data merge block ~0 ~1 ~0 {name:"snowy_tiaga_1",mode:LOAD}

execute if score load_biome funcs matches 15 run data merge block ~0 ~1 ~32 {name:"snowy_tiaga_2",mode:LOAD}

execute if score load_biome funcs matches 15 run data merge block ~32 ~1 ~0 {name:"snowy_tiaga_3",mode:LOAD}

execute if score load_biome funcs matches 15 run data merge block ~32 ~1 ~32 {name:"snowy_tiaga_4",mode:LOAD}


execute if score load_biome funcs matches 16 run say Switching to biome Warm Ocean

execute if score load_biome funcs matches 16 run data merge block ~0 ~1 ~0 {name:"warm_ocean_1",mode:LOAD}

execute if score load_biome funcs matches 16 run data merge block ~0 ~1 ~32 {name:"warm_ocean_2",mode:LOAD}

execute if score load_biome funcs matches 16 run data merge block ~32 ~1 ~0 {name:"warm_ocean_3",mode:LOAD}

execute if score load_biome funcs matches 16 run data merge block ~32 ~1 ~32 {name:"warm_ocean_4",mode:LOAD}


execute if score load_biome funcs matches 17 run say Switching to biome Ocean

execute if score load_biome funcs matches 17 run data merge block ~0 ~1 ~0 {name:"ocean_1",mode:LOAD}

execute if score load_biome funcs matches 17 run data merge block ~0 ~1 ~32 {name:"ocean_2",mode:LOAD}

execute if score load_biome funcs matches 17 run data merge block ~32 ~1 ~0 {name:"ocean_3",mode:LOAD}

execute if score load_biome funcs matches 17 run data merge block ~32 ~1 ~32 {name:"ocean_4",mode:LOAD}


execute if score load_biome funcs matches 18 run say Switching to biome Frozen Ocean

execute if score load_biome funcs matches 18 run data merge block ~0 ~1 ~0 {name:"frozen_ocean_1",mode:LOAD}

execute if score load_biome funcs matches 18 run data merge block ~0 ~1 ~32 {name:"frozen_ocean_2",mode:LOAD}

execute if score load_biome funcs matches 18 run data merge block ~32 ~1 ~0 {name:"frozen_ocean_3",mode:LOAD}

execute if score load_biome funcs matches 18 run data merge block ~32 ~1 ~32 {name:"frozen_ocean_4",mode:LOAD}


execute if score load_biome funcs matches 19 run say Switching to biome The End

execute if score load_biome funcs matches 19 run data merge block ~0 ~1 ~0 {name:"the_end_1",mode:LOAD}

execute if score load_biome funcs matches 19 run data merge block ~0 ~1 ~32 {name:"the_end_2",mode:LOAD}

execute if score load_biome funcs matches 19 run data merge block ~32 ~1 ~0 {name:"the_end_3",mode:LOAD}

execute if score load_biome funcs matches 19 run data merge block ~32 ~1 ~32 {name:"the_end_4",mode:LOAD}


execute if score load_biome funcs matches 20 run say Switching to biome End Island

execute if score load_biome funcs matches 20 run data merge block ~0 ~1 ~0 {name:"end_island_1",mode:LOAD}

execute if score load_biome funcs matches 20 run data merge block ~0 ~1 ~32 {name:"end_island_2",mode:LOAD}

execute if score load_biome funcs matches 20 run data merge block ~32 ~1 ~0 {name:"end_island_3",mode:LOAD}

execute if score load_biome funcs matches 20 run data merge block ~32 ~1 ~32 {name:"end_island_4",mode:LOAD}


execute if score load_biome funcs matches 21 run say Switching to biome Nether

execute if score load_biome funcs matches 21 run data merge block ~0 ~1 ~0 {name:"nether_1",mode:LOAD}

execute if score load_biome funcs matches 21 run data merge block ~0 ~1 ~32 {name:"nether_2",mode:LOAD}

execute if score load_biome funcs matches 21 run data merge block ~32 ~1 ~0 {name:"nether_3",mode:LOAD}

execute if score load_biome funcs matches 21 run data merge block ~32 ~1 ~32 {name:"nether_4",mode:LOAD}


execute if score load_biome funcs matches 22 run say Switching to biome Mineshaft

execute if score load_biome funcs matches 22 run data merge block ~0 ~1 ~0 {name:"mineshaft_1",mode:LOAD}

execute if score load_biome funcs matches 22 run data merge block ~0 ~1 ~32 {name:"mineshaft_2",mode:LOAD}

execute if score load_biome funcs matches 22 run data merge block ~32 ~1 ~0 {name:"mineshaft_3",mode:LOAD}

execute if score load_biome funcs matches 22 run data merge block ~32 ~1 ~32 {name:"mineshaft_4",mode:LOAD}


execute if score load_biome funcs matches 23 run say Switching to biome Monument

execute if score load_biome funcs matches 23 run data merge block ~0 ~1 ~0 {name:"monument_1",mode:LOAD}

execute if score load_biome funcs matches 23 run data merge block ~0 ~1 ~32 {name:"monument_2",mode:LOAD}

execute if score load_biome funcs matches 23 run data merge block ~32 ~1 ~0 {name:"monument_3",mode:LOAD}

execute if score load_biome funcs matches 23 run data merge block ~32 ~1 ~32 {name:"monument_4",mode:LOAD}



setblock ~0 ~ ~0 redstone_torch
setblock ~0 ~ ~0 air

setblock ~0 ~ ~32 redstone_torch
setblock ~0 ~ ~32 air

setblock ~32 ~ ~0 redstone_torch
setblock ~32 ~ ~0 air

setblock ~32 ~ ~32 redstone_torch
setblock ~32 ~ ~32 air
