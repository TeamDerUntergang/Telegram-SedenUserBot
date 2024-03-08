# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from emoji import demojize
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from gtts.lang import tts_langs
from sedenbot import HELP
from sedenecem.core import sedenify, extract_args, extract_args_split, edit, send_log, reply_voice, get_translation


@sedenify(pattern='^.tts')
def text_to_speech(message):
    reply = message.reply_to_message
    args = extract_args(message)
    if args:
        pass
    elif reply:
        if not reply.text:
            return edit(message, f'`{get_translation("ttsUsage")}`')
        args = reply.text
    else:
        edit(message, f'`{get_translation("ttsUsage")}`')
        return

    try:
        gTTS(args, lang=TTS_LANG)
    except AssertionError:
        edit(message, f'`{get_translation("ttsBlank")}`')
        return
    except ValueError:
        edit(message, f'`{get_translation("ttsNoSupport")}`')
        return
    except RuntimeError:
        edit(message, f'`{get_translation("ttsError")}`')
        return
    tts = gTTS(args, lang=TTS_LANG)
    tts.save('h.mp3')
    with open('h.mp3', 'rb') as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(args, lang=TTS_LANG)
        tts.save('h.mp3')
    with open('h.mp3', 'r'):
        reply_voice(reply if reply else message, 'h.mp3', delete_file=True)

    message.delete()
    send_log(get_translation('ttsLog'))


@sedenify(pattern='^.trt')
def translate(message):
    translator = Translator()
    reply = message.reply_to_message
    args = extract_args(message)
    if args:
        pass
    elif reply:
        if not reply.text:
            return edit(message, f'`{get_translation("trtUsage")}`')
        args = reply.text
    else:
        edit(message, f'`{get_translation("trtUsage")}`')
        return

    try:
        reply_text = translator.translate(demojize(args), dest=TRT_LANG)
    except ValueError:
        edit(message, f'`{get_translation("trtError")}`')
        return

    source_lan = LANGUAGES[reply_text.src.lower()]
    transl_lan = LANGUAGES[reply_text.dest.lower()]
    reply_text = '{}\n{}'.format(
        get_translation(
            'transHeader', ['**', '`', source_lan.title(), transl_lan.title()]
        ),
        reply_text.text,
    )

    edit(message, reply_text)

    send_log(get_translation('trtLog', [source_lan.title(), transl_lan.title()]))


@sedenify(pattern='^.lang')
def lang(message):
    arr = extract_args_split(message)

    if len(arr) != 2:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return

    util = arr[0].lower()
    arg = arr[1].lower()
    if util == 'trt':
        scraper = get_translation('scraper1')
        global TRT_LANG
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            edit(message, get_translation('scraperTrt', ['`', LANGUAGES]))
            return
    elif util == 'tts':
        scraper = get_translation('scraper2')
        global TTS_LANG
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            edit(message, get_translation('scraperTts', ['`', tts_langs()]))
            return
    edit(message, get_translation('scraperResult', ['`', scraper, LANG.title()]))

    send_log(get_translation('scraperLog', ['`', scraper, LANG.title()]))

HELP.update({'translator': get_translation('translatorInfo')})