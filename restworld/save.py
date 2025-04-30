from pynecraft.base import Arg, r
from pynecraft.commands import Block, Entity, e, execute, fill, function, kill, n, p, say, setblock, \
    tp
from restworld.rooms import Room
from restworld.world import restworld

"""
Functions for helping capture biome samples from a real world, not used in Restworld itself. But this is a convenient
place to put them.

How to use:

First, find an example of a biome you want to use. Find the corner of the sample area that has the lowest value (x,z)
coordinates. Go underground and place a command block with "function restworld:save/prep {name: plains}".
Trigger that block with a button. This will place four armor stands at the corners of the four segments of the biome
sample with structure blocks above them with the right names in them (e.g., "plains_2").

Go up and make sure the sample is the one you want. You can move that command block around. When you re-run the function,
it will first clean up the existing armor stands and structure blocks.

When you have the sample positioned correctly, run the function "/function restworld:save/next". This will take you to
each structure block in turn. "SAVE" each one. (Currently there is no way to automate a save command, you have to do it
manually, hence the function that moves you to each in turn.) When you've done the final one, the .nbt files will be
in your world's "generated/minecraft/structures" directory. They need to be coped to the restworld structure folder.

Some samples require a two-high space, for a total of eight structure blocks. To get this, set the score "tall save" 
to 1. Then it will create the eight structure blocks, and "next" will take you to all eight, starting with the 
uppermost layer. Saving the lower blocks requires removing the upper ones, so if you need to start over, you'll need 
to re-"prep" the sample. WHich is probably a good idea anyway.

The function restworld:save/start resets the loop to the beginning, and restworld:save/remove removes the armor stands
and structure blocks. Both these functions are run during "prep", so if you move the command block, you only need to
invoke it again.
 
"""

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
    Set structure block to LOAD block with "load entities" on and borders off
    flash redstone block to load
"""

MARKER = 'verdant_froglight'
MAX_STEPS = 150
SAVE_HEIGHT = 25


def room():
    room = Room('save', restworld)

    tall = room.score('tall')
    segments = (r(0, 0.5, 0), r(0, 0.5, 32), r(32, 0.5, 0), r(32, 0.5, 32))
    count = len(segments)

    remove = room.function('remove', home=False).add(
        execute().at(e().tag(Arg('name'))).run(
            fill(r(0, 2, 0), r(0, 2, 0), 'air').destroy(),
            setblock(r(0, 34, 0), 'air')),
        kill(e().tag(Arg('name'))),
    )

    def next_loop(step):
        if step.i < count:
            yield say(step.i + 5)
            yield execute().as_(e().tag(f'saver_{step.i + 1}')).at(n().tag(f'saver_{step.i + 1}')).run(
                tp(p(), r(1, 32, 0)).facing(r(-2, 34, 0)))
        else:
            yield say(step.i - 3)
            yield execute().as_(e().tag(f'saver_{step.i - 3}')).at(n().tag(f'saver_{step.i - 3}')).run(
                setblock(r(0, 34, 0), 'air'),
                tp(p(), r(1, 0, 0)).facing(r(-2, 2, 0)))

    next = room.loop('next', home=False)
    next.add(execute().if_().score(tall).matches(0).if_().score(next.score).matches((0, count - 1)).run(
        function(next))).loop(next_loop, range(count * 2))

    prep_each = room.function('prep_each', home=False).add(
        fill(r(0, 0, 0), r(1, 1, 0), 'air'),
        setblock(r(0, 0, 0), 'torch'),
        setblock(r(0, 2, 0), Block('structure_block',
                                   nbt={'mode': 'SAVE', 'ignoreEntities': False, 'name': '$(name)_$(num)', 'sizeX': 32,
                                        'sizeY': 32, 'sizeZ': 32})),
        execute().if_().score(tall).matches(1).run(
            setblock(r(0, 34, 0), Block('structure_block',
                                        nbt={'mode': 'SAVE', 'ignoreEntities': False, 'name': '$(name)_$(tall_num)',
                                             'sizeX': 32,
                                             'sizeY': 32, 'sizeZ': 32}))
        )
    )

    room.function('prep', home=False).add(
        function(remove, {'name': Arg('name')}),
        ((say(i + 1),
          Entity('armor_stand',
                 {'NoGravity': 1, 'AbsorptionAmount': i, 'CustomName': Arg('name')}).tag('saver',
                                                                                         f'saver_{i + 1}', '$(name)',
                                                                                         f'$(name)_{i + 1}').summon(
              pos), say('summon', i + 1)) for i, pos in enumerate(segments)),
        (execute().as_(e().tag(f'saver_{i + 1}')).at(e().tag(f'saver_{i + 1}')).run(
            function(prep_each, {'y': 0, 'num': i + 1, 'tall_num': i + 5, 'name': Arg('name')})) for i in
            range(count)),
        next.score.set(-1),
    )

    room.function('start', home=False).add(
        next.score.set(count - 1),
        function(next)
    )
