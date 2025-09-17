import re
from collections import defaultdict

from pynecraft import info
from pynecraft.base import Arg, EAST, EQ, as_facing, d, r, to_name
from pynecraft.commands import Block, DIV, MOD, REPLACE, Text, clone, comment, data, e, execute, fill, function, \
    item, kill, n, p, say, schedule, setblock, summon, tag
from pynecraft.info import block_items, default_skins, stems, woods
from pynecraft.simpler import Item, ItemFrame, Sign, WallSign
from restworld import global_
from restworld.rooms import ActionDesc, SignedRoom, Wall, named_frame_item, span
from restworld.world import fast_clock, restworld

# The item area...
#
# See how models work, especially WRT displays. There are two major modes: The user chooses a thing to view,
# or we loop through some set of things. The first mode is relatively simple: The user puts something in the frame,
# and it's copied into many places, but not the user's hands. They have full control of when things change,
# can see first person views themselves.
#
# The second has us putting things into the user's hands, and therefore changing their inventory. This requires
# planning. So...
#
# (*) When the user enters the area, we copy their hotbar and left hand into a chest, and when they leave we replace
# them. The replacement should probably only happen if we have ever put something in their hands in the first place.
# Because placing things into their hands when they leave is probably rather unexpected, it's just the least
# destructive thing we can do.
#
# (*) The user chooses which list of things to loop. Right now there are two: items and blocks. Which gives three
# states: Not looping, or looping one of these. Currently, I have a lever for each list, and turning one on forces
# the other off if needed. This puts the levers next to each other to save room, and it's tricky to get the power
# issues working right.
#
# (*) ...But I can imagine others. For example, a compressed version of these could be built by assuming that we can
# show only one version of things that share a lot of models (stairs, slabs, ...). That might very much reduce the
# length of the list. But that further complicates choosing which list to use. Maybe signs for each one?
#
# (*) Some blocks have no item version (e.g., water and lava). We leave them out of the block list.

ranges = {'A-B': None, 'C-G': None, 'H-O': None, 'P-R': None, 'S-Z': None}

mode_names = ['sampler_blocks', 'blocks', 'manual', 'items', 'sampler_items']
modes = [ActionDesc(e, to_name(e)) for e in mode_names]

sample_pats = (
    'Stairs', r'Slab', r'Planks', r'Fence$', r'Fence Gate', r'Stripped.* (?:Logs|Stem)', r'(?<!Stripped).* Wood$',
    r'Cut Copper', r'(?<!Cut|Raw) Copper$', r'Tulip', r'Dye', r' Wool$', r'Carpet', r'Wall$', r'Anvil',
    r'Stained Glass$', r'Glass Pane', r'Shulker Box', r'Concrete$', r'Concrete Powder', r'Pressure Plate', r'Button',
    r'Boat$', r'Boat with Chest', r'Sword', r'Shovel', r'Pickaxe', r'Axe', r'Hoe', r'Ingot', r'Helmet', r'Leggings',
    r'Chestplate', r'Boots', r'(?<!Wall) Sign', r' Bed$', r'Spawn Egg', r'Horse Armor', r'Banner', r'Music Disc',
    r' Candle$', r'Froglight', r'Coral Block', r'Coral Fan', r'Coral$')
samples_re = re.compile('(' + ')|('.join(sample_pats) + ')')
samples_skip_re = re.compile(r'Stripped.* (Wood|Hyphae)')

# this is for debugging, so we can examine the groupings for the sampled sets.
VERBOSE = False


def sample(which, things):
    seen = defaultdict(list)
    unclassified = '[unclassified]'

    def sample_filter(t):
        name = t.name
        if samples_skip_re.search(name):
            seen[samples_skip_re.pattern].append(name)
        else:
            m = samples_re.search(name)
            if not m:
                seen[unclassified].append(name)
                return True
            else:
                pos = None
                for i, group in enumerate(m.groups()):
                    if group:
                        if pos:
                            print(f'Warning: {name}: Groups {pos} and {i}')
                        pos = i
                if pos is None:
                    raise ValueError(f'{name}: pos is None')
                pattern = sample_pats[pos]
                show = pattern not in seen
                seen[pattern].append(name)
                return show

    try:
        return tuple(filter(sample_filter, things))
    finally:
        if VERBOSE:
            print(f'... {which}')
            for key in sample_pats:
                print(f'{key}: {seen[key]}')
            print(f'{unclassified}: {seen[unclassified]}')


