from __future__ import annotations

from restworld.rooms import Room
from restworld.world import restworld


def room():
    room = Room('the_end', restworld)
    room.function('the_end_controls_init')
