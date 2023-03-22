# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from concurrent.futures import ThreadPoolExecutor
from glob import glob
from os import cpu_count, mkdir, path, remove, rmdir
from threading import Lock
from urllib.request import urlretrieve
from zipfile import ZipFile

from pyrogram import enums
from requests import get
from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args_split,
    get_translation,
    reply_audio,
    reply_doc,
    reply_img,
    sedenify,
)
from spotipy import Spotify, SpotifyClientCredentials
from yt_dlp import YoutubeDL


class Spotipy:
    def __init__(self):
        self.spotify_dir()
        self.sp = Spotify(auth_manager=SpotifyClientCredentials())

    def spotify_dir(self):
        if path.exists('Spotify'):
            rmdir('Spotify')
            mkdir('Spotify')
        else:
            mkdir('Spotify')

    def search_track(self, name: str):
        ydl_opts = {
            'outtmpl': f'Spotify/{name}.%(ext)s',
            'format': 'bestaudio/best',
            'addmetadata': True,
            'writethumbnail': True,
            'prefer_ffmpeg': True,
            "extractaudio": True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'cachedir': False,
            'default_search': 'ytsearch',
            'noplaylist': True,
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
            ydl.download([name])

    def fetch_track(self, message, playlist_url: str, is_zip=False):
        fullname = []
        offset = 0

        edit(message, f'`{get_translation("downloadMedia")}`')

        while True:
            fields = "items.track.name,items.track.artists.name,total"
            playlist = self.sp.playlist_items(
                playlist_url,
                fields=fields,
                offset=offset,
                additional_types=['track'],
            )
            total = playlist['total']

            for item in playlist['items']:
                if item['track'] is None:
                    offset += 1
                    continue

                track = item['track']['name']
                artist = item['track']['artists'][0]['name']
                name = f'{artist} - {track}'
                fullname.append(name)

                offset += 1

            if total == offset:
                break
        self.download_track(message, fullname, is_zip=is_zip)

    def download_track(self, message, song_list: list, is_zip):
        lock = Lock()
        with lock:
            with ThreadPoolExecutor(min(32, cpu_count() or 0) + 4) as executor:
                executor.map(self.search_track, song_list)

        if is_zip:
            zipfile = ZipFile('Spotify/playlist.zip', 'w')
            for song in glob('Spotify/*.mp3'):
                zipfile.write(song)
                remove(song)
            zipfile.close()

            edit(message, f'`{get_translation("uploadingZip")}`')
            reply_doc(
                message,
                'Spotify/playlist.zip',
                delete_orig=True,
                delete_after_send=True,
            )
        else:
            for song in glob('Spotify/*.mp3'):
                reply_audio(message, song, delete_orig=True, delete_file=True)

    def show_playlist(self, username=None):
        global counter
        counter = 0
        users_playlists = '\n'

        if username:
            result = self.sp.user_playlists(username, limit=50)
        else:
            result = self.sp.user_playlists(username=self.username)

        for item in result['items']:
            pl_name = item['name']
            users_playlists += f'▪️ {pl_name}\n'
            counter += 1
        msg = f'{users_playlists}'
        return msg

    def show_users_detail(
        self,
        username,
        message,
    ):
        if username == None:
            return edit(message, (get_translation("invalidUsername")))
        else:
            r = get(f"https://open.spotify.com/user/{username}")
            if r.status_code == 404:
                edit(message, get_translation("userNotFound", ['**', '`', username]))

            else:
                user = self.sp.user(username)
                profile_photo = [i['url'] for i in user['images']]
                if profile_photo:
                    r = urlretrieve("".join(profile_photo), 'Spotify/pfp.png')
                else:
                    profile_photo = None
                    pass

                out = get_translation(
                    'spotifyResult',
                    [
                        '**',
                        '`',
                        username,
                        user['external_urls']['spotify'],
                        self.show_playlist(username),
                        counter,
                    ],
                )

                media_perm = True
                if message.chat.type in [
                    enums.ChatType.SUPERGROUP,
                    enums.ChatType.GROUP,
                ]:
                    perm = message.chat.permissions
                    media_perm = perm.can_send_media_messages

                if profile_photo and media_perm:
                    reply_img(
                        message,
                        photo='Spotify/pfp.png',
                        caption=out,
                        delete_file=True,
                        delete_orig=True,
                    )
                else:
                    edit(message, out, preview=False)


@sedenify(pattern='^.spoti(|fy)')
def spotify_download(message):
    spotify = Spotipy()
    args = extract_args_split(message)

    if len(args) == 2 and args[0] == 'dl' and not args[1] == 'zip':
        url = args[1]
        spotify.fetch_track(message, url)

    elif len(args) == 3 and args[0] == 'dl' and args[1] == 'zip':
        url = args[2]
        spotify.fetch_track(message, url, is_zip=True)

    elif len(args) == 2 and args[0] == 'show':
        username = args[1]
        if len(username) == 1:
            edit(message, f'`{get_translation("invalidUsername")}`')
        else:
            spotify.show_users_detail(username=username, message=message)
    else:
        edit(message, f'`{get_translation("invalidProcess")}`')


HELP.update({'spotify': get_translation('spotifyInfo')})
