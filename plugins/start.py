import os
import logging
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant

from bot import Bot
from config import *
from helper_func import *
from database.database import *
from datetime import datetime, timedelta
from pytz import timezone

SECONDS = TIME 

# Enable logging
logging.basicConfig(level=logging.INFO)

@Bot.on_message(filters.command('start') & filters.private & subscribed1 & subscribed2)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await Rohitdb.present_user(id):
        try:
            await Rohitdb.add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        snt_msgs = []
        for msg in messages:
            original_caption = msg.caption.html if msg.caption else ""
            if CUSTOM_CAPTION:
                caption = f"{original_caption}\n\n{CUSTOM_CAPTION}"
            else:
                caption = original_caption   
            reply_markup = None 

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
                snt_msgs.append(snt_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                snt_msgs.append(snt_msg)
            except:
                pass

        if SECONDS >= 0:
           
            notification_msg = await message.reply(
                f"<b>Tʜɪs ᴠɪᴅᴇᴏ ɪs ᴅᴇʟᴇᴛᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ɪɴ {get_exp_time(SECONDS)}...\nFᴏʀᴡᴀʀᴅ ɪɴ ʏᴏᴜʀ Sᴀᴠᴇᴅ Mᴀssᴀɢᴇs...!!</b>"
            )

            await asyncio.sleep(SECONDS)

            for snt_msg in snt_msgs:    
                if snt_msg:
                    try:    
                        await snt_msg.delete()  
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    f"https://t.me/{client.username}?start={message.command[1]}"
                    if message.command and len(message.command) > 1
                    else None
                )
                keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("ɢᴇᴛ ᴠɪᴅᴇᴏ", url=reload_url)] if reload_url else [],
                [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
                ])

                await notification_msg.edit(
                    "<b>›› Pʀᴇᴠɪᴏᴜs ᴠɪᴅᴇᴏ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ. Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛʜᴇ sᴀᴍᴇ ᴠɪᴅᴇᴏ ᴀɢᴀɪɴ, Cʟɪᴄᴋ ᴏɴ ɢᴇᴛ ᴠɪᴅᴇᴏ👇🏻</b>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")

    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return



#=====================================================================================##

WAIT_MSG = """"<b>Processing ....</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

#=====================================================================================##



@Bot.on_message(filters.command('start') & filters.private) 
async def not_joined(client: Client, message: Message): 
    try: 
        expire_time = datetime.now() + timedelta(seconds=60)

        subscribed1 = False  # Replace with actual subscription check
        subscribed2 = False  # Replace with actual subscription check

        invite_link1 = (await client.create_chat_invite_link(
            chat_id=FORCE_SUB_CHANNEL, 
            creates_join_request=True, 
            expire_date=expire_time
        )).invite_link if not subscribed1 else None

        invite_link2 = (await client.create_chat_invite_link(
            chat_id=FORCE_SUB_CHANNEL2, 
            creates_join_request=True, 
            expire_date=expire_time
        )).invite_link if not subscribed2 else None

        buttons = []
    
        if invite_link1:
            buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link1)])
        if invite_link2:
            buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link2)])
    
        try:
            buttons.append([
                InlineKeyboardButton(
                    text='ᴛʀʏ ᴀɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ])
        except IndexError:
            pass

        sent_message = await message.reply(
            text=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
            disable_web_page_preview=True
        )

        await asyncio.sleep(60)
        await sent_message.delete()

    except Exception as e:
        await message.reply(f"Error: {e}")


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await Rohitdb.full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await Rohitdb.full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcast ho rha till then  </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await Rohitdb.del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await Rohitdb.del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
