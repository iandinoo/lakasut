import asyncio
import datetime

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Media import *
from Media.config import *
from Media.helper.tools import *
from Media.helper.database import *
from Media.helper.date_info import *
from Media.helper.cache import user_cooldowns, users_cancel

C30 = """
<b>ᴘᴇɴɢᴀᴛᴜʀᴀɴ.</b>

__sɪʟᴀʜᴋᴀɴ ᴘɪʟɪʜ ᴍᴇɴᴜ ʏᴀɴɢ ɪɴɢɪɴ ᴋᴀᴍᴜ ɢᴜɴᴀᴋᴀɴ.__
"""

@bot.on_message(filters.command("menu") & filters.private & filters.user(OWNER_ID))
async def menu(client, message):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("sᴇᴛ ʟɪɴᴋ", callback_data="setlink"),
            InlineKeyboardButton("sᴇᴛ ʜᴀʀɢᴀ", callback_data="setprice"),
        ],
        [
            InlineKeyboardButton("sᴇᴛ ғsᴜʙ", callback_data="setforce"),
            InlineKeyboardButton("sᴇᴛ ʟᴏɢs", callback_data="setlogger"),
        ],
        [
            InlineKeyboardButton("sᴇᴛ ᴡᴇʟᴄᴏᴍᴇ", callback_data="setwelcome"),
            InlineKeyboardButton("sᴇᴛ ᴛᴡᴏᴛᴇxᴛ", callback_data="settexttwo"),
        ],
        [
            InlineKeyboardButton("ꜱᴇᴛ ᴏʀᴋᴜᴛ", callback_data="set_merchant"),
            InlineKeyboardButton("🔜", callback_data="callback_two"),
        ],
    ])
    await message.delete()
    user = len(await get_gcast())
    await message.reply_text(C30.format(user), reply_markup=keyboard)
    
@bot.on_callback_query(filters.regex("menu_callback"))
async def menu_callback(client, callback_query):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("sᴇᴛ ʟɪɴᴋ", callback_data="setlink"),
            InlineKeyboardButton("sᴇᴛ ʜᴀʀɢᴀ", callback_data="setprice"),
        ],
        [
            InlineKeyboardButton("sᴇᴛ ғsᴜʙ", callback_data="setforce"),
            InlineKeyboardButton("sᴇᴛ ʟᴏɢs", callback_data="setlogger"),
        ],
        [
            InlineKeyboardButton("sᴇᴛ ᴡᴇʟᴄᴏᴍᴇ", callback_data="setwelcome"),
            InlineKeyboardButton("sᴇᴛ ᴛᴡᴏᴛᴇxᴛ", callback_data="settexttwo"),
        ],
        [
            InlineKeyboardButton("ꜱᴇᴛ ᴏʀᴋᴜᴛ", callback_data="set_merchant"),
            InlineKeyboardButton("🔜", callback_data="callback_two"),
        ],
    ])
    user = len(await get_gcast())
    await callback_query.edit_message_text(C30.format(user), reply_markup=keyboard)

@bot.on_callback_query(filters.regex("callback_two"))
async def callback_two(client, callback_query):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="toggle_broadcast"),
        ],
        [
            InlineKeyboardButton("ᴍᴀɪɴᴛᴇɴᴄᴇɴᴛ", callback_data="toggle_maintenance"),
        ],
        [
            InlineKeyboardButton("ᴏɴ/ᴏғғ ʟᴏɢs", callback_data="toggle_logger"),
        ],
        [
            InlineKeyboardButton("ᴏɴ/ᴏғғ ғsᴜʙ", callback_data="toggle_force"),
        ],
        [
            InlineKeyboardButton("🔚", callback_data="menu_callback"),
        ],
    ])
    user = len(await get_gcast())
    await callback_query.edit_message_text(C30.format(user), reply_markup=keyboard)

