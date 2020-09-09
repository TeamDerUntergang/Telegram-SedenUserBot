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
from base64 import b64decode
from re import match

from sedenbot import KOMUT
from sedenecem.core import edit, reply_doc, extract_args, sedenify, get_webdriver, get_translation


@sedenify(pattern=r'^.ss')
def ss(message):
    input_str = extract_args(message)
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
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
    )
    width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
    )
    driver.set_window_size(width + 125, height + 125)
    wait_for = int(height / 1000)
    edit(
        message, f'`{get_translation("ssResult", [height, width, wait_for])}`')
    sleep(wait_for)
    im_png = driver.get_screenshot_as_base64()
    # Sayfanın ekran görüntüsü kaydedilir.
    driver.close()
    message_id = message.message_id
    if message.reply_to_message:
        message_id = message.reply_to_message
    name = 'screenshot.png'
    with open(name, 'wb') as out:
        out.write(b64decode(im_png))
    edit(message, f'`{get_translation("ssUpload")}`')
    reply_doc(message, name, caption=input_str, delete_after_send=True)


KOMUT.update({"ss": get_translation("ssInfo")})
