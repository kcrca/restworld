from pynecraft.base import to_name
from pynecraft.commands import custom_dialog
from restworld.world import restworld


def create():
    dialogs = restworld.registry('dialogs')
    for d in ('notice', 'confirmation', 'multi_action', 'server_links', 'dialog_list',
              'simple_input_form', 'multi_action_input_form'):
        title = f'{to_name(d)} Dialog'
        dialogs[d] = custom_dialog(d, title, title, {})
