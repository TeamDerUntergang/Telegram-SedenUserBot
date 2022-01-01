# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from re import sub
from urllib.parse import quote

from pylast import LastFMNetwork, User, md5
from sedenbot import HELP, environ
from sedenecem.core import edit, get_translation, sedenify

# =================== CONSTANT ===================
LASTFM_API = environ.get('LASTFM_API', None)
LASTFM_SECRET = environ.get('LASTFM_SECRET', None)
LASTFM_USERNAME = environ.get('LASTFM_USERNAME', None)
LASTFM_PASSWORD_PLAIN = environ.get('LASTFM_PASSWORD', None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    lastfm = LastFMNetwork(
        api_key=LASTFM_API,
        api_secret=LASTFM_SECRET,
        username=LASTFM_USERNAME,
        password_hash=LASTFM_PASS,
    )
else:
    lastfm = None
# ================================================


@sedenify(pattern='^.lastfm$')
def last_fm(message):
    edit(message, f'`{get_translation("processing")}`')
    if not lastfm:
        return edit(
            message, get_translation('lastfmApiMissing', ['**', '`']), preview=False
        )

    playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
    username = f'https://www.last.fm/user/{LASTFM_USERNAME}'
    if playing:
        tags = gettags(isNowPlaying=True, playing=playing)
        rectrack = quote(f'{playing}')
        rectrack = sub('^', 'https://open.spotify.com/search/', rectrack)
        output = get_translation(
            'lastfmProcess',
            [LASTFM_USERNAME, username, '__', playing, rectrack, '`', tags],
        )
    else:
        recent = User(LASTFM_USERNAME, lastfm).get_recent_tracks(limit=5)
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        output = get_translation('lastfmProcess2', [LASTFM_USERNAME, username, '__'])
        for i, track in enumerate(recent):
            printable = artist_and_song(track)
            tags = gettags(track)
            rectrack = quote(str(printable))
            rectrack = sub('^', 'https://open.spotify.com/search/', rectrack)
            output += f'• [{printable}]({rectrack})\n'
            if tags:
                output += f'`{tags}`\n\n'

    edit(message, output, preview=False)


def gettags(track=None, isNowPlaying=None, playing=None):
    if isNowPlaying:
        tags = playing.get_top_tags()
        arg = playing
        if not tags:
            tags = playing.artist.get_top_tags()
    else:
        tags = track.track.get_top_tags()
        arg = track.track
    if not tags:
        tags = arg.artist.get_top_tags()
    tags = ''.join([' #' + t.item.__str__() for t in tags[:5]])
    tags = sub('^ ', '', tags)
    tags = sub(' ', '_', tags)
    tags = sub('_#', ' #', tags)
    return tags


def artist_and_song(track):
    return f'{track.track}'


HELP.update({'lastfm': get_translation('lastfmInfo')})
