fill ~4 ~2 ~-1 ~3 ~2 ~-1 air
fill ~4 ~2 ~1 ~4 ~3 ~2 air
tp @e[tag=wood_boat] @e[tag=death,limit=1]





execute if score wood funcs matches 0 run setblock ~-4 ~2 ~0 minecraft:acacia_fence
execute if score wood funcs matches 0 run setblock ~-4 ~2 ~1 minecraft:acacia_fence_gate[facing=east]
execute if score wood funcs matches 0 run setblock ~-4 ~2 ~2 minecraft:acacia_fence_gate[in_wall=true,facing=east]
execute if score wood funcs matches 0 run fill ~-4 ~2 ~-1 ~-4 ~3 ~-1 minecraft:acacia_wood
execute if score wood funcs matches 0 run fill ~-4 ~2 ~-2 ~-4 ~4 ~-2 minecraft:air
execute if score wood funcs matches 0 run fill ~-4 ~4 ~-3 ~-2 ~4 ~-3 minecraft:acacia_leaves
execute if score wood funcs matches 0 run fill ~-3 ~2 ~-3 ~-3 ~3 ~-3 minecraft:acacia_log
execute if score wood funcs matches 0 run setblock ~-3 ~4 ~-3 minecraft:acacia_log[axis=z]
execute if score wood funcs matches 0 run setblock ~-2 ~2 ~-1 minecraft:acacia_sapling
execute if score wood funcs matches 0 run setblock ~0 ~2 ~-1 minecraft:acacia_sapling[stage=1]
execute if score wood funcs matches 0 run setblock ~-1 ~2 ~-3 minecraft:stripped_acacia_log
execute if score wood funcs matches 0 run setblock ~-1 ~3 ~-3 minecraft:stripped_acacia_log[axis=z]

execute if score wood funcs matches 0 run setblock ~4 ~2 ~-3 minecraft:acacia_slab[type=double]
execute if score wood funcs matches 0 run setblock ~4 ~2 ~-1 minecraft:acacia_door[facing=east,half=lower]
execute if score wood funcs matches 0 run setblock ~4 ~3 ~-1 minecraft:acacia_door[facing=east,half=upper]
execute if score wood funcs matches 0 run setblock ~3 ~2 ~0 minecraft:acacia_pressure_plate
execute if score wood funcs matches 0 run setblock ~3 ~2 ~1 minecraft:acacia_button[face=floor]
execute if score wood funcs matches 0 run setblock ~4 ~2 ~1 minecraft:acacia_door[facing=east,half=lower]
execute if score wood funcs matches 0 run setblock ~4 ~3 ~1 minecraft:acacia_door[facing=east,half=upper]
execute if score wood funcs matches 0 run setblock ~4 ~2 ~2 minecraft:acacia_door[facing=east,half=lower,hinge=right]
execute if score wood funcs matches 0 run setblock ~4 ~3 ~2 minecraft:acacia_door[facing=east,half=upper,hinge=right]
execute if score wood funcs matches 0 run summon minecraft:boat ~-0.5 ~1.525 ~2 {Type:acacia,CustomName:"\"Acacia\"",CustomNameVisible:True,Tags:[wood_boat],Rotation:[90f,0f]}

