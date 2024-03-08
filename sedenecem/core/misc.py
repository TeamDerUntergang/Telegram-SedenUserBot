# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import makedirs
from random import choice
from re import escape, sub
from subprocess import STDOUT, DEVNULL, CalledProcessError, check_output
from typing import List

from bs4 import BeautifulSoup
from pyrogram import enums
from pyrogram.types import Message, User
from requests import get

from sedenbot import BOT_PREFIX, BRAIN, LOG_VERBOSE, app

MARKDOWN_FIX_CHAR = '\u2064'
SPAM_COUNT = [0]
_parsed_prefix = escape(BOT_PREFIX) if BOT_PREFIX else r'\.'
_admin_status_list = [
    enums.ChatMemberStatus.OWNER,
    enums.ChatMemberStatus.ADMINISTRATOR,
]
google_domains = [
    'www.google.com',
    'www.google.ad',
    'www.google.ae',
    'www.google.com.af',
    'www.google.com.ag',
    'www.google.com.ai',
    'www.google.am',
    'www.google.co.ao',
    'www.google.com.ar',
    'www.google.as',
    'www.google.at',
    'www.google.com.au',
    'www.google.az',
    'www.google.ba',
    'www.google.com.bd',
    'www.google.be',
    'www.google.bf',
    'www.google.bg',
    'www.google.com.bh',
    'www.google.bi',
    'www.google.bj',
    'www.google.com.bn',
    'www.google.com.bo',
    'www.google.com.br',
    'www.google.bs',
    'www.google.co.bw',
    'www.google.by',
    'www.google.com.bz',
    'www.google.ca',
    'www.google.cd',
    'www.google.cf',
    'www.google.cg',
    'www.google.ch',
    'www.google.ci',
    'www.google.co.ck',
    'www.google.cl',
    'www.google.cm',
    'www.google.cn',
    'www.google.com.co',
    'www.google.co.cr',
    'www.google.com.cu',
    'www.google.cv',
    'www.google.com.cy',
    'www.google.cz',
    'www.google.de',
    'www.google.dj',
    'www.google.dk',
    'www.google.dm',
    'www.google.com.do',
    'www.google.dz',
    'www.google.com.ec',
    'www.google.ee',
    'www.google.com.eg',
    'www.google.es',
    'www.google.com.et',
    'www.google.fi',
    'www.google.com.fj',
    'www.google.fm',
    'www.google.fr',
    'www.google.ga',
    'www.google.ge',
    'www.google.gg',
    'www.google.com.gh',
    'www.google.com.gi',
    'www.google.gl',
    'www.google.gm',
    'www.google.gp',
    'www.google.gr',
    'www.google.com.gt',
    'www.google.gy',
    'www.google.com.hk',
    'www.google.hn',
    'www.google.hr',
    'www.google.ht',
    'www.google.hu',
    'www.google.co.id',
    'www.google.ie',
    'www.google.co.il',
    'www.google.im',
    'www.google.co.in',
    'www.google.iq',
    'www.google.is',
    'www.google.it',
    'www.google.je',
    'www.google.com.jm',
    'www.google.jo',
    'www.google.co.jp',
    'www.google.co.ke',
    'www.google.com.kh',
    'www.google.ki',
    'www.google.kg',
    'www.google.co.kr',
    'www.google.com.kw',
    'www.google.kz',
    'www.google.la',
    'www.google.com.lb',
    'www.google.li',
    'www.google.lk',
    'www.google.co.ls',
    'www.google.lt',
    'www.google.lu',
    'www.google.lv',
    'www.google.com.ly',
    'www.google.co.ma',
    'www.google.md',
    'www.google.me',
    'www.google.mg',
    'www.google.mk',
    'www.google.ml',
    'www.google.mn',
    'www.google.ms',
    'www.google.com.mt',
    'www.google.mu',
    'www.google.mv',
    'www.google.mw',
    'www.google.com.mx',
    'www.google.com.my',
    'www.google.co.mz',
    'www.google.com.na',
    'www.google.com.nf',
    'www.google.com.ng',
    'www.google.com.ni',
    'www.google.ne',
    'www.google.nl',
    'www.google.no',
    'www.google.com.np',
    'www.google.nr',
    'www.google.nu',
    'www.google.co.nz',
    'www.google.com.om',
    'www.google.com.pa',
    'www.google.com.pe',
    'www.google.com.ph',
    'www.google.com.pk',
    'www.google.pl',
    'www.google.pn',
    'www.google.com.pr',
    'www.google.ps',
    'www.google.pt',
    'www.google.com.py',
    'www.google.com.qa',
    'www.google.ro',
    'www.google.ru',
    'www.google.rw',
    'www.google.com.sa',
    'www.google.com.sb',
    'www.google.sc',
    'www.google.se',
    'www.google.com.sg',
    'www.google.sh',
    'www.google.si',
    'www.google.sk',
    'www.google.com.sl',
    'www.google.sn',
    'www.google.so',
    'www.google.sm',
    'www.google.st',
    'www.google.com.sv',
    'www.google.td',
    'www.google.tg',
    'www.google.co.th',
    'www.google.com.tj',
    'www.google.tk',
    'www.google.tl',
    'www.google.tm',
    'www.google.tn',
    'www.google.to',
    'www.google.com.tr',
    'www.google.tt',
    'www.google.com.tw',
    'www.google.co.tz',
    'www.google.com.ua',
    'www.google.co.ug',
    'www.google.co.uk',
    'www.google.com.uy',
    'www.google.co.uz',
    'www.google.com.vc',
    'www.google.co.ve',
    'www.google.vg',
    'www.google.co.vi',
    'www.google.com.vn',
    'www.google.vu',
    'www.google.ws',
    'www.google.rs',
    'www.google.co.za',
    'www.google.co.zm',
    'www.google.co.zw',
    'www.google.cat',
    'www.google.xxx',
]


