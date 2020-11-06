import logging
logger = logging.getLogger(__name__)

import asyncio
from pyrogram import filters
from bot import feedback
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from translation import Translation
from config import Config

@feedback.on_message(filters.text)
async def text(c, m):
      if m.from_user.id in Config.LOGIN:
         if m.text == Config.PASS:
            Config.LOGIN.remove(m.from_user.id)
            Config.OWNER.append(m.from_user.id)
            await m.reply_text(text="💬 From Now You Will Receive Feedbacks. Untill This Bot Restart.  If You Want To Get Feedbacks Permanently Add Your ID In Config Vars")
         if m.text != Config.PASS:
            Config.LOGIN.remove(m.from_user.id)
            await m.reply_text(text="**⚠️ Incorrect Password ⚠️**", parse_mode="markdown")
      if m.from_user.id in Config.feedback:
         button = [[
                   InlineKeyboardButton("✅ Yes", callback_data="yes"),
                   InlineKeyboardButton("❌ No", callback_data="cancel")
                  ]]
         markup = InlineKeyboardMarkup(button)
         await m.reply_text(text="💬 Are You Sure To Send This Feedback",
                            reply_markup=markup,
                            quote=True)
      try:
          if Config.SEND is not None:
             id = Config.SEND[0]
             await c.send_message(chat_id=int(id), text=m.text, parse_mode="markdown")
             Config.SEND.remove(id)
             await c.send_message(chat_id=m.chat.id, text="✅ Notified Successfully")
      except:
          pass

@feedback.on_message(filters.command(["start"]))
async def start(c, m):
      button = [[
                InlineKeyboardButton("💬 Feedback", callback_data="feedback"),
                InlineKeyboardButton("📜 Rules", callback_data="rules"),
                ],
                [
                InlineKeyboardButton("ℹ About", callback_data="about"),
                InlineKeyboardButton("🔐 Login", callback_data="login"),
               ]]
      markup = InlineKeyboardMarkup(button)
      await c.send_message(chat_id=m.chat.id,
                           text=Translation.START,
                           disable_web_page_preview=True,
                           reply_to_message_id=m.message_id,
                           reply_markup=markup)
