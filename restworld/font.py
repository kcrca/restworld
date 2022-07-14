from __future__ import annotations

from pyker.base import EAST, SOUTH, WEST, r
from pyker.commands import Block, JsonText, data, e, execute, function, kill, s, setblock, tag
from pyker.info import colors, stems, woods
from pyker.simpler import Book, WallSign
from restworld.rooms import Room, ensure, label
from restworld.world import restworld

text_colors = ('black', 'dark_blue', 'dark_green', 'dark_aqua', 'dark_red', 'dark_purple',
               'gold', 'gray', 'dark_gray', 'blue', 'green', 'aqua', 'red', 'light_purple', 'yellow', 'white')


def color_text(color):
    return JsonText.text('Lorem ipsum dolor\\n').color(color).hover_event().show_text(color)


def formatting_book():
    book = Book()
    book.sign_book('Format Book', 'Restworld', 'Text Formatting')
    book.add('',
             JsonText.text('Named text colors\\n').underlined(),
             JsonText.text('    (hover for names)\\n\\n'))
    for c in text_colors[:8]:
        book.add(color_text(c))
    book.next_page()
    for c in text_colors[8:]:
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
    room.function('check_sign').add(
        execute().if_().block(r(0, 3, -1), '#minecraft:wall_signs').run(function('restworld:font/copy_sign')))
    room.function('colored_text').add(
        ensure(r(0, 2, 0), Block('lectern', {'facing': WEST, 'has_book': True}),
               nbt=formatting_book().as_item()))

    materials = tuple(Block(m) for m in woods + stems)
    copy_sign = room.function('copy_sign')
    for i, thing in enumerate(materials):
        x, y = i % 3 - 1, 5 - int(i / 3)
        copy_sign.add(ensure(r(x, y, -1), WallSign((None, str(i)), state={'facing': SOUTH}, wood=thing.id)))

        for path in tuple('Text%d' % i for i in range(1, 5)):
            copy_sign.add(
                execute().at(e().tag('font_action_home')).run(
                    data().modify(r(x, y, -1), path).set().from_(r(0, 2, -1), path)))
        copy_sign.add(data().modify(r(x, y, -1), 'Color').set().from_(r(0, -3, -1), 'Color'))

    copy_sign.add(
        data().modify(r(0, 2, -1), 'Color').set().from_(r(0, -3, -1), 'Color'),
        data().modify(e().tag('font').tag('nameable').limit(1), 'CustomName').set().from_(r(0, 2, -1), 'Text1'),
        data().modify(e().tag('font').tag('nameable').limit(1), 'CustomNameVisible').set().value(True)
    )

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
        execute().positioned(r(0, 0, -2)).run(function('restworld:font/copy_sign')),

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
                     (execute().at(e().tag('font_action_home')).run(
                         data().modify(r(0, -3, -3), 'Color').set().value(c.id)),),
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
        room.mob_placer(r(0, 2, 0), SOUTH, adults=True).summon('rabbit', tags=('nameable',)),
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
