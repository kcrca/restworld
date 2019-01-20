execute at @e[tag=daylight_detector_setup_home] run function v3:redstone/daylight_detector_setup
fill ~3 ~8 ~3 ~-3 ~8 ~-3 minecraft:air


scoreboard players set daylight_detector max 30
execute unless score daylight_detector funcs matches 0..29 run scoreboard players operation daylight_detector funcs %= daylight_detector max

execute if score daylight_detector funcs matches 0 run execute if score daylight_inv funcs matches 0 run time set 8000

execute if score daylight_detector funcs matches 0 run execute if score daylight_inv funcs matches 1 run time set 22300
execute if score daylight_detector funcs matches 0 run execute if score daylight_inv funcs matches 1 run fill ~3 ~8 ~3 ~-3 ~8 ~-3 minecraft:stone


execute if score daylight_detector funcs matches 1 run execute if score daylight_inv funcs matches 0 run time set 9200

execute if score daylight_detector funcs matches 1 run execute if score daylight_inv funcs matches 1 run time set 22300
execute if score daylight_detector funcs matches 1 run execute if score daylight_inv funcs matches 1 run fill ~2 ~8 ~2 ~-2 ~8 ~-2 minecraft:stone


execute if score daylight_detector funcs matches 2 run execute if score daylight_inv funcs matches 0 run time set 10000

execute if score daylight_detector funcs matches 2 run execute if score daylight_inv funcs matches 1 run time set 22300
execute if score daylight_detector funcs matches 2 run execute if score daylight_inv funcs matches 1 run fill ~1 ~8 ~1 ~-1 ~8 ~-1 minecraft:stone


execute if score daylight_detector funcs matches 3 run execute if score daylight_inv funcs matches 0 run time set 10400

execute if score daylight_detector funcs matches 3 run execute if score daylight_inv funcs matches 1 run time set 22300
execute if score daylight_detector funcs matches 3 run execute if score daylight_inv funcs matches 1 run fill ~0 ~8 ~0 ~0 ~8 ~0 minecraft:stone


execute if score daylight_detector funcs matches 4 run execute if score daylight_inv funcs matches 0 run time set 10800

execute if score daylight_detector funcs matches 4 run execute if score daylight_inv funcs matches 1 run time set 22300


execute if score daylight_detector funcs matches 5 run execute if score daylight_inv funcs matches 0 run time set 11100

execute if score daylight_detector funcs matches 5 run execute if score daylight_inv funcs matches 1 run time set 22400


execute if score daylight_detector funcs matches 6 run execute if score daylight_inv funcs matches 0 run time set 11600

execute if score daylight_detector funcs matches 6 run execute if score daylight_inv funcs matches 1 run time set 22600


execute if score daylight_detector funcs matches 7 run execute if score daylight_inv funcs matches 0 run time set 11900

execute if score daylight_detector funcs matches 7 run execute if score daylight_inv funcs matches 1 run time set 22800


execute if score daylight_detector funcs matches 8 run execute if score daylight_inv funcs matches 0 run time set 12100

execute if score daylight_detector funcs matches 8 run execute if score daylight_inv funcs matches 1 run time set 22900


execute if score daylight_detector funcs matches 9 run execute if score daylight_inv funcs matches 0 run time set 12300

execute if score daylight_detector funcs matches 9 run execute if score daylight_inv funcs matches 1 run time set 23100


execute if score daylight_detector funcs matches 10 run execute if score daylight_inv funcs matches 0 run time set 12600

execute if score daylight_detector funcs matches 10 run execute if score daylight_inv funcs matches 1 run time set 23200


execute if score daylight_detector funcs matches 11 run execute if score daylight_inv funcs matches 0 run time set 12800

execute if score daylight_detector funcs matches 11 run execute if score daylight_inv funcs matches 1 run time set 23400


execute if score daylight_detector funcs matches 12 run execute if score daylight_inv funcs matches 0 run time set 13100

execute if score daylight_detector funcs matches 12 run execute if score daylight_inv funcs matches 1 run time set 23600


execute if score daylight_detector funcs matches 13 run execute if score daylight_inv funcs matches 0 run time set 13400

