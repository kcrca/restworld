from pynecraft.simpler import Dialog, Item
from restworld.world import restworld


def create():
    dialogs = restworld.registry('dialog')

    # action = {'label': {'text': 'action2'}, 'id': '123',
    #           'on_submit': {'type': 'custom_form', 'id': '345', 'key': 'bbb'}}
    # actions = [action]
    # inputs = [{'type': 'text', 'key': 'aaa', 'label': {'text': 'action1'}}]
    #
    # types = {
    #     'notice': {
    #         'body': [{'type': 'plain_message', 'contents': {'text': 'My hovercraft is full of eels.'}}]
    #     },
    #     'confirmation': {
    #         'body': [
    #             {'type': 'item', 'item': {'id': 'cake', 'Count': 1}, 'show_decoration': True, 'show_tooltip': True,
    #              'description': {'contents': {'text': 'The Cake'}}},
    #             {'type': 'plain_message', 'contents': {'text': 'Is the cake a lie?'}}],
    #         'yes': {'label': {'text': 'Yes!'}}, 'no': {'label': {'text': 'Nooooo!!!!!!'}}
    #     },
    #     'multi_action': {
    #         'actions': list(
    #             {'label': {'text': f'Choice #{i}'}, 'id': 'foo',
    #              'on_submit': {'type': 'custom_form', 'id': i, 'key': i}} for i
    #             in range(32))
    #     }, 'server_links': {},
    #     'dialog_list': {
    #         'dialogs': [{'type': 'notice', 'title': f'Notice {i}',
    #                      'body': {'type': 'plain_message', 'contents': {'text': f'{i} bottles of beer on the wall'}}}
    #                     for i in range(32)]},
    #     'simple_input_form': {'inputs': [{'type': 'text', 'key': 'text'}], 'action': action},
    #     'multi_action_input_form': {'inputs': inputs, 'actions': actions}
    # }
    #
    # # for d in types:
    # #     title = f'{to_name(d)} Dialog'
    # #     dialogs[d] = custom_dialog(d, title, title, [], types[d])

    dialogs['notice'] = Dialog.notice('Notice', [Dialog.plain_message('My hovercraft is full of eels.')])
    dialogs['confirmation'] = Dialog.confirmation(
        'Confirmation',
        Dialog.click_action('Yes!'),
        Dialog.click_action('Nooooo!!!!!!'),
        body=[
            Dialog.item(Item.nbt_for('cake'), show_decoration=True, show_tooltip=True),
            Dialog.plain_message('Is the cake a lie?')
        ])
    dialogs['multi_action'] = Dialog.multi_action(
        'Multi Action',
        [Dialog.click_action(f'Choice #{i}') for i in range(32)])
    dialogs['dialog_list'] = Dialog.dialog_list(
        'Dialog List',
        [Dialog.notice(f'I said: "{i} BOTTLES OF BEER!!!"') for i in range(32)])
    dialogs['simple_input_form'] = Dialog.simple_input_form(
        'Simple Input Form',
        [Dialog.text('Marco', 'Polo'), Dialog.boolean("I think I'm lost")],
        Dialog.submit_action('Shout', Dialog.custom_form('namespace1'))
    )
    dialogs['multi_action_input_form'] = Dialog.multi_action_input_form(
        'Multi Action Input Form',
        [Dialog.text('Marco', 'Polo'), Dialog.boolean("I think I'm lost")],
        [(Dialog.submit_action('Shout', tooltip='shout out', on_submit=Dialog.custom_form('namespace1'))),
         (Dialog.submit_action('Whisper', tooltip='whisper', on_submit=Dialog.custom_form('namespace2')))]
    )
    return
