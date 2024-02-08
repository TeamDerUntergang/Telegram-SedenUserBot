# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import remove

from sedenbot import LOG_ID, app

from .send import send, send_doc


def send_log(text, fix_markdown=False):
    """
    Sends a log message to the specified Telegram chat or user(self).

    Args:
        text (str): The log message to send.
        fix_markdown (bool): Whether to fix the markdown of the log message. Defaults to False.
    """
    send(app, LOG_ID or 'me', text, fix_markdown=fix_markdown)


def send_log_doc(doc, caption='', fix_markdown=False, remove_file=False):
    """
    Sends a document file to the specified Telegram chat or user(self), along with an caption.

    Args:
        doc (str): The path to the document file to send.
        caption (str): The caption to include with the document file. Defaults to ''.
        fix_markdown (bool): Whether to fix the markdown of the caption. Defaults to False.
        remove_file (bool): Whether to remove the document file after sending. Defaults to False.
    """
    send_doc(app, LOG_ID or 'me', doc, caption=caption, fix_markdown=fix_markdown)
    if remove_file:
        remove(doc)
