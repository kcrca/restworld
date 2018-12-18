kill @e[tag=which_fencelike_home]
execute at @e[tag=fencelike_home] run summon armor_stand ~1 ~ ~ {Tags:[walls_home,which_fencelike_home],Small:True,GravityOn:True}
execute at @e[tag=walls_home] run function v3:materials/walls_cur
