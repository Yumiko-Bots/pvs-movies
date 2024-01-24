from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup, Message, CallbackQuery
import random
from Pvs_Movies import app
#from Pvs_Movies.database.chats_db import(
#       save_users, save_chats, 
#       get_users, get_chats
#)
from config.config import(
       FORCE_SUB_CHANNEL, SUPPORT, 
       UPDATES, PHOTOS, 
       BOT_NAME, BOT_USERNAME, 
       OWNERS, BAN_COMMANDS,
       MOVIE_DL_COMMANDS, MOVIE_FIND_COMMANDS,
       FILTERS_COMMANDS, CONNECT_COMMANDS, 
       PURGE_COMMANDS, MUTE_COMMANDS, 
       FILE_STORE_COMMANDS
)
import asyncio
from pyrogram.errors import UserNotParticipant

COMMANDS_MAPPING = {
    "Owners": OWNERS,
    "Ban": BAN_COMMANDS,
    "Movie Download": MOVIE_DL_COMMANDS,
    "Movie Find": MOVIE_FIND_COMMANDS,
    "Filters": FILTERS_COMMANDS,
    "Connect": CONNECT_COMMANDS,
    "Purge": PURGE_COMMANDS,
    "Mute": MUTE_COMMANDS,
    "File Store": FILE_STORE_COMMANDS,
}
HELP_TEXT_MAPPING = {
    "Owners": "Commands for Owners:\n" + "\n".join(OWNERS),
    "Ban": "Commands for Ban:\n" + "\n".join(BAN_COMMANDS),
    "Movie Download": "Commands for Movie Download:\n" + "\n".join(MOVIE_DL_COMMANDS),
    "Movie Find": "Commands for Movie Find:\n" + "\n".join(MOVIE_FIND_COMMANDS),
    "Filters": "Commands for Filters:\n" + "\n".join(FILTERS_COMMANDS),
    "Connect": "Commands for Connect:\n" + "\n".join(CONNECT_COMMANDS),
    "Purge": "Commands for Purge:\n" + "\n".join(PURGE_COMMANDS),
    "Mute": "Commands for Mute:\n" + "\n".join(MUTE_COMMANDS),
    "File Store": "Commands for File Store:\n" + "\n".join(FILE_STORE_COMMANDS),
}

help_keyboard = Markup([
    [Button(section, callback_data=f"help_{section}")] for section in COMMANDS_MAPPING
])

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

async def edit_message_with_check(chat_id, query, text, reply_markup):
    try:
        current_text = query.message.text if query.message.text else ""
        current_markup = query.message.reply_markup if query.message.reply_markup else None

        if current_text != text or current_markup != reply_markup:
            await query.message.edit_text(text=text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Error editing message: {e}")
        
@app.on_callback_query(filters.regex(r"help"))
async def help_callback(_, query):
    await edit_message_with_check(
        query.message.chat.id,
        query.message.id,
        text="Choose a section:",
        reply_markup=help_keyboard
    )

@app.on_callback_query(filters.regex(r"help_(.*)"))
async def help_section_callback(_, query):
    section = query.matches[0].group(1)
    if section in COMMANDS_MAPPING:
        text = HELP_TEXT_MAPPING[section]
        await edit_message_with_check(
            query.message.chat.id,
            query.message.id,
            text=text,
            reply_markup=Markup([[Button("Back", callback_data="help")]])
        )
    else:
        await edit_message_with_check(
            query.message.chat.id,
            query.message.id,
            text="Invalid help section",
            reply_markup=help_keyboard
        )