execute if score wood funcs matches 0 run setblock ~1 ~2 ~-3 minecraft:acacia_planks
execute if score wood funcs matches 0 run setblock ~1 ~3 ~-3 minecraft:acacia_slab
execute if score wood funcs matches 0 run setblock ~1 ~2 ~-2 minecraft:acacia_trapdoor[facing=south,open=true]
execute if score wood funcs matches 0 run setblock ~1 ~1 ~-1 minecraft:acacia_trapdoor[facing=east,open=true,half=top]
execute if score wood funcs matches 0 run setblock ~2 ~2 ~-2 minecraft:acacia_trapdoor[facing=south,open=false]
execute if score wood funcs matches 0 run setblock ~2 ~1 ~-1 minecraft:acacia_trapdoor[facing=west,open=false,half=top]
execute if score wood funcs matches 0 run fill ~4 ~2 ~-3 ~4 ~3 ~-3 minecraft:acacia_planks
execute if score wood funcs matches 0 run setblock ~2 ~2 ~-3 minecraft:acacia_stairs[facing=north]
execute if score wood funcs matches 0 run setblock ~3 ~2 ~-3 minecraft:acacia_stairs[facing=east,shape=inner_right]
execute if score wood funcs matches 0 run setblock ~3 ~2 ~-2 minecraft:acacia_stairs[facing=east,shape=outer_left]
execute if score wood funcs matches 0 run setblock ~4 ~2 ~-2 minecraft:acacia_stairs[facing=north]



execute if score wood funcs matches 1 run setblock ~-4 ~2 ~0 minecraft:birch_fence
execute if score wood funcs matches 1 run setblock ~-4 ~2 ~1 minecraft:birch_fence_gate[facing=east]
execute if score wood funcs matches 1 run setblock ~-4 ~2 ~2 minecraft:birch_fence_gate[in_wall=true,facing=east]
execute if score wood funcs matches 1 run fill ~-4 ~2 ~-1 ~-4 ~3 ~-1 minecraft:birch_wood
execute if score wood funcs matches 1 run fill ~-4 ~2 ~-2 ~-4 ~4 ~-2 minecraft:air
execute if score wood funcs matches 1 run fill ~-4 ~4 ~-3 ~-2 ~4 ~-3 minecraft:birch_leaves
execute if score wood funcs matches 1 run fill ~-3 ~2 ~-3 ~-3 ~3 ~-3 minecraft:birch_log
execute if score wood funcs matches 1 run setblock ~-3 ~4 ~-3 minecraft:birch_log[axis=z]
execute if score wood funcs matches 1 run setblock ~-2 ~2 ~-1 minecraft:birch_sapling
execute if score wood funcs matches 1 run setblock ~0 ~2 ~-1 minecraft:birch_sapling[stage=1]
execute if score wood funcs matches 1 run setblock ~-1 ~2 ~-3 minecraft:stripped_birch_log
execute if score wood funcs matches 1 run setblock ~-1 ~3 ~-3 minecraft:stripped_birch_log[axis=z]

execute if score wood funcs matches 1 run setblock ~4 ~2 ~-3 minecraft:birch_slab[type=double]
execute if score wood funcs matches 1 run setblock ~4 ~2 ~-1 minecraft:birch_door[facing=east,half=lower]
execute if score wood funcs matches 1 run setblock ~4 ~3 ~-1 minecraft:birch_door[facing=east,half=upper]
execute if score wood funcs matches 1 run setblock ~3 ~2 ~0 minecraft:birch_pressure_plate
execute if score wood funcs matches 1 run setblock ~3 ~2 ~1 minecraft:birch_button[face=floor]
execute if score wood funcs matches 1 run setblock ~4 ~2 ~1 minecraft:birch_door[facing=east,half=lower]
execute if score wood funcs matches 1 run setblock ~4 ~3 ~1 minecraft:birch_door[facing=east,half=upper]
execute if score wood funcs matches 1 run setblock ~4 ~2 ~2 minecraft:birch_door[facing=east,half=lower,hinge=right]
execute if score wood funcs matches 1 run setblock ~4 ~3 ~2 minecraft:birch_door[facing=east,half=upper,hinge=right]
execute if score wood funcs matches 1 run summon minecraft:boat ~-0.5 ~1.525 ~2 {Type:birch,CustomName:"\"Birch\"",CustomNameVisible:True,Tags:[wood_boat],Rotation:[90f,0f]}

