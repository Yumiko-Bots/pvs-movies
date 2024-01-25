from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton as Button,
    InlineKeyboardMarkup as Markup,
)
from Pvs_Movies.database.ban_sql import ban_user, unban_user
from Pvs_Movies import app
from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus

async def admin_check(client, message: Message) -> bool:
    if not message.from_user:
        return False
    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return False
    if message.from_user.id in [
        777000,  # Telegram Service Notifications
        1087968824,  # GroupAnonymousBot
    ]:
        return True
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        check_status = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
    except Exception as e:
        print(f"Error getting chat member: {e}")
        return False

    if check_status.status not in [
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR
    ]:
        return False
    else:
        return True

async def admin_filter_f(_, client, message):
    return (
        not message.edit_date
        and await admin_check(client, message)
    )
    
admin_filter = filters.create(func=admin_filter_f, name="AdminFilter")

@app.on_message(filters.command("ban") & filters.group & admin_filter)
async def ban_command(_, message):
    user_id, username, reason = get_user_info(message)
    if user_id is None:
        await message.reply_text("Please provide a valid user ID, username, or reply to a user to ban.")
        return
    try:
        member = await app.get_chat_member(message.chat.id, user_id)
    except Exception as e:
        print(f"Error getting chat member: {e}")
        await message.reply_text("Error retrieving chat member information.")
        return
    if member is None:
        await message.reply_text("User not found in the chat.")
        return
    if member.status not in ["administrator", "creator"]:
        await message.reply_text("You don't have the necessary rights to ban users in this group.")
        return
    app_id = await app.get_me().id
    if user_id == app_id:
        await message.reply_text("You cannot ban the bot owner.")
        return
    await message.chat.ban_member(message.chat.id, user_id)
    ban_user(user_id, username, reason)
    await message.reply_text(
        f"User {user_id} ({username}) has been banned.\nReason: {reason}",
        reply_markup=get_unban_keyboard(user_id, username)
    )

@app.on_message(filters.command("unban") & filters.group & admin_filter)
async def unban_command(_, message):
    user_id, username, _ = get_user_info(message)
    if user_id is None:
        await message.reply_text("Please provide a valid user ID, username, or reply to a user to unban.")
        return
    try:
        member = await app.get_chat_member(message.chat.id, user_id)
    except Exception as e:
        print(f"Error getting chat member: {e}")
        await message.reply_text("Error retrieving chat member information.")
        return
    if member is None:
        await message.reply_text("User not found in the chat.")
        return
    if member.status not in ["administrator", "creator"]:
        await message.reply_text("You don't have the necessary rights to unban users in this group.")
        return
    unban_user(user_id)
    await message.chat.unban_member(message.chat.id, user_id)
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
            user_info = args[0]
            if user_info.startswith("@"):
                username = user_info[1:]
            else:
                try:
                    user_id = int(user_info)
                except ValueError:
                    pass
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
    if (await app.get_chat_member(query.message.chat.id, query.from_user.id)).status not in ("administrator", "owner"):
        await query.answer("You're not an admin, you don't have the right to unban.", show_alert=True)
        return
    unban_user(user_id)
    await query.message.edit_text(
        f"User {user_id} ({username}) has been unbanned.",
        reply_markup=get_ban_keyboard(user_id, username)
    )

@app.on_callback_query(filters.regex(r"ban_(\d+)_(\w+)"))
async def ban_callback(_, query):
    user_id = int(query.matches[0].group(1))
    username = query.matches[0].group(2)
    if (await app.get_chat_member(query.message.chat.id, query.from_user.id)).status not in ("administrator", "owner"):
        await query.answer("You're not an admin, you don't have the right to ban.", show_alert=True)
        return
    ban_user(user_id, username, "")
    await query.message.edit_text(
        f"User {user_id} ({username}) has been banned.",
        reply_markup=get_unban_keyboard(user_id, username)
    )
