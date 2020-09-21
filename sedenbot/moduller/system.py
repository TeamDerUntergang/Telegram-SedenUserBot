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

from os import execl, remove
from datetime import datetime
from shutil import which
from getpass import getuser
from sys import executable, argv
from operator import add, sub, mul, truediv, pow, xor, neg
from ast import Add, Sub, Mult, Div, Pow, BitXor, USub, parse, Num, BinOp, UnaryOp
from requests import get
from math import floor
from heroku3 import from_key

from sedenbot.moduller.lovers import saniye
from sedenbot.moduller.ecem import ecem
from sedenbot import KOMUT, ALIVE_MESAJI, BOT_VERSION, CHANNEL, HEROKU_KEY, HEROKU_APPNAME
from sedenecem.core import edit, reply, reply_doc, send_log, extract_args, sedenify, get_translation
# ================= CONSTANT =================
KULLANICIMESAJI = ALIVE_MESAJI or get_translation('sedenAlive')
# ============================================


@sedenify(pattern='^.neofetch$')
def neofetch(message):
    try:
        from subprocess import PIPE, Popen
        islem = Popen(['neofetch', '--stdout'], stdout=PIPE, stderr=PIPE)
        sonuc, _ = islem.communicate()
        edit(message, sonuc.decode(), parse=None)
    except BaseException:
        edit(message, f'`{get_translation("neofetchNotFound")}`')


@sedenify(pattern='^.botver$')
def botver(message):
    if which('git'):
        from subprocess import PIPE, Popen
        degisiklik = Popen(['git', 'rev-list', '--all', '--count'],
                           stdout=PIPE, stderr=PIPE, universal_newlines=True)
        sonuc, _ = degisiklik.communicate()

        edit(message,
             get_translation('sedenShowBotVersion',
                             ['**',
                              '`',
                              'Seden UserBot',
                              CHANNEL,
                              BOT_VERSION,
                              sonuc]),
             preview=False,
             fix_markdown=True)
    else:
        edit(message, f'`{get_translation("sedenGitNotFound")}`')


@sedenify(pattern='^.pip')
def pip3(message):
    pipmodule = extract_args(message)
    if len(pipmodule) > 0:
        edit(message, f'`{get_translation("pipSearch")}`')
        pipsorgu = f"pip3 search {pipmodule}"
        from subprocess import PIPE, Popen
        islem = Popen(pipsorgu.split(), stdout=PIPE,
                      stderr=PIPE, universal_newlines=True)
        sonuc, _ = islem.communicate()

        if sonuc:
            if len(sonuc) > 4096:
                edit(message, f'`{get_translation("outputTooLarge")}`')
                file = open('pip3.txt', 'w+')
                file.write(sonuc)
                file.close()
                reply_doc(message, 'pip3.txt')
                remove('pip3.txt')
                return
            edit(message, get_translation(
                'sedenQuery', ['**', '`', pipsorgu, sonuc]))
        else:
            edit(message, get_translation('sedenQuery', [
                 '**', '`', pipsorgu, get_translation('sedenZeroResults')]))
    else:
        edit(message, f'`{get_translation("pipHelp")}`')


@sedenify(pattern='^.(restart|yb)$', compat=False)
def _restart(client, message):
    return restart(client, message)


def restart(client, message):
    edit(message, f'`{get_translation("restart")}`')
    send_log(f'{get_translation("restartLog")}')
    try:
        client.stop()
    except Exception as e:
        pass
    execl(executable, executable, *argv)


@sedenify(pattern='^.(shutdown|kapat)$', compat=False)
def shutdown(client, message):
    edit(message, f'`{get_translation("shutdown")}`')
    send_log(f'{get_translation("shutdownLog")}')
    try:
        client.stop()
    except Exception as e:
        pass


@sedenify(pattern='^.ping$')
def ping(message):
    basla = datetime.now()
    edit(message, '`Pong!`')
    bitir = datetime.now()
    sure = (bitir - basla).microseconds / 1000
    edit(message, f'`Pong!\n{sure}ms`')


@sedenify(pattern='^.alive$')
def alive(message):
    if KULLANICIMESAJI.lower() == 'ecem':
        ecem(message)
        return
    elif KULLANICIMESAJI.lower() == 'saniye':
        saniye(message)
        return
    edit(message, f'`{KULLANICIMESAJI}`')


