execute unless entity @e[type=minecraft:painting,nbt={Motive:wither}] run summon minecraft:painting ~1 ~3 ~1 {Motive:wither,Facing:3}
kill @e[type=item,type=painting]