execute if score wood funcs matches 1 run setblock ~1 ~2 ~-3 minecraft:birch_planks
execute if score wood funcs matches 1 run setblock ~1 ~3 ~-3 minecraft:birch_slab
execute if score wood funcs matches 1 run setblock ~1 ~2 ~-2 minecraft:birch_trapdoor[facing=south,open=true]
execute if score wood funcs matches 1 run setblock ~1 ~1 ~-1 minecraft:birch_trapdoor[facing=east,open=true,half=top]
execute if score wood funcs matches 1 run setblock ~2 ~2 ~-2 minecraft:birch_trapdoor[facing=south,open=false]
execute if score wood funcs matches 1 run setblock ~2 ~1 ~-1 minecraft:birch_trapdoor[facing=west,open=false,half=top]
execute if score wood funcs matches 1 run fill ~4 ~2 ~-3 ~4 ~3 ~-3 minecraft:birch_planks
execute if score wood funcs matches 1 run setblock ~2 ~2 ~-3 minecraft:birch_stairs[facing=north]
execute if score wood funcs matches 1 run setblock ~3 ~2 ~-3 minecraft:birch_stairs[facing=east,shape=inner_right]
execute if score wood funcs matches 1 run setblock ~3 ~2 ~-2 minecraft:birch_stairs[facing=east,shape=outer_left]
execute if score wood funcs matches 1 run setblock ~4 ~2 ~-2 minecraft:birch_stairs[facing=north]



execute if score wood funcs matches 2 run setblock ~-4 ~2 ~0 minecraft:jungle_fence
execute if score wood funcs matches 2 run setblock ~-4 ~2 ~1 minecraft:jungle_fence_gate[facing=east]
execute if score wood funcs matches 2 run setblock ~-4 ~2 ~2 minecraft:jungle_fence_gate[in_wall=true,facing=east]
execute if score wood funcs matches 2 run fill ~-4 ~2 ~-1 ~-4 ~3 ~-1 minecraft:jungle_wood
execute if score wood funcs matches 2 run fill ~-4 ~2 ~-2 ~-4 ~4 ~-2 minecraft:vine[north=true]
execute if score wood funcs matches 2 run fill ~-4 ~4 ~-3 ~-2 ~4 ~-3 minecraft:jungle_leaves
execute if score wood funcs matches 2 run fill ~-3 ~2 ~-3 ~-3 ~3 ~-3 minecraft:jungle_log
execute if score wood funcs matches 2 run setblock ~-3 ~4 ~-3 minecraft:jungle_log[axis=z]
execute if score wood funcs matches 2 run setblock ~-2 ~2 ~-1 minecraft:jungle_sapling
execute if score wood funcs matches 2 run setblock ~0 ~2 ~-1 minecraft:jungle_sapling[stage=1]
execute if score wood funcs matches 2 run setblock ~-1 ~2 ~-3 minecraft:stripped_jungle_log
execute if score wood funcs matches 2 run setblock ~-1 ~3 ~-3 minecraft:stripped_jungle_log[axis=z]

execute if score wood funcs matches 2 run setblock ~4 ~2 ~-3 minecraft:jungle_slab[type=double]
execute if score wood funcs matches 2 run setblock ~4 ~2 ~-1 minecraft:jungle_door[facing=east,half=lower]
execute if score wood funcs matches 2 run setblock ~4 ~3 ~-1 minecraft:jungle_door[facing=east,half=upper]
execute if score wood funcs matches 2 run setblock ~3 ~2 ~0 minecraft:jungle_pressure_plate
execute if score wood funcs matches 2 run setblock ~3 ~2 ~1 minecraft:jungle_button[face=floor]
execute if score wood funcs matches 2 run setblock ~4 ~2 ~1 minecraft:jungle_door[facing=east,half=lower]
execute if score wood funcs matches 2 run setblock ~4 ~3 ~1 minecraft:jungle_door[facing=east,half=upper]
execute if score wood funcs matches 2 run setblock ~4 ~2 ~2 minecraft:jungle_door[facing=east,half=lower,hinge=right]
execute if score wood funcs matches 2 run setblock ~4 ~3 ~2 minecraft:jungle_door[facing=east,half=upper,hinge=right]
execute if score wood funcs matches 2 run summon minecraft:boat ~-0.5 ~1.525 ~2 {Type:jungle,CustomName:"\"Jungle\"",CustomNameVisible:True,Tags:[wood_boat],Rotation:[90f,0f]}

