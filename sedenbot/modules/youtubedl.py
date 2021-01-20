# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
# Copyright (C) 2021 kisekinopureya <https://github.com/kisekinopureya>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove

from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError

from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args,
    sedenify,
    get_translation,
    reply_doc,
    get_translation,
    reply_audio)


@sedenify(pattern='^.(youtube|yt)dl')
def youtubedl(message):
    args = extract_args(message).split(' ', 2)

    if len(args) != 2:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    util = args[0].lower()
    url = args[1]

    try:
        video_info = YoutubeDL().extract_info(url, False)
    except DownloadError as e:
        return edit(message, get_translation('banError', ['`', '**', e]))

    title = video_info.get('title')
    uploader = video_info.get('uploader')
    duration = video_info.get('duration')

    if util == 'mp4':
        edit(message, get_translation('downloadYTVideo', ['**', title, '`']))
        ydl_opts = {
            'outtmpl': f'{title}.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        edit(message, f'{get_translation("uploadMedia")}')
        reply_doc(
            message,
            f'{title}.mp4',
            caption=f"{get_translation('title', ['**' , ':'])} {title}`\n`{get_translation('uploader',['**',':'])} {uploader}",
            delete_after_send=True,
            delete_orig=True)

    elif util == 'mp3':
        edit(message, get_translation('downloadYTAudio', ['**', title, '`']))
        ydl_opts = {
            'outtmpl': f'{title}.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }]}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        edit(message, f'`{get_translation("uploadMedia")}`')
        reply_audio(
            message,
            f'{title}.mp3',
            caption=f"{get_translation('uploader',['**',':'])} {uploader}",
            delete_orig=True)
        remove(f'{title}.mp3')


HELP.update({'youtubedl': get_translation('youtubedlInfo')})
