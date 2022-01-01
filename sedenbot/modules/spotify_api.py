# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from glob import glob
from os import mkdir, path, remove
from queue import Queue
from threading import Thread
from urllib.request import urlretrieve
from zipfile import ZipFile

from requests import get
from sedenbot import HELP
from sedenecem.core import (
    edit,
    extract_args,
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

    def spotify_dir(self):
        if path.exists('./Spotify'):
            pass
        else:
            mkdir('./Spotify')

    def fetch_token(self):
        self.spotify_dir()
        sp = Spotify(auth_manager=SpotifyClientCredentials())
        return sp

    def download_track(self, query):
        ydl_opts = {
            'outtmpl': f'./Spotify/%(title)s.%(ext)s',
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
            ydl.download([query])

    def worker(self, q):
        while not q.empty():
            item = q.get()
            self.download_track(item)
            q.task_done()

    def search_track(self, message):
        sp = self.fetch_token()
        args = extract_args(message)
        if 'zip' in args:
            args = extract_args(message).split(' ', 3)
            playlist_url = args[2]
            edit(message, f'`{get_translation("downloadMedia")}`')
            zip_file = ZipFile('./Spotify/playlist.zip', 'w')
            fields = "items.track.track_number,items.track.name,items.track.artists.name,items.track.album.name,items.track.album.release_date,total,items.track.album.images"
            playlist = sp.playlist_items(
                playlist_url,
                fields=fields,
                additional_types=['track'],
            )['items']
            threads = []
            video_urls = []
            q = Queue()
            for item in playlist:
                track = f'{item["track"]["name"]} '
                artist = item['track']['artists'][0]['name']
                track += artist
                video_urls.append(track)
            for url in video_urls:
                q.put(url)
            for i in range(15):
                t1 = Thread(target=self.worker, args=(q,), daemon=True)
                t1.start()
                threads.append(t1)
            for t in threads:
                t.join()
            for i in glob('./Spotify/*.mp3'):
                zip_file.write(i)
            zip_file.close()
            edit(message, f'`{get_translation("uploadingZip")}`')
            reply_doc(message, './Spotify/playlist.zip', delete_after_send=True)
            message.delete()
            for song in glob('./Spotify/*.mp3'):
                remove(song)

        else:
            args = extract_args(message).split(' ', 2)
            playlist_url = args[1]
            edit(message, f'`{get_translation("downloadMedia")}`')
            fields = "items.track.track_number,items.track.name,items.track.artists.name,items.track.album.name,items.track.album.release_date,total,items.track.album.images"
            playlist = sp.playlist_items(
                playlist_url,
                fields=fields,
                additional_types=['track'],
            )['items']
            threads = []
            video_urls = []
            q = Queue()
            for item in playlist:
                track = f'{item["track"]["name"]} '
                artist = item['track']['artists'][0]['name']
                track += artist
                video_urls.append(track)
            for url in video_urls:
                q.put(url)
            for i in range(15):
                t1 = Thread(target=self.worker, args=(q,), daemon=True)
                t1.start()
                threads.append(t1)
            for t in threads:
                t.join()
            for song in glob('./Spotify/*.mp3'):
                reply_audio(message, song, delete_file=True)
            for song in glob('./Spotify/*.mp3'):
                remove(song)

    def show_playlist(self, username=None):
        sp = self.fetch_token()
        global counter
        counter = 0
        users_playlists = '\n'

        if username:
            result = sp.user_playlists(username, limit=50)
        else:
            result = sp.user_playlists(username=self.username)

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
        sp = self.fetch_token()
        if username == None:
            return edit(message, (get_translation("invalidUsername")))
        else:
            r = get(f"https://open.spotify.com/user/{username}")
            if r.status_code == 404:
                edit(message, get_translation("userNotFound", ['**', '`', username]))

            else:
                user = sp.user(username)
                profile_photo = [i['url'] for i in user['images']]
                if profile_photo:
                    r = urlretrieve("".join(profile_photo), './Spotify/pfp.png')
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
                if 'group' in message.chat.type:
                    perm = message.chat.permissions
                    media_perm = perm.can_send_media_messages

                if profile_photo and media_perm:
                    reply_img(
                        message,
                        photo='./Spotify/pfp.png',
                        caption=out,
                        delete_file=True,
                    )
                    message.delete()
                else:
                    edit(message, out, preview=False)


@sedenify(pattern='^.spoti(|fy)')
def spotify_download(message):
    spotify = Spotipy()
    args = extract_args(message).split(' ', 2)
    if args[0] == 'dl' or args[0] == 'dl zip':
        spotify.search_track(message)

    elif 'show' == args[0]:
        if len(args) == 1:
            edit(message, f'`{get_translation("invalidUsername")}`')
        else:
            username = args[1]
            spotify.show_users_detail(username=username, message=message)
    else:
        edit(message, f'`{get_translation("invalidProcess")}`')


HELP.update({'spotify': get_translation('spotifyInfo')})
