# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
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


@sedenify(pattern='^.earrape')
def earrape(message):
    args = extract_args(message).split(' ', 1)
    reply = message.reply_to_message
    earrape = 'earrape'
    if path.isfile(earrape):
        remove(earrape)

    util = args[0].lower()
    if util == 'mp4':
        if not(reply.video or reply.video_note or (
                reply.document and 'video' in reply.document.mime_type)):
            edit(message, f'`{get_translation("wrongMedia")}`')
        else:
            edit(message, f'`{get_translation("applyEarrape")}`')
            media = download_media_wc(reply, file_name=earrape)
            process = Popen(['ffmpeg',
                             '-i',
                             f'{media}',
                             '-af',
                             'acrusher=.1:1:64:0:log',
                             f'{media}.mp4'])
            final, _ = process.communicate()
            edit(message, f'`{get_translation("uploadMedia")}`')
            reply_doc(
                message,
                f'{media}.mp4',
                delete_after_send=True)
            remove(media)
            message.delete()
    elif util == 'mp3':
        if not(reply.video or reply.video_note or (
            reply.audio or reply.voice or (
                reply.document and 'video' in reply.document.mime_type))):
            edit(message, f'`{get_translation("wrongMedia")}`')
        else:
            edit(message, f'`{get_translation("applyEarrape")}`')
            media = download_media_wc(reply, file_name=earrape)
            process = Popen(['ffmpeg',
                             '-i',
                             f'{media}',
                             '-af',
                             'acrusher=.1:1:64:0:log',
                             f'{media}.mp3'])
            final, _ = process.communicate()
            edit(message, f'`{get_translation("uploadMedia")}`')
            reply_voice(message, f'{media}.mp3')
            remove(media)
            remove(f'{media}.mp3')
            message.delete()
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return


KOMUT.update({'earrape': get_translation('earrapeInfo')})
