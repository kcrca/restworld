from pynecraft.base import as_facing, d, MIDNIGHT, NOON, r, WEST
from pynecraft.commands import Block, data, e, Entity, execute, n, REPLACE, s, say, schedule, setblock, time
from restworld.rooms import kill_em, Room
from restworld.world import restworld


def room():
    room = Room('poses', restworld)

    def pose_funcs(mob, pose, facing, gap, create, remove):
        facing = as_facing(facing)
        placer = room.mob_placer(r(0, 2, 0), facing, adults=True, nbt={'NoAI': False})
        name = f'{mob}_{pose}'
        freeze = room.function(f'{name}_freeze', home=False).add(
            say(f'freeze {name}'),
            execute().as_(e().tag(name, room.name)).at(s()).run(remove),
            data().modify(n().tag(name, room.name), 'NoAI').set().value(True))
        room.function(f'{name}_init').add(
            kill_em(e().tag(name, room.name)),
            placer.summon(Entity(mob), tags=name),
            execute().as_(e().tag(name, room.name)).at(s()).run(create),
            schedule().function(freeze, gap, REPLACE)
        )

    def pose_target(mob, pose, facing, gap, target):
        name = f'{mob}_{pose}'
        pose_funcs(mob, pose, facing, gap, Entity(target).summon(d(0, 0, 5), {'Tags': [name, f'{name}_target']}),
                   kill_em(e().tag(f'{name}_target')))

    pose_target('cat', 'stalk', WEST, 15, 'rabbit')
    pose_funcs('villager', 'sleep', WEST, 30,
               (setblock(d(0, 0, 1), Block('green_bed', {'part': 'foot', 'facing': WEST})),
                setblock(d(0, 0, 2), Block('green_bed', {'part': 'head', 'facing': WEST})),
                time().set(MIDNIGHT)),
               time().set(NOON))
    pose_funcs('camel', 'sit', WEST, 30,
               data().modify(n().tag('camel_sit'), 'LastPoseTick').set().value(0),
               ())
