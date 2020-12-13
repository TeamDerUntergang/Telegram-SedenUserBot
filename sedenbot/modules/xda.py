# Copyright (C) 2020 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from random import choice

from sedenbot import KOMUT
from sedenecem.core import edit, sedenify, get_translation
# ================= CONSTANT =================
XDA_STRINGS = [
    'sur', 'Sir', 'bro', 'yes', 'no', 'bolte', 'bolit', 'bholit', 'volit',
    'mustah', 'fap', 'lit', 'lmao', 'iz', 'jiosim', 'ijo', 'nut', 'workz',
    'workang', 'flashabl zip', 'bateri', 'bacup', 'bad englis', 'sar',
    'treble wen', 'gsi', 'fox bag', 'bag fox', 'fine', 'bast room', 'fax',
    'trable', 'kenzo', 'plz make room', 'andreid pai', 'when', 'port', 'mtk',
    'send moni', 'bad rom', 'dot', 'rr', 'linage', 'arrows', 'kernal',
    'meme12', 'bruh', 'imail', 'email', 'plaka', 'evox']
# ================= CONSTANT =================
'''
Copyright (c) @NaytSeyd, Quotes taken
from friendly-telegram (https://gitlab.com/friendly-telegram) | 2020
'''


@sedenify(pattern='^.xda$')
def xda(message):
    edit(message, choice(XDA_STRINGS))


KOMUT.update({'xda': get_translation('xdaInfo')})
