
import base64
from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from helper_func import *
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>›› Bʏ: ADR ANIME HINDI</b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data = "close")
                    ]
                ]
            )
        )


    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    
