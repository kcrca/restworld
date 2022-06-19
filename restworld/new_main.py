from __future__ import annotations

from restworld import ancient, global_, aquatic, arena, banners, biomes, tags, blocks
from restworld.world import restworld


def main():
    for f in (ancient.room, global_.room, aquatic.room, arena.room, banners.room, biomes.room, blocks.room):
        f()
    tags.tags()
    restworld.save()


if __name__ == '__main__':
    main()
