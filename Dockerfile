# We're Using NaytSeyd's Special Docker
FROM naytseyd/sedenbot:j1xlte

# Working Directory
WORKDIR /trzpro/

# Clone Repo
RUN git clone -b seden https://github.com/trzpro/Telegram-SedenUserBot.git /trzpro/
