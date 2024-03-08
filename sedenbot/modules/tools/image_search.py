# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from mimetypes import guess_type
from os import remove
from random import choice
from re import findall
from time import sleep

from pyrogram.types import InputMediaPhoto
from requests import get
from selenium.webdriver.common.by import By
from sedenbot import HELP

from sedenecem.core import (
    edit,
    extract_args,
    get_translation,
    get_webdriver,
    google_domains,
    reply_doc,
    sedenify,
)


@sedenify(pattern='^.img')
def img(message):
    query = extract_args(message)
    lim = findall(r'lim=\d+', query)
    try:
        lim = lim[0]
        lim = lim.replace('lim=', '')
        query = query.replace('lim=' + lim[0], '')
        lim = int(lim)
        if lim > 10:
            lim = 10
    except IndexError:
        lim = 3

    if len(query) < 1:
        edit(message, f'`{get_translation("imgUsage")}`')
        return
    edit(message, f'`{get_translation("processing")}`')

    url = f'https://{choice(google_domains)}/search?tbm=isch&q={query}&gbv=2&sa=X&biw=1920&bih=1080'
    driver = get_webdriver()
    driver.get(url)
    count = 1
    files = []
    for i in driver.find_elements(
        By.XPATH, '//div[contains(@class,"isv-r PNCib MSM1fd BUooTd")]'
    ):
        i.click()
        try_count = 0
        while (
            len(
                element := driver.find_elements(
                    By.XPATH,
                    '//img[contains(@class,"n3VNCb") and contains(@src,"http")]',
                )
            )
            < 1
            and try_count < 20
        ):
            try_count += 1
            sleep(0.1)
        if len(element) < 1:
            continue
        link = element[0].get_attribute('src')
        filename = f'result_{count}.jpg'
        try:
            with open(filename, 'wb') as result:
                result.write(get(link).content)
            ftype = guess_type(filename)
            if not ftype[0] or ftype[0].split('/')[1] not in ['png', 'jpg', 'jpeg']:
                remove(filename)
                continue
        except Exception:
            continue
        files.append(InputMediaPhoto(filename))
        sleep(1)
        elements = driver.find_elements(By.XPATH, '//a[contains(@class,"hm60ue")]')
        for element in elements:
            element.click()
        count += 1
        if lim < count:
            break
        sleep(1)

    driver.quit()

    reply_doc(message, files, delete_orig=True, delete_after_send=True)


HELP.update({'img': get_translation('imgInfo')})
