from __future__ import annotations

from restworld import ancient, global_, aquatic, arena, banners, biomes
from restworld.world import restworld


def main():
    for f in (ancient.room, global_.room, aquatic.room, arena.room, banners.room, biomes.room):
        f()
    restworld.save()


if __name__ == '__main__':
    main()
