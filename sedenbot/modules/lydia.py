# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep
from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API

from sedenbot import HELP, LOGS, LYDIA_APIKEY
from sedenecem.core import sedenify, edit, reply, get_translation


def lydia_init():
    try:
        global sql
        from importlib import import_module
        sql = import_module('sedenecem.sql.lydia_sql')
    except Exception as e:
        sql = None
        LOGS.warn(get_translation('lydiaSqlLog'))
        raise e


lydia_init()

ACC_LYDIA = {}

if LYDIA_APIKEY:
    api_key = LYDIA_APIKEY
    api_client = API(api_key)
    lydia = LydiaAI(api_client)


@sedenify(pattern='^.repcf')
def repcf(message):
    if not LYDIA_APIKEY:
        return edit(
            message, get_translation(
                'lydiaMissingApi', [
                    '**', '`']), preview=False)
    edit(message, f'`{get_translation("processing")}`')
    try:
        session = lydia.create_session()
        reply = message.reply_to_message
        msg = reply.text
        text_rep = session.think_thought(msg)
        edit(message, get_translation('lydiaResult', ['**', text_rep]))
    except Exception as e:
        edit(message, str(e))


@sedenify(pattern='^.addcf')
def addcf(message):
    if not LYDIA_APIKEY:
        return edit(
            message, get_translation(
                'lydiaMissingApi', [
                    '**', '`']), preview=False)
    edit(message, f'`{get_translation("processing")}`')
    sleep(3)
    reply_msg = message.reply_to_message
    if reply_msg:
        session = lydia.create_session()
        session_id = session.id
        if not reply_msg.from_user.id:
            return edit(message, f'`{get_translation("lydiaError")}`')
        ACC_LYDIA.update({(message.chat.id & reply_msg.from_user.id): session})
        edit(
            message,
            get_translation(
                'lydiaResult2',
                ['**', '`', str(reply_msg.from_user.id),
                 str(message.chat.id)]))
    else:
        edit(message, f'`{get_translation("lydiaError2")}`')


@sedenify(pattern='^.remcf')
def remcf(message):
    if not LYDIA_APIKEY:
        return edit(
            message, get_translation(
                'lydiaMissingApi', [
                    '**', '`']), preview=False)
    edit(message, f'`{get_translation("processing")}`')
    sleep(3)
    reply_msg = message.reply_to_message
    try:
        del ACC_LYDIA[message.chat.id & reply_msg.from_user.id]
        edit(
            message,
            get_translation(
                'lydiaResult3',
                ['**', '`', str(reply_msg.from_user.id),
                 str(message.chat.id)]))
    except Exception:
        edit(message, f'`{get_translation("lydiaError3")}`')


@sedenify(incoming=True,
          outgoing=False,
          disable_edited=True,
          disable_notify=True)
def user(message):
    user_text = message.text
    try:
        session = ACC_LYDIA[message.chat.id & message.from_user.id]
        msg = message.text
        message.reply_chat_action('typing')
        text_rep = session.think_thought(msg)
        wait_time = 0
        for i in range(len(text_rep)):
            wait_time = wait_time + 0.1
        sleep(wait_time)
        reply(message, text_rep)
    except BaseException:
        pass

    message.continue_propagation()

HELP.update({'lydia': get_translation('lydiaInfo')})
