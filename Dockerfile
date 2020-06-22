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

# Copyright (c) @NaytSeyd | 2020
FROM naytseyd/sedenbot:latest

# Maintainer
MAINTAINER Ahmet Acikgoz <NaytSeyd@yandex.com>

# Zaman dilimini ayarla
ENV TZ=Europe/Istanbul

# Çalışma dizini
ENV PATH="/root/sedenuser/bin:$PATH"
WORKDIR /root/sedenuser

# Repoyu klonla
RUN git clone -b seden https://github.com/TeamDerUntergang/Telegram-SedenUserBot /root/sedenuser

# Oturum ve yapılandırmayı kopyala (varsa)
COPY ./sample_config.env ./sedenbot.session* ./config.env* /root/sedenuser/

# Botu çalıştır
RUN pip3 install -r requirements.txt
CMD ["python3","seden.py"]
