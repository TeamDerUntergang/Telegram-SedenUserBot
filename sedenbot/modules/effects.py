# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import path, remove
from subprocess import Popen

from sedenbot import HELP
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
            media = download_media_wc(reply, earrape)
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
                delete_after_send=True,
                delete_orig=True)
            remove(media)
    elif util == 'mp3':
        if not(reply.video or reply.video_note or (
            reply.audio or reply.voice or (
                reply.document and 'video' in reply.document.mime_type))):
            edit(message, f'`{get_translation("wrongMedia")}`')
        else:
            edit(message, f'`{get_translation("applyEarrape")}`')
            media = download_media_wc(reply, earrape)
            process = Popen(['ffmpeg',
                             '-i',
                             f'{media}',
                             '-af',
                             'acrusher=.1:1:64:0:log',
                             f'{media}.mp3'])
            final, _ = process.communicate()
            edit(message, f'`{get_translation("uploadMedia")}`')
            reply_voice(message, f'{media}.mp3', delete_orig=True)
            remove(media)
            remove(f'{media}.mp3')
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return


@sedenify(pattern='^.nightcore')
def nightcore(message):
    reply = message.reply_to_message
    nightcore = 'nightcore'
    if path.isfile(nightcore):
        remove(nightcore)

    if not(reply.audio or reply.voice or (
            reply.document and 'audio' in reply.document.mime_type)):
        edit(message, f'`{get_translation("wrongMedia")}`')
    else:
        edit(message, f'`{get_translation("applyNightcore")}`')
        media = download_media_wc(reply, file_name=nightcore)
        process = Popen(['ffmpeg',
                        '-i',
                        f'{media}',
                        '-af',
                        'asetrate=44100*1.16,aresample=44100,atempo=1',
                        f'{media}.mp3'])
        final, _ = process.communicate()
        edit(message, f'`{get_translation("uploadMedia")}`')
        reply_voice(message, f'{media}.mp3')
        remove(media)
        remove(f'{media}.mp3')
        message.delete()


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


HELP.update({'effects': get_translation('effectsInfo')})