@bot.on_callback_query(filters.regex("set_merchant"))
async def set_merchant(client, callback_query):
    user_id = callback_query.from_user.id
    
    await callback_query.edit_message_text(
        "<b>🤖 Bot:</b> Silakan masukan [QRIS_CODE](t.me/QRcodegen_bot) anda?\n\n"
        "/cancel  - Untuk Membatalkan!"
    )

    try:
        user_response = await client.listen(user_id, filters.text)
        qris_code = user_response.text.strip()

        if user_response.text.startswith("/"):
            await user_response.delete()
            await callback_query.edit_message_text(
                "<b>❌ Proses Input Dibatalkan!</b>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                ])
            )
            return
        
        await user_response.delete()

        await callback_query.edit_message_text(
            "<b>🤖 Bot:</b> Silakan masukan [Merchant Code](https://okeconnect.com/integrasi/payment_gateway) anda?\n\n"
            "/cancel  - Untuk Membatalkan!"
        )

        user_response = await client.listen(user_id, filters.text)
        merchant_code = user_response.text.strip()

        if user_response.text.startswith("/"):
            await user_response.delete()
            await callback_query.edit_message_text(
                "<b>❌ Proses Input Dibatalkan!</b>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                ])
            )
            return
        
        await user_response.delete()

        await callback_query.edit_message_text(
            "<b>🤖 Bot:</b> Silakan masukan [API Key](https://okeconnect.com/integrasi/payment_gateway) anda?\n\n"
            "/cancel  - Untuk Membatalkan!"
        )

        user_response = await client.listen(user_id, filters.text)
        api_key = user_response.text.strip()

        if user_response.text.startswith("/"):
            await user_response.delete()
            await callback_query.edit_message_text(
                "<b>❌ Proses Input Dibatalkan!</b>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                ])
            )
            return
        
        await user_response.delete()

        await set_orkut(qris_code, merchant_code, api_key)

        await callback_query.edit_message_text(
            f"<b>✅ Berhasil Menambahkan Request Order Kuota!</b>\n\n"
            f"<b>• QRIS Code:</b> `{qris_code}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="merchant_orkut")]
            ])
        )
    
    except Exception as e:
        await callback_query.edit_message_text(
            "<b>❌ Terjadi kesalahan, silakan coba lagi!</b>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="merchant_orkut")]
            ])
        )
        
@bot.on_callback_query(filters.regex("toggle_broadcast"))
async def toggle_broadcast(client, callback_query):
    new_status = not await get_broadcast()
    await set_broadcast(new_status)
    status = "Copy" if new_status else "Forward"
    await callback_query.answer(f"Type Broadcast Sekarang Adalah '{status}'", show_alert=True)
    
@bot.on_callback_query(filters.regex("toggle_maintenance"))
async def toggle_maintenance(client, callback_query):
    new_status = not await get_maintenance()
    await set_maintenance(new_status)
    status = "❌ Maintenance Dimatikan." if new_status else "✅ Maintenance Dihidupkan."
    await callback_query.answer(f"'{status}'", show_alert=True)
    
@bot.on_callback_query(filters.regex("toggle_logger"))
async def toggle_logger(client, callback_query):
    if not await get_logger():
        await callback_query.answer(f"❌ Tambahkan Logger Terlebih Dahulu.", show_alert=True)
        return
        
    new_status = not await get_status_logger()
    await set_status_logger(new_status)
    status = "✅ Diaktifkan" if new_status else "❌ Dinonaktifkan"
    await callback_query.answer(f"Logger sekarang {status}", show_alert=True)

@bot.on_callback_query(filters.regex("toggle_force"))
async def toggle_force(client, callback_query):
    if not await get_forcesub():
        await callback_query.answer("❌ Tambahkan Forcesub Terlebih Dahulu.", show_alert=True)
        return
        
    new_status = not await get_force_status()
    await set_force_status(new_status)
    status = "✅ Diaktifkan" if new_status else "❌ Dinonaktifkan"
    await callback_query.answer(f"Fitur ForceSub sekarang {status}", show_alert=True)
    
@bot.on_callback_query(filters.regex("setprice"))
async def setprice(client, callback_query):
    user_id = callback_query.from_user.id

    callback = await callback_query.edit_message_text(
        "<b>🤖 Bot:</b> Silakan masukan harga baru - minimal 100p?\n\n"
        "__Contoh 1000__\n\n"
        f"/cancel - Untuk Membatalkan!"
    )

    while True:
        try:
            message = await bot.listen(user_id, filters.text, timeout=60)
            input_text = message.text.strip()

            if message.text.startswith("/"):
                await message.delete()
                await callback_query.edit_message_text(
                    "<b>❌ Proses Input Dibatalkan!</b>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                    ])
                )
                return
                
            if input_text.isdigit():
                price = int(input_text)
                if price >= 100:
                    await message.delete()
                    await callback.edit(
                        f"<b>✅ Harga Berhasil Diubah Menjadi Rp.{price}</b>",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                        ])
                    )
                    await set_price(input_text)
                    break
                else:
                    await message.delete()
                    clbk = await message.reply("<b>❌ Harga harus minimal Rp.100p Silakan coba lagi.</b>")
                    await asyncio.sleep(2)
                    await clbk.delete()
                    continue
            else:
                await message.delete()
                clbk = await message.reply("<b>❌ Input tidak valid. Harap masukkan angka yang valid.</b>")
                await asyncio.sleep(2)
                await clbk.delete()
                continue

            if users_cancel.get(user_id, False):
                break

        except asyncio.TimeoutError:
            break
            
