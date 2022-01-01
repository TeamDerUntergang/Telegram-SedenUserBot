# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep

from dotenv import dotenv_values
from heroku3 import from_key
from sedenbot import (
    ENV_RESTRICTED_KEYS,
    HELP,
    HEROKU_APPNAME,
    HEROKU_KEY,
    environ,
    reload_env,
    set_local_env,
    unset_local_env,
)
from sedenbot.modules.horeke import restart
from sedenecem.core import edit, extract_args, get_translation, sedenify


@sedenify(pattern='^.env', compat=False)
def manage_env(client, message):
    action = extract_args(message).split(' ', 1)

    if action[0] == 'list':
        pass
    elif len(action) < 2 or action[0] not in ['get', 'set', 'rem', 'copy', 'move']:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return

    heroku_mode = False

    if HEROKU_KEY:
        heroku_mode = True
        heroku = from_key(HEROKU_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            edit(
                message,
                f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`',
            )
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                heroku_env = app.config()
                break
        if heroku_app is None:
            edit(
                message,
                f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`',
            )
            return

    reload_env()

    if action[0] == 'set':
        items = action[1].split(' ', 1)

        if (
            len(items) < 2
            or len(items[1]) < 1
            or items[0].upper() in ENV_RESTRICTED_KEYS
        ):
            edit(message, f"`{get_translation('wrongCommand')}`")
            return

        key, value = items

        key = key.upper()

        if heroku_mode:
            heroku_env[key] = value
        else:
            set_local_env(key, value)

        edit(message, get_translation('envSetSuccess', ['`', '**', key]))
        sleep(2)
        restart(client, message)
    elif action[0] == 'get':
        items = action[1].split(' ', 1)

        if len(items[0]) < 1 or items[0].upper() in ENV_RESTRICTED_KEYS:
            edit(message, f"`{get_translation('wrongCommand')}`")
            return

        items[0] = items[0].upper()

        if heroku_mode and items[0] in heroku_env:
            value = heroku_env[items[0]]
        elif not heroku_mode and (value := environ.get(items[0], None)):
            pass
        else:
            edit(message, get_translation('envNotFound', ['`', '**', items[0]]))
            return

        edit(message, get_translation('envGetValue', ['`', '**', items[0], value]))
    elif action[0] == 'rem':
        items = action[1].split(' ', 1)

        if len(items[0]) < 1 or items[0].upper() in ENV_RESTRICTED_KEYS:
            edit(message, f"`{get_translation('wrongCommand')}`")
            return

        items[0] = items[0].upper()

        if heroku_mode and items[0] in heroku_env:
            del heroku_env[items[0]]
        elif not heroku_mode and (value := environ.get(items[0], None)):
            unset_local_env(items[0])
        else:
            edit(message, get_translation('envNotFound', ['`', '**', items[0]]))
            return

        edit(message, get_translation('envRemSuccess', ['`', '**', items[0]]))
        sleep(2)
        restart(client, message)
    elif action[0] in ['copy', 'move']:
        items = action[1].split(' ', 1)

        if (
            len(items) < 2
            or len(items[0]) < 1
            or items[0].upper() in ENV_RESTRICTED_KEYS
            or items[1].upper() in ENV_RESTRICTED_KEYS
            or items[0].upper() == items[1].upper()
        ):
            edit(message, f"`{get_translation('wrongCommand')}`")
            return

        items[0] = items[0].upper()
        items[1] = items[1].upper()

        if heroku_mode and items[0] in heroku_env:
            value = heroku_env[items[0]]
        elif not heroku_mode and (value := environ.get(items[0], None)):
            pass
        else:
            edit(message, get_translation('envNotFound', ['`', '**', items[0]]))
            return

        if heroku_mode:
            heroku_env[items[1]] = value
        else:
            set_local_env(items[1], value)

        if action[0] == 'move':
            if heroku_mode and items[0] in heroku_env:
                del heroku_env[items[0]]
            elif not heroku_mode and (value := environ.get(items[0], None)):
                unset_local_env(items[0])
            edit(
                message,
                get_translation('envMoveSuccess', ['`', '**', items[0], items[1]]),
            )
            sleep(2)
            restart(client, message)
            return

        edit(
            message, get_translation('envCopySuccess', ['`', '**', items[0], items[1]])
        )
        sleep(2)
        restart(client, message)
    elif action[0] == 'list':
        out = ''
        if heroku_mode:
            horeke = heroku_env.to_dict()
            for i in horeke.keys():
                if i not in ENV_RESTRICTED_KEYS:
                    out += f'%1•%1  %2{i.replace("%", "½")}%2\n'
        else:
            keys = dotenv_values('config.env').keys()
            keys = sorted([x for x in keys if x.upper() not in ENV_RESTRICTED_KEYS])
            for i in keys:
                out += f'%1•%1  %2{i.replace("%", "½")}%2\n'

        edit(message, get_translation('envListKeys', ['**', '`', out]))


HELP.update({'env': get_translation('envInfo')})
