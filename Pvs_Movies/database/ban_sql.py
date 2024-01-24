from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
import psycopg2
from Pvs_Movies.database import cursor, conn

create_table_query = """
CREATE TABLE IF NOT EXISTS banned_users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(255),
    reason VARCHAR(255)
);
"""
cursor.execute(create_table_query)
conn.commit()

def ban_user(user_id, username, reason):
    cursor.execute("INSERT INTO banned_users (user_id, username, reason) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (user_id, username, reason))
    conn.commit()
  
def unban_user(user_id):
    cursor.execute("DELETE FROM banned_users WHERE user_id = %s", (user_id,))
    conn.commit()