execute if score wood funcs matches 2 run setblock ~1 ~2 ~-3 minecraft:jungle_planks
execute if score wood funcs matches 2 run setblock ~1 ~3 ~-3 minecraft:jungle_slab
execute if score wood funcs matches 2 run setblock ~1 ~2 ~-2 minecraft:jungle_trapdoor[facing=south,open=true]
execute if score wood funcs matches 2 run setblock ~1 ~1 ~-1 minecraft:jungle_trapdoor[facing=east,open=true,half=top]
execute if score wood funcs matches 2 run setblock ~2 ~2 ~-2 minecraft:jungle_trapdoor[facing=south,open=false]
execute if score wood funcs matches 2 run setblock ~2 ~1 ~-1 minecraft:jungle_trapdoor[facing=west,open=false,half=top]
execute if score wood funcs matches 2 run fill ~4 ~2 ~-3 ~4 ~3 ~-3 minecraft:jungle_planks
execute if score wood funcs matches 2 run setblock ~2 ~2 ~-3 minecraft:jungle_stairs[facing=north]
execute if score wood funcs matches 2 run setblock ~3 ~2 ~-3 minecraft:jungle_stairs[facing=east,shape=inner_right]
execute if score wood funcs matches 2 run setblock ~3 ~2 ~-2 minecraft:jungle_stairs[facing=east,shape=outer_left]
execute if score wood funcs matches 2 run setblock ~4 ~2 ~-2 minecraft:jungle_stairs[facing=north]



execute if score wood funcs matches 3 run setblock ~-4 ~2 ~0 minecraft:oak_fence
execute if score wood funcs matches 3 run setblock ~-4 ~2 ~1 minecraft:oak_fence_gate[facing=east]
execute if score wood funcs matches 3 run setblock ~-4 ~2 ~2 minecraft:oak_fence_gate[in_wall=true,facing=east]
execute if score wood funcs matches 3 run fill ~-4 ~2 ~-1 ~-4 ~3 ~-1 minecraft:oak_wood
execute if score wood funcs matches 3 run fill ~-4 ~2 ~-2 ~-4 ~4 ~-2 minecraft:air
execute if score wood funcs matches 3 run fill ~-4 ~4 ~-3 ~-2 ~4 ~-3 minecraft:oak_leaves
execute if score wood funcs matches 3 run fill ~-3 ~2 ~-3 ~-3 ~3 ~-3 minecraft:oak_log
execute if score wood funcs matches 3 run setblock ~-3 ~4 ~-3 minecraft:oak_log[axis=z]
execute if score wood funcs matches 3 run setblock ~-2 ~2 ~-1 minecraft:oak_sapling
execute if score wood funcs matches 3 run setblock ~0 ~2 ~-1 minecraft:oak_sapling[stage=1]
execute if score wood funcs matches 3 run setblock ~-1 ~2 ~-3 minecraft:stripped_oak_log
execute if score wood funcs matches 3 run setblock ~-1 ~3 ~-3 minecraft:stripped_oak_log[axis=z]

