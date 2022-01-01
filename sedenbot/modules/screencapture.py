# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from base64 import b64decode
from re import match
from time import sleep

from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    get_webdriver,
    reply_doc,
    sedenify,
)


@sedenify(pattern='^.ss')
def screenshot(message):
    input_str = extract_args(message)
    reply = message.reply_to_message
    link_match = match(r'\bhttp(.*)?://.*\.\S+', input_str)
    if link_match:
        link = link_match.group()
    else:
        edit(message, f'`{get_translation("ssUsage")}`')
        return
    edit(message, f'`{get_translation("processing")}`')
    driver = get_webdriver()
    driver.get(link)
    height = driver.execute_script(
        'return Math.max(document.body.scrollHeight,'
        'document.body.offsetHeight,'
        'document.documentElement.clientHeight,'
        'document.documentElement.scrollHeight,'
        'document.documentElement.offsetHeight);'
    )
    width = driver.execute_script(
        'return Math.max(document.body.scrollWidth,'
        'document.body.offsetWidth,'
        'document.documentElement.clientWidth,'
        'document.documentElement.scrollWidth,'
        'document.documentElement.offsetWidth);'
    )
    driver.set_window_size(width + 125, height + 125)
    wait_for = int(height / 1000)
    edit(message, f'`{get_translation("ssResult", [height, width, wait_for])}`')
    sleep(wait_for)
    im_png = driver.get_screenshot_as_base64()
    driver.close()
    name = 'screenshot.png'
    with open(name, 'wb') as out:
        out.write(b64decode(im_png))
    edit(message, f'`{get_translation("ssUpload")}`')
    reply_doc(reply or message, name, caption=input_str, delete_after_send=True)
    message.delete()


HELP.update({'ss': get_translation('ssInfo')})
