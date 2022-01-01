# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

import math
from os import remove, path

from exifread import process_file
from fractions import Fraction
from PIL import Image
from sedenbot import HELP
from sedenecem.core import (
    download_media_wc,
    edit,
    get_translation,
    sedenify,
)


@sedenify(pattern="^.exif")
def exif_data(message):
    reply = message.reply_to_message
    google_coordinate = ["https://www.google.com/maps?q="]
    edit(message, f'`{get_translation("exifProcess")}`')

    if reply:
        data = check_media(reply)

        if not data:
            edit(message, f'`{get_translation("exifError")}`')
            return

    # Download Media
    image_file = download_media_wc(reply, "image.jpg")
    image = open(image_file, "rb")
    remove(image_file)

    # Extract EXIF data
    data = process_file(image)

    if not data:
        edit(message, f'`{get_translation("exifError")}`')
        return

    # Get EXIF tags
    tag_keys = list(data.keys())
    tag_keys.sort()

    # Create dictionary for conversion functions
    unit_dict = {
        "EXIF ApertureValue": calculate_aperture,
        "EXIF BrightnessValue": calculate_brightness,
        "EXIF FNumber": calculate_fnumber,
        "EXIF FocalLength": calculate_focal,
        "EXIF ShutterSpeedValue": calculate_shutter,
        "GPS GPSAltitude": calculate_altitude,
        "GPS GPSLatitude": calculate_gps,
        "GPS GPSLatitudeRef": calculate_latitude_ref,
        "GPS GPSLongitude": calculate_gps,
        "GPS GPSLongitudeRef": calculate_longitude_ref,
        "JPEGThumbnail": handle_thumbnail,
    }

    # Build EXIF data string
    data_str = get_translation("exifLog")
    for i in tag_keys:
        if i in unit_dict.keys():
            converted = ""

            # GPS Data
            if "GPS" == i.split(" ")[0]:
                converted = unit_dict[i](data[i].printable, google_coordinate)

            # Thumbnail Image Data in Byte Array
            elif type(data[i]) == bytes:
                converted = unit_dict[i](data[i])

            # Others
            else:
                converted = unit_dict[i](data[i].printable)

            data_str += "{0} : {1}\n".format(i, converted)
        else:
            data_str += "{0} : {1}\n".format(i, str(data[i]))
    if len(google_coordinate) == 5:
        google_coordinate.insert(0, get_translation("exifMaps"))
        data_str += "".join(google_coordinate)
        google_coordinate.insert(-1, "\n")

    edit(message, data_str)


def calculate_aperture(string):
    division = string.split("/")
    return "f/%.1f" % (
        math.sqrt(2.0) ** (int(division[0]) / int(division[1]))
    )


def calculate_brightness(string):
    division = string.split("/")
    return "%.2f EV" % (int(division[0]) / int(division[1]))


def calculate_fnumber(string):
    division = string.split("/")
    return "f/%.1f" % (int(division[0]) / int(division[1]))


def calculate_focal(string):
    division = string.split("/")
    return "{0} mm".format(
        str(math.floor(int(division[0]) / int(division[1])))
    )


def calculate_shutter(string):
    division = string.split("/")
    return "1/{0} sec".format(
        str(math.floor(2 ** (int(division[0]) / int(division[1]))))
    )


def calculate_altitude(string, google_coordinate):
    ret = string
    division = string.split("/")
    if "/" in ret:
        ret = "%.1f m" % (int(division[0]) / int(division[1]))
    return ret


def calculate_gps(coord, google_coordinate):
    coord_list = coord.split(",")
    hour = int(coord_list[0].replace("[", ""))
    minutes = coord_list[1].strip().split("/")
    seconds = coord_list[2].strip().replace("]", "").split("/")
    if len(minutes) > 1:
        minutes = int(minutes[0]) / int(minutes[1])
        seconds = (minutes % 1) * 60
    else:
        minutes = int(minutes[0])
        seconds = int(seconds[0]) / int(seconds[1])

    google_coordinate.append(
        f"{hour}%C2%B0{math.floor(minutes)}'{seconds:.2f}%22"
    )
    return f"{hour}°{math.floor(minutes)}'{seconds:.2f}\""


def calculate_latitude_ref(coord, google_coordinate):
    google_coordinate.append(f"{coord.strip()}+")
    return coord.strip()


def calculate_longitude_ref(coord, google_coordinate):
    google_coordinate.append(coord.strip())
    return coord.strip()


def handle_thumbnail(img):
    return ""


def check_media(reply_message):
    data = False

    if reply_message and reply_message.media:
        if reply_message.photo:
            data = True
        elif reply_message.sticker and not reply_message.sticker.is_animated:
            data = True
        elif reply_message.document:
            name = reply_message.document.file_name
            print(name)
            print(name[name.find(".") + 1 :])
            if (
                name
                and "." in name
                and path.splitext(name)[1] in [".png", ".jpg", ".jpeg", ".webp"]
            ):
                data = True

    return data


HELP.update({"exif": get_translation("exifInfo")})
