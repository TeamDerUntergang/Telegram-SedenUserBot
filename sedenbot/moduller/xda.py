# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from random import choice

from sedenbot import KOMUT
from sedenecem.core import edit, sedenify, get_translation
# ================= CONSTANT =================
XDA_STRINGS = [
    "sur",
    "Sir",
    "bro",
    "yes",
    "no",
    "bolte",
    "bolit",
    "bholit",
    "volit",
    "mustah",
    "fap",
    "lit",
    "lmao",
    "iz",
    "jiosim",
    "ijo",
    "nut",
    "workz",
    "workang",
    "flashabl zip",
    "bateri",
    "bacup",
    "bad englis",
    "sar",
    "treble wen",
    "gsi",
    "fox bag",
    "bag fox",
    "fine",
    "bast room",
    "fax",
    "trable",
    "kenzo",
    "plz make room",
    "andreid pai",
    "when",
    "port",
    "mtk",
    "send moni",
    "bad rom",
    "dot",
    "rr",
    "linage",
    "arrows",
    "kernal",
    "meme12",
    "bruh",
    "imail",
]
# ================= CONSTANT =================
"""
Copyright (c) @NaytSeyd, Quotes taken
from friendly-telegram (https://gitlab.com/friendly-telegram) | 2020
"""


@sedenify(pattern='^.xda$')
def xda(message):
    edit(message, choice(XDA_STRINGS))


KOMUT.update({"xda": get_translation("xdaInfo")})
