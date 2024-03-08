# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import path, remove
from time import sleep
from urllib.parse import quote_plus

from gtts import gTTS
from selenium.webdriver.common.by import By

from sedenbot import HELP, SEDEN_LANG
from sedenecem.core import (
    edit,
    extract_args,
    extract_args_split,
    get_translation,
    get_webdriver,
    reply_doc,
    reply_voice,
    sedenify,
    send_log,
)

CARBONLANG = 'auto'
TTS_LANG = SEDEN_LANG
TRT_LANG = SEDEN_LANG


@sedenify(pattern='^.crblang')
def carbonlang(message):
    global CARBONLANG
    CARBONLANG = extract_args(message)
    edit(message, get_translation('carbonLang', ['**', CARBONLANG]))


@sedenify(pattern='^.carbon')
def carbon(message):
    match = extract_args(message)
    if len(match) < 1:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return
    edit(message, f'`{get_translation("processing")}`')
    reply = message.reply_to_message
    pcode = message.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif reply:
        pcode = str(reply.message)
    code = quote_plus(pcode)
    global CARBONLANG
    CARBON = f'https://carbon.now.sh/?l={CARBONLANG}&code={code}'
    edit(message, f'`{get_translation("processing")}\n%25`')
    if path.isfile('./carbon.png'):
        remove('./carbon.png')
    driver = get_webdriver()
    driver.get(CARBON)
    edit(message, f'`{get_translation("processing")}\n%50`')
    driver.command_executor._commands['send_command'] = (
        'POST',
        '/session/$sessionId/chromium/send_command',
    )
    driver.find_element(By.XPATH, "//button[contains(text(),'Export')]").click()
    edit(message, f'`{get_translation("processing")}\n%75`')
    while not path.isfile('./carbon.png'):
        sleep(0.5)
    edit(message, f'`{get_translation("processing")}\n%100`')
    file = './carbon.png'
    edit(message, f'`{get_translation("carbonUpload")}`')
    reply_doc(
        reply if reply else message,
        file,
        caption=get_translation('carbonResult'),
        delete_after_send=True,
    )
    message.delete()
    driver.quit()


HELP.update({'carbon': get_translation('carbonInfo')})
