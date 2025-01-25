from pathlib import Path

from pynecraft.function import DataPack


def tests():
    tst = DataPack('tst')
    instances = tst.test_instance()
    instances['basic'] = {
        'type': 'minecraft:block_based',
        'structure': 'tst:basic',
        'environment': 'tst:default',
        'setup_ticks': 1,
        'max_ticks': 10,
    }
    tst.test_environment()['default'] = {
        "type": "minecraft:all_of",
        "definitions": [],
    }
    dir = f'{Path.home()}/clarity/home/saves/New World'
    if Path(dir).exists():
        tst.save(dir)
