# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
# Copyright (C) 2021 kisekinopureya <https://github.com/kisekinopureya>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from io import BytesIO
from os import remove

from PIL import Image
from requests import get
from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args,
    get_download_dir,
    get_translation,
    reply_audio,
    reply_video,
    sedenify,
)
from yt_dlp import YoutubeDL


@sedenify(pattern='^.(youtube|yt)dl')
def youtubedl(message):
    args = extract_args(message).split(' ', 2)

    if len(args) != 2:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    util = args[0].lower()
    url = args[1]

    if util == 'mp4':
        ydl_opts = {
            'outtmpl': f'%(id)s.%(ext)s',
            'format': 'bestvideo[ext=mp4][height<=?1080]+bestaudio[ext=m4a]/best',
            'addmetadata': True,
            'prefer_ffmpeg': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'postprocessors': [
                {'key': 'FFmpegMetadata'},
                {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
            ],
            'quiet': True,
            'logtostderr': False,
        }
        thumb_path = None
        with YoutubeDL(ydl_opts) as ydl:
            try:
                video_info = ydl.extract_info(url, False)
                title = video_info['title']
                uploader = video_info['uploader']
                duration = video_info['duration']
            except KeyError:
                uploader = get_translation('notFound')
                duration = None
            except BaseException as e:
                return edit(message, get_translation('banError', ['`', '**', e]))

            edit(message, get_translation('downloadYTVideo', ['**', title, '`']))

            try:
                temp = BytesIO()
                with get(video_info['thumbnail']) as req:
                    temp.name = 'file.webp'
                    temp.write(req.content)
                    temp.seek(0)
                im = Image.open(temp)
                imc = im.convert('RGB')
                imc.save(thumb_path := f'{get_download_dir()}/{video_info["id"]}.jpg')
            except BaseException:
                thumb_path = None

            ydl.download([url])

        edit(message, f'`{get_translation("uploadMedia")}`')
        reply_video(
            message,
            f'{video_info["id"]}.mp4',
            thumb=thumb_path,
            caption=f"**{get_translation('videoTitle')}** `{title}`\n**{get_translation('videoUploader')}** `{uploader}`",
            duration=duration,
            delete_orig=True,
            delete_file=True,
        )
        try:
            remove(thumb_path)
        except BaseException:
            pass

    elif util == 'mp3':
        ydl_opts = {
            'outtmpl': f'%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'addmetadata': True,
            'writethumbnail': True,
            'prefer_ffmpeg': True,
            "extractaudio": True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                },
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegMetadata'},
            ],
            'quiet': True,
            'logtostderr': False,
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                video_info = ydl.extract_info(url, False)
                title = video_info['title']
                uploader = video_info['uploader']
                duration = int(video_info['duration'])
            except KeyError:
                uploader = get_translation('notFound')
                duration = None
            except BaseException as e:
                return edit(message, get_translation('banError', ['`', '**', e]))

            edit(message, get_translation('downloadYTAudio', ['**', title, '`']))

            ydl.download([url])
        edit(message, f'`{get_translation("uploadMedia")}`')
        reply_audio(
            message,
            f'{title}.mp3',
            caption=f"**{get_translation('videoUploader')}** `{uploader}`",
            duration=duration,
            delete_orig=True,
            delete_file=True,
        )


HELP.update({'youtubedl': get_translation('youtubedlInfo')})
