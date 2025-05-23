from pynecraft.simpler import Dialog, Item
from restworld.world import restworld


def create():
    dialogs = restworld.registry('dialog')

    dialogs['notice'] = Dialog.notice('Notice', [Dialog.plain_message('My hovercraft is full of eels.')])
    dialogs['confirmation'] = Dialog.confirmation(
        'Confirmation',
        Dialog.click_action('Yes!'),
        Dialog.click_action('Nooooo!!!!!!'),
        body=(
            Dialog.item(Item.nbt_for('cake'), show_decoration=True, show_tooltip=True),
            Dialog.plain_message('Is the cake a lie?')
        ))
    dialogs['multi_action'] = Dialog.multi_action(
        'Multi Action',
        (Dialog.click_action(f'Choice #{i}') for i in range(32)))
    dialogs['dialog_list'] = Dialog.dialog_list(
        'Dialog List',
        (Dialog.notice(f'I said: "{99 - i} BOTTLES OF BEER!!!"', external_title=f'{99 - i} bottles of beer') for i in
         range(32))
    )
    form = (
        Dialog.text('Text', 'Bugs Bunny'),
        Dialog.boolean("Boolean?"),
        Dialog.single_option('Single Option',
                             ('Euphoria', 'Melancholy', {'display': 'Ennui', 'initial': True}, 'Copacetic')),
        Dialog.number_range('Number Range', 0, 20, initial=1)
    )
    dialogs['simple_input_form'] = Dialog.simple_input_form(
        'Simple Input Form',
        form,
        Dialog.submit_action('Shout', Dialog.custom_form('namespace1'))
    )
    dialogs['multi_action_input_form'] = Dialog.multi_action_input_form(
        'Multi Action Input Form',
        form, (
            Dialog.submit_action('Shout', tooltip='shout out', on_submit=Dialog.custom_form('namespace1')),
            Dialog.submit_action('Whisper', tooltip='whisper', on_submit=Dialog.custom_form('namespace2'))
        )
    )
    return
