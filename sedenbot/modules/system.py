# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from datetime import datetime
from shutil import which
from getpass import getuser
from operator import add, sub, mul, truediv, pow, xor, neg
from ast import (Add, Sub, Mult, Div, Pow, BitXor, USub,
                 parse, Num, BinOp, UnaryOp)

from pyrogram.raw.functions.help import GetNearestDc

from sedenbot.modules.lovers import saniye
from sedenbot.modules.ecem import ecem
from sedenbot import (HELP, ALIVE_MSG, CHANNEL,
                      BOT_VERSION, HOSTNAME, USER)
from sedenecem.core import (edit, reply, reply_doc, send_log,
                            extract_args, sedenify, get_translation)
# ================= CONSTANT =================
KULLANICIMESAJI = ALIVE_MSG or f"`{get_translation('sedenAlive')}`"
# ============================================


@sedenify(pattern='^.neofetch$')
def neofetch(message):
    try:
        from subprocess import PIPE, Popen
        islem = Popen(
            ['neofetch', f'HOSTNAME={HOSTNAME}', f'USER={USER}', '--stdout'],
            stdout=PIPE, stderr=PIPE)
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
             preview=False)
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
                reply_doc(message, 'pip3.txt', delete_after_send=True)
                return
            edit(message, get_translation(
                'sedenQuery', ['**', '`', pipsorgu, sonuc]))
        else:
            edit(message, get_translation('sedenQuery', [
                 '**', '`', pipsorgu, get_translation('sedenZeroResults')]))
    else:
        edit(message, f'`{get_translation("pipHelp")}`')


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
    edit(message, f'{KULLANICIMESAJI}')


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
    sonuc = client.send(GetNearestDc())

    edit(message, get_translation('sedenNearestDC', [
         '**', '`', sonuc.country, sonuc.nearest_dc, sonuc.this_dc]))


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
                  caption=f'`{get_translation("outputTooLarge")}`',
                  delete_after_send=True)
        return

    edit(
        message,
        f'`{curruser}:~{"#" if uid == 0 else "$"} {command}\n{sonuc}`')

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
                              caption=f'`{get_translation("outputTooLarge")}`',
                              delete_after_send=True)
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
    expr = expr.lower().replace('x', '*').replace(' ', '')
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


HELP.update({'system': get_translation('systemInfo')})