execute if score wood funcs matches 3 run setblock ~4 ~2 ~-3 minecraft:oak_slab[type=double]
execute if score wood funcs matches 3 run setblock ~4 ~2 ~-1 minecraft:oak_door[facing=east,half=lower]
execute if score wood funcs matches 3 run setblock ~4 ~3 ~-1 minecraft:oak_door[facing=east,half=upper]
execute if score wood funcs matches 3 run setblock ~3 ~2 ~0 minecraft:oak_pressure_plate
execute if score wood funcs matches 3 run setblock ~3 ~2 ~1 minecraft:oak_button[face=floor]
execute if score wood funcs matches 3 run setblock ~4 ~2 ~1 minecraft:oak_door[facing=east,half=lower]
execute if score wood funcs matches 3 run setblock ~4 ~3 ~1 minecraft:oak_door[facing=east,half=upper]
execute if score wood funcs matches 3 run setblock ~4 ~2 ~2 minecraft:oak_door[facing=east,half=lower,hinge=right]
execute if score wood funcs matches 3 run setblock ~4 ~3 ~2 minecraft:oak_door[facing=east,half=upper,hinge=right]
execute if score wood funcs matches 3 run summon minecraft:boat ~-0.5 ~1.525 ~2 {Type:oak,CustomName:"\"Oak\"",CustomNameVisible:True,Tags:[wood_boat],Rotation:[90f,0f]}

execute if score wood funcs matches 3 run setblock ~1 ~2 ~-3 minecraft:oak_planks
execute if score wood funcs matches 3 run setblock ~1 ~3 ~-3 minecraft:oak_slab
execute if score wood funcs matches 3 run setblock ~1 ~2 ~-2 minecraft:oak_trapdoor[facing=south,open=true]
execute if score wood funcs matches 3 run setblock ~1 ~1 ~-1 minecraft:oak_trapdoor[facing=east,open=true,half=top]
execute if score wood funcs matches 3 run setblock ~2 ~2 ~-2 minecraft:oak_trapdoor[facing=south,open=false]
execute if score wood funcs matches 3 run setblock ~2 ~1 ~-1 minecraft:oak_trapdoor[facing=west,open=false,half=top]
execute if score wood funcs matches 3 run fill ~4 ~2 ~-3 ~4 ~3 ~-3 minecraft:oak_planks
execute if score wood funcs matches 3 run setblock ~2 ~2 ~-3 minecraft:oak_stairs[facing=north]
execute if score wood funcs matches 3 run setblock ~3 ~2 ~-3 minecraft:oak_stairs[facing=east,shape=inner_right]
execute if score wood funcs matches 3 run setblock ~3 ~2 ~-2 minecraft:oak_stairs[facing=east,shape=outer_left]
execute if score wood funcs matches 3 run setblock ~4 ~2 ~-2 minecraft:oak_stairs[facing=north]



execute if score wood funcs matches 4 run setblock ~-4 ~2 ~0 minecraft:dark_oak_fence
execute if score wood funcs matches 4 run setblock ~-4 ~2 ~1 minecraft:dark_oak_fence_gate[facing=east]
execute if score wood funcs matches 4 run setblock ~-4 ~2 ~2 minecraft:dark_oak_fence_gate[in_wall=true,facing=east]
execute if score wood funcs matches 4 run fill ~-4 ~2 ~-1 ~-4 ~3 ~-1 minecraft:dark_oak_wood
execute if score wood funcs matches 4 run fill ~-4 ~2 ~-2 ~-4 ~4 ~-2 minecraft:air
execute if score wood funcs matches 4 run fill ~-4 ~4 ~-3 ~-2 ~4 ~-3 minecraft:dark_oak_leaves
execute if score wood funcs matches 4 run fill ~-3 ~2 ~-3 ~-3 ~3 ~-3 minecraft:dark_oak_log
execute if score wood funcs matches 4 run setblock ~-3 ~4 ~-3 minecraft:dark_oak_log[axis=z]
execute if score wood funcs matches 4 run setblock ~-2 ~2 ~-1 minecraft:dark_oak_sapling
execute if score wood funcs matches 4 run setblock ~0 ~2 ~-1 minecraft:dark_oak_sapling[stage=1]
execute if score wood funcs matches 4 run setblock ~-1 ~2 ~-3 minecraft:stripped_dark_oak_log
execute if score wood funcs matches 4 run setblock ~-1 ~3 ~-3 minecraft:stripped_dark_oak_log[axis=z]

