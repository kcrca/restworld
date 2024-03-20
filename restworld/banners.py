from __future__ import annotations

from pynecraft.base import Arg, CYAN, EQ, NORTH, SOUTH, r
from pynecraft.commands import Block, COLORS, Entity, WHITE, data, e, execute, fill, function, kill, s, setblock
from pynecraft.simpler import Shield, Sign, TextDisplay, WallSign
from pynecraft.values import BORDER, BRICKS, CIRCLE, CREEPER, CROSS, CURLY_BORDER, FLOWER, GRADIENT, GRADIENT_UP, \
    HALF_HORIZONTAL, HALF_HORIZONTAL_BOTTOM, MOJANG, PATTERN_GROUP, RHOMBUS, SMALL_STRIPES, STRAIGHT_CROSS, \
    STRIPE_BOTTOM, STRIPE_CENTER, STRIPE_MIDDLE, STRIPE_RIGHT, STRIPE_TOP, TRIANGLES_BOTTOM, TRIANGLES_TOP, \
    TRIANGLE_BOTTOM, TRIANGLE_TOP, as_pattern, patterns
from restworld.rooms import Room
from restworld.world import die, main_clock, restworld

stand_tmpl = Entity('armor_stand', {
    'Invisible': True, 'NoGravity': True, 'ShowArms': True, 'Pose': {'LeftArm': [0, 90, 90]}, 'HandItems': [{}],
    'Tags': ['banner_stand']})

# [xz]n: Adjustments (nudge) for shield's armor stand
# b[xz]: Adjustments for banner position
#                  x   xn  xd   z   zn  zd             bx  bz  skip middle
adjustments = {0: (1, 0.07, 1, -1, 0.30, 0, 0, 'south', 0, +1),
               11: (13, -0.30, 0, 1, 0.07, 1, 90, 'west', -1, 0),
               22: (11, -0.07, -1, 13, -0.30, 0, 180, 'north', 0, -1),
               32: (-1, 0.30, 0, 11, -0.07, -1, 270, 'east', +1, 0)}

