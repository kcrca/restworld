from pynecraft.commands import Text
from pynecraft.dialog import ClickAction, Item, boolean, confirmation, dialog_list, item, multi_action, notice, \
    number_range, \
    plain_message, \
    single_option, \
    text
from restworld.world import restworld


def create():
    dialogs = restworld.registry('dialog')

    dialogs['notice'] = notice('Notice').body(
        plain_message('My hovercraft is full of eels.')
    ).inputs(
        text('Text', 'Four Score…'),
        boolean("Boolean?"),
        single_option('Single Option', ('Euphoria', 'Melancholy', 'Ennui', 'Copacetic'), initial='Ennui'),
        number_range('Number Range', 0, 20, initial=1)
    )
    dialogs['confirmation'] = confirmation('Confirmation', ClickAction('Yes!'), ClickAction('Nooooo!!!!!!')).body(
        item(Item.nbt_for('cake'), show_decoration=True, show_tooltip=True),
        plain_message('Is the cake a lie?')
    )
    dialogs['multi_action'] = multi_action('Multi Action', (ClickAction(f'Choice #{i}') for i in range(32)))
    dialogs['dialog_list'] = dialog_list(
        'Dialog List',
        (notice(f'I said: "{99 - i} BOTTLES OF BEER!!!"', external_title=f'{99 - i} bottles of beer') for i in
         range(32)))

    advice = plain_message(
        Text.text('(The warning icon at the top is a button, you might want to press it if you texture it)').italic())
    for d in dialogs.values():
        if 'body' in d:
            d['body'] += (advice,)
        else:
            d['body'] = (advice,)