execute if score wood funcs matches 4 run setblock ~4 ~2 ~-3 minecraft:dark_oak_slab[type=double]
execute if score wood funcs matches 4 run setblock ~4 ~2 ~-1 minecraft:dark_oak_door[facing=east,half=lower]
execute if score wood funcs matches 4 run setblock ~4 ~3 ~-1 minecraft:dark_oak_door[facing=east,half=upper]
execute if score wood funcs matches 4 run setblock ~3 ~2 ~0 minecraft:dark_oak_pressure_plate
execute if score wood funcs matches 4 run setblock ~3 ~2 ~1 minecraft:dark_oak_button[face=floor]
execute if score wood funcs matches 4 run setblock ~4 ~2 ~1 minecraft:dark_oak_door[facing=east,half=lower]
execute if score wood funcs matches 4 run setblock ~4 ~3 ~1 minecraft:dark_oak_door[facing=east,half=upper]
execute if score wood funcs matches 4 run setblock ~4 ~2 ~2 minecraft:dark_oak_door[facing=east,half=lower,hinge=right]
execute if score wood funcs matches 4 run setblock ~4 ~3 ~2 minecraft:dark_oak_door[facing=east,half=upper,hinge=right]
execute if score wood funcs matches 4 run summon minecraft:boat ~-0.5 ~1.525 ~2 {Type:dark_oak,CustomName:"\"Dark Oak\"",CustomNameVisible:True,Tags:[wood_boat],Rotation:[90f,0f]}

execute if score wood funcs matches 4 run setblock ~1 ~2 ~-3 minecraft:dark_oak_planks
execute if score wood funcs matches 4 run setblock ~1 ~3 ~-3 minecraft:dark_oak_slab
execute if score wood funcs matches 4 run setblock ~1 ~2 ~-2 minecraft:dark_oak_trapdoor[facing=south,open=true]
execute if score wood funcs matches 4 run setblock ~1 ~1 ~-1 minecraft:dark_oak_trapdoor[facing=east,open=true,half=top]
execute if score wood funcs matches 4 run setblock ~2 ~2 ~-2 minecraft:dark_oak_trapdoor[facing=south,open=false]
execute if score wood funcs matches 4 run setblock ~2 ~1 ~-1 minecraft:dark_oak_trapdoor[facing=west,open=false,half=top]
execute if score wood funcs matches 4 run fill ~4 ~2 ~-3 ~4 ~3 ~-3 minecraft:dark_oak_planks
execute if score wood funcs matches 4 run setblock ~2 ~2 ~-3 minecraft:dark_oak_stairs[facing=north]
execute if score wood funcs matches 4 run setblock ~3 ~2 ~-3 minecraft:dark_oak_stairs[facing=east,shape=inner_right]
execute if score wood funcs matches 4 run setblock ~3 ~2 ~-2 minecraft:dark_oak_stairs[facing=east,shape=outer_left]
execute if score wood funcs matches 4 run setblock ~4 ~2 ~-2 minecraft:dark_oak_stairs[facing=north]



