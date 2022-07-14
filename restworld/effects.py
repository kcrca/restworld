from __future__ import annotations

from pyker.base import EAST, SOUTH, WEST, d, r, rotated_facing
from pyker.commands import MAX_EFFECT_SECONDS, e, effect, execute, fill, function, p, setblock
from pyker.enums import Effect
from pyker.simpler import WallSign
from restworld.rooms import ActionDesc, SignedRoom, Wall, label, span
from restworld.world import restworld

effect_note = {
    'Slowness': 'Negative',
    'Mining Fatigue': 'Negative',
    'Weakness': 'Negative',
    'Instant Damage': 'Negative',
    'Nausea': 'Negative',
    'Blindness': 'Negative',
    'Hunger': 'Negative',
    'Poison': 'Negative',
    'Wither': 'Negative',
    'Glowing': 'Neutral',
    'Levitation': 'Negative',
    'unluck': 'Negative',
    'Bad Omen': 'Negative',
}
display_names = {
    Effect.BAD_LUCK: 'Bad Luck',
    Effect.HERO_OF_THE_VILLAGE: 'Hero|of the Village',
}
effects = [ActionDesc(e, display_names.get(e, None), 'Negative' if Effect.negative(e) else None) for e in Effect]
effects.sort()


def room():
    def effect_sign(action_desc, wall):
        dx, _, dz = rotated_facing(wall.facing).scale(1)
        return WallSign(action_desc.sign_text(), (
            setblock(d(-dx, 0, -dz), 'emerald_block'),
            effect().give(p(), action_desc.enum, MAX_EFFECT_SECONDS)))

    wall_used = {4: span(2, 4), 3: span(1, 5), 2: span(2, 4)}
    room = SignedRoom('effects', restworld, SOUTH, (None, 'Mob Effects'), effect_sign, effects, (
        Wall(7, EAST, 1, -1, wall_used),
        Wall(7, SOUTH, 1, -7, wall_used),
        Wall(7, WEST, 7, -7, wall_used),
    ))

    # I could give this for only 30 seconds or so, because finding the 'off' sign is hard
    # with the negative effect visuals. But (a bug?) a few of the effects seem to interpret
    # 'seconds' as 'ticks', and 30 ticks is nothing. So instead I rely on the user being able
    # to find the 'off' button. Reexamine this if someone complains, maybe the bug will be
    # fixed then?
    room.function('effects_all').add(
        (effect().give(p(), x, MAX_EFFECT_SECONDS) for x in Effect),
        execute().at(e().tag('effects_signs_home')).positioned(r(0, 1, 0)).run(
            function('restworld:effects/effects_all_shown')))
    effects_none = room.function('effects_none').add(
        effect().clear(p()),
        execute().at(e().tag('effects_signs_home')).run(
            fill(r(0, 2, 0), r(9, 7, -9), 'smooth_quartz').replace('emerald_block')))
    room.function('effects_none_exit').add(function(effects_none.full_name))
    room.function('effects_none_init').add(label(r(0, 2, 1), 'Effects Can Leave Room'))

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
