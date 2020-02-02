tp @e[tag=villager] @e[tag=death,limit=1]




summon minecraft:zombie_villager ~-2 ~2 ~-6 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:armorer},CustomName:"\"Armorer\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~-2 ~2 ~-4 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:butcher},CustomName:"\"Butcher\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~-2 ~2 ~-2 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:cartographer},CustomName:"\"Cartographer\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~-2 ~2 ~0 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:cleric},CustomName:"\"Cleric\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~-2 ~2 ~2 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:farmer},CustomName:"\"Farmer\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~-2 ~2 ~4 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:fisherman},CustomName:"\"Fisherman\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~-2 ~2 ~6 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:fletcher},CustomName:"\"Fletcher\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
	

summon minecraft:zombie_villager ~0 ~2 ~-7 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:leatherworker},CustomName:"\"Leatherworker\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~0 ~2 ~-5 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:librarian},CustomName:"\"Librarian\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~0 ~2 ~-3 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:mason},CustomName:"\"Mason\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~0 ~2 ~-1 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:nitwit},CustomName:"\"Nitwit\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~0 ~2 ~1 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:shepherd},CustomName:"\"Shepherd\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~0 ~2 ~3 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:toolsmith},CustomName:"\"Toolsmith\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~0 ~2 ~5 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:weaponsmith},CustomName:"\"Weaponsmith\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}
summon minecraft:zombie_villager ~0 ~2 ~7 {Tags:[zombie_villager,friendlies,villager,friendlies],VillagerData:{profession:unemployed},CustomName:"\"Unemployed\"",PersistenceRequired:True,NoAI:True,Silent:True,Rotation:[90f,0f]}

function v3:friendlies/villager_professions_cur

setblock ~-5 ~2 ~0 oak_wall_sign[facing=west]
data modify block ~-5 ~2 ~0 Text3 set value "\"Zombie Villagers\""
