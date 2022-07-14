from __future__ import annotations

from pynecraft.base import r
from restworld.rooms import Room, label
from restworld.world import restworld


def room():
    room = Room('the_end', restworld)
    room.function('the_end_controls_init').add(label(r(1, 2, 0), 'Go Home'))
