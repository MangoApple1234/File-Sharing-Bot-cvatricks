#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from bot import Bot
from config import ADMINS, CHANNEL_ID, FORCE_SUB_CHANNEL
from helper_func import encode

@Bot.on_message((filters.private) & (filters.video | filters.document | filters.audio | filters.photo) & (~filters.command(['start','batch','genlink'])))
async def channel_post(client: Client, message: Message):
    try:
           await bot.get_chat_member(
                 chat_id=FORCE_SUB_CHANNEL,
                 user_id=update.from_user.id
           )
    except UserNotParticipant:
           await bot.send_message(
                 chat_id=update.chat.id,
                 text="You must join my updates channel to use me",
                 parse_mode="html",
                 reply_to_message_id=update.message_id,
                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = '✔️ Updates Channel', url = "https://t.me/Super_botz")]])
           )
           return
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.message_id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)
    await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID) & ~filters.edited)
async def new_post(client: Client, message: Message):
    converted_id = message.message_id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
