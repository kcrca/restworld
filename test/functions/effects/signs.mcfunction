kill @e[type=armor_stand,distance=..10]
summon minecraft:armor_stand ~1 ~0.5 ~-1 {Tags:[signer],Rotation:[90f,0f],ArmorItems:[{},{},{},{id:turtle_helmet,Count:1}]}
execute at @e[tag=signer] run fill ^0 ^0 ^0 ^-6 ^4 ^-6 air
execute at @e[tag=signer] run setblock ^-1 ^3 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Ambient Entity\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/ambient\"}}",Text3:"\"Effect\""}
execute at @e[tag=signer] run setblock ^-2 ^3 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Angry Villager\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/angry_villager\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^3 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Bubbles\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/bubbles\"}}",Text3:"\"and\"",Text4:"\"Whirlpools\""}
execute at @e[tag=signer] run setblock ^-4 ^3 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Clouds\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/clouds\"}}",Text3:"\"(Evaporation)\""}
execute at @e[tag=signer] run setblock ^-5 ^3 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Crit\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/crit\"}}"}
execute at @e[tag=signer] run setblock ^-1 ^2 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Damage Indicator\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/damage_indicator\"}}"}
execute at @e[tag=signer] run setblock ^-2 ^2 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Dolphin\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/dolphin\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^2 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Dragon Breath\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/dragon_breath\"}}"}
execute at @e[tag=signer] run setblock ^-4 ^2 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Dripping Lava\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/dripping_lava\"}}"}
execute at @e[tag=signer] run setblock ^-5 ^2 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Dripping Water\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/dripping_water\"}}"}
execute at @e[tag=signer] run setblock ^-1 ^1 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Dust\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/dust\"}}",Text3:"\"(Redstone Dust)\""}
execute at @e[tag=signer] run setblock ^-2 ^1 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Effect\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/effect\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^1 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Elder Guardian\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/elder_guardian\"}}"}
execute at @e[tag=signer] run setblock ^-4 ^1 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Enchant\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/enchant\"}}"}
execute at @e[tag=signer] run setblock ^-5 ^1 ^ wall_sign[facing=east]{Text2:"{\"text\":\"Enchanted Hit\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/enchanted_hit\"}}"}
execute as @e[tag=signer] run execute at @s run teleport @s ^-6 ^0 ^0 ~90 ~
execute at @e[tag=signer] run setblock ^-1 ^3 ^ wall_sign[facing=south]{Text2:"{\"text\":\"End Rod\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/end_rod\"}}"}
execute at @e[tag=signer] run setblock ^-2 ^3 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Entity Effect\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/entity_effect\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^3 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Explosion\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/explosion\"}}"}
execute at @e[tag=signer] run setblock ^-4 ^3 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Falling Dust\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/falling_dust\"}}"}
execute at @e[tag=signer] run setblock ^-5 ^3 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Fireworks\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/fireworks\"}}"}
execute at @e[tag=signer] run setblock ^-1 ^2 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Fishing\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/fishing\"}}"}
execute at @e[tag=signer] run setblock ^-2 ^2 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Flame\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/flame\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^2 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Happy Villager\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/happy_villager\"}}"}
execute at @e[tag=signer] run setblock ^-4 ^2 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Heart\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/heart\"}}"}
execute at @e[tag=signer] run setblock ^-5 ^2 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Explosion Emitter\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/explosion_emitter\"}}"}
execute at @e[tag=signer] run setblock ^-1 ^1 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Instant Effect\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/instant_effect\"}}"}
execute at @e[tag=signer] run setblock ^-2 ^1 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Item Slime\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/item_slime\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^1 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Item Snowball\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/item_snowball\"}}"}
execute at @e[tag=signer] run setblock ^-4 ^1 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Large Smoke\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/large_smoke\"}}"}
execute at @e[tag=signer] run setblock ^-5 ^1 ^ wall_sign[facing=south]{Text2:"{\"text\":\"Lava\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/lava\"}}"}
execute as @e[tag=signer] run execute at @s run teleport @s ^-6 ^0 ^0 ~90 ~
execute at @e[tag=signer] run setblock ^-1 ^3 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Mycelium\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/mycelium\"}}"}
execute at @e[tag=signer] run setblock ^-2 ^3 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Nautilus\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/nautilus\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^3 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Note\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/note\"}}"}
execute at @e[tag=signer] run setblock ^-4 ^3 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Poof\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/poof\"}}",Text3:"\"(Small Explosion)\""}
execute at @e[tag=signer] run setblock ^-5 ^3 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Portal\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/portal\"}}"}
execute at @e[tag=signer] run setblock ^-1 ^2 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Rain\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/rain\"}}"}
execute at @e[tag=signer] run setblock ^-2 ^2 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Smoke\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/smoke\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^2 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Snow\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/snow\"}}"}
execute at @e[tag=signer] run setblock ^-4 ^2 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Splash\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/splash\"}}"}
execute at @e[tag=signer] run setblock ^-5 ^2 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Squid Ink\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/squid_ink\"}}"}
execute at @e[tag=signer] run setblock ^-1 ^1 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Sweep Attack\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/sweep_attack\"}}"}
execute at @e[tag=signer] run setblock ^-2 ^1 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Totem of Undying\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/totem_of_undying\"}}"}
execute at @e[tag=signer] run setblock ^-3 ^1 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Underwater\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/underwater\"}}"}
execute at @e[tag=signer] run setblock ^-4 ^1 ^ wall_sign[facing=west]{Text2:"{\"text\":\"Witch\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"function allstuff:effects/witch\"}}"}
kill @e[type=armor_stand,distance=..10]