execute if score daylight_detector funcs matches 13 run execute if score daylight_inv funcs matches 1 run time set 23780


execute if score daylight_detector funcs matches 14 run execute if score daylight_inv funcs matches 0 run time set 19000

execute if score daylight_detector funcs matches 14 run execute if score daylight_inv funcs matches 1 run time set 23959


execute if score daylight_detector funcs matches 15 run execute if score daylight_inv funcs matches 0 run time set 22500

execute if score daylight_detector funcs matches 15 run execute if score daylight_inv funcs matches 1 run time set 23960


execute if score daylight_detector funcs matches 16 run execute if score daylight_inv funcs matches 0 run time set 23000

execute if score daylight_detector funcs matches 16 run execute if score daylight_inv funcs matches 1 run time set 23959


execute if score daylight_detector funcs matches 17 run execute if score daylight_inv funcs matches 0 run time set 23100

execute if score daylight_detector funcs matches 17 run execute if score daylight_inv funcs matches 1 run time set 23780


execute if score daylight_detector funcs matches 18 run execute if score daylight_inv funcs matches 0 run time set 23400

execute if score daylight_detector funcs matches 18 run execute if score daylight_inv funcs matches 1 run time set 23600


execute if score daylight_detector funcs matches 19 run execute if score daylight_inv funcs matches 0 run time set 23600

execute if score daylight_detector funcs matches 19 run execute if score daylight_inv funcs matches 1 run time set 23400


execute if score daylight_detector funcs matches 20 run execute if score daylight_inv funcs matches 0 run time set 23800

execute if score daylight_detector funcs matches 20 run execute if score daylight_inv funcs matches 1 run time set 23200


execute if score daylight_detector funcs matches 21 run execute if score daylight_inv funcs matches 0 run time set 0

execute if score daylight_detector funcs matches 21 run execute if score daylight_inv funcs matches 1 run time set 23100


execute if score daylight_detector funcs matches 22 run execute if score daylight_inv funcs matches 0 run time set 300

execute if score daylight_detector funcs matches 22 run execute if score daylight_inv funcs matches 1 run time set 22900


execute if score daylight_detector funcs matches 23 run execute if score daylight_inv funcs matches 0 run time set 700

execute if score daylight_detector funcs matches 23 run execute if score daylight_inv funcs matches 1 run time set 22800


execute if score daylight_detector funcs matches 24 run execute if score daylight_inv funcs matches 0 run time set 1000

execute if score daylight_detector funcs matches 24 run execute if score daylight_inv funcs matches 1 run time set 22600


execute if score daylight_detector funcs matches 25 run execute if score daylight_inv funcs matches 0 run time set 1500

execute if score daylight_detector funcs matches 25 run execute if score daylight_inv funcs matches 1 run time set 22400


execute if score daylight_detector funcs matches 26 run execute if score daylight_inv funcs matches 0 run time set 2000

execute if score daylight_detector funcs matches 26 run execute if score daylight_inv funcs matches 1 run time set 22300


execute if score daylight_detector funcs matches 27 run execute if score daylight_inv funcs matches 0 run time set 2700

execute if score daylight_detector funcs matches 27 run execute if score daylight_inv funcs matches 1 run time set 22300
execute if score daylight_detector funcs matches 27 run execute if score daylight_inv funcs matches 1 run fill ~0 ~8 ~0 ~0 ~8 ~0 minecraft:stone


execute if score daylight_detector funcs matches 28 run execute if score daylight_inv funcs matches 0 run time set 3500

execute if score daylight_detector funcs matches 28 run execute if score daylight_inv funcs matches 1 run time set 22300
execute if score daylight_detector funcs matches 28 run execute if score daylight_inv funcs matches 1 run fill ~1 ~8 ~1 ~-1 ~8 ~-1 minecraft:stone


execute if score daylight_detector funcs matches 29 run execute if score daylight_inv funcs matches 0 run time set 4400

execute if score daylight_detector funcs matches 29 run execute if score daylight_inv funcs matches 1 run time set 22300
execute if score daylight_detector funcs matches 29 run execute if score daylight_inv funcs matches 1 run fill ~2 ~8 ~2 ~-2 ~8 ~-2 minecraft:stone
