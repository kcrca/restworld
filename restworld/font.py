from __future__ import annotations

from pynecraft.base import EAST, JSON_COLORS, SOUTH, WEST, r
from pynecraft.commands import Block, JsonText, clone, data, e, execute, function, kill, s, setblock, tag
from pynecraft.info import colors, stems, woods
from pynecraft.simpler import Book, WallSign
from restworld.rooms import Room, ensure, label
from restworld.world import restworld


def color_text(color):
    return JsonText.text('Lorem ipsum dolor\\n').color(color).hover_event().show_text(color)


def formatting_book():
    book = Book()
    book.sign_book('Format Book', 'Restworld', 'Text Formatting')
    book.add('',
             JsonText.text('Named text colors\\n').underlined(),
             JsonText.text('    (hover for names)\\n\\n'))
    for c in JSON_COLORS[:8]:
        book.add(color_text(c))
    book.next_page()
    for c in JSON_COLORS[8:]:
        book.add(color_text(c))
    book.next_page()
    book.add('',
             JsonText.text('Text Formatting').underlined(),
             '\\n\\n',
             JsonText.text('Bold Text\\n').bold(),
             JsonText.text('Italic Text\\n').italic(),
             JsonText.text('Underline Text\\n').underlined(),
             JsonText.text('Strikethrough Text\\n').strikethrough(),
             JsonText.text('Obfuscated Text\\n').obfuscated().hover_event().show_text('Obfuscated'))
    return book


def room():
    room = Room('font', restworld, SOUTH, (None, 'Fonts'))
    src_pos = r(0, 2, -3)
    save_pos = r(0, -2, -3)
    color_pos = r(0, -3, -3)
    at = execute().at(e().tag('font_action_home'))
    room.function('check_sign', home=False).add(
        at.run(function('restworld:font/copy_sign')))

    materials = tuple(Block(m) for m in woods + stems)
    copy_sign = room.function('copy_sign', home=False).add(clone(src_pos, src_pos, save_pos))
    for i, thing in enumerate(materials):
        x, y = i % 3 - 1, 5 - int(i / 3)
        pos = r(x, y, -3)
        copy_sign.add(ensure(pos, WallSign((), state={'facing': SOUTH}, wood=thing.id)))

        for path in tuple('Text%d' % i for i in range(1, 5)):
            copy_sign.add(data().modify(pos, path).set().from_(src_pos, path))
        copy_sign.add(data().modify(pos, 'Color').set().from_(color_pos, 'Color'))

    copy_sign.add(
        data().modify(e().tag('font').tag('nameable').limit(1), 'CustomName').set().from_(src_pos, 'Text1'))

    room.function('colored_text').add(
        ensure(r(0, 2, 0), Block('lectern', {'facing': WEST, 'has_book': True}),
               nbt=formatting_book().as_item()))

    room.function('font_run_enter').add(
        setblock(r(0, -2, -2), 'redstone_torch'),
        setblock(r(-3, -2, 0), 'redstone_torch'),
        setblock(r(3, -2, 0), 'redstone_torch'),
    )
    room.function('font_run_exit').add(
        setblock(r(0, -2, -2), 'air'),
        setblock(r(-3, -2, 0), 'air'),
        setblock(r(3, -2, 0), 'air'),
    )
    font_run_init = room.function('font_run_init').add(
        tag(e().tag('font_run_home')).add('font_action_home'),
        WallSign(('Lorem ipsum', 'dolor sit amet,', 'consectetur', 'adipiscing elit.')).place(r(0, 2, -3), SOUTH),
        execute().at(e().tag('font_action_home')).run(setblock(save_pos, 'air')),
        function('restworld:font/check_sign'),
        WallSign((None, 'Color Holder')).place(r(0, -3, -3), SOUTH),
        label(r(0, 2, -1), 'Reset'),
        label(r(0, 6, -3), 'Glowing', facing=3),
    )

    for i, c in enumerate(colors):
        x = int(i / 4) - 3
        if x > -2:
            x += 3
        y = 5 - i % 4
        font_run_init.add(
            WallSign((None, 'Use', c.name, 'Text'),
                     (at.run(data().modify(r(0, -3, -3), 'Color').set().value(c.id)),
                      at.run(setblock(save_pos, 'air'))),
                     nbt={'Color': c.id}).place(r(x, y, -3), SOUTH))

    maybe_glow = room.function('maybe_glow')
    font_glow = room.score('font_glow')
    for x in range(0, 30):
        for y in range(0, 4):
            maybe_glow.add(
                execute().if_().score(font_glow).matches(0).at(e().tag('font_run_home')).run(
                    data().merge(r(x - 3, y + 2, -3), {'GlowingText': False})),
                execute().if_().score(font_glow).matches(1).at(e().tag('font_run_home')).run(
                    data().merge(r(x - 3, y + 2, -3), {'GlowingText': True}))
            )

    room.function('nameable_init').add(
        kill(e().tag('font_mobs')),
        room.mob_placer(r(0, 2, 0), SOUTH, adults=True).summon('rabbit', tags=('nameable',), auto_tag=False),
        execute().as_(e().tag('font').tag('nameable').limit(1)).run(
            data().modify(s(), 'CustomNameVisible').set().value(True)),
    )

    # This is easiest to do with basic string manipulation
    with open('unicode_text.txt') as input:
        book = ''
        found_start = False
        for line in input:
            if not found_start:
                found_start = line.find('give @p') > 0
            else:
                book += line.replace('\n', '').replace('.png', '').replace('.otf', '')
    room.function('unicode_text').add(
        str(ensure(r(0, 2, 0), ('lectern', {'facing': EAST, 'has_book': True}))) +
        '{Book:{id:"minecraft:written_book", Count:1, tag: %s}}' % book)
