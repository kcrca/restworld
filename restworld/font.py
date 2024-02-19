from __future__ import annotations

from pynecraft import info
from pynecraft.base import EAST, JSON_COLORS, SOUTH, WEST, r
from pynecraft.commands import Block, JsonText, clone, data, e, execute, function, kill, s, setblock, tag
from pynecraft.info import colors, stems
from pynecraft.simpler import Book, TextDisplay, WallSign
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
    room.reset_at((1, -4))
    src_pos = r(0, 2, 0)
    save_pos = r(0, -2, -3)
    color_pos = r(0, -3, -3)
    at = execute().at(e().tag('font_action_home'))
    room.function('check_sign', home=False).add(
        at.run(function('restworld:font/copy_sign')))

    font_run_init = room.function('font_run_init').add(label(r(-1, 2, 1), 'Glowing Text'))

    woods = info.woods
    materials = tuple(Block(m) for m in woods + stems)
    copy_sign = room.function('copy_sign', home=False).add(
        execute().if_().block(src_pos, '#wall_signs').run(clone(src_pos, src_pos, save_pos))
    )
    row_lengths = [3, 3, 2, 2]
    if 'Cherry' in woods:
        row_lengths[2] = 3
    row, x, y = 0, 0, 5
    for i, thing in enumerate(materials):
        pos = r(x - 1, y, 0)
        copy_sign.add(ensure(pos, WallSign((), state={'facing': SOUTH}, wood=thing.id)))

        copy_sign.add(data().modify(pos, 'front_text.messages').set().from_(src_pos, 'front_text.messages'),
                      data().modify(pos, 'back_text.messages').set().from_(src_pos, 'front_text.messages'),
                      data().modify(pos, 'front_text.color').set().from_(color_pos, 'front_text.color'),
                      data().modify(pos, 'back_text.color').set().from_(color_pos, 'front_text.color'))

        x += 1
        if x >= row_lengths[row]:
            x = 0
            y -= 1
            row += 1
        elif x == 1 and row_lengths[row] == 2:
            x += 1

    copy_sign.add(data().modify(e().tag('font').tag('nameable').limit(1), 'CustomName').set().from_(save_pos,
                                                                                                    'front_text.messages[0]'))

    room.function('colored_text').add(
        ensure(r(0, 2, 0), Block('lectern', {'facing': WEST, 'has_book': True}),
               nbt=formatting_book().as_item()))

    room.function('font_run_enter').add(
        setblock(r(0, -2, -2), 'redstone_torch'),
        setblock(r(-3, -2, 2), 'redstone_torch'),
        setblock(r(3, -2, 2), 'redstone_torch'),
    )
    room.function('font_run_exit').add(
        setblock(r(0, -2, -2), 'air'),
        setblock(r(-3, -2, 2), 'air'),
        setblock(r(3, -2, 2), 'air'),
    )
    # noinspection SpellCheckingInspection
    init_text = ('Lorem ipsum', 'dolor sit amet,', 'consectetur', 'adipiscing elit.')
    font_run_init.add(tag(e().tag('font_run_home')).add('font_action_home'),
                      WallSign(init_text).wax(False).place(src_pos, SOUTH),
                      execute().at(e().tag('font_action_home')).run(setblock(save_pos, 'air')),
                      function('restworld:font/check_sign'),
                      WallSign((None, 'Color Holder')).place(r(0, -3, -3), SOUTH), kill(e().tag('sign_desc')),
                      TextDisplay('A sign here sets the text',
                                  {'text_opacity': 255, 'background': 0, 'line_width': 80, 'shadow_radius': 0}
                                  ).scale(0.5).tag('sign_desc').summon(r(0, 2, -0.4)))

    for i, c in enumerate(colors):
        x = int(i / 4) - 3
        if x > -2:
            x += 3
        y = 5 - i % 4
        txt = (None, c.name, 'Text')
        cmds = (at.run(data().modify(r(0, -3, -3), 'front_text.color').set().value(c.id)),
                at.run(data().modify(r(0, -3, -3), 'back_text.color').set().value(c.id)),
                at.run(setblock(save_pos, 'air')))
        font_run_init.add(WallSign(txt, cmds).messages(txt, cmds).color(c.id).place(r(x, y, 0), SOUTH))

    maybe_glow = room.function('maybe_glow')
    font_glow = room.score('font_glow')
    for x in range(0, 30):
        for y in range(0, 4):
            maybe_glow.add(
                execute().if_().score(font_glow).matches(0).at(e().tag('font_run_home')).run(
                    data().merge(r(x - 3, y + 2, 0), {'front_text': {'has_glowing_text': False}}),
                    data().merge(r(x - 3, y + 2, 0), {'back_text': {'has_glowing_text': False}})),
                execute().if_().score(font_glow).matches(1).at(e().tag('font_run_home')).run(
                    data().merge(r(x - 3, y + 2, 0), {'front_text': {'has_glowing_text': True}}),
                    data().merge(r(x - 3, y + 2, 0), {'back_text': {'has_glowing_text': True}}))
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
