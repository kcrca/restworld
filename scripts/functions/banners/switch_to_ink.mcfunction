kill @e[tag=banners_which]
execute at @e[tag=all_banners_home] positioned ~ ~-0.5 ~ run function v3:banners/banner_ink_home
tag @e[tag=banner_ink_home] add banners_which
