import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

from Media import bot
from Media.helper.database import get_forcesub, get_force_status

def force_channel(forcesub, username):
    FORCESUB = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=f"t.me/{forcesub}"),
            ],
            [
                InlineKeyboardButton(f"• ᴄᴏʙᴀ ʟᴀɢɪ •", url=f"http://t.me/{username}?start=start"),
            ]
        ]
    )
    return FORCESUB
    
@bot.on_message(filters.incoming & filters.private, group=-1)
async def forced_entry_into_groups(client, message):
    if not await get_force_status():
        return
        
    try:
        try:
            forcesub = await get_forcesub()
            await client.get_chat_member(forcesub, message.from_user.id)
        except UserNotParticipant:
            if forcesub.isalpha():
                link = "https://t.me/" + forcesub
            else:
                chat_info = await client.get_chat(forcesub)
                link = chat_info.invite_link
            try:
                btn = force_channel(forcesub, (await bot.get_me()).username)
                
                await message.reply_text(
                    f"<b>{message.from_user.first_name}</b>ᴀɴᴅᴀ ᴅɪ ᴡᴀᴊɪʙ ᴋᴀɴ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴋsᴇs ʜᴀʟᴀᴍᴀɴ ʙᴇʀɪᴋᴜᴛɴʏᴀ..",
                    disable_web_page_preview=True, reply_markup=btn)

                await message.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        await message.reply_text("<b>ʙᴏᴛ ᴡᴀᴊɪʙ ᴀᴅᴍɪɴ ᴅɪ ᴄʜᴀɴɴᴇʟ ғsᴜʙ.</b>")