@bot.on_callback_query(filters.regex("setlink"))
async def setlink(client, callback_query):
    user_id = callback_query.from_user.id

    callback = await callback_query.edit_message_text(
        "<b>🤖 Bot:</b> Silakan masukan chat_id grup/channel anda untuk membuat link anda?\n\n"
        "__Contoh -100__\n\n"
        f"/cancel - Untuk Membatalkan!"
    )
    
    while True:
        try:
            message = await bot.listen(user_id, filters.text)
            chat_id = int(message.text)
            
            if message.text.startswith("/"):
                await message.delete()
                await callback_query.edit_message_text(
                    "<b>❌ Proses Input Dibatalkan!</b>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                    ])
                )
                return
                            
            try:
                await set_chat_id(chat_id)
                await bot.send_message(chat_id, "<b>✅ Groups/Channel Ini Berhasil Diatur Untuk Link.</b>")
                await callback.edit(
                    "<b>✅ Groups/Channel ini berhasil diatur untuk chat_id link:</b> " + str(chat_id),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                    ])
                )
                
                await asyncio.sleep(2)
                await message.delete()
                break
                
            except Exception as e:
                xx = await callback_query.message.reply(f"<b>❌ Terjadi kesalahan saat memeriksa keanggotaan bot di chat.</b> `{e}`")
                await asyncio.sleep(2)
                await message.delete()
                await xx.delete()
                continue

        except ValueError:
            xx = await callback_query.message.reply_text("<b>❌ Harap masukkan chat_id yang valid.</b>")
            await asyncio.sleep(2)
            await message.delete()
            await xx.delete()
            continue
        except Exception as e:
            xx = await callback_query.message.reply(f"<b>❌ Terjadi kesalahan.</b> `{e}`")
            await asyncio.sleep(2)
            await message.delete()
            await xx.delete()
            continue 
            
@bot.on_callback_query(filters.regex("setlogger"))
async def setlogger(client, callback_query):
    user_id = callback_query.from_user.id

    callback = await callback_query.edit_message_text(
        "<b>🤖 Bot:</b> Silakan masukan chat_id grup/channel anda untuk membuat logger anda?\n\n"
        "__Contoh -100__\n\n"
        f"/cancel - Untuk Membatalkan!"
    )

    while True:
        try:
            message = await bot.listen(user_id, filters.text)
            chat_id = int(message.text)
            
            if message.text.startswith("/"):
                await message.delete()
                await callback_query.edit_message_text(
                    "<b>❌ Proses Input Dibatalkan!</b>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                    ])
                )
            
            return
                            
            try:
                await set_logger(chat_id)
                await bot.send_message(chat_id, "<b>✅ Groups/Channel Ini Berhasil Diatur Untuk Logger.</b>")
                await callback.edit(
                    "<b>✅ Groups/Channel ini berhasil diatur untuk chat_id logger:</b> " + str(chat_id),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                    ])
                )
                
                await asyncio.sleep(2)
                await message.delete()
                break
                
            except Exception as e:
                xx = await callback_query.message.reply(f"<b>❌ Terjadi kesalahan saat memeriksa keanggotaan bot di chat.</b> `{e}`")
                await asyncio.sleep(2)
                await message.delete()
                await xx.delete()
                continue

        except ValueError:
            xx = await callback_query.message.reply_text("<b>❌ Harap masukkan chat_id yang valid.</b>")
            await asyncio.sleep(2)
            await message.delete()
            await xx.delete()
            continue
        except Exception as e:
            xx = await callback_query.message.reply(f"<b>❌ Terjadi kesalahan saat mengatur logging.</b> `{e}`")
            await asyncio.sleep(2)
            await message.delete()
            await xx.delete()
            continue 

