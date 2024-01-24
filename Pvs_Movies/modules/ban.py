from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from Pvs_Movies.database.ban_sql import ban_user, unban_user
from Pvs_Movies import app

async def is_admin(chat_id, user_id):
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in ("administrator", "creator")

@app.on_message(filters.command("ban") & filters.group)
async def ban_command(_, message):
    user_id, username, reason = get_user_info(message)
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply_text("You must be an admin to use this command.")
        return
    ban_user(user_id, username, reason)
    await message.reply_text(
        f"User {user_id} ({username}) has been banned.\nReason: {reason}",
        reply_markup=get_unban_keyboard(user_id, username)
    )

@app.on_message(filters.command("unban") & filters.group)
async def unban_command(_, message):
    user_id, username, _ = get_user_info(message)
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply_text("You must be an admin to use this command.")
        return
    unban_user(user_id)
    await message.reply_text(
        f"User {user_id} ({username}) has been unbanned.",
        reply_markup=get_ban_keyboard(user_id, username)
    )

def get_user_info(message):
    user_id = None
    username = None
    reason = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
    else:
        args = message.command[1:]
        if args:
            try:
                user_id = int(args[0])
            except ValueError:
                username = args[0]
        if len(args) > 1:
            reason = " ".join(args[1:])
    return user_id, username, reason

def get_unban_keyboard(user_id, username):
    return Markup([[Button("Unban", callback_data=f"unban_{user_id}_{username}")]])

def get_ban_keyboard(user_id, username):
    return Markup([[Button("Ban Again", callback_data=f"ban_{user_id}_{username}")]])

@app.on_callback_query(filters.regex(r"unban_(\d+)_(\w+)"))
async def unban_callback(_, query):
    user_id = int(query.matches[0].group(1))
    username = query.matches[0].group(2)  
    unban_user(user_id)   
    await query.message.edit_text(
        f"User {user_id} ({username}) has been unbanned.",
        reply_markup=get_ban_keyboard(user_id, username)
    )
  
@app.on_callback_query(filters.regex(r"ban_(\d+)_(\w+)"))
async def ban_callback(_, query):
    user_id = int(query.matches[0].group(1))
    username = query.matches[0].group(2)  
    ban_user(user_id, username, "")  
    await query.message.edit_text(
        f"User {user_id} ({username}) has been banned.",
        reply_markup=get_unban_keyboard(user_id, username)
    )
