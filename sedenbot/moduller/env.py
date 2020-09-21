# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from time import sleep
from heroku3 import from_key

from sedenbot.moduller.system import restart
from sedenbot import KOMUT, HEROKU_KEY, HEROKU_APPNAME, set_local_env, unset_local_env, environ, reload_env, ENV_RESTRICTED_KEYS
from sedenecem.core import edit, sedenify, extract_args, get_translation


@sedenify(pattern='^.env', compat=False)
def manage_env(client, message):
    action = extract_args(message).split(' ', 1)

    if len(action) < 2 or action[0] not in ['get', 'set', 'rem']:
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
                ups,
                f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                heroku_env = app.config()
                break
        if heroku_app is None:
            edit(
                ups,
                f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')
            return

    reload_env()

    if action[0] == 'set':
        items = action[1].split(' ', 1)

        if len(items) < 2 or len(
                items[1]) < 1 or items[0] in ENV_RESTRICTED_KEYS:
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

        if len(items[0]) < 1 or items[0] in ENV_RESTRICTED_KEYS:
            edit(message, f"`{get_translation('wrongCommand')}`")
            return

        items[0] = items[0].upper()

        if heroku_mode and items[0] in heroku_env:
            value = heroku_env[items[0]]
        elif not heroku_mode and (value := environ.get(items[0], None)):
            pass
        else:
            edit(
                message, get_translation(
                    'envNotFound', [
                        '`', '**', items[0]]))
            return

        edit(
            message, get_translation(
                'envGetValue', [
                    '`', '**', items[0], value]))
    elif action[0] == 'rem':
        items = action[1].split(' ', 1)

        if len(items[0]) < 1 or items[0] in ENV_RESTRICTED_KEYS:
            edit(message, f"`{get_translation('wrongCommand')}`")
            return

        items[0] = items[0].upper()

        if heroku_mode and items[0] in heroku_env:
            del heroku_env[items[0]]
        elif not heroku_mode and (value := environ.get(items[0], None)):
            unset_local_env(items[0])
        else:
            edit(
                message, get_translation(
                    'envNotFound', [
                        '`', '**', items[0]]))
            return

        edit(message, get_translation('envRemSuccess', ['`', '**', items[0]]))
        sleep(2)
        restart(client, message)


KOMUT.update({"env": get_translation("envInfo")})
