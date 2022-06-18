from __future__ import annotations

from pyker.commands import NORTH, r, WEST
from pyker.function import Function
from restworld.rooms import Room
from restworld.world import restworld


def room():
    room = Room('ancient', restworld, NORTH, (None, 'Warden'))
    room.add(
        Function('warden_init').add((room.mob_placer(r(0, 2, 0), WEST, adults=True).summon('warden'),)),
    )