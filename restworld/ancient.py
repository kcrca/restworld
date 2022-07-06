from __future__ import annotations

from pyker.commands import r, NORTH
from restworld.rooms import Room
from restworld.world import restworld


def room():
    room = Room('ancient', restworld, NORTH, (None, 'Warden'))
    room.function('warden_init').add((room.mob_placer(r(0, 2, 0), NORTH, adults=True).summon('warden'),))
