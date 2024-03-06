from __future__ import annotations

from pynecraft.base import EQ, SOUTH, d, r
from pynecraft.commands import Block, COLORS, Entity, INT, RESULT, WHITE, data, e, execute, fill, function, kill, s, \
    setblock, tag
from pynecraft.simpler import Shield, TextDisplay, WallSign
from pynecraft.values import PATTERN_GROUP, as_pattern, patterns
from restworld.rooms import Room, label
from restworld.world import die, main_clock, restworld

stand_tmpl = Entity('armor_stand', {
    'Invisible': True, 'NoGravity': True, 'ShowArms': True, 'Pose': {'LeftArm': [0, 90, 90]}, 'HandItems': [{}],
    'Tags': ['banner_stand']})

# [xz]n: Adjustments (nudge) for shield's armor stand
# b[xz]: Adjustments for banner position
#                  x   xn  xd   z   zn  zd             bx  bz
adjustments = {0: (1, 0.07, 1, -1, 0.30, 0, 0, 'south', 0, +1),
               11: (13, -0.30, 0, 1, 0.07, 1, 90, 'west', -1, 0),
               21: (11, -0.07, -1, 13, -0.30, 0, 180, 'north', 0, -1),
               31: (-1, 0.30, 0, 11, -0.07, -1, 270, 'east', +1, 0)}

# noinspection SpellCheckingInspection
authored_patterns = (
    (Block('blue_banner', nbt={'Patterns': [
        {'Color': 0, 'Pattern': 'bri'}, {'Color': 11, 'Pattern': 'hhb'}, {'Color': 15, 'Pattern': 'sc'},
        {'Color': 11, 'Pattern': 'sc'}, {'Color': 15, 'Pattern': 'bo'}, {'Color': 11, 'Pattern': 'bo'}]}),
     'Tardis', 'Pikachu'),
    (Block('purple_banner', nbt={'Patterns': [
        {'Color': 2, 'Pattern': 'ss'}, {'Color': 10, 'Pattern': 'bri'}, {'Color': 2, 'Pattern': 'cbo'},
        {'Color': 15, 'Pattern': 'bo'}]}),
     'Portail du Nether', 'Akkta'),
    (Block('white_banner', nbt={'Patterns': [
        {'Color': 15, 'Pattern': 'mr'}, {'Color': 1, 'Pattern': 'cbo'}, {'Color': 1, 'Pattern': 'mc'},
        {'Color': 1, 'Pattern': 'cre'}, {'Color': 1, 'Pattern': 'tt'}, {'Color': 1, 'Pattern': 'tts'}]}),
     'Fox', 'mr.crafteur'),
    (Block('white_banner', nbt={'Patterns': [
        {'Color': 15, 'Pattern': 'mc'}, {'Color': 0, 'Pattern': 'flo'}, {'Color': 15, 'Pattern': 'tt'},
        {'Color': 0, 'Pattern': 'cr'}, {'Color': 15, 'Pattern': 'cbo'}, {'Color': 0, 'Pattern': 'bts'}]}),
     'Rabbit', 'googolplexbyte'),
    (Block('light_blue_banner', nbt={'Patterns': [
        {'Color': 11, 'Pattern': 'gra'}, {'Color': 0, 'Pattern': 'cbo'}, {'Color': 0, 'Pattern': 'cr'},
        {'Color': 0, 'Pattern': 'mc'}, {'Color': 11, 'Pattern': 'flo'}, {'Color': 0, 'Pattern': 'tt'}]}),
     'Angel', 'PK?'),
    (Block('white_banner', nbt={'Patterns': [
        {'Color': 15, 'Pattern': 'sc'}, {'Color': 0, 'Pattern': 'sc'}, {'Color': 15, 'Pattern': 'flo'},
        {'Color': 0, 'Pattern': 'flo'}]}),
     'Quartz sculpte', 'Pikachu'),
    (Block('black_banner', nbt={'Patterns': [
        {'Color': 5, 'Pattern': 'cbo'}, {'Color': 15, 'Pattern': 'rs'}, {'Color': 14, 'Pattern': 'flo'},
        {'Color': 5, 'Pattern': 'ms'}, {'Color': 15, 'Pattern': 'tt'}, {'Color': 5, 'Pattern': 'moj'}]}),
     'DRAGON !', 'kraftime'),
    (Block('white_banner', nbt={'Patterns': [
        {'Color': 15, 'Pattern': 'ts'}, {'Color': 0, 'Pattern': 'sc'}, {'Color': 14, 'Pattern': 'hhb'},
        {'Color': 0, 'Pattern': 'bo'}, {'Color': 0, 'Pattern': 'bs'}, {'Color': 4, 'Pattern': 'ms'}]}),
     'Poule', 'mish80'),
    (Block('black_banner', nbt={'Patterns': [
        {'Color': 14, 'Pattern': 'gru'}, {'Color': 14, 'Pattern': 'bt'}, {'Color': 0, 'Pattern': 'bts'},
        {'Color': 0, 'Pattern': 'tts'}]}),
     'Bouche', 'entonix69'),
    (Block('lime_banner', nbt={'Patterns': [
        {'Color': 4, 'Pattern': 'gra'}, {'Color': 3, 'Pattern': 'gru'}, {'Color': 0, 'Pattern': 'cbo'},
        {'Color': 0, 'Pattern': 'cr'}, {'Color': 0, 'Pattern': 'mr'}, {'Color': 5, 'Pattern': 'mc'}]}),
     'Like pls ^-^', 'Harmony'),
)


