tp @e[tag=holder] @e[tag=death,limit=1]


summon donkey ~-3 ~1.5 ~0 {Tags:[holder],Variant:2,ChestedHorse:True,Tame:True,NoAI:True,Silent:True,Rotation:[180f,0f],Stringth:5}
summon minecraft:llama ~3 ~1.5 ~0 {Tags:[strength_llama,holder],Variant:2,ChestedHorse:True,Tame:True,NoAI:True,Silent:True,Rotation:[180f,0f],Strength:5}

summon minecraft:villager ~0 ~1.5 ~0 {Tags:[holder],gProfession:1,CareerLevel:100,NoAI:True,Silent:True,Rotation:[180f,0f],CanPickUpLoot:False,Offers:{Recipes:[{maxUses:10000,buy:{id:"minecraft:paper",Count:24b},sell:{id:"minecraft:emerald",Count:1},uses:0,rewardExp:True},{maxUses:10000,buyB:{id:"minecraft:emerald",Count:20b},buy:{id:"minecraft:book",Count:1},sell:{id:"minecraft:enchanted_book",Count:1,tag:{StoredEnchantments:[{lvl:2s,id:"minecraft:bane_of_arthropods"}]}},uses:0,rewardExp:True},{maxUses:10000,buyB:{id:"minecraft:emerald",Count:32b},buy:{id:"minecraft:book",Count:1},sell:{id:"minecraft:enchanted_book",Count:1,tag:{StoredEnchantments:[{lvl:2s,id:"minecraft:mending"}]}},uses:0,rewardExp:True}]}}