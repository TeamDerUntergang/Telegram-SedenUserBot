# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
# Copyright (C) 2021 kisekinopureya <https://github.com/kisekinopureya>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import path, remove
from subprocess import Popen

from sedenbot import KOMUT
from sedenecem.core import (edit, sedenify, download_media_wc, reply_voice,
                            extract_args, reply_doc, get_translation)


@sedenify(pattern='^.slowedtoperfection')
def slowedtoperfection(message):
    reply = message.reply_to_message
    slowedtoperfection = 'slowedtoperfection'
    if path.isfile(slowedtoperfection):
        remove(slowedtoperfection)

    if not(reply.audio or reply.voice or (
            reply.document and 'audio' in reply.document.mime_type)):
        edit(message, f'`{get_translation("wrongMedia")}`')
    else:
        edit(message, f'`{get_translation("applySlowedtoperfection")}`')
        media = download_media_wc(reply, file_name=slowedtoperfection)
        process = Popen(['ffmpeg',
                        '-i',
                        f'{media}',
                        '-af',
                        'aecho=1.0:0.7:20:0.5,asetrate=44100*0.84,aresample=44100,atempo=1',
                        f'{media}.mp3'])
        final, _ = process.communicate()
        edit(message, f'`{get_translation("uploadMedia")}`')
        reply_voice(message, f'{media}.mp3')
        remove(media)
        remove(f'{media}.mp3')
        message.delete()


KOMUT.update({'slowedtoperfection': get_translation('slowedtoperfectionInfo')})
