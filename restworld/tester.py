from pynecraft.__init__ import NORTH, SOUTH, UP, r
from pynecraft.commands import say
from pynecraft.menus import Menu, Submenu
from restworld.rooms import Room
from restworld.world import restworld


def room():
    room = Room('tester', restworld, SOUTH, ('Testing',))

    menu = Menu(lambda x, **kwargs: room.function(f'menu_{x}', home=x == 'init', **kwargs),
                lambda x: say(x), dir=UP, close_menus=True).add(('One', 'Two', 'Three'))
    submenu = Submenu(menu, 'Sub')
    menu.add(submenu)
    submenu.add(('alpha', 'beta', 'gamma'))
    menu.place('menu_home', r(0, 5, 0), NORTH)
