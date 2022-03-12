from io import FileIO
from os import path, remove
from queue import Queue
from re import findall, search
from shutil import copy
from time import time

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from pyrogram.types import Message
from requests import get
from sedenbot import GDRIVE_FOLDER_ID, HELP, LOGS
from sedenecem.core import (
    download_media_wc,
    edit,
    extract_args,
    get_translation,
    reply_doc,
    sedenify,
)


class Progress:
    def __init__(self, msg: Message, file_name, start_time):
        self.msg = msg
        self.file_name = file_name
        self.start_time = start_time

    def pyrogram_download(self, current, total):
        percentage = float(current * 100 / total)
        if (curr_time := time()) - self.start_time > 5:
            self.start_time = curr_time
            self.msg.edit_text(
                get_translation(
                    'pyrogramDown',
                    ['**', '`', self.file_name, f'½{round(percentage, 2)}'],
                )
            )


class WebHelper:
    def __init__(self, message: Message):
        self.message = message

    def download_link(self, queue: Queue):
        while not queue.empty():
            url = queue.get()
            re_url = search("^https://drive.google.com", url)
            if re_url:
                self.download_link_gdrive(url)

                queue.task_done()
            else:
                r = get(url, stream=True)

                total_size = int(r.headers.get('content-length', 0))
                downloaded_size = 0

                if 'Content-Disposition' in r.headers.keys():
                    fname = findall("filename=(.+)", r.headers["Content-Disposition"])[
                        0
                    ]
                else:
                    fname = url.split('/')[-1]

                start_time = time()
                with open(f'./{fname}', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=50 * 1024 * 1024):
                        f.write(chunk)
                        downloaded_size += int(len(chunk))
                        percentage = round(float(downloaded_size * 100 / total_size), 2)
                        print(f'Hız {downloaded_size / total_size}\n')
                        if (curr_time := time()) - start_time > 5:
                            start_time = curr_time
                            edit(
                                self.message,
                                get_translation(
                                    'reqDown', ['**', '`', fname, f'½{percentage}']
                                ),
                            )
                self.upload_to_gdrive(fname)
                del fname

                queue.task_done()

    def download_link_gdrive(self, link):
        file_id = search('d\/(.*)\/v', link).group(1)

        scopes = ['https://www.googleapis.com/auth/drive']
        creds = Credentials.from_authorized_user_file('token.json', scopes)
        service = build('drive', 'v3', credentials=creds)

        file_info = (
            service.files()
            .get(fileId=file_id, fields='name,size', supportsTeamDrives=True)
            .execute()
        )
        request = service.files().get_media(fileId=file_id, supportsTeamDrives=True)

        fh = open(f'{file_info.get("name")}', 'wb')
        downloader = MediaIoBaseDownload(
            fd=fh, request=request, chunksize=50 * 1024 * 1024
        )

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            progress = edit(
                get_translation(
                    self.message,
                    'gdriveDown',
                    [
                        '**',
                        '`',
                        file_info.get('name'),
                        f'½{int(status.progress() * 100)}',
                    ],
                )
            )
        edit(
            self.message,
            get_translation('gdriveDownComplete', ['**', '`', file_info.get('name')]),
        )
        self.upload_to_gdrive(file_info.get("name"))

    def upload_to_gdrive(self, filename):

        scopes = ['https://www.googleapis.com/auth/drive']
        creds = Credentials.from_authorized_user_file('token.json', scopes)
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': filename,
            'parents': [GDRIVE_FOLDER_ID],
        }

        media = MediaFileUpload(filename, resumable=True, chunksize=50 * 1024 * 1024)

        file = service.files().create(
            body=file_metadata, media_body=media, fields='id', supportsTeamDrives=True
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
                            'gdriveUp',
                            ['**', '`', filename, f'½{int(status.progress() * 100)}'],
                        ),
                    )
            else:
                edit(
                    self.message,
                    get_translation('gdriveUpComplete', ['**', '`', filename]),
                )
                remove(filename)


@sedenify(pattern='.gauth')
def drive_auth(message):
    msg = message.reply_to_message
    if msg and msg.document:
        download_media_wc(data=msg, file_name='token.json')
        copy('./downloads/token.json', '.')
        edit(message, get_translation('gauthTokenSucces', ['`']))
    else:
        edit(message, get_translation('gdriveTokenErr', ['`']))


@sedenify(pattern='.gupload')
def drive_upload(message):

    if path.exists('token.json'):
        pass
    else:
        return edit(message, get_translation('gauthTokenErr', ['`']))

    reply = message.reply_to_message
    if reply:
        file_name = reply.document.file_name

        start_time = time()
        progress = Progress(message, file_name, start_time)

        down_file = download_media_wc(
            reply, file_name, progress=progress.pyrogram_download
        )

        scopes = ['https://www.googleapis.com/auth/drive']
        creds = Credentials.from_authorized_user_file('token.json', scopes)
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': file_name,
            'parents': [GDRIVE_FOLDER_ID],
        }

        media = MediaFileUpload(down_file, resumable=True, chunksize=50 * 1024 * 1024)

        file = service.files().create(
            body=file_metadata, media_body=media, fields='id', supportsTeamDrives=True
        )
        start_time = time()
        response = None
        while response is None:
            status, response = file.next_chunk()
            if status:
                if (curr_time := time()) - start_time > 5:
                    start_time = curr_time
                    edit(
                        message,
                        get_translation(
                            'gdriveUp',
                            ['**', '`', file_name, int(status.progress() * 100)],
                        ),
                    )
        edit(message, get_translation('gdriveUpComplete', ['**', '`', file_name]))
        remove(down_file)
    else:
        args = extract_args(message).split(' ')
        queue = Queue()

        for i in args:
            queue.put(i)

        web = WebHelper(message)
        web.download_link(queue)


@sedenify(pattern='.gdownload')
def gdownload(message):
    if path.exists('token.json'):
        pass
    else:
        return edit(message, get_translation('gauthTokenErr', ['`']))
    args = extract_args(message)
    file_id = search('d\/(.*)\/v', args).group(1)

    scopes = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_authorized_user_file('token.json', scopes)
    service = build('drive', 'v3', credentials=creds)

    file_info = (
        service.files()
        .get(fileId=file_id, fields='name,size', supportsTeamDrives=True)
        .execute()
    )

    if int(file_info.get('size')) >= 2147483648:
        return edit(message, get_translation('tgUpLimit', ['`']))
    request = service.files().get_media(fileId=file_id, supportsTeamDrives=True)

    fh = FileIO(f'./downloads/{file_info.get("name")}', 'wb')
    downloader = MediaIoBaseDownload(fd=fh, request=request, chunksize=50 * 1024 * 1024)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        progress = edit(
            message,
            get_translation(
                'gdriveDown',
                ['**', '`', file_info.get('name'), int(status.progress() * 100)],
            ),
        )

    start_time = time()
    progress = Progress(message, file_info.get('name'), start_time)

    reply_doc(
        message,
        f'./downloads/{file_info.get("name")}',
        progress=progress.pyrogram_download,
        delete_orig=False,
    )
    message.delete()


HELP.update({'gdrive': get_translation('gdriveUsage')})
