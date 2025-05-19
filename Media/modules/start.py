import os
import uuid
import json
import random
import logging
import asyncio
import requests
from PIL import Image
from io import BytesIO

from pyrogram import *
from pyromod import listen
from pyrogram.types import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Media import *
from Media.config import *
from Media.helper.tools import *
from Media.helper.database import *
from Media.helper.date_info import *
from httpx import AsyncClient, HTTPStatusError, TimeoutException, RequestError, ReadTimeout
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, UserDeactivatedBan

from datetime import timedelta
import datetime
import time

logging.basicConfig(level=logging.INFO)

C10 = """
<b>ᴅᴇᴛᴀɪʟs ᴘᴇᴍʙᴀʏᴀʀᴀɴ : </b>
- ᴛᴏᴛᴀʟ ғᴇᴇ : <b>{}</b>
- ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ : <b>{}</b>
sɪʟᴀʜᴋᴀɴ ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴍᴇᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ǫʀɪs.
• sᴇᴛᴇʟᴀʜ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ʟɪɴᴋ ᴀᴋᴀɴ ᴏᴛᴏᴍᴀᴛɪs ᴅɪʙᴇʀɪᴋᴀɴ.

<b>ᴘᴀʏᴍᴇɴᴛ ɪɴᴠᴏɪᴄᴇ</b>
{}
"""

API_CREATE_QRIS = "http://qris.autsc.my.id/api/create"
API_CHECK_PAYMENT = "https://mutasiv2.vercel.app/check-payment"

async def generate_unique_ref_id():
    return 'DCAS - ' + uuid.uuid4().hex[:16].upper()

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    gcast = await get_gcast()
    welcome = await get_welcome()
    if message.from_user.id not in gcast:
        await add_gcast(message.from_user.id)

    start_button = InlineKeyboardButton("• ᴊᴏɪɴ ᴍᴇᴅɪᴀ •", callback_data="create_qris")
    start_markup = InlineKeyboardMarkup([[start_button]])
        
    if not await get_maintenance():
        return await message.reply("ʙᴏᴛ sᴇᴅᴀɴɢ ᴅɪ ᴘᴇʀʙᴀɪᴋɪ ᴛᴏʟᴏɴɢ ʙᴇʀsᴀʙᴀʀ⏳")
    try:
        await message.reply(text=welcome, reply_markup=start_markup)
    except Exception as e:
        await message.reply(text=welcome, reply_markup=start_markup)

@bot.on_callback_query(filters.regex("transaction"))
async def view_transaction(client, callback_query):
    user_id = callback_query.from_user.id
    
    if "_" in callback_query.data:
        data_parts = callback_query.data.split("_")
        final_amount = int(data_parts[1])
        pay_invoice = data_parts[2]
    else:
        await callback_query.message.delete()
        await callback_query.answer('Terjadi kesalahan. ID transaksi tidak ditemukan.', show_alert=True)
        return
        
    try:
        user_data = await get_orkut()
        response = requests.get(API_CHECK_PAYMENT, params={"merchant": user_data.get('merchant'), "key": user_data.get('api_key')})

        if response.status_code == 200:
            data = response.json()
            
            if data["status"] == "success" and data["data"]:
                for payment in data["data"]:
                    if payment["amount"] == final_amount:
                        await callback_query.message.delete()
                        await delete_pending_transaction(user_id)
                        LOGGER("INFO").info(f"✅ Pembayaran Berhasil: {pay_invoice}")
                        await create_chat_invite(callback_query, pay_invoice)
                        await create_logger_link(callback_query, pay_invoice)
                        return
        else:
            await callback_query.message.delete()
            await callback_query.answer('❌ Terjadi kesalahan saat memeriksa status pembayaran.', show_alert=True)
            return
            
        await callback_query.message.reply("<b>❌ Selesaikan Pembayaran Terlebih Dahulu.</b>\n\n__Jika Anda Merasa Sudah Membayarnya, Silahkan Tunggu Beberapa Detik Lalu Coba Lagi.__")
    except UserIsBlocked:
        LOGGER("INFO").info(f"⛔ UserIsBlocked: {pay_invoice}")
        return
    except (UserDeactivatedBan, InputUserDeactivated):
        LOGGER("INFO").info(f"⛔ UserDeactivatedBan InputUserDeactivated: {pay_invoice}")
        return
    except Exception as e:
        await callback_query.message.reply(f'<b>❌ Terjadi kesalahan:</b> {str(e)}')
        return
            