def reply(
    message,
    text,
    preview=True,
    fix_markdown=False,
    delete_orig=False,
    parse=enums.ParseMode.MARKDOWN,
):
    """
    Reply to a message with the given text.

    Args:
        message (pyrogram.types.Message): The message to reply to.
        text (str): The text to send in the reply.
        preview (bool): Whether to enable link previews for URLs in the text. Defaults to True.
        fix_markdown (bool): Whether to add a special character to fix issues with markdown formatting. Defaults to False.
        delete_orig (bool): Whether to delete the original message after sending the reply. Defaults to False.
        parse (pyrogram.enums.ParseMode): The parse mode to use for the text. Defaults to `pyrogram.enums.ParseMode.MARKDOWN`.

    Returns:
        pyrogram.types.Message: The message object of the sent reply.
    """
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        ret = message.reply_text(
            text.strip(), disable_web_page_preview=not preview, parse_mode=parse
        )
        if delete_orig:
            message.delete()
        return ret
    except BaseException:
        pass


def extract_args(message, markdown=True, line=True):
    """
    Extracts arguments from a given text.

    Args:
        message (pyrogram.types.Message): The message to extract arguments from.
        markdown (bool): Whether to treat the message text as Markdown. Defaults to True.
        line (bool): Whether to remove line breaks from the message text. Defaults to True.

    Returns:
        str: The extracted arguments.
    """
    if not (message.text or message.caption):
        return ''

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if ' ' not in text:
        return ''

    text = sub(r'\s+', ' ', text) if line else text
    text = text[text.find(' ') :].strip()
    return text


def extract_args_split(message, markdown=True, line=True):
    """
    Extracts arguments from a given text and splits them into a list.

    Args:
        message (pyrogram.types.Message): The message to extract arguments from.
        markdown (bool): Whether to treat the message text as Markdown. Defaults to True.
        line (bool): Whether to remove line breaks from the message text. Defaults to True.

    Returns:
        List[str]: The extracted arguments, split into a list.
    """
    return extract_args(message, markdown, line).split()


def edit(
    message, text, preview=True, fix_markdown=False, parse=enums.ParseMode.MARKDOWN
):
    """
    Edits the text of a message.

    Args:
        message (pyrogram.types.Message): The message to edit.
        text (str): The new text to replace the message with.
        preview (bool): Whether to enable link previews for URLs in the text. Defaults to True.
        fix_markdown (bool): Whether to add a special character to fix issues with markdown formatting. Defaults to False.
        parse (pyrogram.enums.ParseMode): The parse mode to use for the text. Defaults to `pyrogram.enums.ParseMode.MARKDOWN`.

    Returns:
        None
    """
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        if message.from_user.id != message._client.me.id:
            reply(message, text, preview=preview, parse=parse)
            return
        message.edit_text(
            text.strip(), disable_web_page_preview=not preview, parse_mode=parse
        )
    except BaseException:
        pass


