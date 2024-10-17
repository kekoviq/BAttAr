import sys
import asyncio
import randomstuff
import BRUS
from BRUS import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from .Config import Config
from .core.logger import logging
from .core.session import kekoviq
from .utils import (
    add_bot_to_logger_group,
    install_externalrepo,
    ipchange,
    load_plugins,
    setup_bot,
    mybot,
    startupmessage,
    verifyLoggerGroup,
    saves,
)

LOGS = logging.getLogger("BRUS")

print(BRUS.__copyright__)
print("Licensed under the terms of the " + BRUS.__license__)

cmdhr = Config.COMMAND_HAND_LER

async def create_rs_client():
    return randomstuff.AsyncClient(api_key=Config.RANDOM_STUFF_API_KEY, version="4")

try:
    LOGS.info("جارِ بدء بوت الخفاش ✓")
    kekoviq.loop.run_until_complete(setup_bot())
    LOGS.info("تم اكتمال تنصيب البوت ✓")
except Exception as e:
    LOGS.error(f"Error during bot setup: {str(e)}")
    sys.exit()

try:
    LOGS.info("يتم تفعيل وضع الانلاين")
    kekoviq.loop.run_until_complete(mybot())
    LOGS.info("تم تفعيل وضع الانلاين بنجاح ✓")
except Exception as jep:
    LOGS.error(f"- {jep}")
    sys.exit()

class CatCheck:
    def __init__(self):
        self.sucess = True

Catcheck = CatCheck()

async def startup_process():
    check = await ipchange()
    if check is not None:
        Catcheck.sucess = False
        return
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨")
    print("᯽︙بـوت الخفاش يعـمل بـنجاح ")
    print(
        f"تم تشغيل الانلاين تلقائياً ارسل {cmdhr}الاوامر لـرؤيـة اوامر السورس\
        \nللمسـاعدة تواصـل  https://t.me/ISVSVI"
    )
    print("✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨")
    await verifyLoggerGroup()
    await saves()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Catcheck.sucess = True
    return

async def externalrepo():
    if Config.VCMODE:
        await install_externalrepo("https://github.com/kekoviq/music", "main", "music")

async def main():
    await externalrepo()
    await startup_process()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    if len(sys.argv) not in (1, 3, 4):
        kekoviq.disconnect()
    elif not Catcheck.sucess:
        if HEROKU_APP is not None:
            HEROKU_APP.restart()
    else:
        try:
            kekoviq.run_until_disconnected()
        except ConnectionError:
            pass