# noinspection SpellCheckingInspection
authored_patterns = (
    (Block('blue_banner', nbt={'patterns': [
        {'color': COLORS[0], 'pattern': BRICKS}, {'color': COLORS[11], 'pattern': HALF_HORIZONTAL_BOTTOM},
        {'color': COLORS[15], 'pattern': STRAIGHT_CROSS}, {'color': COLORS[11], 'pattern': STRAIGHT_CROSS},
        {'color': COLORS[15], 'pattern': BORDER}, {'color': COLORS[11], 'pattern': BORDER}]}),
     'Tardis', 'Pikachu'),
    (Block('purple_banner', nbt={'patterns': [
        {'color': COLORS[2], 'pattern': SMALL_STRIPES}, {'color': COLORS[10], 'pattern': BRICKS},
        {'color': COLORS[2], 'pattern': CURLY_BORDER}, {'color': COLORS[15], 'pattern': BORDER}]}),
     'Portail du Nether', 'Akkta'),
    (Block('white_banner', nbt={'patterns': [
        {'color': COLORS[15], 'pattern': RHOMBUS}, {'color': COLORS[1], 'pattern': CURLY_BORDER},
        {'color': COLORS[1], 'pattern': CIRCLE}, {'color': COLORS[1], 'pattern': CREEPER},
        {'color': COLORS[1], 'pattern': TRIANGLE_TOP}, {'color': COLORS[1], 'pattern': TRIANGLES_TOP}]}),
     'Fox', 'rhombus.crafteur'),
    (Block('white_banner', nbt={'patterns': [
        {'color': COLORS[15], 'pattern': CIRCLE}, {'color': COLORS[0], 'pattern': FLOWER},
        {'color': COLORS[15], 'pattern': TRIANGLE_TOP}, {'color': COLORS[0], 'pattern': CROSS},
        {'color': COLORS[15], 'pattern': CURLY_BORDER}, {'color': COLORS[0], 'pattern': TRIANGLES_BOTTOM}]}),
     'Rabbit', 'googolplexbyte'),
    (Block('light_blue_banner', nbt={'patterns': [
        {'color': COLORS[11], 'pattern': GRADIENT}, {'color': COLORS[0], 'pattern': CURLY_BORDER},
        {'color': COLORS[0], 'pattern': CROSS}, {'color': COLORS[0], 'pattern': CIRCLE},
        {'color': COLORS[11], 'pattern': FLOWER}, {'color': COLORS[0], 'pattern': TRIANGLE_TOP}]}),
     'Angel', 'PK?'),
    (Block('white_banner', nbt={'patterns': [
        {'color': COLORS[15], 'pattern': STRAIGHT_CROSS}, {'color': COLORS[0], 'pattern': STRAIGHT_CROSS},
        {'color': COLORS[15], 'pattern': FLOWER}, {'color': COLORS[0], 'pattern': FLOWER}]}), 'Quartz sculpte',
     'Pikachu'),
    (Block('black_banner', nbt={'patterns': [
        {'color': COLORS[5], 'pattern': CURLY_BORDER}, {'color': COLORS[15], 'pattern': STRIPE_RIGHT},
        {'color': COLORS[14], 'pattern': FLOWER}, {'color': COLORS[5], 'pattern': STRIPE_MIDDLE},
        {'color': COLORS[15], 'pattern': TRIANGLE_TOP}, {'color': COLORS[5], 'pattern': MOJANG}]}),
     'DRAGON !', 'kraftime'),
    (Block('white_banner', nbt={'patterns': [
        {'color': COLORS[15], 'pattern': STRIPE_TOP}, {'color': COLORS[0], 'pattern': STRAIGHT_CROSS},
        {'color': COLORS[14], 'pattern': HALF_HORIZONTAL_BOTTOM}, {'color': COLORS[0], 'pattern': BORDER},
        {'color': COLORS[0], 'pattern': STRIPE_BOTTOM}, {'color': COLORS[4], 'pattern': STRIPE_MIDDLE}]}),
     'Poule', 'mishCOLORS[80]'),
    (Block('black_banner', nbt={'patterns': [
        {'color': COLORS[14], 'pattern': GRADIENT_UP}, {'color': COLORS[14], 'pattern': TRIANGLE_BOTTOM},
        {'color': COLORS[0], 'pattern': TRIANGLES_BOTTOM}, {'color': COLORS[0], 'pattern': TRIANGLES_TOP}]}),
     'Bouche', 'entonixCOLORS[69]'),
    (Block('lime_banner', nbt={'patterns': [
        {'color': COLORS[4], 'pattern': GRADIENT}, {'color': COLORS[3], 'pattern': GRADIENT_UP},
        {'color': COLORS[0], 'pattern': CURLY_BORDER}, {'color': COLORS[0], 'pattern': CROSS},
        {'color': COLORS[0], 'pattern': RHOMBUS}, {'color': COLORS[5], 'pattern': CIRCLE}]}),
     'Like pls ^-^', 'Harmony'),
)


