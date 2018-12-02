fill ~3 ~2 ~0 ~4 ~4 ~4 minecraft:air


execute unless score steppable funcs matches 0.. run function steppable_init
scoreboard players add steppable funcs 1
execute unless score steppable funcs matches 0..10 run scoreboard players set steppable funcs 0

execute if score steppable funcs matches 0 run setblock ~1 ~3 ~0 minecraft:sandstone
execute if score steppable funcs matches 0 run data merge block ~0 ~2 ~1 {Text2:"\"Sandstone\""}
execute if score steppable funcs matches 0 run setblock ~1 ~3 ~1 minecraft:sandstone_slab
execute if score steppable funcs matches 0 run setblock ~0 ~3 ~2 minecraft:sandstone_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 0 run setblock ~1 ~3 ~2 minecraft:sandstone_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 0 run setblock ~0 ~3 ~3 minecraft:sandstone_stairs[facing=east]
execute if score steppable funcs matches 0 run setblock ~1 ~4 ~3 minecraft:sandstone_slab[type=top]
execute if score steppable funcs matches 0 run setblock ~0 ~3 ~4 minecraft:sand

execute if score steppable funcs matches 0 run setblock ~4 ~3 ~0 minecraft:chiseled_sandstone
execute if score steppable funcs matches 0 run setblock ~3 ~2 ~0 minecraft:wall_sign[facing=west]{Text2:"\"Chiseled\""}
execute if score steppable funcs matches 0 run setblock ~4 ~3 ~2 minecraft:cut_sandstone
execute if score steppable funcs matches 0 run setblock ~3 ~2 ~2 minecraft:wall_sign[facing=west]{Text2:"\"Cut\""}
execute if score steppable funcs matches 0 run setblock ~4 ~3 ~4 minecraft:smooth_sandstone
execute if score steppable funcs matches 0 run setblock ~3 ~2 ~4 minecraft:wall_sign[facing=west]{Text2:"\"Smooth\""}



execute if score steppable funcs matches 1 run setblock ~1 ~3 ~0 minecraft:red_sandstone
execute if score steppable funcs matches 1 run data merge block ~0 ~2 ~1 {Text2:"\"Red Sandstone\""}
execute if score steppable funcs matches 1 run setblock ~1 ~3 ~1 minecraft:red_sandstone_slab
execute if score steppable funcs matches 1 run setblock ~0 ~3 ~2 minecraft:red_sandstone_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 1 run setblock ~1 ~3 ~2 minecraft:red_sandstone_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 1 run setblock ~0 ~3 ~3 minecraft:red_sandstone_stairs[facing=east]
execute if score steppable funcs matches 1 run setblock ~1 ~4 ~3 minecraft:red_sandstone_slab[type=top]
execute if score steppable funcs matches 1 run setblock ~0 ~3 ~4 minecraft:red_sand

execute if score steppable funcs matches 1 run setblock ~4 ~3 ~0 minecraft:chiseled_red_sandstone
execute if score steppable funcs matches 1 run setblock ~3 ~2 ~0 minecraft:wall_sign[facing=west]{Text2:"\"Chiseled\""}
execute if score steppable funcs matches 1 run setblock ~4 ~3 ~2 minecraft:cut_red_sandstone
execute if score steppable funcs matches 1 run setblock ~3 ~2 ~2 minecraft:wall_sign[facing=west]{Text2:"\"Cut\""}
execute if score steppable funcs matches 1 run setblock ~4 ~3 ~4 minecraft:smooth_red_sandstone
execute if score steppable funcs matches 1 run setblock ~3 ~2 ~4 minecraft:wall_sign[facing=west]{Text2:"\"Smooth\""}



execute if score steppable funcs matches 2 run setblock ~1 ~3 ~0 minecraft:quartz_block
execute if score steppable funcs matches 2 run data merge block ~0 ~2 ~1 {Text2:"\"Quartz\""}
execute if score steppable funcs matches 2 run setblock ~1 ~3 ~1 minecraft:quartz_slab
execute if score steppable funcs matches 2 run setblock ~0 ~3 ~2 minecraft:quartz_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 2 run setblock ~1 ~3 ~2 minecraft:quartz_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 2 run setblock ~0 ~3 ~3 minecraft:quartz_stairs[facing=east]
execute if score steppable funcs matches 2 run setblock ~1 ~4 ~3 minecraft:quartz_slab[type=top]
execute if score steppable funcs matches 2 run setblock ~0 ~3 ~4 minecraft:nether_quartz_ore

execute if score steppable funcs matches 2 run setblock ~4 ~3 ~0 minecraft:chiseled_quartz_block
execute if score steppable funcs matches 2 run setblock ~3 ~2 ~0 minecraft:wall_sign[facing=west]{Text2:"\"Chiseled\""}
execute if score steppable funcs matches 2 run setblock ~4 ~3 ~2 minecraft:quartz_pillar
execute if score steppable funcs matches 2 run setblock ~4 ~4 ~2 minecraft:quartz_pillar[axis=x]
execute if score steppable funcs matches 2 run setblock ~3 ~2 ~2 minecraft:wall_sign[facing=west]{Text2:"\"Pillar\""}
execute if score steppable funcs matches 2 run setblock ~4 ~3 ~4 minecraft:smooth_quartz
execute if score steppable funcs matches 2 run setblock ~3 ~2 ~4 minecraft:wall_sign[facing=west]{Text2:"\"Smooth\""}