@bot.on_callback_query(filters.regex("create_qris"))
async def create_payment_link(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id

    if not await get_orkut():
        return await cb.answer("❌ Pasang Orkut Terlebih Dahulu", show_alert=True)
        
    maintenance = await get_maintenance()
    if not maintenance:
        return await cb.answer("🛠️ BOT SEDANG PERBAIKAN - KEMBALI LAGI NANTI", show_alert=True)

    if await check_pending_transaction(user_id):
        return await cb.answer("❌ Anda masih punya transaksi yang belum terselesaikan, harap selesaikan terlebih dahulu atau dibatalkan.", show_alert=True)
    
    pay_invoice = await generate_unique_ref_id()

    try:
        minimal_amount = int(await get_price())
        total_fee = random.randint(1, 500)
        final_amount = minimal_amount + total_fee

        random_addition = f"Rp.{total_fee:,}".replace(",", ".")
        final_amount_str = f"Rp.{final_amount:,}".replace(",", ".")

        user_data = await get_orkut()
        response = requests.get(API_CREATE_QRIS, params={"amount": final_amount, "qrisCode": user_data.get('qris_code')})

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                download_url = data["data"]["download_url"]
                image_response = requests.get(download_url)

                if image_response.status_code == 200:
                    image = Image.open(BytesIO(image_response.content))
                    bio = BytesIO()
                    bio.name = 'qris.png'
                    image.save(bio, 'PNG')
                    bio.seek(0)

                    success_button = InlineKeyboardButton("• sᴜᴅᴀʜ ᴍᴇᴍʙᴀʏᴀʀ •", callback_data=f"transaction_{final_amount}_{pay_invoice}")
                    cancel_button = InlineKeyboardButton("• ʙᴀᴛᴀʟᴋᴀɴ ᴛʀᴀɴsᴀᴋsɪ •", callback_data="cancel")
                    start_markup = InlineKeyboardMarkup([[success_button], [cancel_button]])
                    
                    await cb.message.delete()
                    qris_message = await cb.message.reply_photo(photo=bio, caption=C10.format(random_addition, final_amount_str, pay_invoice), reply_markup=start_markup)

                    await create_pending_transaction(user_id)
                    LOGGER("INFO").info(f"🌀 Pembayaran Pending: {pay_invoice}")
                else:
                    await cb.message.reply("❌ Gagal mengambil gambar QRIS.")
            else:
                await cb.message.reply(f"❌ Error: {data.get('message', 'Unknown error.')}")
        else:
            await cb.message.reply("❌ Gagal memproses permintaan. Coba lagi nanti.")

    except UserIsBlocked:
        LOGGER("INFO").info(f"⛔ UserIsBlocked: {pay_invoice}")
        return
    except (UserDeactivatedBan, InputUserDeactivated):
        LOGGER("INFO").info(f"⛔ UserDeactivatedBan InputUserDeactivated: {pay_invoice}")
        return
    except Exception as e:
        await cb.message.reply(f"❌ Terjadi kesalahan: {str(e)}")
        return

@bot.on_callback_query(filters.regex("cancel"))
async def cancel(client, cb):
    user_id = cb.from_user.id
    await cb.message.delete()
    LOGGER("INFO").info(f"❌ Pembayaran Dibatalkan.")
    await delete_pending_transaction(user_id)
    await cb.message.reply("<b>ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴅɪʙᴀᴛᴀʟᴋᴀɴ.</b>")

@bot.on_message(filters.command("cncl") & filters.private)
async def cancel(client, message):
    user_id = message.from_user.id
    await delete_pending_transaction(user_id)
    await message.reply("<b>Pembayaran dibatalkan.</b>")

@bot.on_message(filters.command("clear") & filters.private)
async def clear(client, message):
    await clear_gcast()
    await message.reply("sukses")
    
async def create_chat_invite(cb, pay_invoice):
    chat_id = int(await get_chat_id())
    try:
        welcome = await get_text_two()
        expire_time = datetime.datetime.now() + timedelta(hours=1)
        invite_link = await bot.create_chat_invite_link(chat_id, member_limit=1, expire_date=expire_time)
        await cb.message.reply(
            f"{welcome}\n\n"
            f"{invite_link.invite_link}",
            disable_web_page_preview=True
        )
    except UserIsBlocked:
        LOGGER("INFO").info(f"⛔ UserIsBlocked: {pay_invoice}")
        return
    except (UserDeactivatedBan, InputUserDeactivated):
        LOGGER("INFO").info(f"⛔ UserDeactivatedBan InputUserDeactivated: {pay_invoice}")
        return
    except Exception as e:
        await cb.message.reply(f"<b>Terjadi kesalahan:</b> `{str(e)}`")
        return
        
async def create_logger_link(cb, pay_invoice):
    if not await get_status_logger():
        return
        
    chat = await bot.get_chat(await get_logger())
    price = float(await get_price())
    nominal = f"Rp.{price:,.2f}".replace(",", ".")
    mention = f"@{cb.from_user.username}" if cb.from_user.username else cb.from_user.mention

    view_profile_button = InlineKeyboardButton(
        "Profile", 
        url=f"t.me/{cb.from_user.username}"
    )
    
    try:
        message = await bot.send_message(
            chat_id=chat.id,
            text=(
                f"<b>ᴘᴇɴɢɢᴜɴᴀ ʙᴇʀɢᴀʙᴜɴɢ</b>\n"
                f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {mention}\n"
                f"<b>ʜᴀʀɢᴀ :</b> {nominal}\n"
                f"<b>ɪɴᴠᴏɪᴄᴇ</b> `{pay_invoice}`\n"             
            ),
        )
    except UserIsBlocked:
        LOGGER("INFO").info(f"⛔ UserIsBlocked: {pay_invoice}")
        return
    except (UserDeactivatedBan, InputUserDeactivated):
        LOGGER("INFO").info(f"⛔ UserDeactivatedBan InputUserDeactivated: {pay_invoice}")
        return
    except Exception as e:
        await cb.message.reply(f"<b>Terjadi kesalahan:</b> `{str(e)}`")
        return

@bot.on_message(filters.command("id") & filters.user(OWNER_ID))
async def id(client, message):
    user_id = message.from_user.id
    await delete_pending_transaction(user_id)
    await message.reply(f"🆔 {message.chat.title} : `{message.chat.id}`")
