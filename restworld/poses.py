from pynecraft.base import as_facing, d, EAST, MIDNIGHT, NOON, r, WEST
from pynecraft.commands import as_entity, Block, data, e, Entity, execute, n, p, REPLACE, s, say, \
    schedule, \
    setblock, \
    tag, tellraw, time
from restworld.rooms import kill_em, Room
from restworld.world import restworld


def room():
    room = Room('poses', restworld)

    def pose_funcs(mob, pose, facing, gap, create, remove):
        mob = as_entity(mob)
        facing = as_facing(facing)
        placer = room.mob_placer(r(0, 2, 0), facing, adults=True, nbt={'NoAI': False})
        name = f'{mob.id}_{pose}'
        freeze = room.function(f'{name}_freeze', home=False).add(
            say(f'freeze {name}'),
            execute().as_(e().tag(name, room.name)).at(s()).run(remove),
            data().modify(n().tag(name, room.name), 'NoAI').set().value(True))
        room.function(f'{name}_init').add(
            kill_em(e().tag(name, room.name)),
            placer.summon(mob, tags=name),
            execute().as_(e().tag(name, room.name)).at(s()).run(create),
            schedule().function(freeze, gap, REPLACE)
        )

    def pose_target(mob, pose, facing, gap, target):
        mob = as_entity(mob)
        name = f'{mob.id}_{pose}'
        pose_funcs(mob, pose, facing, gap, Entity(target).summon(d(0, 0, 5), {'Tags': [name, f'{name}_target']}),
                   kill_em(e().tag(f'{name}_target')))

    pose_target('cat', 'stalk', WEST, 15, 'rabbit')
    pose_funcs('villager', 'sleep', WEST, 30,
               (setblock(d(0, 0, 0), Block('green_bed', {'part': 'head', 'facing': EAST})),
                setblock(d(0, 0, 1), Block('green_bed', {'part': 'foot', 'facing': EAST})),
                time().set(MIDNIGHT)),
               time().set(NOON))
    pose_funcs('camel', 'sit', WEST, 30,
               data().modify(n().tag('camel_sit'), 'LastPoseTick').set().value(0),
               ())

    pose_funcs(Entity('cat', {'Tame': True}), 'sleep', WEST, 90,
               (setblock(d(0, 0, 0), Block('green_bed', {'part': 'head', 'facing': EAST})),
                setblock(d(0, 0, 1), Block('green_bed', {'part': 'foot', 'facing': EAST})),
                tag(n().tag('cat_sleep')).add('cat_sleep_wait'),
                data().modify(n().tag('cat_sleep'), 'Owner').set().from_(p(), 'UUID'),
                time().set(MIDNIGHT),
                tellraw(p(), 'Now sleep in the bed!'),
                ),
               (time().set(NOON)))