execute if score steppable funcs matches 3 run setblock ~1 ~3 ~0 minecraft:cobblestone
execute if score steppable funcs matches 3 run data merge block ~0 ~2 ~1 {Text2:"\"Cobblestone\""}
execute if score steppable funcs matches 3 run setblock ~1 ~3 ~1 minecraft:cobblestone_slab
execute if score steppable funcs matches 3 run setblock ~0 ~3 ~2 minecraft:cobblestone_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 3 run setblock ~1 ~3 ~2 minecraft:cobblestone_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 3 run setblock ~0 ~3 ~3 minecraft:cobblestone_stairs[facing=east]
execute if score steppable funcs matches 3 run setblock ~1 ~4 ~3 minecraft:cobblestone_slab[type=top]
execute if score steppable funcs matches 3 run setblock ~0 ~3 ~4 minecraft:stone

execute if score steppable funcs matches 3 run setblock ~4 ~3 ~0 minecraft:mossy_cobblestone
execute if score steppable funcs matches 3 run setblock ~3 ~2 ~0 minecraft:wall_sign[facing=west]{Text2:"\"Mossy\""}
execute if score steppable funcs matches 3 run fill ~4 ~3 ~1 ~4 ~3 ~2 minecraft:mossy_cobblestone_wall
execute if score steppable funcs matches 3 run setblock ~3 ~2 ~2 minecraft:wall_sign[facing=west]{Text2:"\"Mossy Wall\""}
execute if score steppable funcs matches 3 run fill ~4 ~3 ~3 ~4 ~3 ~4 minecraft:cobblestone_wall
execute if score steppable funcs matches 3 run setblock ~3 ~2 ~4 minecraft:wall_sign[facing=west]{Text2:"\"Wall\""}



execute if score steppable funcs matches 4 run setblock ~1 ~3 ~0 minecraft:stone_bricks
execute if score steppable funcs matches 4 run data merge block ~0 ~2 ~1 {Text2:"\"Stone Brick\""}
execute if score steppable funcs matches 4 run setblock ~1 ~3 ~1 minecraft:stone_brick_slab
execute if score steppable funcs matches 4 run setblock ~0 ~3 ~2 minecraft:stone_brick_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 4 run setblock ~1 ~3 ~2 minecraft:stone_brick_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 4 run setblock ~0 ~3 ~3 minecraft:stone_brick_stairs[facing=east]
execute if score steppable funcs matches 4 run setblock ~1 ~4 ~3 minecraft:stone_brick_slab[type=top]
execute if score steppable funcs matches 4 run setblock ~0 ~3 ~4 minecraft:stone

execute if score steppable funcs matches 4 run setblock ~4 ~3 ~0 minecraft:chiseled_stone_bricks
execute if score steppable funcs matches 4 run setblock ~3 ~2 ~0 minecraft:wall_sign[facing=west]{Text2:"\"Chiseled\""}
execute if score steppable funcs matches 4 run setblock ~4 ~3 ~2 minecraft:cracked_stone_bricks
execute if score steppable funcs matches 4 run setblock ~3 ~2 ~2 minecraft:wall_sign[facing=west]{Text2:"\"Cracked\""}
execute if score steppable funcs matches 4 run setblock ~4 ~3 ~4 minecraft:mossy_stone_bricks
execute if score steppable funcs matches 4 run setblock ~3 ~2 ~4 minecraft:wall_sign[facing=west]{Text2:"\"Mossy\""}



execute if score steppable funcs matches 5 run setblock ~1 ~3 ~0 minecraft:nether_bricks
execute if score steppable funcs matches 5 run data merge block ~0 ~2 ~1 {Text2:"\"Nether Brick\""}
execute if score steppable funcs matches 5 run setblock ~1 ~3 ~1 minecraft:nether_brick_slab
execute if score steppable funcs matches 5 run setblock ~0 ~3 ~2 minecraft:nether_brick_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 5 run setblock ~1 ~3 ~2 minecraft:nether_brick_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 5 run setblock ~0 ~3 ~3 minecraft:nether_brick_stairs[facing=east]
execute if score steppable funcs matches 5 run setblock ~1 ~4 ~3 minecraft:nether_brick_slab[type=top]
execute if score steppable funcs matches 5 run setblock ~0 ~3 ~4 minecraft:netherrack

execute if score steppable funcs matches 5 run setblock ~4 ~3 ~0 minecraft:red_nether_bricks
execute if score steppable funcs matches 5 run setblock ~3 ~2 ~0 minecraft:wall_sign[facing=west]{Text2:"\"Red Nether Bricks\""}
execute if score steppable funcs matches 5 run fill ~4 ~3 ~2 ~4 ~3 ~4 minecraft:nether_brick_fence
execute if score steppable funcs matches 5 run setblock ~3 ~2 ~4 minecraft:wall_sign[facing=west]{Text2:"\"Nether Brick Fence\""}



