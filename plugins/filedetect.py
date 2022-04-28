from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR) 

@Client.on_message(filters.private & filters.reply)
async def refunc(client,message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
       new_name = message.text 
      # await message.delete() 
      # await message.reply_to_message.delete()
       media = reply_message.media
      #  media = getattr(message, reply_message.media)
       try:
           check = new_name.split(".") 
       except:
           return await message.reply_text(
                     "**Error** :  No  Extension in File, Not Supporting",
                      reply_to_message_id=reply_message.id)
       button = [[InlineKeyboardButton("📁 Documents",callback_data = "doc")]]
       if media == "video":
           button[-1].append(InlineKeyboardButton("🎥 Video",callback_data = "vid"))
       elif media == "audio":
           button[-1].append(InlineKeyboardButton("🎵 audio",callback_data = "aud"))
       await message.reply_text(
          f"**Select the output file type**\n**Output FileName** :- ```{new_name}```",
          reply_to_message_id=reply_message.id,
          reply_markup=InlineKeyboardMarkup(button))