@bot.on_callback_query(filters.regex("setforce"))
async def setforce(client, callback_query):
    user_id = callback_query.from_user.id

    callback = await callback_query.edit_message_text(
        "<b>🤖 Bot:</b> Silakan masukkan username grup/channel anda?\n\n"
        "__Tanpa @ Dan htpps__\n\n"
        f"/cancel - Untuk Membatalkan!"
    )
    
    while True:
        try:
            message = await bot.listen(user_id, filters.text)
            username = message.text.strip()
            
            if message.text.startswith("/"):
                await message.delete()
                await callback_query.edit_message_text(
                    "<b>❌ Proses Input Dibatalkan!</b>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                    ])
                )
                return
                            
            if "@" in username:
                await message.delete()
                xx = await callback_query.message.reply("❌ <b>Username tidak valid!</b> Jangan sertakan '@' dalam username.")
                await asyncio.sleep(2)
                await xx.delete()
                continue

            try:
                chat_info = await bot.get_chat(username)
                await set_forcesub(username)
                await bot.send_message(chat_info.id, "<b>✅ Groups/Channel ini berhasil diatur untuk force subscribe!</b>")
                
                await callback.edit(
                    f"<b>✅ Force subscribe berhasil diatur untuk @{chat_info.username} dan username disimpan.</b>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                    ])
                )
                await message.delete()
            except Exception as e:
                await message.delete()
                xx = await callback_query.message.reply(f"<b>❌ Terjadi kesalahan saat menyimpan username:</b> `{str(e)}`")
                await asyncio.sleep(2)
                await xx.delete()
                continue
                
        except Exception as e:
            await message.delete()
            xx = await callback_query.message.reply(f"<b>❌ Terjadi kesalahan:</b> `{str(e)}`")
            await asyncio.sleep(2)
            await xx.delete()
            continue 

@bot.on_callback_query(filters.regex("setwelcome"))
async def setwelcome(client, callback_query):
    user_id = callback_query.from_user.id

    callback = await callback_query.edit_message_text(
        "<b>🤖 Bot:</b> Silakan masukkan pesan welcome yang baru?\n\n"
        "/cancel - Untuk Membatalkan!"
    )

    try:
        user_response = await bot.listen(user_id, filters.text)
        user_input = user_response.text.strip()
        
        if user_response.text.startswith("/"):
            await user_response.delete()
            await callback_query.edit_message_text(
                "<b>❌ Proses Input Dibatalkan!</b>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                ])
            )
            return

        await user_response.delete()
        await set_welcome(user_input)
        await callback.edit(
            f"<b>✅ Successfully Saved Welcome Message.</b>\n\n`{user_input}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
            ])
        )
            
    except Exception as e:
        await callback_query.message.reply("<b>Terjadi Kesahalan:</b> `{e}`")
        return

@bot.on_callback_query(filters.regex("settexttwo"))
async def settexttwo(client, callback_query):
    user_id = callback_query.from_user.id

    callback = await callback_query.edit_message_text(
        "<b>🤖 Bot:</b> Silakan masukkan pesan text saat orang membeli link?\n\n"
        "/cancel - Untuk Membatalkan!"
    )

    try:
        user_response = await bot.listen(user_id, filters.text)
        user_input = user_response.text.strip()

        if user_response.text.startswith("/"):
            await user_response.delete()
            await callback_query.edit_message_text(
                "<b>❌ Proses Input Dibatalkan!</b>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
                ])
            )
            return
        
        await user_response.delete()
        await set_text_two(user_input)
        await callback.edit(
            f"<b>✅ Successfully Saved Message.</b>\n\n`{user_input}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kembali", callback_data="menu_callback")]
            ])
        )
            
    except Exception as e:
        await callback_query.message.reply("<b>Terjadi Kesahalan:</b> `{e}`")
        return
        
@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    users = await get_gcast()
    users = await remove_duplicates(users)
    msg = get_arg(message)
    if message.reply_to_message:
        msg = message.reply_to_message

    if not msg:
        await message.reply(text="**Reply atau berikan saya sebuah pesan!**")
        return
    
    out = await message.reply(text="**Memulai Broadcast...**")
    
    if not users:
        await out.edit(text="**Maaf, Broadcast Gagal Karena Belum Ada user**")
        return
    
    done = 0
    failed = 0
    for user in users:
        try:
            await send_msg(user, message=msg)
            done += 1
        except:
            failed += 1
    await out.edit(f"✅ **Berhasil Mengirim Pesan Ke {done} User.**\n❌ **Gagal Mengirim Pesan Ke {failed} User.**")
