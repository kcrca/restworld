from pynecraft.base import EAST, Nbt, SOUTH, d, good_facing, r
from pynecraft.commands import Entity, FURTHEST, INT, RESULT, data, e, execute, function, kill, s, say, setblock, \
    summon, tag, tp
from pynecraft.simpler import Item, Offset
from restworld.rooms import Room
from restworld.world import restworld

"""
Setup:
Mark the starting point, at a known distance below the NW corner (the lowest coordinate values) with an armor stand (say).
These can all have the same tag, so we can use "execute as" commands and hit every room. These must below the lowest
Y we want to save.

Starting point has
    command block that summons armor stand
    some standard block that can be flickered with redstone blocks to (re-)summon the stand
    structure block with the room name set, placed where it can easily encompass an entre room
    some standard block that can be flickered with redstone blocks to (re-)trigger the structure block

For the largest rooms, we need two of these starting points.

Marker blocks at SE and SW corners at floor level.

Basic functions:

To do this in one set of code, names of the armor_stands, etc. must be shared. (Alternative would be to embed this in the per-room
functions.) So this is done in a sequential way: To kick things off:

    Clear all existing 'active' tags (just in case)
    All starting point armor stands have a 'pending' tag applied.
    The 'next' function is invoked:
        start the 'save' function at a (random?) single 'pending' stand.
        (This naturally ends the overall loop when none are left.)

Save:
    remove the 'pending' tag from our stand
    add the 'active' tag to our stand; this is used to identify the home base of all the save action for a single room.
    Set structure block to SAVE block with "save entities" on.
    Summon armor stand at floor level, facing S
    Move it forward until it hits marker block at SW corner
    Turn it to face west
    Move it forward until it hits marker block at SE corner
    Calculate size
        copy X and Z coords into scores
        subtract x and Z coords from marker armor stand
        adjust x and z (if needed)
        set width and depth in structure block
            seems to require setting it somewhere else first, like storage
        set height to known fixed value
        (set width and height in the 'in room' detection too)
        [Note: Can't see how to trigger size detection using corners or I'd use them.]
    Trigger DETECT in SAVE block
    flash redstone block to save
    Cleanup:
        Remove CORNER and kill armor stand
        Set structure block to CORNER (the safest block)
        Clear the 'active' tag from our stand
        call the 'next' function

Validate:
    All the above without the cleanup. This lets you see what it _would_ save to debug the system

Show area:
    Set structure block to LOAD block with borders enabled

Load area:
    Set structure block to LOAD block with "load entites" on and borders off
    flash redstone block to load
"""

MARKER = 'verdant_froglight'
MAX_STEPS = 150
SAVE_HEIGHT = 25


def room():
    room = Room('save', restworld)

    x = room.score('x')
    z = room.score('z')
    step_num = room.score('step')
    found = room.score('found')
    saved = room.score('saved')

    helmet = Item.nbt_for('turtle_helmet')
    detector_stand = Entity('armor_stand',
                            dict(Rotation=good_facing(EAST).rotation, Small=True, NoGravity=True,
                                 ArmorItems=[{}, {}, {}, helmet])).tag('save_detector')
    block_nbt = Nbt(sizeY=SAVE_HEIGHT, posX=0, posY=1, posZ=-1, ignoreEntities=False)

    all_detectors = e().tag('save_detector')
    detector = all_detectors.limit(1)
    savers = e().tag('save_home')
    active = e().tag('save_active').limit(1)

    block_pos = r(0, -1, 1)
    redstone_pos = Offset(0, -1, 0).r(*block_pos)
    prep = room.function('prep', home=False).add(
        execute().store(RESULT).storage('save_start', f'sizeX', INT, 1).run(x.get()),
        execute().store(RESULT).storage('save_start', f'sizeZ', INT, 1).run(z.get()),
        data().modify(block_pos, 'sizeX').set().from_('save_start', 'sizeX'),
        data().modify(block_pos, 'sizeZ').set().from_('save_start', 'sizeZ'),
        data().merge(block_pos, block_nbt.merge({'mode': 'SAVE', 'showboundingbox': True})),
    )

    as_detector = execute().as_(detector).at(detector)
    step = room.function('step', home=False)
    step.add(
        as_detector.run(tp(s(), d(0, 0, 1))),
        step_num.add(1),
        execute().if_().score(found).matches(0).run(x.add(1)),
        execute().if_().score(found).matches(1).run(z.add(1)),
        as_detector.if_().block(r(0, 0, 0), MARKER).run(
            data().merge(s(), {'Rotation': good_facing(SOUTH).rotation}),
            found.add(1),
        ),
        execute().if_().score(step_num).matches((MAX_STEPS, None)).run(say("NO END FOUND")),
        execute().unless().score(step_num).matches((MAX_STEPS, None)).if_().score(found).matches(2).as_(
            active).at(active).run(function(prep)),
        execute().unless().score(step_num).matches((MAX_STEPS, None)).unless().score(found).matches(2).run(
            function(step)),
    )
    setup = room.function('setup', home=False).add(
        execute().unless().block(block_pos, 'structure_block').run(say("NO STRUCTURE BLOCK")),
        saved.add(1),
        kill(all_detectors),
        tag(e().tag('save_active')).remove('save_active'),
        tag(s()).add('save_active'),
        summon(detector_stand, r(0, 7, 0)),
        step_num.set(0),
        x.set(1),
        z.set(1),
        found.set(0),
        function(step),
        tag(s()).remove('save_active'),
    )

    setup_all = room.function('setup_all', home=False).add(
        kill(all_detectors),
        tag(e().tag('save_active')).remove('save_active'),
        saved.set(0),
        execute().as_(savers.sort(FURTHEST)).run(execute().as_(s()).at(s()).run(function(setup))),
    )

    save = room.function('save').add(
        setblock(redstone_pos, 'redstone_block'),
        setblock(redstone_pos, 'shroomlight'),
    )

    room.function('save_all', home=False).add(
        function(setup_all),
        execute().as_(savers.sort(FURTHEST)).run(execute().as_(s()).at(s()).run(function(setup))),
        execute().as_(savers.sort(FURTHEST)).run(execute().as_(s()).at(s()).run(function(save))),
    )

    home = room.function('save_home', exists_ok=True)
    commands = home.commands()
    for i in range(len(commands)):
        if commands[i].startswith('kill'):
            del commands[i]
            break
