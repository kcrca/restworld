from restworld.world import restworld


def loot_tables():
    # This is used to get the player name so we can put their head on the armor stand in the models room. At least
    # as of 1.21, this was the only way to do this.
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