execute if score wood funcs matches 5 run setblock ~-4 ~2 ~0 minecraft:spruce_fence
execute if score wood funcs matches 5 run setblock ~-4 ~2 ~1 minecraft:spruce_fence_gate[facing=east]
execute if score wood funcs matches 5 run setblock ~-4 ~2 ~2 minecraft:spruce_fence_gate[in_wall=true,facing=east]
execute if score wood funcs matches 5 run fill ~-4 ~2 ~-1 ~-4 ~3 ~-1 minecraft:spruce_wood
execute if score wood funcs matches 5 run fill ~-4 ~2 ~-2 ~-4 ~4 ~-2 minecraft:air
execute if score wood funcs matches 5 run fill ~-4 ~4 ~-3 ~-2 ~4 ~-3 minecraft:spruce_leaves
execute if score wood funcs matches 5 run fill ~-3 ~2 ~-3 ~-3 ~3 ~-3 minecraft:spruce_log
execute if score wood funcs matches 5 run setblock ~-3 ~4 ~-3 minecraft:spruce_log[axis=z]
execute if score wood funcs matches 5 run setblock ~-2 ~2 ~-1 minecraft:spruce_sapling
execute if score wood funcs matches 5 run setblock ~0 ~2 ~-1 minecraft:spruce_sapling[stage=1]
execute if score wood funcs matches 5 run setblock ~-1 ~2 ~-3 minecraft:stripped_spruce_log
execute if score wood funcs matches 5 run setblock ~-1 ~3 ~-3 minecraft:stripped_spruce_log[axis=z]

execute if score wood funcs matches 5 run setblock ~4 ~2 ~-3 minecraft:spruce_slab[type=double]
execute if score wood funcs matches 5 run setblock ~4 ~2 ~-1 minecraft:spruce_door[facing=east,half=lower]
execute if score wood funcs matches 5 run setblock ~4 ~3 ~-1 minecraft:spruce_door[facing=east,half=upper]
execute if score wood funcs matches 5 run setblock ~3 ~2 ~0 minecraft:spruce_pressure_plate
execute if score wood funcs matches 5 run setblock ~3 ~2 ~1 minecraft:spruce_button[face=floor]
execute if score wood funcs matches 5 run setblock ~4 ~2 ~1 minecraft:spruce_door[facing=east,half=lower]
execute if score wood funcs matches 5 run setblock ~4 ~3 ~1 minecraft:spruce_door[facing=east,half=upper]
execute if score wood funcs matches 5 run setblock ~4 ~2 ~2 minecraft:spruce_door[facing=east,half=lower,hinge=right]
execute if score wood funcs matches 5 run setblock ~4 ~3 ~2 minecraft:spruce_door[facing=east,half=upper,hinge=right]
execute if score wood funcs matches 5 run summon minecraft:boat ~-0.5 ~1.525 ~2 {Type:spruce,CustomName:"\"Spruce\"",CustomNameVisible:True,Tags:[wood_boat],Rotation:[90f,0f]}

execute if score wood funcs matches 5 run setblock ~1 ~2 ~-3 minecraft:spruce_planks
execute if score wood funcs matches 5 run setblock ~1 ~3 ~-3 minecraft:spruce_slab
execute if score wood funcs matches 5 run setblock ~1 ~2 ~-2 minecraft:spruce_trapdoor[facing=south,open=true]
execute if score wood funcs matches 5 run setblock ~1 ~1 ~-1 minecraft:spruce_trapdoor[facing=east,open=true,half=top]
execute if score wood funcs matches 5 run setblock ~2 ~2 ~-2 minecraft:spruce_trapdoor[facing=south,open=false]
execute if score wood funcs matches 5 run setblock ~2 ~1 ~-1 minecraft:spruce_trapdoor[facing=west,open=false,half=top]
execute if score wood funcs matches 5 run fill ~4 ~2 ~-3 ~4 ~3 ~-3 minecraft:spruce_planks
execute if score wood funcs matches 5 run setblock ~2 ~2 ~-3 minecraft:spruce_stairs[facing=north]
execute if score wood funcs matches 5 run setblock ~3 ~2 ~-3 minecraft:spruce_stairs[facing=east,shape=inner_right]
execute if score wood funcs matches 5 run setblock ~3 ~2 ~-2 minecraft:spruce_stairs[facing=east,shape=outer_left]
execute if score wood funcs matches 5 run setblock ~4 ~2 ~-2 minecraft:spruce_stairs[facing=north]