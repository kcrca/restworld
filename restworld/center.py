from __future__ import annotations

from pynecraft.base import DARK_PURPLE, NE, NORTH, NW, Nbt, SE, SOUTH, SW, WEST, r
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
    book.add(
        r'This world lets you test how your resource pack looks. Almost everything is here: blocks, mobs, particles, UI, moon phases…\n\n'
        r'The world loops through variants, which takes less space. You can also compare textures that you may want to make,')
    book.next_page(),
    book.add(
        r'look similar.\n\n',
        r'Levers and buttons control modes, like whether horses have saddles. Buttons on red or green blocks show if clocks are on: A button on a red block will stop the clocks; one on a green block starts them.\n\n', )
    book.next_page()
    book.add(
        r'You start with a control book. This lets you change clock speeds, step loops one at a time, and teleport to various areas. You can get a replacement book with the button on the purple block nearby.')
    book.next_page()
    book.add(
        r'I also have two texture packs that might interest you:\n\n',
        Text.text(r'Call Out').underlined().italic().color(DARK_PURPLE).click_event(ClickEvent.open_url(
            'https://claritypack.com/call_out/')),
        ', which highlights untextured blocks, helping you make a complete pack.\n\n',
        Text.text(r'Clarity').underlined().italic().color(DARK_PURPLE).click_event(ClickEvent.open_url(
            'https://claritypack.com/')),
        ', the pack I originally built RestWorld for.')
    book.next_page()
    book.add(
        Text.text(r'Credits:\n\n'),
        Text.text(r'BlueMeanial:\n').bold(),
        r'  Software Design\n  Programming\n\n',
        Text.text(r'JUMBOshrimp277:\n').bold(),
        r'  Visual Design\n  Testing\n  Rubber Duck\n',
        r'\n',
        r'Details on ',
        Text.text(r'our site').underlined().italic().color(DARK_PURPLE).click_event(ClickEvent.open_url(
            'https://claritypack.com/restworld/')),
        '.')

    return book


def room():
    room = Room('center', restworld)

    room.function('intro').add(
        ensure(r(0, 2, 0), Block('lectern', {'facing': NORTH, 'has_book': True}), nbt=intro_book().as_item()))
    room.function('intro_enter').add(setblock(r(0, -1, -1), 'redstone_block'))
    room.function('intro_exit').add(setblock(r(0, -1, -1), 'air'))
    room.function('intro_init').add(
        TextDisplay(r'Welcome!\nRead This\nIntroduction',
                    nbt={'Tags': ['center', 'intro'], 'Rotation': [180, 0], 'background': 0x7f000000}).scale(0.61).summon(
            r(0, 2.18, -1.4)))

    room.function('example_painting_init').add(
        kill(e().tag('center_painting')),
        summon(Entity('painting', {'variant': 'prairie_ride', 'facing': 3, 'Tags': ['center_painting']}), r(0, 4, 0)))
    speed_fast = Score('SPEED_FAST', 'clocks')
    speed_main = Score('SPEED_MAIN', 'clocks')
    speed_slow = Score('SPEED_SLOW', 'clocks')
    room.function('faster_clocks', home=False).add(
        execute().if_().score(speed_fast).matches((13, None)).run(scoreboard().players().remove(speed_fast, 2)),
        execute().if_().score(speed_main).matches((13, None)).run(scoreboard().players().remove(speed_main, 6)),
        execute().if_().score(speed_slow).matches((13, None)).run(scoreboard().players().remove(speed_slow, 10)))
    room.function('slower_clocks', home=False).add(
        fast_clock.speed.add(2),
        main_clock.speed.add(6),
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

    all = {'Tags': ['center', 'mob_display'], 'PersistenceRequired': True}
    trim_stand = Entity('armor_stand', all).tag('center_stand')
    armor_for(trim_stand, 'iron', {'components': {'trim': {'pattern': 'flow', 'material': 'resin'}}})
    silent = Nbt({'Silent': True})
    room.function('mobs_display_init').add(
        summon(Entity('mooshroom', silent).tag('mob_display'), r(-6, 2.5, 0), all),
        summon(Entity('panda', {'MainGene': 'playful', 'Silent': True}).tag('mob_display'), r(-6, 2.5, 0), all),
        summon(Horse('horse', Horse.Color.CHESTNUT, Horse.Markings.WHITE, silent).tag('mob_display'), r(-6, 2.5, 0),
               all),
        summon(Entity('pig', silent.merge({'variant': 'cold'})).tag('mob_display'), r(-6, 2.5, 0), all),

        summon(Entity('llama', silent).tag('mob_display'), r(6, 2.5, 0), all),
        summon(Entity('cow', silent.merge({'variant': 'warm'})).tag('mob_display'), r(6, 2.5, 0), all),
        summon(Entity('piglin_brute', silent.merge({'IsImmuneToZombification': True})).tag('mob_display'), r(6, 2.5, 0),
               all),
        summon(Entity('armadillo', silent).tag('mob_display'), r(6, 2.5, 0), all),

        trim_stand.summon(r(10.51, 2, 0), facing=NORTH),

        kill(e().type('item')),
    )
    messages = (None, Text.text('F u cn rd ths').obfuscated(True),
                Text.text('u cd b hm by nw').obfuscated(True).extra(Text.text('‽').obfuscated(False)))
    room.function('plants_display_init').add(WallSign(messages).place(r(5, 3, -4), SOUTH))
    room.function('materials_display_init').add(ItemFrame(WEST).item('clock').tag('mob_display').summon(r(4, 4, 5)))
