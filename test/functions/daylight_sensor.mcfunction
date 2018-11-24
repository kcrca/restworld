



execute unless score daylight_sensor funcs matches 0.. run function daylight_sensor_init
scoreboard players add daylight_sensor funcs 1
execute unless score daylight_sensor funcs matches 0..29 run scoreboard players set daylight_sensor funcs 0
execute if score daylight_sensor funcs matches 0 run time set 4400
execute if score daylight_sensor funcs matches 1 run time set 8000
execute if score daylight_sensor funcs matches 2 run time set 9200
execute if score daylight_sensor funcs matches 3 run time set 10000
execute if score daylight_sensor funcs matches 4 run time set 10400
execute if score daylight_sensor funcs matches 5 run time set 10800
execute if score daylight_sensor funcs matches 6 run time set 11100
execute if score daylight_sensor funcs matches 7 run time set 11600
execute if score daylight_sensor funcs matches 8 run time set 11900
execute if score daylight_sensor funcs matches 9 run time set 12100
execute if score daylight_sensor funcs matches 10 run time set 12300
execute if score daylight_sensor funcs matches 11 run time set 12600
execute if score daylight_sensor funcs matches 12 run time set 12800
execute if score daylight_sensor funcs matches 13 run time set 13100
execute if score daylight_sensor funcs matches 14 run time set 13400
execute if score daylight_sensor funcs matches 15 run time set 19000
execute if score daylight_sensor funcs matches 16 run time set 22500
execute if score daylight_sensor funcs matches 17 run time set 23000
execute if score daylight_sensor funcs matches 18 run time set 23100
execute if score daylight_sensor funcs matches 19 run time set 23400
execute if score daylight_sensor funcs matches 20 run time set 23600
execute if score daylight_sensor funcs matches 21 run time set 23800
execute if score daylight_sensor funcs matches 22 run time set 0
execute if score daylight_sensor funcs matches 23 run time set 300
execute if score daylight_sensor funcs matches 24 run time set 700
execute if score daylight_sensor funcs matches 25 run time set 1000
execute if score daylight_sensor funcs matches 26 run time set 1500
execute if score daylight_sensor funcs matches 27 run time set 2000
execute if score daylight_sensor funcs matches 28 run time set 2700
execute if score daylight_sensor funcs matches 29 run time set 3500