def room():
    room = Room('banners', restworld, SOUTH, (None, 'Banners &', 'Shields'))
    room.reset_at((0, -11))

    banner_color = room.score('banner_color')
    banner_ink = room.score('banner_ink')
    stands = e().tag('banner_stand')

    room.function('names_on', home=False).add(execute().as_(e().tag('banner_name')).run(
        data().merge(s(), {'text_opacity': 255, 'background': 0x40_00_00_00})))
    names_off = room.function('names_off', home=False).add(execute().as_(e().tag('banner_name')).run(
        data().merge(s(), {'text_opacity': 25, 'background': 25})))

    # noinspection PyUnusedLocal
    def armor_stands(x, xn, z, zn, angle, facing, bx, bz, y_banner, y_shield, pattern, handback=None):
        shield = Shield().add_pattern(pattern, 9)
        stand = stand_tmpl.clone()
        stand.merge_nbt({'Rotation': [angle, 0]})
        stand.nbt['HandItems'].append(shield.nbt)
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
        nbt = {'Rotation': [angle, 0], 'Tags': stand.nbt['Tags']}
        yield TextDisplay(name).scale(0.5).tag('banner_name').summon(r(x + xt, text_y, z + zt), nbt)

    def render_banners(render, handback=None):
        # These are in the first adjustment, but python doesn't know that, so this keeps it happy
        x = z = xd = zd = xn = zn = angle = facing = bx = bz = 0
        for i, pat in enumerate(PATTERN_GROUP):
            pattern = patterns[pat]
            try:
                x, xn, xd, z, zn, zd, angle, facing, bx, bz = adjustments[i]
            except KeyError:
                x += xd
                z += zd
            if i > 10 and i % 10 == 6:
                x += xd
                z += zd
            yield render(x, xn, z, zn, angle, facing, bx, bz, 3.65, 3.65, pattern.value, handback)

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

    # noinspection PyUnusedLocal
    def render_banner_color(x, xn, z, zn, angle, facing, bx, bz, y_banner, y_shield, pattern, handback=None):
        color = handback
        return setblock(r(x + bx, y_banner, z + bz), Block(color + '_wall_banner', {'facing': facing},
                                                           {'Patterns': [{'Color': 9, 'Pattern': pattern}]}))

    # noinspection PyUnusedLocal
    def render_banner_ink(x, xn, z, zn, angle, facing, bx, bz, y_banner, y_shield, pattern, handback=None):
        return (
            execute().store(RESULT).block(r(x + bx, y_banner, z + bz), 'Patterns[0].Color', INT, 1).run(
                banner_ink.get()),
        )

    def banner_color_loop(step):
        return render_banners(render_banner_color, handback=step.elem)

    def banner_ink_change():
        yield execute().as_(stands).at(stands).run(
            execute().store(RESULT).block((d(0, 0, 1)), 'Patterns[0].Color', INT, 1).run(banner_ink.get()))
        yield execute().as_(stands).run(
            execute().store(RESULT).entity(s(), 'HandItems[1].tag.BlockEntityTag.Patterns[0].Color', INT, 1).run(
                banner_ink.get()))

    def switch_banners(which):
        return (
            tag(e().tag('all_banners_home')).remove('banner_color_action_home'),
            tag(e().tag('all_banners_home')).remove('banner_color_home'),
            tag(e().tag('all_banners_home')).remove('banner_ink_action_home'),
            tag(e().tag('all_banners_home')).remove('banner_ink_home'),
            tag(e().tag('all_banners_home')).add('banner_' + which + '_action_home'),
            tag(e().tag('all_banners_home')).add('banner_' + which + '_home'),
            tag(e().tag('all_banners_home')).add('banners_action_home'),
        )

    banner_color_init = function('restworld:banners/switch_to_color')
    room.function('all_banners_init').add(
        banner_color.set(0),
        banner_ink.set(9),
        kill(stands),
        fill(r(-2, -2, -2), r(16, 16, 16), 'air').replace('#banners'),
        render_banners(armor_stands),
        setblock(r(-0.2, 3, 11.8), Block('white_banner', {'rotation': 10}, {
            'Patterns': [{'Pattern': 'mr', 'Color': 9}, {'Pattern': 'bs', 'Color': 8}, {'Pattern': 'cs', 'Color': 7},
                         {'Pattern': 'bo', 'Color': 8}, {'Pattern': 'ms', 'Color': 15}, {'Pattern': 'hh', 'Color': 8},
                         {'Pattern': 'mc', 'Color': 8}, {'Pattern': 'bo', 'Color': 15}]})),
        setblock(r(11.8, 3, 0.2), Block('magenta_banner', {'rotation': 2}, {
            'Patterns': [{'Pattern': 'bt', 'Color': 15}, {'Pattern': 'tt', 'Color': 15}]})),
        custom_banner(0.2, 0.2, 0.1),
        custom_banner(11.8, 11.8, -0.1),
        banner_color_init,
        function('restworld:banners/banner_color_cur'),
        function(names_off),
    )

    if len(authored_patterns) % 2 != 0:
        die('Must have an even number of custom patterns')
    room.loop('all_banners', main_clock).add(
        setblock(r(0, 3, 0), 'air'),
        setblock(r(11, 3, 11), 'air'),
    ).loop(render_authored_banners, range(0, half))

    room.function('banner_color_init').add(banner_color_init)

    color_loop = room.loop('banner_color', main_clock)
    ink_loop = room.loop('banner_ink', main_clock)

    color_loop.adjust(
        execute().if_().score(color_loop.score).is_(EQ, ink_loop.score).run(color_loop.score.add(1))
    ).add(
        fill(r(1, 3, 0), r(11, 5, 0), 'air').replace('#banners'),
        fill(r(12, 3, 1), r(12, 5, 11), 'air').replace('#banners'),
        fill(r(1, 3, 12), r(11, 5, 12), 'air').replace('#banners'),
        fill(r(0, 3, 11), r(0, 5, 1), 'air').replace('#banners'),
    ).loop(banner_color_loop, COLORS).add(execute().as_(stands).run(
        execute().store(RESULT).entity(s(), 'HandItems[1].tag.BlockEntityTag.Base', INT, 1).run(
            banner_color.get())), function('restworld:banners/banner_ink_cur'))

    banner_controls = room.function('banner_controls').add(
        function('restworld:banners/banner_controls_remove'),
        function('restworld:global/clock_off'),
        WallSign((None, 'Set Banner', 'Color'), (function('restworld:banners/switch_to_color', )),
                 wood='dark_oak').color(WHITE).place(r(4, 3, 1), SOUTH),
        WallSign((None, 'Set Banner', 'Ink'), (function('restworld:banners/switch_to_ink', )),
                 wood='dark_oak').color(WHITE).place(r(4, 2, 2), SOUTH),
    )
    for i, c in enumerate(COLORS):
        x = i % 8
        # Leave room for the middle signs
        if x >= 4:
            x += 1
        row = int(i / 8)
        y = 3 if row == 0 else 2
        z = 1 if row == 0 else 2
        if_colors = execute().at(e().tag('banner_color_home'))
        if_ink = execute().at(e().tag('banner_ink_home'))
        banner_controls.add(WallSign((None, c), (
            if_colors.run(banner_color.set(i)),
            if_colors.run(function('restworld:banners/banner_color_cur')),
            if_ink.run(banner_ink.set(i)),
            if_ink.run(function('restworld:banners/banner_ink_cur')),
        )).place(r(x, y, z), SOUTH))
    room.function('banner_controls_init').add(
        label(r(5, 2, 4), 'Banner / Ink'),
        label(r(3, 2, 4), 'Labels'),
        label(r(4, 2, 3), 'Controls'),
        function('restworld:banners/switch_to_color'),
    )
    room.function('banner_controls_remove', home=False).add(
        fill(r(0, 2, 0), r(8, 4, 4), 'air').replace('#wall_signs'))

    ink_loop.adjust(
        execute().if_().score(ink_loop.score).is_(EQ, color_loop.score).run(ink_loop.score.add(1))
    ).loop(None, COLORS).add(*banner_ink_change())

    # ^Cyan Lozenge
    # ^Light Gray Base
    # ^Gray Pale
    # ^Light Gray Bordure
    # ^Black Fess
    # ^Light Gray Per Fess
    # ^Light Gray Roundel
    # ^Black Bordure
    room.function('ominous_banner').add(
        setblock(r(0, 0, 0), Block('white_banner', nbt={
            'Patterns': [{'Pattern': 'mr', 'Color': 9}, {'Pattern': 'bs', 'Color': 8}, {'Pattern': 'cs', 'Color': 7},
                         {'Pattern': 'bo', 'Color': 8}, {'Pattern': 'ms', 'Color': 15}, {'Pattern': 'hh', 'Color': 8},
                         {'Pattern': 'mc', 'Color': 8}, {'Pattern': 'bo', 'Color': 15}]})))

    room.function('switch_to_color', home=False).add(switch_banners('color'))
    room.function('switch_to_ink', home=False).add(switch_banners('ink'))
