# Copyright (C) 2020-2023 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import path, remove, replace
from re import match, search
from time import time
from urllib.parse import unquote

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client.client import FlowExchangeError, OAuth2WebServerFlow
from pyrogram.types import Message
from pySmartDL import SmartDL
from requests import get
from sedenbot import DRIVE_CLIENT, DRIVE_SECRET, GDRIVE_FOLDER_ID, HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    extract_args_split,
    get_translation,
    reply_doc,
    sedenify,
)
from sedenecem.sql.gdrive_sql import get, remove_, set


def extract_code(url) -> str:
    if "error" in url:
        return ""
    if "%2F" in url:
        url = unquote(url)
    code = search("code=(\d\/.*)&", url)[1]
    return code


class Progress:
    def __init__(self, msg: Message, file_name, start_time):
        self.msg = msg
        self.file_name = file_name
        self.start_time = start_time

    def download(self, current, total):
        percentage = float(current * 100 / total)
        if (curr_time := time()) - self.start_time > 5:
            self.start_time = curr_time
            self.msg.edit_text(
                get_translation(
                    "pyrogramDown",
                    ["**", "`", self.file_name, f"½{round(percentage, 2)}"],
                )
            )

    def upload(self, current, total):
        percentage = float(current * 100 / total)
        if (curr_time := time()) - self.start_time > 5:
            self.start_time = curr_time
            self.msg.edit_text(
                get_translation(
                    "pyrogramUp",
                    ["**", "`", self.file_name, f"½{round(percentage, 2)}"],
                )
            )


class Gdrive:
    def __init__(self, message: Message):
        self.message = message
        self.dl_path = "."
        self.service = build("drive", "v3", credentials=get(self.message.from_user.id))
        self.folder_mimetype = "application/vnd.google-apps.folder"

    def get_file_id(self, link):
        file_id = search("d\/(.+)\/v", link).group(1)
        return file_id

    def download_link(self, url):
        try:
            dl = SmartDL(urls=url, dest=self.dl_path, progress_bar=False)
            dl.start(blocking=False)
            start_time = time()
            while not dl.isFinished():
                if dl.isFinished():
                    break
                if (curr_time := time()) - start_time > 5:
                    start_time = curr_time
                    edit(
                        self.message,
                        get_translation(
                            "gdriveDown",
                            [
                                "**",
                                "`",
                                path.basename(dl.get_dest()),
                                round(dl.get_progress(), 2),
                            ],
                        ),
                    )
            return path.basename(dl.get_dest())
        except:
            return edit(self.message, f"Bir Hatayla Karşılaşıldı")

    def upload_to_telegram(self, url):
        file_id = self.get_file_id(url)

        file_info = (
            self.service.files()
            .get(fileId=file_id, fields="size,name", supportsAllDrives=True)
            .execute()
        )
        size = file_info.get("size")
        file_name = file_info.get("name")

        if int(size) > 4294967296 if self.message.from_user.is_premium else 2147483648:
            return edit(self.message, get_translation("tgUpLimit", ["`"]))
        else:
            file_name = self.download_from_gdrive(url)
            start_time = time()
            progress = Progress(self.message, file_name, start_time)

            reply_doc(
                self.message,
                file_name,
                progress=progress.upload,
            )
            self.message.delete()

    def download_from_gdrive(self, link) -> str:
        file_id = self.get_file_id(link)

        file_info = (
            self.service.files()
            .get(fileId=file_id, fields="name,size", supportsAllDrives=True)
            .execute()
        )
        request = self.service.files().get_media(fileId=file_id, supportsAllDrives=True)

        fh = open(f'{file_info.get("name")}', "wb")
        downloader = MediaIoBaseDownload(
            fd=fh, request=request, chunksize=100 * 1024 * 1024
        )

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            progress = edit(
                self.message,
                get_translation(
                    "gdriveDown",
                    [
                        "**",
                        "`",
                        file_info.get("name"),
                        f"½{int(status.progress() * 100)}",
                    ],
                ),
            )
        edit(
            self.message,
            get_translation("gdriveDownComplete", ["**", "`", file_info.get("name")]),
        )
        return file_info.get("name")

    def copy_file_gdrive(self, link):

        edit(self.message, get_translation('processing'))
        file_id = self.get_file_id(link)

        meta = (
            self.service.files()
            .get(
                supportsAllDrives=True,
                fileId=file_id,
                fields="name,id,mimeType,size",
            )
            .execute()
        )

        if meta.get('mimeType') == self.folder_mimetype:
            return edit(self.message, f"`{get_translation('gdriveCopyErr')}`")

        body = {'parents': [GDRIVE_FOLDER_ID]}

        self.service.files().copy(
            fileId=file_id, body=body, supportsAllDrives=True
        ).execute()

        edit(self.message, get_translation('gdriveCopyFile'))

    def upload_to_gdrive(self, filename):
        file_metadata = {
            "name": filename,
            "parents": [GDRIVE_FOLDER_ID],
        }

        media = MediaFileUpload(filename, resumable=True, chunksize=100 * 1024 * 1024)

        file = self.service.files().create(
            body=file_metadata, media_body=media, fields="id", supportsAllDrives=True
        )
        response = None
        start_time = time()
        while response is None:
            status, response = file.next_chunk()
            if status:
                if (curr_time := time()) - start_time > 5:
                    start_time = curr_time
                    edit(
                        self.message,
                        get_translation(
                            "gdriveUp",
                            ["**", "`", filename, f"½{int(status.progress() * 100)}"],
                        ),
                    )
            else:
                edit(
                    self.message,
                    get_translation("gdriveUpComplete", ["**", "`", filename]),
                )
                remove(filename)


