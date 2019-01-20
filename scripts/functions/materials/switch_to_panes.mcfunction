kill @e[tag=which_fencelike_home]
execute at @e[tag=fencelike_home] run summon armor_stand ~1 ~ ~ {Tags:[panes_home,which_fencelike_home],Small:True,GravityOn:True}
execute at @e[tag=panes_home] run function v3:materials/panes_cur