def download_media(client, data, file_name=None, progress=None, sticker_orig=True):
    """
    Downloads media from a given message and saves it to a file.

    Args:
        client (pyrogram.Client): The client to use for downloading the media.
        data (pyrogram.types.Message): The message containing the media to download.
        file_name (str): The name of the file to save the media to. Defaults to None.
        progress (callable, optional): A callback function to report the progress of the download. Defaults to None.
        sticker_orig (bool): Whether to download the original sticker file. Defaults to True.

    Returns:
        Union[None, str]: None if media download fails, else the absolute path of downloaded file.
    """
    if not file_name:
        if data.document:
            file_name = (
                data.document.file_name
                if data.document.file_name
                else f'{data.document.file_id}.bin'
            )
        elif data.audio:
            file_name = (
                data.audio.file_name
                if data.audio.file_name
                else f'{data.audio.file_id}.mp3'
            )
        elif data.photo:
            file_name = f'{data.photo.file_id}.png'
        elif data.voice:
            file_name = f'{data.voice.file_id}.ogg'
        elif data.video:
            file_name = (
                data.video.file_name
                if data.video.file_name
                else f'{data.video.file_id}.mp4'
            )
        elif data.animation:
            file_name = f'{data.animation.file_id}.mp4'
        elif data.video_note:
            file_name = f'{data.video_note.file_id}.mp4'
        elif data.sticker:
            file_name = f'sticker.{("tgs" if sticker_orig else "json.gz") if data.sticker.is_animated else "webm" if data.sticker.is_video else "webp" if sticker_orig else "png"}'
        else:
            return None

    if progress:
        return client.download_media(data, file_name=file_name, progress=progress)

    return client.download_media(data, file_name=file_name)


def download_media_wc(data, file_name=None, progress=None, sticker_orig=False):
    """
    Downloads media from a given message and saves it to a file.

    Args:
        data (pyrogram.types.Message): The message containing the media to download.
        file_name (str): The name to save the downloaded file as. If not specified, the file will be saved with a default name based on the media type.
        progress (callable, optional): A function to call with the download progress percentage as an argument. Useful for displaying a progress bar. The function should take a single `float` argument between 0 and 100.
        sticker_orig (bool): If `True`, downloads the original TGS or JSON file for stickers, instead of converting to a static image format. Has no effect for non-sticker media.

    Returns:
        None: If the media type is not supported or the download fails for any reason.
        str: The name of the file the media was saved as, if the download was successful.
    """
    return download_media(app, data, file_name, progress, sticker_orig)


def forward(message, chat_id):
    """
    Forwards a given message to a specified chat.

    Args:
        message (pyrogram.types.Message): The message to forward.
        chat_id (int or str): The ID of the chat to forward the message to.
            If not specified, forwards the message to the saved messages.

    Raises:
        Exception: If the message forwarding fails.

    Returns:
        pyrogram.types.Message: The forwarded message object.
    """
    try:
        return message.forward(chat_id or 'me')
    except Exception as e:
        raise e


def get_messages(chat_id, msg_ids=None, client=app):
    """
    Retrieves one or more messages from a specified chat.

    Args:
        chat_id (int or str): The ID of the chat to retrieve messages from. If not specified, retrieves messages from the saved messages.
        msg_ids (int or List[int]): The ID or list of IDs of the messages to retrieve. If not specified, retrieves the latest message in the chat.
        client (pyrogram.Client): The client instance used to retrieve the messages.

    Returns:
        List[pyrogram.types.Message]: A list of message objects that were retrieved, sorted in ascending order based on their IDs (oldest message first). If no messages are found or an error occurs, an empty list is returned.
    """
    try:
        ret = client.get_messages(chat_id=(chat_id or 'me'), message_ids=msg_ids)
        return [ret] if ret and isinstance(ret, Message) else ret
    except BaseException:
        return []


def amisudo():
    """
    Checks if the user is authorized to execute sudo commands.

    Returns:
        bool: True if the user is authorized to execute sudo commands, False otherwise.
    """
    return app.me.id in BRAIN


