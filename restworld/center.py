from __future__ import annotations

from pynecraft.base import DARK_BLUE, DARK_GREEN, DARK_PURPLE, GOLD, LIGHT_PURPLE, NE, NORTH, NW, Nbt, RED, \
    SE, \
    SOUTH, SW, \
    WEST, \
    r
from pynecraft.commands import Block, ClickEvent, Entity, Score, Text, clone, e, execute, fill, function, kill, \
    scoreboard, \
    setblock, summon, tag
from pynecraft.info import Horse
from pynecraft.simpler import Book, ItemFrame, Sign, TextDisplay, WallSign
from restworld.materials import armor_for
from restworld.rooms import Room, ensure
from restworld.world import fast_clock, main_clock, restworld, slow_clock


def intro_book():
    book = Book()
    book.sign_book('Welcome!', 'RestWorld', 'Welcome to RestWorld!')
    rainbow = (RED, GOLD, DARK_GREEN, DARK_BLUE, LIGHT_PURPLE, DARK_PURPLE)
    title = 'RestWorld'
    book.add('',
             Text.text('Welcome to\n').bold().extra(
                 *tuple(Text.text(title[x]).color(rainbow[x % len(rainbow)]) for x in range(len(title))), r'!\n\n')),
    book.add(
        r'This world lets you test your resource pack. Almost everything is here: blocks, mobs, particles, UI, moon phases, models…\n\n'
        r'RestWorld loops through variants, which takes less'),
    book.next_page(),
    book.add(
        r'space, and also helps you compare textures that you may want to look similar.\n\n',
        r'Many levers and buttons control modes, like whether horses have saddles or ore is in deepslate.\n\n'
        r'This looping is run by clocks. You can start or stop the clocks by'),
    book.next_page()
    book.add(
        'pushing a button on a green or red block (red means "stop", etc.).\n\n'
        r'You start with a control book. Buttons inside it let you change clock speeds, step loops one at a time, and teleport to various areas. You can get a replacement book with the button'),
    book.next_page()
    book.add(
        r'on the magenta block near the start.\n\n',
        'Start exploring! There\'s a lot to play with, almost every texturable thing is here! ',
        text_url('Let me know',
                 'https://www.planetminecraft.com/project/restworld-a-complete-resourcepack-testing-world-for-1-15-2/'),
        ' what you think, or anything that\'s missing!\n\n',
        Text.text(r'\n      Have fun!').bold())
    book.next_page()
    book.add(
        r'I also have two texture packs that might interest you:\n\n',
        text_url(r'Call Out', 'https://claritypack.com/call_out/'),
        ', which highlights untextured blocks, helping you make a complete pack.\n\n',
        text_url(r'Clarity', 'https://claritypack.com/'),
        ', the pack I originally built RestWorld for.')
    book.next_page()
    book.add('',
        Text.text(r'Credits:\n\n').italic(),
        Text.text(r'BlueMeanial:\n').bold(),
        r'  Software Design\n  Programming\n\n',
        Text.text(r'JUMBOshrimp277:\n').bold(),
        r'  Visual Design\n  Testing\n  Rubber Duck\n',
        r'\n',
        r'Details on ',
        text_url(r'our site', 'https://claritypack.com/restworld/'),
        '.')

    return book


def text_url(text, url):
    return Text.text(text).underlined().italic().color(DARK_PURPLE).click_event(ClickEvent.open_url(url))