execute if score steppable funcs matches 6 run setblock ~1 ~3 ~0 minecraft:bricks
execute if score steppable funcs matches 6 run data merge block ~0 ~2 ~1 {Text2:"\"Brick\""}
execute if score steppable funcs matches 6 run setblock ~1 ~3 ~1 minecraft:brick_slab
execute if score steppable funcs matches 6 run setblock ~0 ~3 ~2 minecraft:brick_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 6 run setblock ~1 ~3 ~2 minecraft:brick_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 6 run setblock ~0 ~3 ~3 minecraft:brick_stairs[facing=east]
execute if score steppable funcs matches 6 run setblock ~1 ~4 ~3 minecraft:brick_slab[type=top]
execute if score steppable funcs matches 6 run setblock ~0 ~3 ~4 minecraft:clay




execute if score steppable funcs matches 7 run setblock ~1 ~3 ~0 minecraft:purpur_block
execute if score steppable funcs matches 7 run data merge block ~0 ~2 ~1 {Text2:"\"Purpur\""}
execute if score steppable funcs matches 7 run setblock ~1 ~3 ~1 minecraft:purpur_slab
execute if score steppable funcs matches 7 run setblock ~0 ~3 ~2 minecraft:purpur_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 7 run setblock ~1 ~3 ~2 minecraft:purpur_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 7 run setblock ~0 ~3 ~3 minecraft:purpur_stairs[facing=east]
execute if score steppable funcs matches 7 run setblock ~1 ~4 ~3 minecraft:purpur_slab[type=top]
execute if score steppable funcs matches 7 run setblock ~0 ~3 ~4 minecraft:air

execute if score steppable funcs matches 7 run setblock ~4 ~3 ~2 minecraft:purpur_pillar
execute if score steppable funcs matches 7 run setblock ~4 ~4 ~2 minecraft:purpur_pillar[axis=x]
execute if score steppable funcs matches 7 run setblock ~3 ~2 ~2 minecraft:wall_sign[facing=west]{Text2:"\"Pillar\""}



execute if score steppable funcs matches 8 run setblock ~1 ~3 ~0 minecraft:prismarine
execute if score steppable funcs matches 8 run data merge block ~0 ~2 ~1 {Text2:"\"Prismarine\""}
execute if score steppable funcs matches 8 run setblock ~1 ~3 ~1 minecraft:prismarine_slab
execute if score steppable funcs matches 8 run setblock ~0 ~3 ~2 minecraft:prismarine_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 8 run setblock ~1 ~3 ~2 minecraft:prismarine_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 8 run setblock ~0 ~3 ~3 minecraft:prismarine_stairs[facing=east]
execute if score steppable funcs matches 8 run setblock ~1 ~4 ~3 minecraft:prismarine_slab[type=top]
execute if score steppable funcs matches 8 run setblock ~0 ~3 ~4 minecraft:air




execute if score steppable funcs matches 9 run setblock ~1 ~3 ~0 minecraft:prismarine_bricks
execute if score steppable funcs matches 9 run data merge block ~0 ~2 ~1 {Text2:"\"Prismarine Brick\""}
execute if score steppable funcs matches 9 run setblock ~1 ~3 ~1 minecraft:prismarine_brick_slab
execute if score steppable funcs matches 9 run setblock ~0 ~3 ~2 minecraft:prismarine_brick_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 9 run setblock ~1 ~3 ~2 minecraft:prismarine_brick_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 9 run setblock ~0 ~3 ~3 minecraft:prismarine_brick_stairs[facing=east]
execute if score steppable funcs matches 9 run setblock ~1 ~4 ~3 minecraft:prismarine_brick_slab[type=top]
execute if score steppable funcs matches 9 run setblock ~0 ~3 ~4 minecraft:air




execute if score steppable funcs matches 10 run setblock ~1 ~3 ~0 minecraft:dark_prismarine
execute if score steppable funcs matches 10 run data merge block ~0 ~2 ~1 {Text2:"\"Dark Prismarine\""}
execute if score steppable funcs matches 10 run setblock ~1 ~3 ~1 minecraft:dark_prismarine_slab
execute if score steppable funcs matches 10 run setblock ~0 ~3 ~2 minecraft:dark_prismarine_stairs[facing=south,shape=outer_left]
execute if score steppable funcs matches 10 run setblock ~1 ~3 ~2 minecraft:dark_prismarine_stairs[facing=south,shape=inner_left]
execute if score steppable funcs matches 10 run setblock ~0 ~3 ~3 minecraft:dark_prismarine_stairs[facing=east]
execute if score steppable funcs matches 10 run setblock ~1 ~4 ~3 minecraft:dark_prismarine_slab[type=top]
execute if score steppable funcs matches 10 run setblock ~0 ~3 ~4 minecraft:air