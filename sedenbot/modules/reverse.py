# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import path, remove
from re import I, M, findall
from urllib import parse, request

from bs4 import BeautifulSoup
from PIL import Image
from pyrogram.types import InputMediaPhoto
from requests import get, post
from sedenbot import HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_translation,
    reply_doc,
    sedenify,
)

opener = request.build_opener()
useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4464.5 Safari/537.36'
opener.addheaders = [('User-agent', useragent)]


@sedenify(pattern='^.reverse$')
def reverse(message):
    photo = 'reverse.png'
    if path.isfile(photo):
        remove(photo)

    reverse = message.reply_to_message
    revfile = None
    if reverse and reverse.media:
        revfile = download_media_wc(reverse, photo)
    else:
        edit(message, f'`{get_translation("reverseUsage")}`')
        return

    if photo:
        edit(message, f'`{get_translation("processing")}`')
        try:
            image = Image.open(revfile)
        except OSError:
            edit(message, f'`{get_translation("reverseError")}`')
            return
        image.save(photo, 'PNG')
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = 'https://www.google.com/searchbyimage/upload'
        multipart = {'encoded_image': (photo, open(photo, 'rb')), 'image_content': ''}
        response = post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']

        if response != 400:
            edit(message, f'`{get_translation("reverseProcess")}`')
        else:
            edit(message, f'`{get_translation("reverseGoogle")}`')
            return

        remove(photo)
        match = ParseSauce(fetchUrl + '&preferences?hl=en&fg=1#languages')
        guess = match['best_guess']
        imgspage = match['similar_images']

        if guess and imgspage:
            edit(message, get_translation("reverseResult", [guess, fetchUrl, '`']))
        else:
            edit(message, f'`{get_translation("reverseError2")}`')
            return

        msg = extract_args(message)
        if len(msg) > 1 and msg.isdigit():
            lim = msg
        else:
            lim = 3
        images = scam(match, lim)
        yeet = []
        for i in range(len(images)):
            k = get(images[i])
            n = f'reverse_{i}.png'
            file = open(n, 'wb')
            file.write(k.content)
            file.close()
            yeet.append(InputMediaPhoto(n))
        reply_doc(message, yeet)
        edit(message, get_translation("reverseResult", [guess, fetchUrl, imgspage]))


def ParseSauce(googleurl):

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, 'html.parser')

    results = {'similar_images': '', 'best_guess': ''}

    try:
        for similar_image in soup.findAll('input', {'class': 'gLFyf'}):
            url = 'https://www.google.com/search?tbm=isch&q=' + parse.quote_plus(
                similar_image.get('value')
            )
            results['similar_images'] = url
    except BaseException:
        pass

    for best_guess in soup.findAll('div', attrs={'class': 'r5a77d'}):
        results['best_guess'] = best_guess.get_text()

    return results


def scam(results, lim):

    single = opener.open(results['similar_images']).read()
    decoded = single.decode('utf-8')

    imglinks = []
    counter = 0

    pattern = r'^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$'
    oboi = findall(pattern, decoded, I | M)

    for imglink in oboi:
        counter += 1
        if not counter >= int(lim):
            imglinks.append(imglink)
        else:
            break

    return imglinks


HELP.update({'reverse': get_translation('reverseInfo')})