def increment_spam_count():
    """
    Increments the spam count and checks if the current spam count is within the allowed limit.

    Returns:
        bool: True if the current spam count is within the allowed limit, False otherwise.
    """
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    """
    Checks if spamming is allowed based on the current spam count or user permissions.

    Returns:
        bool: True if spamming is allowed, False otherwise.
    """
    return amisudo() or SPAM_COUNT[0] < 50


def get_cmd(message):
    """
    Extracts the command from a given message.

    Args:
        message (pyrogram.types.Message): The message from which to extract the command.

    Returns:
        str: The command string without the leading slash, or an empty string if no command was found.
    """
    text = message.text or message.caption
    if text:
        text = text.strip()
        return parse_cmd(text)
    return ''


def parse_cmd(text):
    """
    Parses a command string from the given text.

    Args:
        text (str): The text from which to parse the command.

    Returns:
        str: The parsed command string without the leading slash.
    """
    cmd = sub(r'\s+', ' ', text)
    cmd = cmd.split()[0]
    cmd = cmd.split(_parsed_prefix)[-1] if BOT_PREFIX else cmd[1:]
    return cmd


def is_admin(message):
    """
    Checks if the sender of the given message is an admin in the chat.

    Args:
        message (pyrogram.types.Message): The message to check.

    Returns:
        bool: True if the sender is an admin, False otherwise.
    """
    if not message.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
        return True

    user = app.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return user.status in _admin_status_list


def is_admin_myself(chat):
    """
    Checks if the user is an admin in the given chat.

    Args:
        chat (pyrogram.types.Chat): The chat to check.

    Returns:
        bool: True if the bot is an admin, False otherwise.
    """
    if not chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
        return True

    user = app.get_chat_member(chat_id=chat.id, user_id='me')
    return user.status in _admin_status_list


def get_download_dir() -> str:
    """
    Gets the directory path for downloaded files.

    Returns:
        str: The directory path.
    """
    dir = './downloads'
    makedirs(dir, exist_ok=True)
    return dir


def get_duration(media):
    """
    Returns the duration of a media file.

    Args:
        media (str): The file path.

    Returns:
        int: The duration in seconds or None if the duration cannot be determined.
    """
    out = get_status_out(
        f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{media}"'
    )
    if LOG_VERBOSE:
        print(out)
    if out[0] == 0:
        return int(float(out[1]))
    return None


def get_status_out(cmd, encoding='utf-8'):
    """
    Runs a shell command and captures its output.

    Args:
        cmd (str): The shell command to be run.
        encoding (str): The encoding to use for the command's output. Defaults to 'utf-8'.

    Returns:
        tuple: A tuple containing the return code of the command and its output.
    """
    try:
        output = check_output(
            cmd,
            shell=True,
            text=True,
            stderr=STDOUT if LOG_VERBOSE else DEVNULL,
            encoding=encoding,
        )
        return (0, output)
    except CalledProcessError as ex:
        return (ex.returncode, ex.output)
    except BaseException as e:
        if encoding != 'latin-1':
            return get_status_out(cmd, 'latin-1')
        raise e


def extract_user(message: Message) -> List[User]:
    """
    Extracts user information from a given message.

    Args:
        message (pyrogram.types.Message): Message object.

    Returns:
        List[User]: A list of User objects representing the users mentioned or replied to in the message.
    """
    users: List[User] = []
    mentions = None

    if message.text and not mentions:
        try:
            users.append(message._client.get_users(message.text.split()[1]))
        except BaseException:
            pass

    if message.reply_to_message:
        users.append(message.reply_to_message.from_user)

    if message.entities:
        mentions = [
            entity
            for entity in message.entities
            if entity.type == enums.MessageEntityType.TEXT_MENTION
        ]
        no_username = [
            i.user for i in mentions if i.type == enums.MessageEntityType.TEXT_MENTION
        ]
        users += no_username

        for i in mentions:
            try:
                users.append(
                    message._client.get_users(
                        message.text[i.offset : i.offset + i.length]
                    )
                )
            except BaseException:
                pass

    return users


def useragent():
    """
    Generate a random user agent string.

    Returns:
        str: A random user agent string.
    """
    try:
        req = get('https://gist.githubusercontent.com/naytseyd/b4f924774f68cf57e54d646ba600abbc/raw/b8fc2569bb600fa338b26b148736007c133ef026')
        user_agents = req.text.split('\n')
        return choice(user_agents)
    except Exception as e:
        print("Error fetching user agent:", e)
        return 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
