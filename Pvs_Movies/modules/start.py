from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
import random
from Pvs_Movies import app
#from Pvs_Movies.database.chats_db import save_users, save_chats, get_users, get_chats
from config.config import FORCE_SUB_CHANNEL, SUPPORT, UPDATES, PHOTOS, BOT_NAME, BOT_USERNAME
import asyncio
from pyrogram.errors import UserNotParticipant

start_keyboard = Markup([
    [Button("Help & Commands", callback_data="help")],
    [Button("Support", url=f"https://t.me/{SUPPORT}"), Button("Updates", url=f"https://t.me/{UPDATES}")],
    [Button("Add to Your Group", url=f"t.me/{BOT_USERNAME}?startgroup=True")],
])

@app.on_message(filters.command("start"))
async def start_command(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        is_subscribed = await app.get_chat_member(FORCE_SUB_CHANNEL, user_id)
    except UserNotParticipant:
        keyboard = Markup([[Button("📢 Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL}")]])
        await message.reply_text(
            "To use this bot, you must subscribe to our channel.",
            reply_markup=keyboard
        )
        return   
    await message.reply_photo(
        photo=random.choice(PHOTOS),
        caption=f"🎬 **Welcome to the {BOT_NAME} Movies Download Bot!** 🎥\n\n🤖 This bot allows you to download and watch your favorite movies right here on Telegram.\n\n📌 **Note:**This bot is for educational and entertainment purposes only.\nMake sure to follow the channel for the latest updates and movie recommendations.\n\n🙏 Thank you for choosing {BOT_NAME} Movies Download Bot! Enjoy your movie experience!🍿", 
        reply_markup=start_keyboard
    )

  
