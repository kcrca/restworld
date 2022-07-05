import amulet

level = amulet.load_level('/Applications/MultiMC.app/Data/instances/1.18.2/.minecraft/saves/New World')

chunk = level.get_chunk(0, 0, 'minecraft:overworld')

print(chunk)
