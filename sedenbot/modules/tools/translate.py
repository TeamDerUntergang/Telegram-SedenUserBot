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
from sedenbot import HELP, SEDEN_LANG
from sedenecem.core import (
    sedenify,
    extract_args_split,
    edit,
    send_log,
    reply_voice,
    get_translation,
)


@sedenify(pattern='^.tts')
def text_to_speech(message):
    reply = message.reply_to_message
    args = extract_args_split(message)

    if reply and reply.text:
        if args:
            lang = args[0].lower()
            text = reply.text
        else:
            lang = SEDEN_LANG
            text = reply.text
    elif args:
        if len(args) >= 2:
            lang = args[0].lower()
            text = ' '.join(args[1:])
        else:
            lang = args[0].lower()
            text = ''
    else:
        edit(message, f'`{get_translation("ttsUsage")}`')
        return

    if lang not in tts_langs():
        lang = SEDEN_LANG
        text = ' '.join(args)

    if not text:
        edit(message, f'`{get_translation("ttsUsage")}`')
        return

    try:
        tts = gTTS(text, lang=lang)
        tts.save('h.mp3')
    except AssertionError:
        edit(message, f'`{get_translation("ttsBlank")}`')
        return
    except ValueError:
        edit(message, f'`{get_translation("ttsNoSupport")}`')
        return
    except RuntimeError:
        edit(message, f'`{get_translation("ttsError")}`')
        return

    with open('h.mp3', 'rb') as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(text, lang=lang)
        tts.save('h.mp3')
    with open('h.mp3', 'r'):
        reply_voice(reply if reply else message, 'h.mp3', delete_file=True)

    message.delete()
    send_log(get_translation('ttsLog'))


@sedenify(pattern='^.trt')
def translate(message):
    translator = Translator()
    reply = message.reply_to_message
    args = extract_args_split(message)

    if reply and reply.text:
        if args:
            dest_lang = args[0].lower()
            text = reply.text
        else:
            dest_lang = SEDEN_LANG
            text = reply.text
    elif args:
        if len(args) == 2:
            lang, text = args
            if lang.lower() in LANGUAGES:
                dest_lang = lang.lower()
                text = text
            else:
                dest_lang = SEDEN_LANG
                text = ' '.join(args)
        else:
            dest_lang = SEDEN_LANG
            text = ' '.join(args)
    else:
        edit(message, f'`{get_translation("trtUsage")}`')
        return

    try:
        translated_text = translator.translate(demojize(text), dest=dest_lang)
    except ValueError:
        edit(message, f'`{get_translation("trtError")}`')
        return

    source_lang = LANGUAGES[translated_text.src.lower()]
    transl_lang = LANGUAGES[translated_text.dest.lower()]
    translated_text = '{}\n{}'.format(
        get_translation(
            'transHeader', ['**', '`', source_lang.title(), transl_lang.title()]
        ),
        translated_text.text,
    )

    edit(message, translated_text)

    send_log(get_translation('trtLog', [source_lang.title(), transl_lang.title()]))


HELP.update({'translator': get_translation('translatorInfo')})
