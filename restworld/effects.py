from __future__ import annotations

from pynecraft.base import EAST, NORTH, SOUTH, WEST, as_facing, d, r
from pynecraft.commands import MAX_EFFECT_SECONDS, e, effect, execute, fill, function, p, setblock
from pynecraft.simpler import WallSign
from pynecraft.values import BAD_LUCK, EFFECT_GROUP, HERO_OF_THE_VILLAGE, effects
from restworld.rooms import ActionDesc, SignedRoom, Wall, span
from restworld.world import restworld

display_names = {
    BAD_LUCK: 'Bad Luck',
    HERO_OF_THE_VILLAGE: 'Hero|of the Village',
}


def _desc_for(effect):
    pos = effects[effect].positive
    return 'Positive' if pos else 'Negative' if pos is not None else None


actions = [ActionDesc(e, display_names.get(e, None), _desc_for(e)) for e in EFFECT_GROUP]
actions.sort()


def room():
    def effect_sign(action_desc, wall):
        dx, _, dz = as_facing(wall.facing).scale(1)
        return WallSign(action_desc.sign_text(), (
            setblock(d(-dx, 0, -dz), 'emerald_block'),
            effect().give(p(), action_desc.which, MAX_EFFECT_SECONDS)))

    wall_used = {4: span(2, 4), 3: span(1, 5), 2: span(2, 4)}
    room = SignedRoom('effects', restworld, SOUTH, (None, 'Mob Effects'), effect_sign, actions, (
        Wall(7, EAST, 1, -1, wall_used),
        Wall(7, SOUTH, 1, -7, wall_used),
        Wall(7, WEST, 7, -7, wall_used),
    ))
    room.reset_at((0, -6))

    # I could give this for only 30 seconds or so, because finding the 'off' sign is hard
    # with the negative effect visuals. But (a bug?) a few of the effects seem to interpret
    # 'seconds' as 'ticks', and 30 ticks is nothing. So instead I rely on the user being able
    # to find the 'off' button. Reexamine this if someone complains, maybe the bug will be
    # fixed then?
    room.function('effects_all').add(
        (effect().give(p(), x, MAX_EFFECT_SECONDS) for x in EFFECT_GROUP),
        execute().at(e().tag('effects_signs_home')).positioned(r(0, 1, 0)).run(
            function('restworld:effects/effects_all_shown')))
    effects_none = room.function('effects_none').add(
        effect().clear(p()),
        execute().at(e().tag('effects_signs_home')).run(
            fill(r(0, 2, 0), r(9, 7, -9), 'smooth_quartz').replace('emerald_block')))
    room.function('effects_none_exit').add(function(effects_none.full_name))
    room.function('effects_none_init').add(room.label(r(0, 2, 1), 'Effects Can Leave Room', NORTH))

    all_effects = WallSign((None, 'All Effects'), (None, function('restworld:effects/effects_all')))
    no_effects = WallSign((None, 'No Effects'), (None, function('restworld:effects/effects_none')))
    room.function('effects_global_init').add(
        all_effects.place(r(0, 6, 0), SOUTH),
        all_effects.place(r(0, 2, 0), SOUTH),
        no_effects.place(r(2, 6, 0), SOUTH),
        no_effects.place(r(2, 2, 0), SOUTH),
    )
    room.function('effects_signs_init').add(
        execute().positioned(r(0, 1, 0)).run(function('restworld:effects/signs')),
    )