flow = None


@sedenify(pattern="^.gauth")
def drive_auth(message):
    global flow
    user_id = message.from_user.id
    args = extract_args_split(message)

    if len(args) == 0:
        creds = get(user_id)
        if creds is not None:
            creds.refresh(Http())
            edit(message, f'`{get_translation("gdriveAuth")}`')
            set(user_id, creds)
        else:
            OAUTH_SCOPE = "https://www.googleapis.com/auth/drive"
            REDIRECT_URI = "http://localhost"

            flow = OAuth2WebServerFlow(
                DRIVE_CLIENT, DRIVE_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI
            )
            auth_url = flow.step1_get_authorize_url()
            edit(
                message,
                f'{get_translation("gauthURL", ["**","`"])} [Google Drive Auth URL]({auth_url})',
            )

    elif args[0] == "token":
        url = args[1]
        code = extract_code(url)
        if not code:
            return edit(message, f'`{get_translation("gauthTokenErr")}`')
        if flow:
            try:
                creds = flow.step2_exchange(code)
                set(user_id, creds)
                edit(message, f'`{get_translation("gauthTokenSuccess")}`')
            except FlowExchangeError:
                edit(
                    message,
                    f'`{get_translation("gauthTokenInvalid")}`',
                )
            flow = None
        else:
            edit(message, f'`{get_translation("gauthFirstRun")}`')
    elif args[0] == "revoke":
        remove_(user_id)
        edit(message, f'`{get_translation("gauthTokenRevoke")}`')
    else:
        edit(message, get_translation("gdriveUsage"))


@sedenify(pattern="^.gupload")
def drive_upload(message):

    if get(message.from_user.id) is None:
        return edit(message, f'`{get_translation("gauthFirstRun")}`')

    drive = Gdrive(message)
    reply = message.reply_to_message
    if reply and reply.document:
        file_name = reply.document.file_name

        start_time = time()
        progress = Progress(message, file_name, start_time)

        down_file = download_media_wc(reply, file_name, progress=progress.download)
        replace(path.join("downloads", file_name), file_name)

        drive.upload_to_gdrive(file_name)

    else:

        args = extract_args(message)
        if not args.startswith("https://" or "http://"):
            return edit(message, f"`Geçerli bir url girin.`")

        is_drive = match("^https://drive.google.com", args)
        if is_drive:
            return drive.copy_file_gdrive(args)
        else:
            dl = drive.download_link(args)

        drive.upload_to_gdrive(dl)


@sedenify(pattern=".gdownload")
def gdownload(message):
    if get(message.from_user.id) is None:
        return edit(message, f'`{get_translation("gauthFirstRun")}`')
    else:
        pass
    args = extract_args(message)

    if not match("^https://drive\.google\.com", args):
        return edit(message, f'`{get_translation("onlySupportGdrive")}`')

    drive = Gdrive(message)
    drive.upload_to_telegram(args)


HELP.update({"gdrive": get_translation("gdriveUsage")})