def room():
    room = Room('banners', restworld, SOUTH, (None, 'Banners &', 'Shields'))
    room.reset_at((0, -11))

    banner_color = room.score('banner_color')
    banner_ink = room.score('banner_ink')
    which = room.score('which')
    stands = e().tag('banner_shield_stand')

    room.function('names_on', home=False).add(execute().as_(e().tag('banner_name')).run(
        data().merge(s(), {'text_opacity': 255, 'background': 0x40_00_00_00})))
    names_off = room.function('names_off', home=False).add(execute().as_(e().tag('banner_name')).run(
        data().merge(s(), {'text_opacity': 25, 'background': 25})))

    # noinspection PyUnusedLocal
    def init_armor_stands(x, xn, z, zn, angle, facing, bx, bz, y_banner, y_shield, pattern, handback=None):
        shield = Shield().color(WHITE)
        if pattern != 'base':
            shield.add_pattern(pattern, CYAN)
        stand = stand_tmpl.clone()
        stand.merge_nbt({'Rotation': [angle, 0], 'HandItems': [{}, shield.nbt]}).tag('banners', 'banner_shield_stand')
        yield stand.summon(r(x + xn, y_shield, z + zn))

        text_y = y_shield + 0.5
        if (x + z) % 2 == 0:
            text_y -= 0.25
        xt = 0.6 if abs(xn) > abs(zn) else 0
        zt = 0.6 if abs(zn) > abs(xn) else 0
        if xn < 0:
            xt = -xt
        if zn < 0:
            zt = -zt
        name = patterns[as_pattern(pattern)].name
        nbt = {'Rotation': [angle, 0], 'Tags': ['banners']}
        yield TextDisplay(name).scale(0.5).tag('banner_name').summon(r(x + xt, text_y, z + zt), nbt)

    def render_banners(render):
        # These are in the first adjustment, but python doesn't know that, so this keeps it happy
        x = z = xd = zd = xn = zn = angle = facing = bx = bz = 0
        for i, pat in enumerate(PATTERN_GROUP):
            pattern = patterns[pat]
            try:
                x, xn, xd, z, zn, zd, angle, facing, bx, bz = adjustments[i]
            except KeyError:
                x += xd
                z += zd
            if facing == 'north' and i == 27:
                x += xd
                z += zd
            yield render(x, xn, z, zn, angle, facing, bx, bz, 3.65, 3.65, pattern.value)

    # noinspection PyUnusedLocal
    def render_updates(x, xn, z, zn, angle, facing, bx, bz, y_banner, y_shield, pattern):
        banner = Block('$(color)_wall_banner', {'facing': facing})
        if pattern != 'base':
            banner.nbt['patterns'] = [{'color': Arg('ink'), 'pattern': pattern}]
        yield setblock(r(x + bx, y_banner, z + bz), banner)

    update = room.function('update_banners', home=False).add(
        execute().as_(stands).run(
            data().modify(s(), 'HandItems[1].components.minecraft:base_color').set().value(Arg('color')),
            data().modify(s(), 'HandItems[1].components.minecraft:banner_patterns[].color').set().value(Arg('ink'))),
        fill(r(1, 3, 0), r(11, 5, 0), 'air').replace('#banners'),
        fill(r(12, 3, 1), r(12, 5, 11), 'air').replace('#banners'),
        fill(r(1, 3, 12), r(11, 5, 12), 'air').replace('#banners'),
        fill(r(0, 3, 11), r(0, 5, 1), 'air').replace('#banners'),
        render_banners(render_updates)
    )

    def custom_banner(x, z, nudge):
        stand1 = stand_tmpl.clone()
        stand1.nbt.get_list('Tags').extend(('banner_stand', 'banner_pattern_custom'))
        stand2 = stand_tmpl.clone()
        stand2.nbt.get_list('Tags').extend(('banner_stand', 'banner_pattern_custom_author'))
        return stand1.summon(r(x + nudge, 3.1, z + nudge)), stand2.summon(r(x + nudge, 2.8, z + nudge))

    def authored_banners(pattern, x, z, rot):
        return (
            setblock(r(x, 3, z), pattern[0].merge_state({'rotation': rot})),
            execute().positioned(r(x, 3, z)).as_(
                e().tag('banner_pattern_custom').distance((None, 2))).run(
                data().merge(s(), {'CustomName': pattern[1]})),
            execute().positioned(r(x, 3, z)).as_(
                e().tag('banner_pattern_custom_author').distance((None, 2))).run(
                data().merge(s(), {'CustomName': pattern[2]})),
        )

    half = int(len(authored_patterns) / 2)

    def render_authored_banners(step):
        return (
            authored_banners(authored_patterns[step.i], 0.2, 0.2, 14),
            authored_banners(authored_patterns[step.i + half], 11.8, 11.8, 6),
        )

    # init: set up all armor stands, initialize restworld:banners.color and .ink, call 'function banners with storage restworld:banners'
    # function banners is a macro that sets the color and ink for all stands, plus setblock for each place.
    # (In principle for ink we could be setting the data values for all of them, but the special case is probably not worth it; reexamine when done)
    # The loops just changes banners.color or banners.ink, and then calls function banners, as above

    def banner_color_loop(step):
        yield data().modify('restworld:banners', 'color').set().value(step.elem)
        yield Sign.change(color_sign, (None, None, step.elem))

    def switch_banners(to):
        yield which.set(0 if to == 'color' else 1)

    color_sign = r(4, 2, 6)
    ink_sign = r(8, 2, 6)
    room.function('all_banners_init').add(
        # /data modify storage restworld:banners.ink
        which.set(0),
        banner_color.set(0),
        data().modify('restworld:banners', 'color').set().value(WHITE),
        banner_ink.set(9),
        data().modify('restworld:banners', 'ink').set().value(CYAN),
        kill(e().tag('banners')),
        fill(r(-2, -2, -2), r(16, 16, 16), 'air').replace('#banners'),
        render_banners(init_armor_stands),
        setblock(r(-0.2, 3, 11.8), Block('white_banner', {'rotation': 10}, {
            'patterns': [
                {'pattern': RHOMBUS, 'color': COLORS[9]}, {'pattern': STRIPE_BOTTOM, 'color': COLORS[8]},
                {'pattern': STRIPE_CENTER, 'color': COLORS[7]}, {'pattern': BORDER, 'color': COLORS[8]},
                {'pattern': STRIPE_MIDDLE, 'color': COLORS[15]}, {'pattern': HALF_HORIZONTAL, 'color': COLORS[8]},
                {'pattern': CIRCLE, 'color': COLORS[8]}, {'pattern': BORDER, 'color': COLORS[15]}]})),
        setblock(r(11.8, 3, 0.2), Block('magenta_banner', {'rotation': 2}, {
            'patterns': [{'pattern': TRIANGLE_BOTTOM, 'color': COLORS[15]},
                         {'pattern': TRIANGLE_TOP, 'color': COLORS[15]}]})),
        custom_banner(0.2, 0.2, 0.1),
        custom_banner(11.8, 11.8, -0.1),
        WallSign((None, 'Color:', 'white')).place(color_sign, SOUTH),
        WallSign((None, 'Ink:', 'cyan')).place(ink_sign, SOUTH),
        function(names_off),
    )

    color_loop = room.loop('banner_color', main_clock, home=False)
    ink_loop = room.loop('banner_ink', main_clock, home=False)

    if len(authored_patterns) % 2 != 0:
        die('Must have an even number of custom patterns')
    room.loop('all_banners', main_clock).add(
        setblock(r(0, 3, 0), 'air'),
        setblock(r(11, 3, 11), 'air'),
    ).loop(render_authored_banners, range(0, half)).add(
        execute().if_().score(which).matches(0).run(function(color_loop)),
        execute().unless().score(which).matches(0).run(function(ink_loop)),
        function(update).with_().storage('restworld:banners'),
    )

    color_loop.loop(banner_color_loop, COLORS).add(
        # make sure the two values are different.
        execute().if_().score(banner_ink).is_(EQ, banner_color).unless().score(('_to_incr', 'banners')).matches(0).run(
            function(color_loop))
    )

    def banner_ink_loop(step):
        yield data().modify('restworld:banners', 'ink').set().value(step.elem)
        yield Sign.change(ink_sign, (None, None, step.elem))

    ink_loop.loop(banner_ink_loop, COLORS).add(
        # make sure the two values are different.
        execute().if_().score(banner_ink).is_(EQ, banner_color).unless().score(('_to_incr', 'banners')).matches(0).run(
            function(ink_loop)))

    room.function('switch_to_color', home=False).add(switch_banners('color'))
    room.function('switch_to_ink', home=False).add(switch_banners('ink'))

    banner_controls = room.function('banner_controls').add(
        function('restworld:banners/banner_controls_remove'),
        function('restworld:global/clock_off'),
        WallSign((None, 'Set Banner', 'color'), (function('restworld:banners/switch_to_color'),),
                 wood='dark_oak', front=None).color(WHITE).place(r(4, 3, 1), SOUTH),
        WallSign((None, 'Set Banner', 'Ink'), (function('restworld:banners/switch_to_ink'),),
                 wood='dark_oak', front=None).color(WHITE).place(r(4, 2, 2), SOUTH),
    )
    for i, c in enumerate(COLORS):
        x = i % 8
        # Leave room for the middle signs
        if x >= 4:
            x += 1
        row = int(i / 8)
        y = 3 if row == 0 else 2
        z = 1 if row == 0 else 2
        banner_controls.add(WallSign((None, c), (
            execute().if_().score(which).matches(0).run(banner_color.set(i)),
            execute().unless().score(which).matches(0).run(banner_ink.set(i)),
            execute().at(e().tag('all_banners_home')).run(function('restworld:banners/all_banners_cur'))
        ), front=None).place(r(x, y, z), SOUTH))
    room.function('banner_controls_init').add(
        room.label(r(5, 2, 4), 'Banner / Ink', NORTH),
        room.label(r(3, 2, 4), 'Labels', NORTH),
        room.label(r(4, 2, 3), 'Controls', NORTH),
        function('restworld:banners/switch_to_color'),
    )
    room.function('banner_controls_remove', home=False).add(
        fill(r(0, 2, 0), r(8, 4, 3), 'air').replace('#wall_signs'))
