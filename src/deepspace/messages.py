'''Websocket messagees validators
'''

def is_valid_mouse_command(message_object):
    'check all fields for mouse command'
    try:
        if (message_object["command"] != "mouse_click"
            ) or (
            message_object["button"] not in (1,2,3)
            ) or (
            message_object["x"] is None
            ) or (
            message_object["y"] is None):
            return False

    except BaseException:
        return False

    return True


def is_valid_upd_display_command(message_object):
    'check all fields for upd_display_size command'
    try:
        if (message_object["command"] != "upd_display_size"
            ) or (
            message_object["display_x"] is None
            ) or (
            message_object["display_y"] is None):
            return False

    except BaseException:
        return False

    return True
    