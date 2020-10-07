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

from os import execl
from sys import executable, argv
from requests import get
from math import floor
from heroku3 import from_key

from sedenbot import KOMUT, HEROKU_KEY, HEROKU_APPNAME
from sedenecem.core import edit, sedenify, get_translation, send_log, reply_doc


@sedenify(pattern='^.(quota|kota)$')
def dyno(message):
    if not HEROKU_KEY:
        edit(message, f"`{get_translation('notHeroku')}`")
        return

    edit(message, f"`{get_translation('processing')}`")

    heroku = from_key(HEROKU_KEY)
    heroku_app = None
    heroku_applications = heroku.apps()
    if not HEROKU_APPNAME:
        edit(
            message,
            f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')

    for app in heroku_applications:
        if app.name == HEROKU_APPNAME:
            heroku_app = app
            break

    if heroku_app is None:
        edit(
            message,
            f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')
        return

    acc_id = heroku.account().id

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Authorization': f'Bearer {HEROKU_KEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }

    req = get(
        f'https://api.heroku.com/accounts/{acc_id}/actions/get-quota',
        headers=headers)

    if req.status_code != 200:
        edit(message, f"`{get_translation('covidError')}`")
        return

    json = req.json()

    acc_quota = json['account_quota']
    acc_quota_used = json['quota_used']
    acc_quota_remaining = acc_quota - acc_quota_used
    acc_quota_percent = floor(acc_quota_used / acc_quota * 100)
    acc_quota_rem_percent = 100 - acc_quota_percent

    def get_app_quota():
        for app in json['apps']:
            if app['app_uuid'] == heroku_app.id:
                return app['quota_used']
        return 0

    app_quota = get_app_quota()
    app_quota_percent = floor(app_quota / acc_quota * 100)
    app_quota = app_quota / 60
    app_quota_hrs = int(app_quota / 60)
    app_quota_min = int(app_quota % 60)

    acc_remaining = acc_quota_remaining / 60
    acc_remaining_hrs = int(acc_remaining / 60)
    acc_remaining_min = int(acc_remaining % 60)

    acc_total = acc_quota / 60
    acc_total_hrs = int(acc_total / 60)
    acc_total_min = int(acc_total % 60)

    acc_used = acc_quota_used / 60
    acc_used_hrs = int(acc_used / 60)
    acc_used_min = int(acc_used % 60)

    edit(
        message,
        get_translation(
            'herokuQuotaInfo',
            ['`', '**',
             get_translation(
                 'herokuQuotaInHM', [acc_total_hrs, acc_total_min]),
             get_translation(
                 'herokuQuotaInHM', [acc_used_hrs, acc_used_min]),
             acc_quota_percent,
             get_translation(
                 'herokuQuotaInHM', [acc_remaining_hrs, acc_remaining_min]),
             acc_quota_rem_percent,
             get_translation(
                 'herokuQuotaInHM', [app_quota_hrs, app_quota_min]),
             app_quota_percent]))


@sedenify(pattern='^.(restart|yb)$', compat=False)
def _restart(client, message):
    return restart(client, message)


@sedenify(pattern='^.d(restart|yb)$', compat=False)
def _drestart(client, message):
    return restart(client, message, dyno=True)


def restart(client, message, dyno=False):
    send_log(f'{get_translation("restartLog")}')

    def std_off():
        try:
            client.stop()
        except Exception as e:
            pass

    def std_ret():
        edit(message, f'`{get_translation("restart")}`')
        std_off()
        execl(executable, executable, *argv)

    if not HEROKU_KEY or not dyno:
        std_ret()
        return

    heroku = from_key(HEROKU_KEY)
    heroku_app = None
    heroku_applications = heroku.apps()
    if not HEROKU_APPNAME:
        edit(
            message,
            f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')
        std_ret()
        return

    for app in heroku_applications:
        if app.name == HEROKU_APPNAME:
            heroku_app = app
            break

    if heroku_app is None:
        edit(
            message,
            f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')
        std_ret()
        return

    edit(message, f'`{get_translation("restart")}`')
    std_off()
    dynos = heroku_app.dynos()
    dynos[0].restart()


@sedenify(pattern='^.(shutdown|kapat)$', compat=False)
def shutdown(client, message):
    edit(message, f'`{get_translation("shutdown")}`')
    send_log(f'{get_translation("shutdownLog")}')

    def std_off():
        try:
            client.stop()
        except Exception as e:
            pass

    if not HEROKU_KEY:
        std_off()
        return

    heroku = from_key(HEROKU_KEY)
    heroku_app = None
    heroku_applications = heroku.apps()
    if not HEROKU_APPNAME:
        edit(
            message,
            f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')
        std_off()
        return

    for app in heroku_applications:
        if app.name == HEROKU_APPNAME:
            heroku_app = app
            break

    if heroku_app is None:
        edit(
            message,
            f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')
        std_off()
        return

    std_off()
    heroku_app.scale_formation_process('seden', 0)


@sedenify(pattern='^.logs$')
def dyno(message):
    if not HEROKU_KEY:
        edit(message, f"`{get_translation('notHeroku')}`")
        return

    edit(message, f"`{get_translation('processing')}`")

    heroku = from_key(HEROKU_KEY)
    heroku_app = None
    heroku_applications = heroku.apps()
    if not HEROKU_APPNAME:
        edit(
            message,
            f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')

    for app in heroku_applications:
        if app.name == HEROKU_APPNAME:
            heroku_app = app
            break

    if heroku_app is None:
        edit(
            message,
            f'`{get_translation("updateHerokuVariables", ["HEROKU_APPNAME "])}`')
        return

    filename = 'seden_heroku_log.txt'

    with open(filename, 'w+') as log:
        log.write(heroku_app.get_log())

    reply_doc(message, filename)


KOMUT.update({"heroku": get_translation("herokuInfo")})
KOMUT.update({"restart": get_translation("restartInfo")})
KOMUT.update({"shutdown": get_translation("shutdownInfo")})
