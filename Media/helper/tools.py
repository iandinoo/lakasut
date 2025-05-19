import asyncio
import datetime

from pyrogram import *
from pytz import timezone
from datetime import datetime

from Media.helper.database import *
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, UserDeactivatedBan

async def get_readable_time(seconds: int) -> str:    
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time
    
def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])
  
async def send_msg(chat_id, message):
    try:
        broadcast = await get_broadcast()
        if broadcast == False:
            await message.forward(chat_id=chat_id)
        elif broadcast == True:
            await message.copy(chat_id=chat_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(int(e.value))
        return await send_msg(chat_id, message)
    except UserIsBlocked:
        await increment_bot_removed_users()
        await remove_gcast(chat_id)
        return 403, "Pengguna diblokir"
    except (UserDeactivatedBan, InputUserDeactivated):
        await increment_deleted_accounts()
        await remove_gcast(chat_id)
        return 410, "Akun pengguna dinonaktifkan"
        
async def remove_duplicates(users):
    seen = set()
    unique_users = []
    
    for user in users:
        if user not in seen:
            seen.add(user)
            unique_users.append(user)
        else:
            print(f"ID pengguna duplikat ditemukan dan dihapus: {user}")
            await remove_gcast(user)
    return unique_users
