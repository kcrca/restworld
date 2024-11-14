from restworld.world import restworld


def loot_tables():
    tables = restworld.loot_table()
    tables['player_head'] = {
        "pools": [
            {
                "rolls": 1,
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": "minecraft:player_head",
                        "functions": [
                            {
                                "function": "minecraft:fill_player_head",
                                "entity": "this"
                            }
                        ]
                    }
                ]
            }
        ]
    }