def room():
    room = Room('center', restworld)

    room.function('intro').add(
        ensure(r(0, 2, 0), Block('lectern', {'facing': NORTH, 'has_book': True}), nbt=intro_book().as_item()))
    room.function('intro_enter').add(setblock(r(0, -1, -1), 'redstone_block'))
    room.function('intro_exit').add(setblock(r(0, -1, -1), 'air'))
    room.function('intro_init').add(
        TextDisplay(r'Welcome!\nRead This\nIntroduction!',
                    nbt={'Tags': ['center', 'intro'], 'Rotation': [180, 0], 'background': 0x7f000000}).scale(
            0.615).summon(
            r(0.01, 2.18, -1.4)))

    room.function('example_painting_init').add(
        kill(e().tag('center_painting')),
        summon(Entity('painting', {'variant': 'prairie_ride', 'facing': 3, 'Tags': ['center_painting']}), r(0, 4, 0)))
    speed_fast = Score('SPEED_FAST', 'clocks')
    speed_main = Score('SPEED_MAIN', 'clocks')
    speed_slow = Score('SPEED_SLOW', 'clocks')
    room.function('faster_clocks', home=False).add(
        execute().if_().score(speed_fast).matches((10, None)).run(scoreboard().players().remove(speed_fast, 2)),
        execute().if_().score(speed_main).matches((10, None)).run(scoreboard().players().remove(speed_main, 5)),
        execute().if_().score(speed_slow).matches((10, None)).run(scoreboard().players().remove(speed_slow, 10)))
    room.function('slower_clocks', home=False).add(
        fast_clock.speed.add(2),
        main_clock.speed.add(5),
        slow_clock.speed.add(10))
    room.function('reset_clocks', home=False).add(
        list(c.speed.set(c.init_speed) for c in restworld.clocks()))

    # noinspection GrazieInspection
    top_sign = Sign((None, 'Touch the', 'sign below', 'to go to …'), hanging=True, state={'attached': True})
    room.function('lights_init').add(
        top_sign.place(r(6, 5, 6), NW),
        Sign(('the', 'Optifine', 'Rooms'), (function('restworld:global/goto_optifine'),), hanging=True).place(
            r(6, 4, 6), NW),
        top_sign.place(r(6, 5, -6), SW),
        Sign(('the', 'Battle', 'Arena'), (function('restworld:global/goto_arena'),), hanging=True).place(r(6, 4, -6),
                                                                                                         SW),
        top_sign.place(r(-6, 5, -6), SE),
        Sign(('the', 'Biome', 'Sampler'), (function('restworld:global/goto_biomes'),), hanging=True).place(r(-6, 4, -6),
                                                                                                           SE),
        top_sign.place(r(-6, 5, 6), NE),
        Sign(('the', 'Photo', 'Area'), (function('restworld:global/goto_photo'),), hanging=True).place(r(-6, 4, 6), NE),

        tag(e().tag('lights_home')).add('fast_lights_home'),
        tag(e().tag('lights_home')).add('main_lights_home'),
        tag(e().tag('lights_home')).add('slow_lights_home'),
    )

    def lights_loop(y, block):
        yield fill(r(2, y, 2), r(-2, y, -2), 'redstone_block').replace(block)
        yield clone(r(2, y, 2), r(-2, y, -2), r(-2, 1, -2)).masked()
        yield fill(r(2, y, 2), r(-2, y, -2), block).replace('redstone_block')
        yield clone(r(2, y, 2), r(-2, y, -2), r(-2, 1, -2)).masked()

    # The "kill" here is to pick up the scutes the armadillo drops occasionally; could add a loop just for this
    room.loop('fast_lights', fast_clock).loop(lambda x: lights_loop(-3, 'stone'), range(0, 1)).add(
        kill(e().type('item').distance((None, 25))))
    room.loop('main_lights', main_clock).loop(lambda x: lights_loop(-4, 'diamond_block'), range(0, 1))
    room.loop('slow_lights', slow_clock).loop(lambda x: lights_loop(-5, 'emerald_block'), range(0, 1))

    all = Nbt({'Tags': ['center', 'mob_display'], 'PersistenceRequired': True})
    trim_stand = Entity('armor_stand', all.merge({'ShowArms': True})).tag('center_stand')
    armor_for(trim_stand, 'copper', {'components': {'trim': {'pattern': 'flow', 'material': 'lapis'}}})
    silent = Nbt({'Silent': True})
    room.function('mobs_display_init').add(
        summon(Entity('copper_golem', silent).tag('mob_display'), r(-6, 2.5, 0), all),
        summon(Entity('panda', {'MainGene': 'playful', 'Silent': True}).tag('mob_display'), r(-6, 2.5, 0), all),
        summon(Horse('horse', Horse.Color.CHESTNUT, Horse.Markings.WHITE, silent).tag('mob_display'), r(-6, 2.5, 0),
               all),
        summon(Entity('pig', silent.merge({'variant': 'cold'})).tag('mob_display'), r(-6, 2.5, 0), all),

        summon(Entity('llama', silent).tag('mob_display'), r(6, 2.5, 0), all),
        summon(Entity('cow', silent.merge({'variant': 'warm'})).tag('mob_display'), r(6, 2.5, 0), all),
        summon(Entity('piglin_brute', silent.merge({'IsImmuneToZombification': True})).tag('mob_display'), r(6, 2.5, 0),
               all),
        summon(Entity('mooshroom', silent).tag('mob_display'), r(6, 2.5, 0), all),

        trim_stand.summon(r(10.51, 2, 0), facing=NORTH),

        kill(e().type('item')),
    )
    messages = (None, Text.text('F u cn rd ths').obfuscated(True),
                Text.text('u cd b hm by nw').obfuscated(True).extra(Text.text('‽').obfuscated(False)))
    room.function('plants_display_init').add(WallSign(messages).place(r(5, 3, -4), SOUTH))
    room.function('materials_display_init').add(ItemFrame(WEST).item('clock').tag('mob_display').summon(r(4, 4, 5)))
