from pynecraft.base import SOUTH, NORTH, r
from pynecraft.commands import say
from pynecraft.menus import Menu, Submenu
from restworld.rooms import Room
from restworld.world import restworld


def room():
    room = Room('tester', restworld, SOUTH, ('Testing',))

    menu = Menu('menu_home', lambda x, **kwargs: room.function(f'menu_{x}', home=x == 'init', **kwargs),
                lambda x: say(x), close_menus=True).add(('One', 'Two', 'Three'))
    submenu = Submenu(menu, 'Sub')
    menu.add(submenu)
    submenu.add(('alpha', 'beta', 'gamma'))
    menu.place(r(0, 5, 0), NORTH)