def room():
    model_home = e().tag('model_home')

    def mode_sign(action_desc: ActionDesc, wall):
        dx, _, dz = as_facing(wall.facing).scale(1)
        # noinspection PyTypeChecker
        return WallSign(action_desc.sign_text(), (
            fill(r(-dx, -2, -5), r(-dx, 2, 5), 'smooth_quartz').replace('emerald_block'),
            setblock(d(-dx, 0, -dz), 'emerald_block'),
            execute().at(model_home).run(function(f'restworld:models/start_{action_desc.which}'))))

    wall_used = {3: span(1, 5)}
    room = SignedRoom('models', restworld, EAST, (None, None, 'Models'), mode_sign, modes,
                      (Wall(7, EAST, 1, -1, wall_used),))
    room.reset_at((-4, -1))

    room.function('model_signs_init').add(function('restworld:models/signs'))

    placer = room.mob_placer(r(0, 3, 0), EAST, auto_tag=False, adults=True, nbt={'ShowArms': True})
    all_src = e().tag('model_src')
    model_src = all_src.limit(1)
    all_ground = e().tag('model_ground')
    model_ground = all_ground.limit(1)
    model_holder = e().tag('model_holder').limit(1)
    invis_frame = e().tag('model_invis_frame').limit(1)
    all_things_home = e().tag('all_things_home')

    is_empty = room.score('model_is_empty')
    was_empty = room.score('model_was_empty')
    needs_restore = room.score('needs_restore')

    # +1 because we also copy the player's own skin for a modeler
    num_skins = room.score('num_skins', len(default_skins) + 1)
    skin_every = room.score('skin_every', 4)
    cur_skin = room.score('cur_skin')
    recent_things_signs = (r(-2, 4, 1), r(-2, 4, 0), r(-2, 4, -1))[::-1]
    chest_pos = r(-1, -2, 0)
    room.function('models_room_init', exists_ok=True).add(
        room.label(r(-2, 2, -1), 'See in Hands', EAST))
    under = {'chorus_flower': 'end_stone', 'chorus_plant': 'end_stone', 'sugar_cane': 'grass_block',
             'wheat': 'farmland', 'bamboo': 'grass_block'}
    model_init = room.function('model_init').add(
        kill(all_src),
        kill(all_ground),
        placer.summon('mannequin', nbt={'immovable': True, 'hide_description': True},
                      tags=('model_holder', 'model_hands')),
        data().modify(room.store, 'under').set().value(
            [{'id': f'minecraft:{k}', 'under': v} for k, v in under.items()]),
        setblock(r(1, 2, 1), 'structure_void'),
        setblock(r(-1, 2, 1), 'structure_void'),
        setblock(r(0, 2, 2), 'structure_void'),
        setblock(r(0, -6, 0), 'stone_bricks'),
        ItemFrame(EAST).item('iron_pickaxe').tag('model_src', 'models').fixed(False).summon(r(2, 2, 2)),
        ItemFrame(EAST, nbt={'Invisible': True}, name='Invisible Frame').tag('model_invis_frame', 'models').fixed(
            False).summon(r(2, 2, -2)),
        room.label(r(1.5, 3, 2), 'Put something in this frame to see it in many views', EAST, vertical=True),

        (WallSign((), wood='birch').place(pos, EAST) for pos in recent_things_signs),
        setblock(chest_pos, 'chest'),
        needs_restore.set(0),

        room.label(r(0, 2, -1), 'On Head', EAST),
        room.label(r(0.5, 2.5, 0), 'None', EAST, vertical=True, tags=('current_model',)),

        is_empty.set(1),
        schedule().function('restworld:models/model_copy', '1s', REPLACE)
    )
    ground_default_nbt = {'Item': Item.nbt_for('iron_pickaxe'), 'Age': -32768, 'PickupDelay': 2147483647,
                          'Tags': ['model_ground']}
    named_frame_data = named_frame_item(name='Invisible Frame').merge({'ItemRotation': 0})
    do_set_if_block = room.function('do_set_if_block', home=False).add(
        setblock(r(0, -6, 0), Arg('under_block')),
        setblock(r(0, -5, 0), '$(block)$(block_state)'),
    )
    # We set the block somewhere and clone it over so we can filter doors and beds, which come out weird.
    set_if_block = room.function('set_if_block', home=False).add(
        setblock(r(0, -5, 0), 'air'),
        data().modify(room.store, 'under_block').set().value('stone_bricks'),
        execute().if_().data(room.store, 'under[{id: "$(block)"}]').run(
            data().modify(room.store, 'under_block').set().from_(room.store, 'under[{id: "$(block)"}].under')),
        data().modify(room.store, 'block_state').set().value(''),
        execute().if_().data(room.store, 'states[{id: "$(block)"}]').run(
            data().modify(room.store, 'block_state').set().from_(room.store, 'states[{id: "$(block)"}].state')),
        function(do_set_if_block).with_().storage(room.store),
        execute().unless().block(r(0, -5, 0), '#restworld:no_model_block').run(
            clone(r(0, -5, 0), r(0, -6, 0), r(0, 1, 1))))

    at_home = execute().at(model_home).run

    see_in_hands = room.score('see_in_hands')
    model_copy = room.function('model_copy', home=False).add(
        data().merge(model_src, {'ItemRotation': 0}),
        execute().unless().data(model_src, 'Item.id').run(kill(all_ground)),
        execute().at(model_home).run(setblock(r(0, 2, 1), 'air')),
        execute().if_().data(model_src, 'Item.id').run(
            execute().unless().entity(model_ground).at(model_home).run(
                summon('item', r(1, 3, -2), ground_default_nbt)),
            data().modify(model_ground, 'Item').set().from_(model_src, 'Item'),
            data().merge(model_ground, {'Age': -32768, 'PickupDelay': 2147483647}),
            data().modify(room.store, 'block').set().from_(model_src, 'Item.id'),
            data().modify(room.store, 'shelf_slots[0].id').set().from_(model_src, 'Item.id'),
            data().modify(room.store, 'shelf_slots[1].id').set().from_(model_src, 'Item.id'),
            data().modify(room.store, 'shelf_slots[2].id').set().from_(model_src, 'Item.id'),
            data().modify(r(0, 3, -1), 'Items').set().from_(room.store, 'shelf_slots'),
            at_home(function(set_if_block).with_().storage(room.store)),
        ),
        item().replace().entity(model_holder, 'weapon.mainhand').from_().entity(model_src, 'container.0'),
        item().replace().entity(model_holder, 'weapon.offhand').from_().entity(model_src, 'container.0'),
        execute().if_().score(room.score('model_head')).matches(0).run(data().remove(model_holder, 'equipment.head')),
        execute().if_().score(room.score('model_head')).matches(1).run(
            item().replace().entity(model_holder, 'armor.head').from_().entity(model_src, 'container.0')),
        item().replace().entity(invis_frame, 'container.0').from_().entity(model_src, 'container.0'),
        data().merge(invis_frame, named_frame_data),
        global_.if_clock_running.at(e().tag('all_things_home')).if_().score(see_in_hands).matches(1).run(
            say('hi'),
            item().replace().entity(p(), 'weapon.mainhand').from_().entity(model_src, 'container.0'),
            item().replace().entity(p(), 'weapon.offhand').from_().entity(model_src, 'container.0'),
            needs_restore.set(1)),
    )
    model_save = room.function('model_save', home=False).add(
        (item().replace().block(chest_pos, f'container.{i}').from_().entity(p(), f'hotbar.{i}') for i in range(0, 9)),
        item().replace().block(chest_pos, 'container.1').from_().entity(p(), 'weapon.offhand'),
        needs_restore.set(0))
    model_restore = room.function('model_restore', home=False).add(
        (item().replace().entity(p(), f'hotbar.{i}').from_().block(chest_pos, f'container.{i}') for i in range(0, 9)),
        item().replace().entity(p(), 'weapon.offhand').from_().block(chest_pos, 'container.1'),
        needs_restore.set(0))
    room.function('see_in_hands_on', home=False).add(at_home(function(model_save)), see_in_hands.set(1))
    room.function('see_in_hands_off', home=False).add(at_home(function(model_restore)), see_in_hands.set(0))
    room.function('model_run', home=False).add(
        was_empty.operation(EQ, is_empty),
        is_empty.set(1),
        execute().if_().data(model_src, 'Item.id').run(is_empty.set(0)),
        execute().unless().score(was_empty).is_(EQ, is_empty).run(
            function(model_copy),
            execute().if_().score(is_empty).matches(True).run(
                data().modify(n().tag('current_model'), 'text').set().value(Text.text(''))),
        ),
    )
    redstone_block_pos = r(1, -2, 1)
    room.function('model_enter').add(
        execute().at(model_home).run(function(model_save)),
        setblock(redstone_block_pos, 'redstone_block'))
    room.function('model_exit').add(
        setblock(redstone_block_pos, 'air'),
        execute().if_().score(needs_restore).matches(1).at(model_home).run(function(model_restore))
    )

    def change_modeler_loop(step):
        if step.elem:
            nbt = {'profile': {'texture': f'entity/player/wide/{step.elem}'}, 'CustomName': f'{to_name(step.elem)}'}
        else:
            nbt = {'profile': {'id': [1, 2, 3, 4]}, 'CustomName': 'You'}
        yield data().merge(model_holder, nbt)
        if not step.elem:
            yield data().remove(model_holder, 'profile.texture')
            yield data().modify(model_holder, 'profile.id').set().from_(p(), 'UUID')

    change_modeler = room.loop('change_modeler', home=False)
    change_modeler.add(
        data().remove(model_holder, 'profile.UUID'),
    ).loop(
        change_modeler_loop, default_skins + (None,)).add(
    )
    thing_ranges = {}

    def thing_funcs(which, things):
        nonlocal thing_ranges

        signs = recent_things_signs
        range_keys = tuple(ranges.keys())
        thing_ranges[which] = {}
        next_range = range_keys[0]

        def all_loop(step):
            nonlocal next_range
            block = step.elem
            if block.name[0] == next_range[0]:
                thing_ranges[which][next_range] = step.i - 1
                try:
                    next_range = range_keys[len(thing_ranges[which])]
                except IndexError:
                    next_range = '1'  # This means it was the last range, so set it to something never found
            item_block = block.clone()
            item_block.state = {}
            yield item().replace().entity(model_src, 'container.0').with_(item_block)
            name = block.name.replace(' [x]', '')
            yield at_home(Sign.change(signs[-1], (name,), front=True))
            yield data().modify(n().tag('current_model'), 'text').set().value(Text.text(name))

        all_things = things
        all_things_loop = room.loop(f'all_{which}', fast_clock).add(is_empty.set(1))
        for i, pos in enumerate(signs):
            all_things_loop.add(
                at_home(data().modify(pos, 'front_text.messages[3]').set().from_(pos, 'front_text.messages[2]')),
                at_home(data().modify(pos, 'front_text.messages[2]').set().from_(pos, 'front_text.messages[1]')),
                at_home(data().modify(pos, 'front_text.messages[1]').set().from_(pos, 'front_text.messages[0]')),
                at_home(data().modify(pos, 'front_text.messages[0]').set().from_(signs[i + 1],
                                                                                 'front_text.messages[3]')) if i < len(
                    signs) - 1 else comment('start'))
        all_things_loop.add(
            execute().unless().block(r(1, 1, 1), 'stone_bricks').run(setblock(r(1, 1, 1), 'stone_bricks')),
            cur_skin.operation(EQ, all_things_loop.score),
            cur_skin.operation(DIV, skin_every),
            cur_skin.operation(MOD, num_skins),
            execute().unless().score(cur_skin).is_(EQ, change_modeler.score).run(function(change_modeler))
        ).loop(
            all_loop, all_things)
        room.function(f'all_{which}_home', exists_ok=True).add(tag(e().tag(f'all_{which}_home')).add('all_things_home'))

        room.function(f'start_{which}', home=False).add(
            kill(all_things_home),
            execute().positioned(r(-1, -0.5, 0)).run(function(f'restworld:models/all_{which}_home')),
            tag(e().tag(f'all_{which}_home')).add('all_things_home'))

    def block_filter(block) -> bool:
        if block.name in block_items:
            return False
        if 'Air' in block.name:
            return False
        if 'Hanging' in block.name and 'Sign' not in block.name:
            return False
        if 'Wheat' in block.name:
            return False
        return True

    block_list = tuple(filter(block_filter, info.blocks.values()))

    state = {'sculk_vein': {'down': True, 'north': True}, 'grindstone': {'face': 'floor'}}
    easterly = {'furnace', 'dropper', 'dispenser', 'blast_furnace', 'smoker', 'chest', 'lectern', 'lever', 'observer'}
    for b in block_list:
        if re.search(r'_(head|skull)$', b.id):
            state[b] = {'rotation': 4}
        elif b.id.endswith('_banner'):
            state[b] = {'rotation': 12}
        elif re.search(r'_(button|fence_gate|chest)$', b.id) or b.id in easterly:
            state[b] = {'facing': EAST}
        elif b.id.endswith('_sign'):
            state[b] = {'facing': EAST} if b.id.endswith('_wall_sign') else {'rotation': 4}
        elif re.search(r'_(coral(_fan)?)$|^kelp$|^(tall_)?sea', b.id):
            state[b] = {'waterlogged': False}
        elif b.id == 'tripwire_hook':
            state[b] = {'facing': EAST}

    thing_funcs('blocks', block_list)
    thing_funcs('sampler_blocks', sample('blocks', block_list))
    item_list = tuple(filter(lambda row: 'Spawn' not in row.name, info.items.values()))
    thing_funcs('items', item_list)
    thing_funcs('sampler_items', sample('items', item_list))
    room.function('start_manual').add(kill(all_things_home))
    loop_names = tuple(filter(lambda x: x != 'manual', mode_names))
    for i, rng in enumerate(ranges):
        cmds = tuple(execute().at(e().tag(f'all_{x}_home')).run(
            room.score(f'all_{x}').set(thing_ranges[x][rng])) for x in loop_names)
        model_init.add(WallSign((None, rng), cmds).place(r(-2, 2, 2 - i), EAST))

    model_init.add(
        data().modify(room.store, 'states').set().value(
            [{'id': f'minecraft:{k}', 'state': Block.state_str(v)} for k, v in state.items()]),
        data().remove(room.store, 'shelf_slots'),
        data().modify(room.store, 'shelf_slots').set().value([{'Slot': 0, 'count': 1}, {'Slot': 1}, {'Slot': 2}]))

    def models_shelf_wood_loop(step):
        yield setblock(r(0, 2, 0), (f'{step.elem}_shelf', {'facing': EAST}))
        yield setblock(r(-1, 2, 0), f'{step.elem}_planks')
        yield is_empty.set(1)

    room.loop('models_shelf_wood').loop(models_shelf_wood_loop, woods + stems).add(is_empty.set(1))
    room.function('models_shelf_wood_init').add(
        room.label(r(1, 2, 1), 'Shelf Wood', EAST),
        room.label(r(3, 2, 1), 'Shelf Powered', EAST))
