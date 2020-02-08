scoreboard players add all_banners funcs 0
scoreboard players add banner_color funcs 0
scoreboard players add banner_ink funcs 0

tp @e[tag=banners] @e[tag=death,limit=1]


execute at @e[tag=all_banners_home] run function v3:banners/all_banners_init