@sedenify(pattern='^.alives')
def alives(message):
    alives = extract_args(message)
    sonuc = f'`{get_translation("alivesUsage")}`'
    if len(alives) > 0:
        global KULLANICIMESAJI
        KULLANICIMESAJI = alives
        sonuc = get_translation('sedenSetAlive', [KULLANICIMESAJI])
    edit(message, '`' f'{sonuc}' '`')


@sedenify(pattern='^.resalive$')
def resalive(message):
    global KULLANICIMESAJI
    KULLANICIMESAJI = ALIVE_MESAJI or get_translation('sedenAlive')
    edit(message, f'`{get_translation("aliveReset")}`')


@sedenify(pattern='^.echo')
def echo(message):
    args = extract_args(message)
    if len(args) > 0:
        message.delete()
        reply(message, args)
    else:
        edit(message, f'`{get_translation("echoHelp")}`')


@sedenify(pattern='^.dc$', compat=False)
def dc(client, message):
    sonuc = client.send(functions.help.GetNearestDc())

    edit(message, get_translation('sedenNearestDC', [
         '**', '`', sonuc.country, sonuc.nearest_dc, sonuc.this_dc]))

# Copyright (c) @NaytSeyd, @frknkrc44 | 2020


@sedenify(pattern='^.term')
def terminal(message):
    command = extract_args(message)

    if len(command) < 1:
        edit(message, f'`{get_translation("termUsage")}`')
        return

    curruser = getuser()
    try:
        from os import geteuid
        uid = geteuid()
    except ImportError:
        uid = 0

    if not command:
        edit(message, f'`{get_translation("termHelp")}`')
        return

    sonuc = f'`{get_translation("termNoResult")}`'
    try:
        from subprocess import getoutput
        sonuc = getoutput(command)
    except BaseException:
        pass

    if len(sonuc) > 4096:
        output = open('output.txt', 'w+')
        output.write(sonuc)
        output.close()
        reply_doc(message, 'output.txt',
                  caption=f'`{get_translation("outputTooLarge")}`')
        remove('output.txt')
        return

    edit(
        message,
        f'`{curruser}:~{"#" if uid == 0 else "$"} {command}\n{sonuc}`',
        fix_markdown=True)

    send_log(get_translation('termLog', [command]))


@sedenify(pattern='^.eval')
def eval(message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, f'`{get_translation("evalUsage")}`')
        return

    try:
        evaluation = safe_eval(args)
        if evaluation:
            if isinstance(evaluation, str):
                if len(evaluation) >= 4096:
                    file = open('output.txt', 'w+')
                    file.write(evaluation)
                    file.close()
                    reply_doc(message,
                              'output.txt',
                              caption=f'`{get_translation("outputTooLarge")}`')
                    remove('output.txt')
                    return
                edit(message, get_translation(
                    'sedenQuery', ['**', '`', args, evaluation]))
        else:
            edit(message, get_translation('sedenQuery', [
                 '**', '`', args, get_translation('sedenErrorResult')]))
    except Exception as err:
        edit(message, get_translation(
            'sedenQuery', ['**', '`', args, str(err)]))

    send_log(get_translation('evalLog', [args]))


operators = {Add: add, Sub: sub, Mult: mul,
             Div: truediv, Pow: pow, BitXor: xor,
             USub: neg}


def safe_eval(expr):
    expr = expr.lower().replace("x", "*").replace(" ", "")
    return str(_eval(parse(expr, mode='eval').body))


def _eval(node):
    if isinstance(node, Num):
        return node.n
    elif isinstance(node, BinOp):
        return operators[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, UnaryOp):
        return operators[type(node.op)](_eval(node.operand))
    else:
        raise TypeError(f'`{get_translation("safeEval")}`')


@sedenify(pattern='^.quota$')
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


KOMUT.update({"neofetch": get_translation("neofetchInfo")})
KOMUT.update({"botver": get_translation("botverInfo")})
KOMUT.update({"pip": get_translation("pipInfo")})
KOMUT.update({"dc": get_translation("dcInfo")})
KOMUT.update({"restart": get_translation("restartInfo")})
KOMUT.update({"shutdown": get_translation("shutdownInfo")})
KOMUT.update({"ping": get_translation("pingInfo")})
KOMUT.update({"echo": get_translation("echoInfo")})
KOMUT.update({"eval": get_translation("evalInfo")})
KOMUT.update({"term": get_translation("termInfo")})
KOMUT.update({"alive": get_translation("aliveInfo")})
KOMUT.update({"quota": get_translation("herokuInfo")})
