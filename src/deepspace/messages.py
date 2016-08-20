'''Websocket messagees validators
'''

def is_valid_mouse_command(message_object):
    'check all fields for mouse command'
    try:
        if message_object["command"] != "mouse_click":
            return False
        if message_object["button"] not in (1,2,3):
            return False
        if message_object["x"] is None:
            return False
        if message_object["y"] is None:
            return False

    except BaseException:
        return False

    return True

    