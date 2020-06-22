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

import time

from base64 import b64decode
from re import match
from os.path import exists
from os import remove

from sedenbot import KOMUT
from sedenecem.events import edit, reply_doc, extract_args, sedenify, get_webdriver

@sedenify(pattern=r'^.ss')
def ss(message):
    input_str = extract_args(message)
    link_match = match(r'\bhttp(.*)?://.*\.\S+', input_str)
    if link_match:
        link = link_match.group()
    else:
        edit(message, '`Ekran görüntüsü alabilmem için geçerli bir bağlantı vermelisin.`')
        return
    edit(message, '`İşleniyor ...`')
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
    edit(message, f'`Sayfanın ekran görüntüsü oluşturuluyor ...`\
    \n`Sayfanın yüksekliği: {height} piksel`\
    \n`Sayfanın genişliği: {width} piksel`\
    \n`Sayfanın yüklenmesi için {wait_for} saniye beklendi.`')
    time.sleep(wait_for)
    im_png = driver.get_screenshot_as_base64()
    # Sayfanın ekran görüntüsü kaydedilir.
    driver.close()
    message_id = message.message_id
    if message.reply_to_message:
        message_id = message.reply_to_message
    name = 'ekran_goruntusu.png'
    with open(name, 'wb') as out:
        out.write(b64decode(im_png))
    edit(message, '`Ekran görüntüsü karşıya yükleniyor ...`')
    reply_doc(message, name, caption=input_str, delete_after_send=True)

KOMUT.update({
    "ss":
    ".ss <url>\
    \nKullanım: Belirtilen web sitesinden bir ekran görüntüsü alır ve gönderir.\
    \nGeçerli bir site bağlantısı örneği: `https://devotag.com`"
})
